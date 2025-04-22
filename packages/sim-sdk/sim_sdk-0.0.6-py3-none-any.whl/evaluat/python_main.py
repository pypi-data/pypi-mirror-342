import sys
import base64
import git_util
from operator_framework import OperatorFramework
import logging
from util import nacos_client
import json
from evaluat import db_util
from evaluat.const import SOURCE, LOGSIM, SCENE, SUCCESS, FAILED, EXECUTE, ERROR, STR_FAIL, STR_PASS, STR_ERROR
from evaluat.source_data_init_strategy import SourceDatasetInitStrategy
from evaluat.logsim_data_init_strategy import LogsimDatasetInitStrategy
from evaluat.sence_data_init_strategy import SenceDatasetInitStrategy
import const_key
import data_deal_util
import scene_util
from evaluat import data_util
import traceback
import es_util
import pandas as pd
import os
import shutil
import label_util
from collections import defaultdict
from env_manager import env_manager

strategy_dict = {
    LOGSIM: LogsimDatasetInitStrategy(),
    SCENE: SenceDatasetInitStrategy(),
    SOURCE: SourceDatasetInitStrategy()}

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

# 通过 get_config() 函数获取配置（懒加载）
current_config = nacos_client.get_config()


def main():
    task_id = None
    try:
        # 解析参数，获取任务id
        param_page, param_pipeline = parse_params()

        # 初始化任务和数据
        task_dataset_list, task_id, script_local_paths, metric_config_json = init_task_data(param_page, param_pipeline)

        # 要评价的任务数据
        task_dataset = task_dataset_list[0]

        # 加载算子
        operator_framework = OperatorFramework()
        operator_framework.load_multiple_operators(script_local_paths)

        # 执行算子
        task_result = execute_operator(operator_framework, param_page, param_pipeline, script_local_paths,
                                       metric_config_json, task_dataset)

        # 更新任务状态
        db_util.update_task_4_success(task_id, task_result)
        db_util.update_logsim_eval_task_dataset(task_dataset["id"], task_result)

        # 输出参数到下一个节点
        param_pipeline_next = {'task_id': task_id, 'node_name': "评测任务"}
        param_pipeline_next = json.dumps(param_pipeline_next)
        # 写入回灌流水线中间数据到下一个节点
        with open('./outParams.txt', 'w', encoding='utf-8') as file:
            file.write(param_pipeline_next)
    except Exception as err:
        logging.error("评测任务失败")
        error_info = traceback.format_exc()
        logging.info(f"Error: {err.__class__.__name__}: {err}。详细信息：{error_info}")

        # 任务状态更新
        if env_manager.is_prod() and task_id is not None:
            db_util.update_task_4_failed(task_id, ERROR)
            db_util.update_logsim_eval_task_dataset_by_task_id(task_id, ERROR)
    finally:
        # 删除临时文件
        if env_manager.is_prod():
            if os.path.exists(const_key.EVAL_LOCAL_DIR_PREFX):
                shutil.rmtree(const_key.EVAL_LOCAL_DIR_PREFX)

            path = current_config.get('containerPath')
            if os.path.exists(path):
                shutil.rmtree(path)


def parse_params():
    logging.info("入口参数：%s", sys.argv)

    if len(sys.argv) <= 0:
        raise Exception("Please provide arguments.")

    # 页面参数
    param_page = sys.argv[1]
    param_page = json.loads(param_page)
    logging.info("页面参数为：{}".format(param_page))

    # 上游传递参数
    param_pipeline = sys.argv[2]
    param_pipeline = json.loads(param_pipeline)
    logging.info("传递参数：{}".format(param_pipeline))

    return param_page, param_pipeline


