# -*- coding: utf-8 -*-
import base64
import copy
import json
import logging
import os
import shutil
import sys
from datetime import datetime
import pandas as pd
from pyarrow import parquet as pq
import const_key
import label_util
import makeMcap
from data_deal_util import execute_sql, getObject, set_str_cache, insert_and_get_id, \
    query_data_all, Source, upload_to_obs, generate_local_op_file
from operator_framework import OperatorFramework
from scene_util import remove_files
from util import nacos_client
from util.db_module import db_util
from util import data_utils
from util.redis_module import redis_client
import traceback
from log_manager import LoggingManager
import ulid
import pyarrow as pa

# 状态
# 执行中
EXECUTE = 1
# 执行成功
SUCCESS = 2
# 执行失败
FAILED = 3

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 通过 get_config() 函数获取配置（懒加载）
current_config = nacos_client.get_config()


class SceneObject:
    def __init__(self, source_id, start_time, end_time, start_frame, end_frame, custom_tags,
                 operator_version):
        self.id = source_id
        self.timePeriod = [{
            "start_time": start_time,
            "end_time": end_time,
            "start_frame": start_frame,
            "end_frame": end_frame
        }]
        self.custom_tags = custom_tags
        self.operator_version = operator_version

    def to_dict(self):
        return {
            "source_id": self.id,
            "timePeriod": self.timePeriod,
            "custom_tags": self.custom_tags,
            "operator_version": self.operator_version
        }


def format_date(dt, fmt):
    return dt.strftime(fmt)


def convert_timestamp_to_datetime(timestamp):
    """将时间戳转换为 MySQL 可接受的 DATETIME 格式"""
    if timestamp:
        return datetime.fromtimestamp(float(timestamp))
    return None  # 如果没有有效的时间戳，返回 None 或者你可以返回默认时间


def get_closest_frame(local_time_path, target_timestamp):
    if not os.path.exists(local_time_path):
        logging.error("本地时间戳文件不存在：%s", local_time_path)
        return ""
    # 读取JSON文件
    with open(local_time_path, 'r') as file:
        data = json.load(file)
    # 获取sensor节点下的内容
    sensor_data = data.get('sensor', {})

    first_sensor_key = list(sensor_data.keys())[0]
    first_sensor_value = sensor_data[first_sensor_key]

    # 计算最接近的帧号
    closest_frame = min(first_sensor_value, key=lambda frame: abs(first_sensor_value[frame] - float(target_timestamp)))

    return closest_frame


def save_middle_files(operators_cvs_df_list, operators_topic_df_list, main_task_id, source_data_id):
    # 合并所有 cvs_df
    if operators_cvs_df_list:
        operators_cvs_df = pd.concat(operators_cvs_df_list, ignore_index=True)  # 合并所有 DataFrame
        # 保存到本地 CSV 文件
        dataset_csv_path = os.path.join(const_key.LOCAL_RESULT_PREFIX, "analysis.csv")
        operators_cvs_df.to_csv(dataset_csv_path, index=False)  # 保存为 CSV，不包括行索引
        LoggingManager.logging().info("analysis.csv has been saved ")
    else:
        LoggingManager.logging().info("No analysis.csv to save ")

    # 如果你需要处理 operators_topic_df_list，可以在这里添加类似的逻辑
    # 例如：
    if operators_topic_df_list:
        operators_topic_df = pd.concat(operators_topic_df_list, ignore_index=True)
        dataset_topic_path = os.path.join(const_key.LOCAL_RESULT_PREFIX, "topic.csv")
        operators_topic_df.to_csv(dataset_topic_path, index=False)
        LoggingManager.logging().info("topic.csv has been saved")
    else:
        LoggingManager.logging().info("No topic.csv to save")

    # 上传文件
    package_log_file = str(source_data_id) + ".log"
    file_names = ["analysis.csv", "topic.csv", package_log_file]  # scene_util.list_file_names(const.LOCAL_RESULT_PREFIX)
    obs_dir = ("datacenter_result/dig/" + str(main_task_id) + "_"
               + str(source_data_id) + "/")
    LoggingManager.logging().info(f"中间文件上传到: {obs_dir}")

    # 关闭日志记录器
    LoggingManager.release_logger()

    # /a/b/a.txt /a/b/c.txt
    result_local_file = []
    # 云完整路径
    resul_file_name = []

    for file_name in file_names:
        result_obs_file = obs_dir + ("log.log" if file_name == package_log_file else file_name)
        # 上传回灌结果
        file_path = os.path.join(const_key.LOCAL_RESULT_PREFIX, file_name)
        if not os.path.isfile(file_path):
            logging.info(f"File {file_path} does not exist.")
            continue

        result_local_file.append(file_path)
        upload_to_obs(result_obs_file, file_path)

        resul_file_name.append("log.log" if file_name == package_log_file else file_name)
        logging.info(f"评价中间文件{file_path}保存到OBS {result_obs_file}")

    if result_local_file:
        # 删除临时文件：结果文件
        remove_files(result_local_file)

    return resul_file_name

