# -*- coding: utf-8 -*-
import base64
import copy
import json
import logging
import os
import shutil
import sys
from collections import defaultdict
from datetime import datetime

import pandas as pd
import ulid

import const_key
import env_manager
import label_util
from data_deal_util import execute_sql, upload_to_obs, generate_local_op_file, download_files_by_extension
from operator_framework import OperatorFramework
from util import data_utils
from util import nacos_client
from util.db_module import db_util
import git_util
from env_manager import env_manager

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
    def __init__(self, start_time, end_time, start_frame, end_frame, custom_tags,
                 operator_version, source_data_ids=None):
        self.timePeriod = [{
            "start_time": start_time,
            "end_time": end_time,
            "start_frame": start_frame,
            "end_frame": end_frame,
            "custom_tags": custom_tags,
            "operator_version": operator_version,
            "source_data_ids": source_data_ids
        }]

    def to_dict(self):
        return {
            "timePeriod": self.timePeriod,
        }


def convert_timestamp_to_datetime(timestamp):
    """将时间戳转换为 MySQL 可接受的 DATETIME 格式"""
    if timestamp:
        return datetime.fromtimestamp(float(timestamp))
    return None  # 如果没有有效的时间戳，返回 None 或者你可以返回默认时间


def get_closest_frame(merged_sensor_data, target_timestamp):
    # 检查 merged_sensor_data 是否为空
    if not merged_sensor_data:
        logging.warning("没有帧号数据，无法找到最近的帧号")
        return None

    # 计算每个时间戳与目标时间戳的差值，找到差值最小的帧号
    closest_frame = min(merged_sensor_data, key=lambda frame: abs(merged_sensor_data[frame] - target_timestamp))

    return closest_frame


def save_middle_files(operators_cvs_df_list, operators_topic_df_list, obs_prefix, local_path_prefix):
    # 合并所有 cvs_df
    if operators_cvs_df_list:
        operators_cvs_df = pd.concat(operators_cvs_df_list, ignore_index=True)  # 合并所有 DataFrame
        # 保存到本地 CSV 文件
        dataset_csv_path = os.path.join(local_path_prefix, "analysis.csv")
        operators_cvs_df.to_csv(dataset_csv_path, index=False)  # 保存为 CSV，不包括行索引
        logging.info("analysis.csv has been saved ")
    else:
        logging.info("No analysis.csv to save ")

    # 如果你需要处理 operators_topic_df_list，可以在这里添加类似的逻辑
    # 例如：
    if operators_topic_df_list:
        operators_topic_df = pd.concat(operators_topic_df_list, ignore_index=True)
        dataset_topic_path = os.path.join(local_path_prefix, "topic.csv")
        operators_topic_df.to_csv(dataset_topic_path, index=False)
        logging.info("topic.csv has been saved")
    else:
        logging.info("No topic.csv to save")

    # 上传文件
    file_names = ["analysis.csv", "topic.csv"]
    # 云完整路径
    resul_file_name = []

    for file_name in file_names:
        result_obs_file = obs_prefix + file_name
        # 上传回灌结果
        file_path = os.path.join(local_path_prefix, file_name)
        if not os.path.isfile(file_path):
            logging.info(f"File {file_path} does not exist.")
            continue

        upload_to_obs(result_obs_file, file_path)
        resul_file_name.append(result_obs_file)
        logging.info(f"挖掘中间文件{file_path}保存到OBS {result_obs_file}")

    return resul_file_name