def init_task_data(param_page, param_pipeline):
    """
    初始化任务数据、算子文件
    """

    op_file_name = param_page["op_file_name"]

    if env_manager.is_debug():
        logging.info("调试模式")
        task_id = 1
        logsim_task_id = param_pipeline['logsim_task_id']
        source_id_list = param_pipeline['source_id_list']
        if logsim_task_id is not None:
            task_dataset_list = strategy_dict[LOGSIM].debug_task_dataset(logsim_task_id, source_id_list)
        else:
            task_dataset_list = strategy_dict[SCENE].debug_task_dataset(task_id, source_id_list)

        script_local_path_list, metric_config_json = git_util.parse_debug_operator_info_by_json(
            op_file_name, "")

        if not script_local_path_list:
            raise Exception("获取算子文件失败")
    else:
        logging.info("生产模式")
        task_id = param_pipeline['task_id']
        # 设置任务状态：执行中
        db_util.update_task_4_start(task_id, EXECUTE)

        task_info = db_util.get_evaluate_task(task_id)[0]
        main_task_id = task_info["parent_task_id"]

        # 获取评测数据集列表
        task_dataset_list = db_util.get_evluate_task_dataset(task_id)

        if len(task_dataset_list) <= 0:
            raise Exception(f"任务id main_task_id {main_task_id} task {task_id} 为查询到回灌数据")

        task_dataset = task_dataset_list[0]
        db_util.update_logsim_eval_task_dataset(task_dataset["id"], EXECUTE)

        metric_config = base64.b64decode(param_page['metric_config']).decode('utf-8')
        op_strs = param_page['op_strs']
        common_strs = param_page['common_strs']

        # 从git中拉取算子代码及对应配置
        metric_config_json = json.loads(metric_config)
        script_local_path_list = data_deal_util.generate_local_op_file(op_strs)
        # 保存common函数脚本文件，用于后续算子调用
        data_deal_util.generate_local_op_file(common_strs)

        if not script_local_path_list:
            raise Exception("下载算子文件失败")

    return task_dataset_list, task_id, script_local_path_list, metric_config_json


def save_middle_files(operators_cvs_df_list, operators_topic_df_list, task_dataset_id, dataset_id):
    # 合并所有 cvs_df
    if operators_cvs_df_list:
        operators_cvs_df = pd.concat(operators_cvs_df_list, ignore_index=True)  # 合并所有 DataFrame
        # 保存到本地 CSV 文件
        dataset_csv_path = os.path.join(const_key.LOCAL_RESULT_PREFIX, "analysis.csv")
        operators_cvs_df.to_csv(dataset_csv_path, index=False)  # 保存为 CSV，不包括行索引
        logging.info("analysis.csv has been saved ")
    else:
        logging.info("No analysis.csv to save ")

    # 如果你需要处理 operators_topic_df_list，可以在这里添加类似的逻辑
    # 例如：
    if operators_topic_df_list:
        operators_topic_df = pd.concat(operators_topic_df_list, ignore_index=True)
        dataset_topic_path = os.path.join(const_key.LOCAL_RESULT_PREFIX, "topic.csv")
        operators_topic_df.to_csv(dataset_topic_path, index=False)
        logging.info("topic.csv has been saved")
    else:
        logging.info("No topic.csv to save")

    # 上传文件
    file_names = ["analysis.csv", "topic.csv"]
    obs_dir = "datacenter_result/eval/" + str(task_dataset_id) + "/"
    logging.info(f"中间文件上传到: {obs_dir}")


    # /a/b/a.txt /a/b/c.txt
    result_local_file = []
    result_local_file_name = []
    # 云完整路径
    result_obs_path = []

    for file_name in file_names:
        # 统一上传后的日志文件
        result_obs_file = obs_dir + file_name
        # 上传回灌结果
        file_path = os.path.join(const_key.LOCAL_RESULT_PREFIX, file_name)
        if not os.path.isfile(file_path):
            logging.info(f"File {file_path} does not exist.")
            continue

        result_local_file_name.append(file_name)
        result_local_file.append(file_path)
        data_deal_util.upload_to_obs(result_obs_file, file_path)

        result_obs_path.append(result_obs_file)
        logging.info(f"评价中间文件{file_path}保存到OBS {result_obs_file}")

    if result_local_file_name:
        # 更新文件地址
        db_util.update_evluate_task_dataset_middle_files(task_dataset_id, ",".join(map(str, result_local_file_name)))

        # 删除临时文件：结果文件
        scene_util.remove_files(result_local_file)

    return result_obs_path