def save_dig_result(json_data, task_id, dataset_id, is_assets):
    """
    保存场景挖掘结果，并返回批量插入后的 ID 集合

    :param json_data: JSON 字符串，包含多个场景挖掘结果
    :param task_id: 任务 ID
    :param dataset_id: 数据集 ID
    :return: 插入的 ID 集合
    """
    # 解析 JSON 数据
    scene_object_list = json.loads(json_data)  # 将 JSON 字符串解析为 Python 对象

    sql = f"select deal_name from datacenter_datadeal where id = {task_id}"
    result = db_util.fetch_one(sql)
    task_name = result.get('deal_name')

    # 按 source_id 分组插入的数据
    source_id_map = {}

    # 准备插入的数据
    for scene_object in scene_object_list:
        source_id = scene_object["source_id"]
        # middle_files = scene_object["middle_files"]

        for time_period in scene_object["timePeriod"]:
            param = (
                task_id,
                dataset_id,  # scene_id
                task_name,
                source_id,  # source_id
                convert_timestamp_to_datetime(time_period["start_time"]),  # start_time
                convert_timestamp_to_datetime(time_period["end_time"]),  # end_time
                int(time_period["start_frame"]) if time_period.get("start_frame") else 0,
                int(time_period["end_frame"]) if time_period.get("end_frame") else 0,  # end_frame (为空则设置为 None)
                is_assets,  # 是否资产化
                'admin',  # 创建人 (根据实际情况填充)
                datetime.now(),  # 创建时间 (当前时间)
                # middle_files,  # 中间文件obs路径
                0,  # 是否删除
                ulid.ulid(),  # 场景数据id ULID
            )

            # 将数据按 source_id 分组
            if source_id not in source_id_map:
                source_id_map[source_id] = []
            source_id_map[source_id].append(param)

    # 插入数据的 SQL 语句，使用 %s 作为占位符
    insert_sql = """
    INSERT INTO datacenter_dig_detail 
    (task_id, scene_id, task_name, source_data_id, start_time, end_time, start_frame, end_frame, is_assets, creater, 
    create_time, is_delete, data_id)  
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # 为每个 source_id 执行 insert_batch
    insert_batch_map = {}
    for source_id, params in source_id_map.items():
        insert_batch_map[source_id] = db_util.insert_batch([insert_sql] * len(params), params)

    # 返回按 source_id 分组的 insert_batch 列表
    return insert_batch_map, source_id_map


def save_dig_middle_files(main_task_id, middle_files_map, source_state_map):
    """
    保存场景挖掘中间文件

    :param main_task_id: 主任务id
    :param middle_files_map: 中间文件名，按 source_id 分组
    """
    # 准备插入的数据
    params = []
    for source_id, middle_files in middle_files_map.items():
        param = (
            main_task_id,
            source_id,  # scene_id
            source_state_map[source_id],
            ",".join(middle_files)
        )
        params.append(param)

    # 插入数据的 SQL 语句，使用 %s 作为占位符
    insert_sql = """
    INSERT INTO datacenter_dig_detail_files 
    (main_id, source_id, state, middle_files)  
    VALUES (%s, %s, %s, %s)
    """

    db_util.insert_batch([insert_sql] * len(params), params)


def update_dig_task_middle_files(id, middle_files):
    # 更新任务
    sql_list = []
    args_list = []

    sql = "update datacenter_logsim_evaluat_task_dataset set middle_files = %s where id = %s"
    params = (middle_files, id,)

    sql_list.append(sql)
    args_list.append(params)

    execute_sql(sql_list, args_list)


def bulk_insert_to_es(insert_batch_results, source_id_map, source_id_operator_data_map,
                      task_id, op_file_name, bc_name, config_str, source_state_map):
    """
    批量将挖掘结果插入到 Elasticsearch 中

    :param insert_batch_results: 每个原始数据挖掘的结果
    :param task_id: 当前任务的 ID
    """
    # 获取所有的 source_id
    all_source_ids = list(insert_batch_results.keys())

    # 调用 selectByIdList 方法批量查询 Elasticsearch，获取原始文档
    original_docs = label_util.selectSourceDataLabelByIdList(all_source_ids)

    # 准备批量插入的文档数据
    doc_list = []
    all_insert_ids = []

    # 自定义标签:
    custom_tags_list = []

    # 获得任务信息
    sql = f"SELECT creater, main_id, deal_name FROM datacenter_datadeal WHERE id = {task_id}"
    task_result = db_util.fetch_one(sql)

    for source_id, insert_ids in insert_batch_results.items():
        # 获取原始文档
        doc = original_docs.get(source_id)

        if not doc:
            logging.error(f"Source ID: {source_id} not found in Elasticsearch for task {task_id}")
            continue  # 如果没有找到该 source_id 跳过本次循环

        for i in range(len(insert_ids)):
            inserted_id = insert_ids[i]
            detail_msg = source_id_map[source_id][i]

            operator_custom_data = source_id_operator_data_map[source_id]

            # 创建 doc 的副本，防止修改原文档
            doc_copy = copy.deepcopy(doc)
            # 更新文档数据
            doc_copy['data_info']['dig_info'] = {
                "id": inserted_id,  # 从插入的 ID 集合获取 dig_id
                "task_id": task_id,  # 使用传入的 task_id
                "create_time": int(detail_msg[10].timestamp() * 1000),  # 创建时间
                "creator": task_result.get('creater'),  # 创建人
                "end_frame": detail_msg[7],  # 结束帧号
                "end_time": int(detail_msg[5].timestamp() * 1000),  # 结束时间戳
                "operator_commit": bc_name,  # commit号
                "operator_configure": config_str,  # 算子配置
                "operator_name": op_file_name,  # 算子名称
                "start_frame": detail_msg[6],  # 开始帧号
                "start_time": int(detail_msg[4].timestamp() * 1000),  # 开始时间戳
                "is_assets": detail_msg[8],  # 是否资产化
                "task_name": detail_msg[2],  # 任务名称
                "operator_version": float(operator_custom_data["operator_version"]),  # 算子版本
                "data_id": detail_msg[12]  # 场景数据id ULID
            }

            # 算子返回的标签 operator_tag_dict = {"category": "ACC", "sub_category": "cut-in", "custom_tags": {}}
            for key, value in operator_custom_data["custom_tags"].items():
                if key not in doc_copy['data_info']['dig_info']:
                    doc_copy['data_info']['dig_info'][key] = value

            # 将处理后的文档添加到 doc_list 中
            doc_list.append(doc_copy)
            all_insert_ids.append(inserted_id)
            custom_tags_list.append(operator_custom_data["custom_tags"])


    # 调用 insertBatchSceneDataLabel 方法批量插入文档
    if doc_list:
        try:
            # 校验dig_info start
            error_index_list, error_msg_map = label_util.verify_dig_info(doc_list)
            if len(error_index_list) > 0:
                # 打印错误日志
                for key, value in error_msg_map.items():
                    error_msg_str = "\n".join(list(value))
                    logging.error(f"custom_tags verification failed: \n{custom_tags_list[key]}\n{error_msg_str}")
                # 1.获得所有错误的数据的原始数据包id
                source_data_id_set = set()
                for error_index in error_index_list:
                    source_data_id = doc_list[error_index]['basic_info']['source_data_id']
                    source_data_id_set.add(source_data_id)
                source_data_id_list = list(source_data_id_set)
                # 2.获得原始数据包-错误日志map
                source_id_error_log_map = {}
                for key, value in error_msg_map.items():
                    error_msg_str = "\n".join(list(value))  # 单个场景数据的错误消息
                    source_data_id = doc_list[key]['basic_info']['source_data_id']  # 原始数据包id
                    if source_data_id not in source_id_error_log_map.keys():
                        source_id_error_log_map[
                            source_data_id] = f"custom_tags verification failed: \n{custom_tags_list[key]}\n{error_msg_str}"
                    else:
                        source_id_error_log_map[
                            source_data_id] = f"{source_id_error_log_map[source_data_id]} \n{custom_tags_list[key]}\n{error_msg_str}"
                # 3.过滤 all_insert_ids 和 doc_list (删除错误包的所有es数据)
                all_insert_ids_filter = []
                doc_list_filter = []
                need_delete_id = []  # 需要删除的mysql id
                for i in range(len(all_insert_ids)):
                    if doc_list[i]['basic_info']['source_data_id'] in source_data_id_list:
                        need_delete_id.append(all_insert_ids[i])
                    else:
                        all_insert_ids_filter.append(all_insert_ids[i])
                        doc_list_filter.append(doc_list[i])
                all_insert_ids = all_insert_ids_filter
                doc_list = doc_list_filter
                # 4.删除mysql场景数据 (删除错误包的所有mysql数据)
                for d in need_delete_id:
                    sql_statements = []
                    values_list = []
                    values_list.append(d)
                    sql = "UPDATE datacenter_dig_detail SET is_delete = 1 WHERE id = %s"
                    sql_statements.append(sql)
                    db_util.execute_sql(sql_statements, values_list)
                # 5.添加日志
                for key, value in source_id_error_log_map.items():
                    source_state_map[str(key)] = FAILED
                    update_log(task_result.get('main_id'), key, value)

            # 校验dig_info end
            if len(doc_list) > 0:
                label_util.insertBatchSceneDataLabel(all_insert_ids, doc_list)
                logging.info(f"Successfully inserted {len(doc_list)} documents for task {task_id}")
        except Exception as e:
            logging.error(f"Failed to insert documents for task {task_id}: {e}")
    else:
        logging.warning(f"No documents to insert for task {task_id}")



def generate_taskid_dataset_name(pipeline_value, page_value, source_id_list, op_file_name, config_str, bc_name, argo_pod_name):
    if 'task_id' in pipeline_value:
        task_id = pipeline_value['task_id']
        dataset_name = pipeline_value['dataset_name']
    else:
        sql = """
                            INSERT INTO datacenter_datadeal (deal_Type, deal_Name, source_File_Ids, op_file_name, config_str, bc_name, status, argo_task_name, creater, create_Time)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """
        # 获取当前时间
        now = datetime.now()

        # 按指定格式输出时间
        formatted_time = now.strftime("%Y%m%d%H%M%S")
        job_code = page_value['job_code']
        dataset_name = 'dig_' + formatted_time + "_" + job_code

        values = ('2', dataset_name, source_id_list, op_file_name, config_str, bc_name, '1', argo_pod_name, 'admin', now)
        task_id = insert_and_get_id(sql, values)

    return task_id, dataset_name


def generate_input_data(source_id_list: str) -> []:
    sql = f"select a.id, a.source_file, a.project_name, a.plate_no, a.raw_time from datacenter_source_data a where a.id in ({source_id_list})"

    source_data_list = query_data_all(sql)

    # 初始化结果列表
    inputData = []
    directory_path_list = set()

    # 遍历 source_data_list
    for s in source_data_list:
        source_data = {"sourceDataId": s["id"]}

        source_channel_file_list = json.loads(s["source_file"])
        channel_file_list = []

        for t in source_channel_file_list:
            source_file_list = [{"fileName": f} for f in t["fileNameList"]]

            directory = t["directory"]
            real_obs_dir = f"{s['project_name']}/{s['plate_no']}/raw_{format_date(s['raw_time'], '%Y%m%d_%H%M%S')}"
            channel_file = {
                "dataType": t["dataType"],
                "realObsDir": real_obs_dir,
                "directory": directory,
                "sourceFileList": source_file_list
            }
            channel_file_list.append(channel_file)

        source_data["channelFiles"] = channel_file_list
        inputData.append(source_data)

    return inputData


def exe_dig(inputData: [], page_value: dict, script_local_path_list, metric_config_json, main_task_id, task_id, operator_framework):
    # 初始化结果列表
    directory_path_list = set()
    source_file_ids = []
    task_result = []
    middle_files_map = {}
    source_state_map = {}

    for i, data in enumerate(inputData):
        sourceDataId = data["sourceDataId"]
        channel_files = data["channelFiles"]

        operators_cvs_df_combine_list = []
        operators_topic_df_combine_list = []

        try:
            for j, item in enumerate(channel_files):
                source_file_list = item["sourceFileList"]
                data_type = item["dataType"]
                real_obs_dir = item["realObsDir"]
                directory = item["directory"]

                # 本次先处理asc文件
                if data_type is not None and data_type == current_config.get('DATA_TYPE_ASC'):
                    parquet_list = []

                    for source_file_item in source_file_list:
                        source_file = source_file_item['fileName']
                        file_prefix = os.path.splitext(source_file)[0]
                        file_extension = os.path.splitext(source_file)[1]

                        local_parquet_file = current_config.get('containerPath') + file_prefix + '.parquet'
                        if file_extension == ".asc":
                            getObject(real_obs_dir + "/" + directory + "/" + file_prefix + '.parquet',
                                      local_parquet_file)
                            if os.path.exists(local_parquet_file):
                                parquet_list.append(local_parquet_file)

                    # 算子：2 构建参数
                    operator_param = {const_key.PARAM_PAGE: page_value,  # env:算子文件配置项
                                      const_key.LOCAL_RAW_DOWNLOAD_PATH_KEY: parquet_list,  # dig数据本地数据集路径
                                      const_key.KEY_METRIC_CONFIG: metric_config_json,  # 算子json内配置项
                                      "real_obs_dir": real_obs_dir,  # 原始obs路径
                                      "main_task_id": main_task_id,  # 主任务ID
                                      "task_id": task_id,  # 任务ID
                                      "source_data_id": sourceDataId  # 源数据ID
                                      }
                    # 算子：3 执行算子
                    # 结果为：{'acc_warning_new_1203': [(1724070116.0, 1724070415.979714)]}
                    dig_result_dict, operators_cvs_df_list, operators_topic_df_list, operator_version_dict = operator_framework.execute_multiple_operators(
                        script_local_path_list, operator_param)
                    logging.info("挖掘结果：%s", dig_result_dict)
                    operators_cvs_df_combine_list.extend(operators_cvs_df_list)
                    operators_topic_df_combine_list.extend(operators_topic_df_list)

                    if dig_result_dict:
                        # 获取字典中的第一个键值对
                        # 目前近支持一个挖掘算子，TODO 支持多个不同算子结果处理
                        operator_name, dig_result_list = next(iter(dig_result_dict.items()))
                        operator_version = operator_version_dict[operator_name]

                        if len(dig_result_list) > 0:
                            source_file_ids.append(sourceDataId)

                            file_time_path = f"{real_obs_dir}/unify_dataset/time_stamp.json"
                            local_time_path = f"{current_config.get('containerPath')}unify_dataset/time_stamp.json"
                            getObject(file_time_path, local_time_path)

                            directory_path_list.add(real_obs_dir)

                            for dig_result in dig_result_list:
                                start_frame = get_closest_frame(local_time_path, dig_result[0])
                                end_frame = get_closest_frame(local_time_path, dig_result[1])
                                custom_tags = dig_result[2] if len(dig_result) >= 3 else {}
                                result_obj = SceneObject(sourceDataId, dig_result[0], dig_result[1], start_frame,
                                                         end_frame, custom_tags,
                                                         operator_version)
                                task_result.append(result_obj)
                            if os.path.exists(local_time_path):
                                os.remove(local_time_path)
                    break

            # 数据包成功处理
            source_state_map[str(sourceDataId)] = SUCCESS
        except Exception as e:
            logging.exception("原始数据ID：%s，数据处理异常", sourceDataId)
            # 数据包成功处理
            source_state_map[str(sourceDataId)] = FAILED

        # 中间文件，没有挖到结果也有中间文件，比如日志
        middle_files_obs_path = save_middle_files(operators_topic_df_combine_list, operators_cvs_df_combine_list,
                                                  main_task_id, sourceDataId)
        middle_files_map[str(sourceDataId)] = middle_files_obs_path

    return directory_path_list, source_file_ids, task_result, middle_files_map, source_state_map


def check_clean_result(source_file_ids: [], task_id: int, dataset_name: str, task_result, source_state_map,
                        is_assets, op_file_name, bc_name, config_str):

    sql_statements = []
    values_list = []

    if not source_file_ids:
        logging.info("未筛选出对应的场景")
        sql_statements.append("update datacenter_datadeal set status = " + str(
            current_config.get('STATUS_SUCCESS')) + ", result_time = now() where id =%s")
        values_list.append(task_id)
    else:
        # 创建一个空列表，用于存储最终结果
        final_result = []

        # 创建一个字典，用于存储每个 source_id 对应的 timePeriod
        source_time_periods = {}
        source_custom_tags = {}
        source_operator_version = {}

        # 遍历 task_result 列表
        for scene_object in task_result:
            source_id = scene_object.id
            time_period = scene_object.timePeriod[0]  # 因为每个 SceneObject 只有一个 timePeriod

            source_custom_tags[source_id] = scene_object.custom_tags
            source_operator_version[source_id] = scene_object.operator_version

            # 如果 source_id 已经在字典中，则将当前的 timePeriod 添加到对应的列表中
            if source_id in source_time_periods:
                source_time_periods[source_id].append(time_period)
            else:
                # 如果 source_id 不在字典中，则创建一个新列表，并将当前的 timePeriod 添加到列表中
                source_time_periods[source_id] = [time_period]

        # 遍历 source_time_periods 字典，将结果转换为所需的格式并添加到最终结果列表中
        for source_id, time_periods in source_time_periods.items():
            final_result.append({"source_id": source_id, "timePeriod": time_periods,
                                 # "middle_files": source_middle_files[source_id],
                                 "custom_tags": source_custom_tags[source_id],
                                 "operator_version": source_operator_version[source_id]})

        # 将最终结果转换为 JSON 字符串
        final_json = json.dumps(final_result)

        sql_statements.append("update datacenter_datadeal set status = " + str(
            current_config.get('STATUS_SUCCESS')) + ", result_time = now() where id =%s")
        source_file_ids_str = [str(item) for item in source_file_ids]
        values_list.append(task_id)

        insert_dataset_sql = "INSERT INTO datacenter_dataset (dataset_name, dataset_type, source_type, source_ids, task_type, task_result, source_file_ids, is_delete, creater, create_time) " + "VALUES (%s, " + str(
            current_config.get('DATASET_TYPE_TASK')) + "," + str(
            current_config.get('SOURCE_TYPE_TASK')) + ", %s," + str(
            current_config.get('TASK_TYPE_DIG_SCENE')) + ", %s, %s," + str(
            current_config.get('IS_DELETE_NO')) + ", %s, now())"
        val = (dataset_name, task_id, final_json, ','.join(source_file_ids_str), 'admin')
        dataset_id = db_util.insert_and_get_id(insert_dataset_sql, val)

        # # 保存挖掘结果
        insert_batch_results, source_id_map = save_dig_result(final_json, task_id, dataset_id, is_assets)

        source_id_operator_data_map = {}
        # 解析 JSON 数据
        scene_object_list = json.loads(final_json)  # 将 JSON 字符串解析为 Python 对象
        for scene_object in scene_object_list:
            source_id = scene_object["source_id"]
            operator_version = scene_object["operator_version"]
            custom_tags = scene_object["custom_tags"]

            # 自定义标签 和 算子版本
            source_id_operator_data_map[source_id] = {"custom_tags": custom_tags, "operator_version": operator_version}

        # 插入索引
        bulk_insert_to_es(insert_batch_results, source_id_map, source_id_operator_data_map,
                          task_id, op_file_name, bc_name, config_str, source_state_map)

        source = Source(2, str(dataset_id))
        source_dict = source.to_dict()
        source_json = json.dumps(source_dict)

        # 写入清洗数据集ID到临时文件中
        with open('./outParams.txt', 'w', encoding='utf-8') as file:
            file.write(source_json)

    execute_sql(sql_statements, values_list)

def get_current_time_with_milliseconds():
    now = datetime.now()
    milliseconds = int(now.microsecond / 1000)
    return f'{now.strftime("%Y-%m-%d %H:%M:%S")},{milliseconds:03d}'

# 更新日志
def update_log(task_id, source_id, log_msg):
    log_path = f"datacenter_result/dig/{task_id}_{source_id}/log.log"
    try:
        getObject(log_path, log_path)

        with open(log_path, 'r', encoding='utf-8') as file:
            existing_content = file.read()

        updated_content = existing_content + get_current_time_with_milliseconds() + " - ERROR - dig_scene.py - " + log_msg.replace("\n", " ") + '\n'
        with open(log_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)

        upload_to_obs(log_path, log_path)
    except FileNotFoundError:
        logging.error(f"The file {log_path} does not exist.")
    except IOError as e:
        logging.error(f"An error occurred: {e}")


def download_parquet_files(obs_prefix, local_path):
    obs_body = data_utils.listObjects(obs_prefix)

    if obs_body is None:
        logging.error("下载文件失败：%s", obs_prefix)
        raise Exception("下载文件失败")

    objects = obs_body['contents']
    parquet_files = [obj['key'] for obj in objects if obj['key'].endswith(".parquet")]

    downloaded_files = []
    for obs_file in parquet_files:
        local_file = os.path.join(local_path, os.path.basename(obs_file))
        data_utils.get_object(obs_file, local_file)
        downloaded_files.append(local_file)

    return downloaded_files


def unify_schema(parquet_files):
    """ 读取所有 Parquet 文件，统一 Schema """
    tables = [pq.read_table(f) for f in parquet_files]
    all_fields = set()

    # 获取所有可能的字段
    for table in tables:
        all_fields.update(table.schema.names)

    # 统一 schema
    new_tables = []
    for table in tables:
        missing_fields = all_fields - set(table.schema.names)
        for field in missing_fields:
            table = table.append_column(field, pa.array([None] * len(table), type=pa.string()))  # 以 string 类型填充
        new_tables.append(table)

    return new_tables


def merge_parquet_files(parquet_files, output_file):
    tables = unify_schema(parquet_files)  # 先统一 schema
    merged_table = pa.concat_tables(tables)
    pq.write_table(merged_table, output_file)

    print(f"Merged {len(parquet_files)} files into {output_file}")


def fetch_source_data(source_data_ids):
    query = f"""
        SELECT *
        FROM source_data
        WHERE source_data_id IN ({source_data_ids})
        ORDER BY raw_time
    """
    return db_util.fetch_all(query)


def get_merged_parquet_file(source_data_ids):
    df = fetch_source_data(source_data_ids)
    merged_files = {}
    local_dir = current_config.get('containerPath')

    for _, row in df.iterrows():
        raw_time_str = row['raw_time'].strftime("%Y%m%d_%H%M%S")
        obs_prefix = f"{row['project_name']}/{row['plate_no']}/raw_{raw_time_str}/canbus/"
        local_path = os.path.join(local_dir, raw_time_str)
        os.makedirs(local_path, exist_ok=True)

        downloaded_files = download_parquet_files(obs_prefix, local_path)

        # 归类相同通道
        file_groups = {}
        for file in downloaded_files:
            key = "_".join(os.path.basename(file).split("_")[:2])  # 例如 Fusion_5
            file_groups.setdefault(key, []).append(file)

        # 合并相同通道的 parquet 文件
        for key, files in file_groups.items():
            output_file = os.path.join(local_dir, f"{key}.parquet")
            merge_parquet_files(files, output_file)
            merged_files[key] = output_file

    return merged_files


# 挖掘逻辑
def dig_data():
    task_id = None
    try:
        # 页面参数
        param_page = sys.argv[1]
        logging.info("页面参数为：%s", param_page)
        # 上游传递参数
        param_pipeline = sys.argv[2]
        logging.info("传递参数：%s", param_pipeline)
        argo_pod_name = sys.argv[3]

        if param_page is None or param_pipeline is None:
            raise Exception("参数错误")

        page_value = json.loads(param_page)

        op_file_name = page_value['op_file_name']
        bc_name = page_value['bc_name']
        config_str = page_value['config_str']
        is_make_mcap = page_value['is_make_mcap']
        is_assets = page_value['is_assets']
        main_task_id = page_value['main_task_id']
        metric_config = base64.b64decode(page_value['metric_config']).decode('utf-8')
        op_strs = page_value['op_strs']
        common_strs = page_value['common_strs']

        if config_str is None or bc_name is None:
            raise Exception("参数错误")

        pipeline_value = json.loads(param_pipeline)

        source_id_list = pipeline_value['source_id_list']

        task_id, dataset_name = generate_taskid_dataset_name(pipeline_value, page_value, source_id_list, op_file_name, config_str, bc_name, argo_pod_name)

        # 从git中拉取算子代码及对应配置
        metric_config_json = json.loads(metric_config)
        script_local_path_list = generate_local_op_file(op_strs)
        # 保存common函数脚本文件，用于后续算子调用
        generate_local_op_file(common_strs)

        if not script_local_path_list:
            raise Exception("下载算子文件失败")

        operator_framework = OperatorFramework()

        # 用户自定义的算子公共函数
        operator_framework.load_multiple_operators(script_local_path_list)

        merged_files = get_merged_parquet_file(source_id_list)

        directory_path_list, source_file_ids, task_result, middle_files_map, source_state_map = exe_dig(merged_files,
                                                                    page_value, script_local_path_list,
                                                                    metric_config_json, main_task_id, task_id,
                                                                    operator_framework)

        check_clean_result(source_file_ids, task_id, dataset_name, task_result,source_state_map, is_assets, op_file_name, bc_name, config_str)

        if is_make_mcap == 1:
            if len(directory_path_list) > 0:
                makeMcap.create_mcap(directory_path_list)

        # 保存中间文件
        save_dig_middle_files(main_task_id, middle_files_map, source_state_map)
    except Exception as e:
        logging.exception("场景挖掘异常")
        if task_id is not None:
            sql_statements = []
            values_list = []
            sql_statements.append("update datacenter_datadeal set status = 4, result_time = now() where id =%s")
            values_list.append(task_id)
            execute_sql(sql_statements, values_list)

        raise Exception(e)
    finally:
        if os.path.exists(current_config.get('containerPath')):
            shutil.rmtree(current_config.get('containerPath'))

    logging.info("dig data end.")


if __name__ == "__main__":
    dig_data()