def save_dig_result(json_data, task_id, is_assets):
    """
    保存场景挖掘结果，并返回插入的数据列表，包含插入后的 ID

    :param json_data: JSON 字符串，包含多个场景挖掘结果
    :param task_id: 任务 ID
    :param is_assets: 是否资产化
    :return: 插入的数据列表
    """
    # 解析 JSON 数据
    scene_object_list = json.loads(json_data)

    # 获取任务名称
    sql = "SELECT deal_name FROM datacenter_datadeal WHERE id = %s"
    result = db_util.fetch_one(sql, (task_id,))
    task_name = result.get('deal_name') if result else ""

    insert_params = []
    operator_datas = []

    # 准备插入的数据
    for scene_object in scene_object_list:
        for time_period in scene_object.get("timePeriod", []):
            data_id = ulid.ulid()
            start_time = convert_timestamp_to_datetime(time_period.get("start_time"))
            end_time = convert_timestamp_to_datetime(time_period.get("end_time"))
            start_frame = time_period.get("start_frame")
            start_frame = int(start_frame) if start_frame is not None else 0

            end_frame = time_period.get("end_frame")
            end_frame = int(end_frame) if end_frame is not None else 0

            param = (
                task_id, task_name, time_period.get("source_data_ids"), start_time, end_time,
                start_frame, end_frame, is_assets, 'admin', datetime.now(), 0, data_id
            )
            insert_params.append(param)

            # 记录算子版本和自定义标签
            operator_datas.append({
                "custom_tags": time_period["custom_tags"],
                "operator_version": time_period["operator_version"]
            })

    if not insert_params:
        return []  # 若无数据可插入，直接返回空列表

    # 批量插入 SQL 语句
    insert_sql = """
        INSERT INTO datacenter_dig_detail 
        (task_id, task_name, source_data_ids, start_time, end_time, start_frame, end_frame, is_assets, creater, create_time, is_delete, data_id)  
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

    # 执行批量插入并获取插入后的 ID
    inserted_ids = db_util.insert_batch([insert_sql] * len(insert_params), insert_params)

    # 构造返回的数据列表
    insert_data_list = []
    for idx, param in enumerate(insert_params):
        insert_data_list.append({
            "id": inserted_ids[idx],  # 数据库插入后的 ID
            "task_id": param[0],
            "task_name": param[1],
            "source_data_ids": param[2],
            "start_time": param[3],
            "end_time": param[4],
            "start_frame": param[5],
            "end_frame": param[6],
            "is_assets": param[7],
            "creater": param[8],
            "create_time": param[9],
            "is_delete": param[10],
            "data_id": param[11],
            "operator_datas": operator_datas[idx]  # 对应的 operator_datas 数据
        })

    return insert_data_list


def save_dig_middle_files(main_task_id, task_id, middle_files_obs_path, dig_result):
    """
    保存场景挖掘中间文件
    :param main_task_id: 主任务id
    :param task_id: 任务id
    :param middle_files_obs_path: 中间文件obs路径
    :param dig_result: 挖掘结果
    """
    if dig_result:
        stat = SUCCESS
    else:
        stat = FAILED
    # 准备插入的数据
    param = (
        main_task_id,
        task_id,
        stat,
        ",".join(middle_files_obs_path)
    )

    # 插入数据的 SQL 语句，使用 %s 作为占位符
    insert_sql = """
    INSERT INTO datacenter_dig_detail_files 
    (main_id, task_id, state, middle_files)  
    VALUES (%s, %s, %s, %s)
    """

    db_util.insert_and_get_id(insert_sql, param)


def bulk_insert_to_es(first_source_data_id, dig_detail_list, task_data):
    """
    批量将挖掘结果插入到 Elasticsearch 中
    :param first_source_data_id: 第一个原始数据包的 ID
    :param dig_detail_list: 每个原始数据挖掘的结果
    :param task_data: 任务数据
    """
    task_id = task_data["id"]
    need_delete_dig_id = []
    try:
        # 调用 selectByIdList 方法批量查询 Elasticsearch，获取原始文档
        original_doc = label_util.selectSourceDataLabelById(first_source_data_id)

        # 准备批量插入的文档数据
        doc_list = []
        all_insert_ids = []

        # 自定义标签:
        custom_tags_list = []

        for detail_msg in dig_detail_list:
            # 创建 doc 的副本，防止修改原文档
            doc_copy = copy.deepcopy(original_doc)
            operator_version = detail_msg.get("operator_datas", {}).get("operator_version")
            operator_version = float(operator_version) if operator_version else 0.0
            is_cross = len(detail_msg['source_data_ids'].split(",")) > 1
            # 更新文档数据
            doc_copy['data_info']['dig_info'] = {
                "id": detail_msg['id'],  # 从插入的 ID 集合获取 dig_id
                "task_id": task_id,  # 使用传入的 task_id
                "create_time": int(detail_msg['create_time'].timestamp() * 1000),  # 创建时间
                "creator": task_data['creater'],  # 创建人
                "end_frame": detail_msg['end_frame'],  # 结束帧号
                "end_time": int(detail_msg['end_time'].timestamp() * 1000),  # 结束时间戳
                "operator_commit": task_data['bc_name'],  # commit号
                "operator_configure": task_data['config_str'],  # 算子配置
                "operator_name": task_data['op_file_name'],  # 算子名称
                "start_frame": detail_msg['start_frame'],  # 开始帧号
                "start_time": int(detail_msg['start_time'].timestamp() * 1000),  # 开始时间戳
                "is_assets": detail_msg['is_assets'],  # 是否资产化
                "is_cross": is_cross,  # 是否跨包
                "task_name": detail_msg['task_name'],  # 任务名称
                "operator_version": operator_version,  # 算子版本
                "data_id": detail_msg['data_id']  # 场景数据id ULID
            }
            custom_tags = detail_msg.get("operator_datas", {}).get("custom_tags", {})

            # 算子返回的标签 operator_tag_dict = {"category": "ACC", "sub_category": "cut-in", "custom_tags": {}}
            for key, value in custom_tags.items():
                if key not in doc_copy['data_info']['dig_info']:
                    doc_copy['data_info']['dig_info'][key] = value

            # 将处理后的文档添加到 doc_list 中
            doc_list.append(doc_copy)
            all_insert_ids.append(detail_msg['id'])  # 添加 dig_id
            custom_tags_list.append(detail_msg["operator_datas"]["custom_tags"])

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
            # 3.过滤 all_insert_ids 和 doc_list (删除错误包的所有es数据)
            all_insert_ids_filter = []
            doc_list_filter = []
            for i in range(len(all_insert_ids)):
                if doc_list[i]['basic_info']['source_data_id'] in source_data_id_list:
                    need_delete_dig_id.append(all_insert_ids[i])
                else:
                    all_insert_ids_filter.append(all_insert_ids[i])
                    doc_list_filter.append(doc_list[i])
            all_insert_ids = all_insert_ids_filter
            doc_list = doc_list_filter
        # 校验dig_info end
        if len(doc_list) > 0:
            label_util.insertBatchSceneDataLabel(all_insert_ids, doc_list)
            logging.info(f"Successfully inserted {len(doc_list)} documents for task {task_id}")
    except Exception as e:
        logging.exception(f"Failed to insert documents for task {task_id}: {e}")

    return need_delete_dig_id


def execute_dig_scene(channel_file_index, page_value, script_local_path_list, metric_config_json, operator_framework,
                      source_data_list, obs_prefix, local_path_prefix):
    operators_cvs_df_combine_list = []
    operators_topic_df_combine_list = []
    task_result = []
    # 算子：2 构建参数
    operator_param = {const_key.PARAM_PAGE: page_value,  # env:算子文件配置项
                      const_key.LOCAL_CHANNEL_FILE_INDEX: channel_file_index,  # dig数据本地数据集路径
                      const_key.KEY_METRIC_CONFIG: metric_config_json,  # 算子json内配置项
                      "obs_prefix": obs_prefix,  # 原始obs路径
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
            merged_sensor_data = merge_and_sort_timestamps(source_data_list, local_path_prefix)

            for dig_result in dig_result_list:
                start_time = dig_result[0]
                end_time = dig_result[1]

                # 检查时间差是否超过5分钟（300秒）
                if (end_time - start_time) > 300:
                    raise ValueError(f"时间区间过长: {end_time - start_time} 秒 (超过 5 分钟)")

                start_frame = get_closest_frame(merged_sensor_data, start_time)
                end_frame = get_closest_frame(merged_sensor_data, end_time)
                custom_tags = dig_result[2] if len(dig_result) >= 3 else {}
                result_obj = SceneObject(start_time, end_time, start_frame,
                                         end_frame, custom_tags,
                                         operator_version)
                task_result.append(result_obj)
    return task_result, operators_cvs_df_combine_list, operators_topic_df_combine_list


def check_dig_result(task_data, task_result):
    task_id = task_data["id"]
    is_assets = task_data["is_assets"]

    sql_statements = []
    values_list = []

    if not task_result:
        logging.info("未筛选出对应的场景")
        return True
    else:
        task_result_dicts = [obj.to_dict() for obj in task_result]
        # 将最终结果转换为 JSON 字符串
        final_json = json.dumps(task_result_dicts)
        # 状态设置为成功：3
        sql_statements.append(
            f"update datacenter_datadeal set status = 3, result_num = {len(task_result)}, result_time = now() where id =%s")
        values_list.append(task_id)

        # 保存挖掘结果
        dig_detail_list = save_dig_result(final_json, task_id, is_assets)
        first_source_id = task_result[0].timePeriod[0]["source_data_ids"].split(",")[0]
        # 插入索引
        need_delete_dig_id = bulk_insert_to_es(first_source_id, dig_detail_list, task_data)

        if need_delete_dig_id:
            logging.info("删除挖掘结果：%s", need_delete_dig_id)
            sql_statements.append("update datacenter_dig_detail set is_delete = 1 where id in %s")
            values_list.append((need_delete_dig_id,))

        execute_sql(sql_statements, values_list)

        if need_delete_dig_id:
            return False
        else:
            return True
        # 工作流暂时不使用，先注释掉
        # source = Source(2, ",".join(map(str, insert_batch_ids)))
        # source_dict = source.to_dict()
        # source_json = json.dumps(source_dict)
        #
        # # 写入清洗数据集ID到临时文件中
        # with open('./outParams.txt', 'w', encoding='utf-8') as file:
        #     file.write(source_json)


def merge_parquet_files(input_files, output_file):
    """
    只合并 `timestamp` 字段的 Parquet 文件，并按时间排序，去重后保存
    """
    merged_df = pd.concat(
        (pd.read_parquet(file, columns=["timestamp"]) for file in input_files),
        ignore_index=True
    )

    # 按时间戳排序
    merged_df = merged_df.sort_values(by="timestamp")

    # 去重（如果有重复时间戳）
    merged_df = merged_df.drop_duplicates()

    # 存储合并后的数据
    merged_df.to_parquet(output_file, index=False)


def fetch_source_data(source_data_ids):
    query = f"""
        SELECT *
        FROM datacenter_source_data
        WHERE id IN ({source_data_ids})
        ORDER BY raw_time
    """
    return db_util.fetch_all(query)


def fetch_source_data_by_data_id(source_data_data_ids):
    data_ids = source_data_data_ids.split(",")
    quoted_ids = ", ".join(f"'{id}'" for id in data_ids)

    query = f"""
        SELECT *
        FROM datacenter_source_data
        WHERE data_id IN ({quoted_ids})
        ORDER BY raw_time
    """
    return db_util.fetch_all(query)


def merge_and_sort_timestamps(source_data_list, local_path_prefix):
    time_stamp_paths = download_sensor_files(source_data_list, local_path_prefix)

    if not time_stamp_paths:
        logging.error("下载时间戳文件失败")
        return {}

    all_timestamps = set()  # 使用 set 去重

    for path in time_stamp_paths:
        if not os.path.exists(path):
            logging.warning("文件不存在，跳过：%s", path)
            continue

        try:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            logging.error("解析 JSON 失败：%s，文件：%s", e, path)
            continue
        except Exception as e:
            logging.error("读取 JSON 失败：%s，文件：%s", e, path)
            continue

        # 获取 sensor 数据
        sensor_data = data.get('sensor', {})
        if not sensor_data:
            logging.warning("文件中未找到 'sensor' 数据，跳过：%s", path)
            continue

        # 取第一个 sensor 设备的数据
        first_sensor_key = next(iter(sensor_data), None)
        if first_sensor_key is None:
            logging.warning("sensor_data 为空，跳过：%s", path)
            continue

        first_sensor_value = sensor_data[first_sensor_key]  # 取出帧号 → 时间戳映射

        if not first_sensor_value:
            logging.warning("传感器数据为空，跳过：%s", path)
            continue

        # **收集所有时间戳**
        all_timestamps.update(first_sensor_value.values())

    # 检查 all_timestamps 是否为空
    if not all_timestamps:
        logging.warning("没有找到任何时间戳，无法生成帧号 → 时间戳映射")
        return {}

    # **排序所有时间戳**
    sorted_timestamps = sorted(all_timestamps)

    # **生成新的帧号 → 时间戳映射**
    merged_sensor_data = {i + 1: ts for i, ts in enumerate(sorted_timestamps)}

    return merged_sensor_data  # 返回新的字典


def download_sensor_files(source_data_list, local_path_prefix):
    time_stamp_paths = []

    for row in source_data_list:
        raw_time_str = row['raw_time'].strftime("%Y%m%d_%H%M%S")
        obs_unify_file = f"{row['project_name']}/{row['plate_no']}/raw_{raw_time_str}/unify_dataset/time_stamp.json"
        local_path = os.path.join(local_path_prefix, raw_time_str)
        os.makedirs(local_path, exist_ok=True)

        result = data_utils.get_object(obs_unify_file, local_path + "/time_stamp.json")
        if result:
            time_stamp_paths.append(local_path + "/time_stamp.json")

    return time_stamp_paths


def get_data_deal_by_id(task_id):
    sql = f"SELECT * FROM datacenter_datadeal WHERE id = {task_id}"
    return db_util.fetch_one(sql)


def get_parquet_time_range(file):
    """
    读取 Parquet 文件的最小和最大时间戳，只加载 timestamp 列
    """
    min_time, max_time = None, None

    df = pd.read_parquet(file, columns=["timestamp"])
    if not df.empty:
        file_min_time, file_max_time = df["timestamp"].min(), df["timestamp"].max()
        min_time = file_min_time if min_time is None else min(min_time, file_min_time)
        max_time = file_max_time if max_time is None else max(max_time, file_max_time)
    return min_time, max_time


def get_parquet_index(source_data_list, local_path_prefix):
    """
    计算每个 source_data_id 独立的时间区间，并建立：
    1. `index`：数据包级别索引，仅包含 min_time 和 max_time
    2. `channel_file_index`：按通道（如 pcan, acan）组织，存储相关的 parquet 文件，方便跨包合并

    确保时间段连续，返回两个索引结构。
    """
    index = {}
    channel_file_index = defaultdict(list)  # 以通道为 key，存储相关的 parquet 文件
    previous_max_time = None  # 记录上一包的 max_time

    # 按 raw_time 排序，确保顺序处理
    for row in sorted(source_data_list, key=lambda x: x['raw_time']):
        source_data_id = row['id']
        raw_time_str = row['raw_time'].strftime("%Y%m%d_%H%M%S")
        obs_prefix = f"{row['project_name']}/{row['plate_no']}/raw_{raw_time_str}/canbus/"
        local_path = local_path_prefix + raw_time_str

        # 下载该包的所有 Parquet 文件
        downloaded_files = download_files_by_extension(obs_prefix, local_path, ".parquet")

        # 计算当前包的 min_time 和 max_time
        package_min_time, package_max_time = None, None

        for file in downloaded_files:
            min_time, max_time = get_parquet_time_range(file)  # 获取单个 parquet 的时间范围
            if min_time is not None and max_time is not None:
                if package_min_time is None or min_time < package_min_time:
                    package_min_time = min_time
                if package_max_time is None or max_time > package_max_time:
                    package_max_time = max_time

                # 解析通道名称，例如 pcan_1.parquet -> pcan
                channel_key = os.path.basename(file).split("_")[0].lower()
                channel_file_index[channel_key].append(file)

        # 确保时间连续
        if previous_max_time is not None and package_min_time is not None:
            package_min_time = max(package_min_time, previous_max_time)

        # 更新 previous_max_time
        previous_max_time = package_max_time if package_max_time is not None else previous_max_time

        # 存储 source_data_id 索引
        if package_min_time is not None and package_max_time is not None:
            index[source_data_id] = {
                "min_time": package_min_time,
                "max_time": package_max_time
            }

    return index, dict(channel_file_index)  # 返回两个索引


def get_source_ids_in_range(source_index, start_time, end_time):
    """
    根据给定的时间范围，获取所有在 [start_time, end_time] 内的 source_data_id。

    :param source_index: dict, 形如 {source_id: {"min_time": ..., "max_time": ...}}
    :param start_time: float, 查询的起始时间
    :param end_time: float, 查询的结束时间
    :return: list, 按时间排序的 source_data_id 列表
    """
    if start_time > end_time:
        raise ValueError("起始时间不能大于结束时间")

    # 选取所有时间区间与 [start_time, end_time] 有交集的 source_data_id
    filtered_ids = [
        source_id for source_id, time_range in source_index.items()
        if time_range["max_time"] > start_time and time_range["min_time"] < end_time
    ]

    # 按 min_time 进行排序
    filtered_ids.sort(key=lambda x: source_index[x]["min_time"])

    return filtered_ids


# 挖掘逻辑
def dig_data():
    task_id = None
    try:
        local_path_prefix, main_task_id, metric_config_json, obs_prefix, script_local_path_list, source_data_list, task_data, task_id, page_value = (
            parse_params() if env_manager.is_prod() else parse_debug_params())

        operator_framework = OperatorFramework()

        # 用户自定义的算子公共函数
        operator_framework.load_multiple_operators(script_local_path_list)

        source_index, channel_file_index = get_parquet_index(source_data_list, local_path_prefix)

        # 执行挖掘逻辑
        task_result, operators_cvs_df_combine_list, operators_topic_df_combine_list = execute_dig_scene(
            channel_file_index,
            page_value,
            script_local_path_list,
            metric_config_json,
            operator_framework,
            source_data_list,
            obs_prefix,
            local_path_prefix)

        if env_manager.is_debug():
            logging.info("调试模式，不更新任务状态")
            return

        # 保存中间文件
        middle_files_obs_path = save_middle_files(operators_topic_df_combine_list, operators_cvs_df_combine_list,
                                                  obs_prefix, local_path_prefix)

        if task_result:
            for result in task_result:
                start_time = result.timePeriod[0]["start_time"]
                end_time = result.timePeriod[0]["end_time"]

                # 获取当前 SceneObject 对应的 source_data_id 集合
                result_source_ids = get_source_ids_in_range(source_index, start_time, end_time)

                if not result_source_ids:
                    logging.error(f"挖掘结果start_time: {start_time}, end_time:{end_time} 未找到对应的 source_data_id")
                    raise Exception(
                        f"挖掘结果start_time: {start_time}, end_time:{end_time} 未找到对应的 source_data_id")
                # 以逗号分隔的字符串存储
                source_ids_str = ",".join(map(str, result_source_ids))
                result.timePeriod[0]["source_data_ids"] = source_ids_str

            # 更新任务状态
            dig_result = check_dig_result(task_data, task_result)
        else:
            logging.info("未筛选出对应的场景")
            dig_result = False
            sql_statements = []
            values_list = []
            sql_statements.append("update datacenter_datadeal set status = 3, result_time = now() where id =%s")
            values_list.append(task_id)
            execute_sql(sql_statements, values_list)
        # if is_make_mcap == 1:
        # if len(directory_path_list) > 0:
        #     makeMcap.create_mcap(directory_path_list)

        # 保存中间文件
        save_dig_middle_files(main_task_id, task_id, middle_files_obs_path, dig_result)
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


def parse_params():
    # 页面参数
    param_page = sys.argv[1]
    logging.info("页面参数为：%s", param_page)
    # 上游传递参数
    param_pipeline = sys.argv[2]
    logging.info("传递参数：%s", param_pipeline)

    if param_page is None or param_pipeline is None:
        raise Exception("参数错误")

    page_value = json.loads(param_page)

    metric_config = base64.b64decode(page_value['metric_config']).decode('utf-8')
    op_strs = page_value['op_strs']
    common_strs = page_value['common_strs']

    pipeline_value = json.loads(param_pipeline)
    task_id = pipeline_value['task_id']

    task_data = get_data_deal_by_id(task_id)

    sql_statements_process = []
    values_list_process = []
    sql_statements_process.append("update datacenter_datadeal set status = 2 where id =%s")
    values_list_process.append(task_id)
    execute_sql(sql_statements_process, values_list_process)

    if task_data is None:
        raise Exception("未查询到任务信息")

    page_value['task_id'] = task_id
    page_value['op_file_name'] = task_data['op_file_name']
    page_value['bc_name'] = task_data['bc_name']
    page_value['config_str'] = task_data['config_str']
    page_value['is_make_mcap'] = task_data['is_make_mcap']
    page_value['is_assets'] = task_data['is_assets']
    page_value['main_task_id'] = task_data['main_id']

    main_task_id = task_data['main_id']

    source_ids = task_data['source_file_ids']
    source_data_list = fetch_source_data(source_ids)

    if not source_data_list:
        raise Exception("未查询到原始数据")

    project_name = source_data_list[0]['project_name']
    plate_no = source_data_list[0]['plate_no']

    obs_prefix = project_name + "/" + plate_no + "/dig/" + str(main_task_id) + "_" + str(task_id) + "/"
    # 本地路径前缀
    local_path_prefix = current_config.get('containerPath') + obs_prefix

    # 从git中拉取算子代码及对应配置
    metric_config_json = json.loads(metric_config)
    script_local_path_list = generate_local_op_file(op_strs, local_path_prefix)
    # 保存common函数脚本文件，用于后续算子调用
    generate_local_op_file(common_strs, local_path_prefix)

    if not script_local_path_list:
        raise Exception("下载算子文件失败")

    return local_path_prefix, main_task_id, metric_config_json, obs_prefix, script_local_path_list, source_data_list, task_data, task_id, page_value


def parse_debug_params():
    # 页面参数
    param_page = sys.argv[1]
    logging.info("页面参数为：%s", param_page)
    # 上游传递参数
    param_pipeline = sys.argv[2]
    logging.info("传递参数：%s", param_pipeline)

    if param_page is None or param_pipeline is None:
        raise Exception("参数错误")

    page_value = json.loads(param_page)
    pipeline_value = json.loads(param_pipeline)

    op_file_name = page_value['op_file_name']
    data_ids = pipeline_value['source_id_list']

    main_task_id = 1
    task_id = 1

    source_data_list = fetch_source_data_by_data_id(data_ids)

    if not source_data_list:
        raise Exception("未查询到原始数据")

    project_name = source_data_list[0]['project_name']
    plate_no = source_data_list[0]['plate_no']

    obs_prefix = project_name + "/" + plate_no + "/dig/" + str(main_task_id) + "_" + str(task_id) + "/"
    # 本地路径前缀
    local_path_prefix = current_config.get('containerPath') + obs_prefix

    script_local_path_list, metric_config_json = git_util.parse_debug_operator_info_by_json(op_file_name, "")

    if not script_local_path_list:
        raise Exception("下载算子文件失败")

    return local_path_prefix, main_task_id, metric_config_json, obs_prefix, script_local_path_list, source_data_list, None, task_id, page_value


if __name__ == "__main__":
    dig_data()