def save_label(operator_result_dict, params):
    """
    保存评测标签
    @param operator_result_dict: 每个算子的结果 key 算子名称，value 算子结果
    """
    task_dataset = params[const_key.KEY_TASK_DATASET]
    task_info = db_util.get_evaluate_task(task_dataset["task_id"])[0]
    main_task_info = db_util.get_evaluate_main_tas_by_id(task_info["parent_task_id"])[0]

    # 评测算子处理的数据包信息
    dataset_label_dict = params[const_key.DATASET_LABEL_KEY]
    # 保存评测标签
    evaluate_info_label = {"create_time": main_task_info["create_time"].timestamp() * 1000,
                           "creator": main_task_info["creater"],
                           "id": task_dataset["id"],
                           "task_id": main_task_info["id"],
                           "task_name": main_task_info["task_name"]}

    # 所有算子结果
    # 记录每一个算子名（key）和该算子结果（value:pass\fail)，同是汇总所有算子结果(key:reslut value:pass/fail)，作为数据包的处理结果
    operator_pass_dict = {}
    if operator_result_dict:
        for operator_name, operator_result in operator_result_dict.items():
            if not operator_result:
                continue

            # 检查 operator_data 是字典（对应 JSONObject）还是列表（对应 JSONArray）
            if isinstance(operator_result, dict):
                # 获取 'result' 字段的值
                result = operator_result.get("result")
                # 将算子结果名称和 result 值存入字典
                operator_pass_dict[operator_name] = result.strip() if result else STR_ERROR
            elif isinstance(operator_result, list):
                # 遍历所有结果，都为 "pass" 才认为通过
                pass_value = None
                for item in operator_result:
                    if not isinstance(item, dict):
                        continue
                    result_str = item.get("result")
                    result_str = result_str.strip() if result_str else STR_ERROR
                    # 有一个失败表示本次算子失败
                    if result_str == STR_ERROR:
                        pass_value = STR_ERROR
                        break

                    if result_str == STR_FAIL:
                        pass_value = STR_FAIL
                        break
                    pass_value = result_str
                operator_pass_dict[operator_name] = pass_value
            else:
                operator_pass_dict[operator_name] = STR_ERROR

    # 汇总所有算子结果
    # total_result = STR_FAIL if any(value == STR_FAIL for value in operator_pass_dict.values()) else STR_PASS

    values = operator_pass_dict.values()
    if any(value == STR_ERROR for value in values):
        total_result = STR_ERROR
        task_result = ERROR
    elif any(value == STR_FAIL for value in values):
        total_result = STR_FAIL
        task_result = FAILED
    else:
        total_result = STR_PASS
        task_result = SUCCESS

    operator_pass_dict["result"] = total_result

    evaluate_info_label["operator_result"] = operator_pass_dict

    dataset_label_dict["evaluate_info"] = evaluate_info_label

    logging.info(f"保存评测标签：{dataset_label_dict}")
    label_util.saveEvaluateDataLabel(task_dataset["id"], dataset_label_dict)

    return task_result


def save_result(operator_name: str, operator_result: dict, metric_config: dict, params: dict,
                table_name: str, dataset_label: dict) -> None:
    """
    将算子结果保存到ES
    @param operator_name: 算子名称
    @param operator_result: 算子结果
    @param params: 算子参数
    @param table_name: 算子结果保存的表名
    @param dataset_label: 数据标签
    """

    # 确保有结果返回
    if not operator_result:
        logging.info(f"算子 {operator_name} 结果是 None or empty.")
        return

    # 算子任务需要处理的数据集
    task_dataset = params[const_key.KEY_TASK_DATASET]

    # 获取公共数据信息
    dataset_info, operator_info = data_util.get_operator_common_data(params, task_dataset)

    operator_info["metric_config"] = metric_config
    operator_info["operator_name"] = operator_name

    # 获取任务信息
    task_info_dict = {}
    if env_manager.is_prod():
        task_info = db_util.get_evaluate_task(task_dataset["task_id"])[0]
        task_info_dict = {"task_id": task_info["parent_task_id"],
                          "son_task_id": task_info["id"],
                          "batch_no": task_info["batch_no"],
                          "op_file_name": task_info["op_file_name"],
                          "bc_name": task_info["bc_name"],
                          "config_str": task_info["config_str"]}

    # 保存结果到ES：每隔一个segment保存一条记录
    # 判断 operator_result 的类型并根据不同类型进行处理
    if isinstance(operator_result, dict):
        # 如果是 dict 类型，进行相关处理
        logging.info("处理 operator_result dict 类型的数据")
        save(dataset_info, operator_name, operator_result, task_info_dict, operator_info, dataset_label, table_name)
    elif isinstance(operator_result, list) and len(operator_result) > 0:
        # 如果是 list 类型，进行相关处理
        logging.info("处理 operator_result list 类型的数据")
        for item in operator_result:
            save(dataset_info, operator_name, item, task_info_dict, operator_info, dataset_label, table_name)
    else:
        # 如果不是 dict 或 list，可能是错误或其他类型，可以抛出异常或做默认处理
        logging.info("operator_result 结果类型未知或空列表")


def save(dataset_info, operator_name, operator_result, task_info, operator_info, dataset_label, table_name):
    operator_info = {operator_name: operator_info}

    # 构建最终回灌结果数据
    operator_name_result = {operator_name: operator_result}
    result = {"operator_result": operator_name_result,
              "task_info": task_info,
              "dataset_info": dataset_info,
              "operator_name": operator_name,
              "operator_info": operator_info}

    # 标签信息
    label_dict = {"basic_info": dataset_label["basic_info"],
                  "data_info": dataset_label["data_info"]}
    result.update(label_dict)

    logging.info(f"算子 {operator_name} 结果表 {table_name}：结果为 {result}")

    # 入库
    if env_manager.is_prod():
        es_util.save(table_name, result)


def is_operator_success(operator_result_dict: dict):
    """
    判断所有算子结果是否全部为success
    @param operator_result_dict: 算子结果
        {"operator_a":[{result:success, ...}, {...}], "operator_b":[{result:success, ...}, {...}}]}
    """

    if operator_result_dict is None or not operator_result_dict:
        return False

    all_success = True

    # 遍历所有可能的result字段
    for key, value_list in operator_result_dict.items():
        for item in value_list:
            if 'result' not in item or item['result'] != 'pass':
                all_success = False
                break  # 如果找到一个不是success的，就可以提前退出内层循环
        if not all_success:
            break  # 同样，如果外层循环中已经确定不是所有都是success，也可以提前退出

    return all_success


def execute_operator(operator_framework, param_page, param_pipeline,
                     script_local_path_list, metric_config, task_dataset):
    """
    按数据集循环执行算子
    @:param task_id: 子任务ID
    """

    # 算子部分参数
    operator_param = {"param_page": param_page, "param_pipeline": param_pipeline}

    dataset_id = task_dataset["dataset_id"]

    task_result = FAILED

    try:
        logging.info(f"准备一个数据包的评价 start:{dataset_id}")

        dataset_info = {"dataset_path": task_dataset["dataset_path"],
                        "start_timestamp": task_dataset["start_timestamp"],
                        "end_timestamp": task_dataset["end_timestamp"],
                        "start_frame_no": task_dataset["start_frame_no"],
                        "end_frame_no": task_dataset["end_frame_no"],
                        "tag_name": task_dataset["tag_name"]}
        operator_param[const_key.KEY_DATASET_INFO] = dataset_info

        # 下载评价数据集
        local_parquet_paths, channel_mcap_paths, local_logsim_result_paths, json_paths = download_dataset(
            task_dataset)

        # 算子参数：评测数据本地数据集路径
        operator_param[const_key.LOCAL_CHANNEL_FILE_INDEX] = local_parquet_paths
        operator_param[const_key.LOCAL_CHANNEL_MCAP_FILE_INDEX] = channel_mcap_paths
        operator_param[const_key.LOCAL_RAW_DOWNLOAD_PATH_KEY] = json_paths
        operator_param[const_key.LOCAL_LOGSIM_RESULT_PATH_KEY] = local_logsim_result_paths

        # 数据包标签
        try:
            operator_param[const_key.DATASET_LABEL_KEY] = get_dataset_label(task_dataset["dataset_id"],
                                                                            task_dataset["dataset_type"])
        except Exception as e:
            logging.error(f'获取数据集 data_id {task_dataset["data_id"]}标签失败：{e}')
            operator_param[const_key.DATASET_LABEL_KEY] = {}

        # json 算子配置信息
        operator_param[const_key.KEY_METRIC_CONFIG] = metric_config
        operator_param[const_key.KEY_TASK_DATASET] = task_dataset

        # 执行算子
        operator_result_dict, operators_cvs_df_list, operators_topic_df_list, operator_version_dict = (
            operator_framework.execute_multiple_operators(script_local_path_list, operator_param,
                                                          save_result_method=save_result))

        if operator_result_dict:
            operator_result_json = json.dumps(operator_result_dict)
        else:
            operator_result_json = None

        logging.info(f"完成一个数据包的评价 end:{dataset_id}")

        if env_manager.is_prod():
            task_result = save_label(operator_result_dict, operator_param)
            # 完成一个数据包的评测：成功
            db_util.update_evluate_task_dataset(task_dataset["id"], operator_result_json, task_result)
    except Exception as err:
        if env_manager.is_prod():
            save_label({"result": {"result": STR_ERROR}}, operator_param)

        raise err

    return task_result


def get_index_by_extension(source_data_list, extension):
    """
    计算每个 source_data_id 独立的时间区间，并建立：
    2. `channel_file_index`：按通道（如 pcan, acan）组织，存储相关的 parquet 文件，方便跨包合并

    确保时间段连续，返回两个索引结构。
    """
    logging.info("download scene dataset")

    channel_file_index = defaultdict(list)  # 以通道为 key，存储相关的 parquet 文件

    # 按 raw_time 排序，确保顺序处理
    for row in sorted(source_data_list, key=lambda x: x['raw_time']):
        raw_time_str = row['raw_time'].strftime("%Y%m%d_%H%M%S")
        obs_prefix = f"{row['project_name']}/{row['plate_no']}/raw_{raw_time_str}/canbus/"
        local_path = data_util.get_local_path(obs_prefix)

        # 下载该包的所有 Parquet 文件
        downloaded_files = data_deal_util.download_files_by_extension(obs_prefix, local_path, extension)

        for file in downloaded_files:
            # 解析通道名称，例如 pcan_1.parquet -> pcan
            channel_key = os.path.basename(file).split("_")[0].lower()
            channel_file_index[channel_key].append(file)

    return dict(channel_file_index)


def download_by_extension(file_extension: str, source_data):
    """
    按扩展名下载包内文件
    """
    # 仅仅下载特定文件
    raw_time_str = source_data['raw_time'].strftime("%Y%m%d_%H%M%S")
    cloud_raw_path = f"{source_data['project_name']}/{source_data['plate_no']}/raw_{raw_time_str}/"
    local_raw_path = data_util.get_local_path(cloud_raw_path)
    filter_file_subfix_tuple = (file_extension)
    success, local_path_list = data_deal_util.download_folder_from_obs(cloud_raw_path, local_raw_path,
                                                                       filter_file_subfix_tuple)
    return local_path_list


def download_dataset(task_dataset):
    """
    下载一个评测数据集包
    """
    # 评测数据集
    # 获取到需要回灌场景数据
    if task_dataset["dataset_type"] == LOGSIM:  # 针对非回灌数据评价
        source_data_ids = task_dataset["source_data_ids"]
    else:
        dataset_id = task_dataset['dataset_id']
        dig_data = db_util.get_dig_data_by_id(dataset_id)
        source_data_ids = dig_data["source_data_ids"]

    # 获取到场景数据对应的原始数据列表(支持跨片挖掘回灌)
    source_data_list = db_util.get_source_data(source_data_ids)
    channel_parquet_file_index = get_index_by_extension(source_data_list, ".parquet")
    channel_mcap_file_index = get_index_by_extension(source_data_list, ".mcap")

    json_list = download_by_extension(".json", source_data_list[0])

    # 如果评测的是回灌结果，下载回灌结果文件
    local_logsim_result_data_path_list = {}
    if task_dataset["dataset_type"] == LOGSIM:  # 针对非回灌数据评价
        logging.info(f"download logsim result data")
        # 下载单个回灌结果文件
        logsim_task_dataset = db_util.get_logsim_task_dataset(task_dataset["dataset_id"])[0]
        cloud_raw_path = logsim_task_dataset["result_path"]
        local_raw_path = data_util.get_local_path(cloud_raw_path)
        success_logsim_result_data, local_logsim_result_data_path_list = data_deal_util.download_folder_from_obs(
            cloud_raw_path, local_raw_path)

        if not success_logsim_result_data:
            logging.info(f"eval file download failed: {cloud_raw_path} exit")
            raise Exception("eval file download failed: {}".format(cloud_raw_path))

    return channel_parquet_file_index, channel_mcap_file_index, local_logsim_result_data_path_list, json_list


def get_dataset_label(dataset_id, dataset_type):
    """
    获取到数据对应的标签
    @param 源数据表、切片表、场景表、回灌结果表 对应主键id
    """
    # 根据数据集类型、数据集来源类型、任务类型，初始化评价数据集
    init_data_strategy = strategy_dict[dataset_type]
    if not init_data_strategy:
        raise Exception("不支持的评价数据集类型 dataset_type:{}".format(dataset_type))

    return init_data_strategy.get_dataset_label(dataset_id)


if __name__ == '__main__':
    main()
