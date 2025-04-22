import json
import logging
import const_key
import pandas as pd
from util import nacos_client
import scene_util
from evaluat import db_util
import datetime

# 通过 get_config() 函数获取配置（懒加载）
current_config = nacos_client.get_config()

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def tags(local_tag_path):
    """
        - 道路类型
    """
    # 行车场景：高速
    tag_road = []
    # 白天黑夜
    # day_night_tag = []
    # 车辆载重：空载、半载、满载
    tag_car_load = []
    # 标签名-地区
    tag_region = []
    json_array = None

    try:
        with open(local_tag_path, 'r', encoding='utf-8') as file:
            json_array = json.loads(file.read())
    except Exception as err:
        logging.error(f'tag.json {local_tag_path}  json解析失败：' + str(err))

    if json_array is None:
        return '其他', '其他', '其他'

    for item in json_array:
        if item is None:
            continue

        if 'stowageState' in item and item['stowageState'] != '':
            tag_car_load.append(item['stowageState'])

        if 'station' in item and item['station'] != '':
            tag_region.append(item['station'])

        if 'sectionTag' in item and 'tagName' in item['sectionTag']:
            tagName = item['sectionTag']['tagName']
            if tagName == '行车场景' and 'tagName' in item['sectionTag']['children']:
                tag_road.append(item['sectionTag']['children']['tagName'])

    # 过滤无意义的标签

    tag_road = list(filter(lambda x: x and x != '', tag_road))
    tag_car_load = list(filter(lambda x: x and x != '', tag_car_load))
    tag_region = list(filter(lambda x: x and x != '', tag_region))

    # 取第一个，检测不到标签类型用其他代替
    tag_road = tag_road[0:1] if tag_road else ['其他']
    tag_car_load = tag_car_load[0:1] if tag_road else ['其他']
    tag_region = tag_region[0:1] if tag_road else ['其他']

    # 结果以逗号分隔
    return ','.join(tag_road), ','.join(tag_car_load), ','.join(tag_region)


def tag_day_or_night(raw_time: datetime):
    if raw_time is None:
        return "其他"

    hour = raw_time.now().hour
    if 0 <= int(hour) <= 7:
        return "清晨"
    elif 7 < int(hour) <= 12:
        return "上午"
    elif 12 < int(hour) <= 18:
        return "下午"
    elif 18 < int(hour) <= 21:
        return "傍晚"
    else:
        return "夜晚"


def get_local_path(cloud_raw_path):
    return const_key.EVAL_LOCAL_DIR_PREFX + cloud_raw_path


def is_valid_timestamp(timestamp):
    """
    检查时间戳是否有效
    """
    try:
        return timestamp is not None and float(timestamp) > 0
    except (ValueError, TypeError):
        return False


def cal_mileage(pcan_path, start_timestamp, end_timestamp):
    """
    计算里程
    :param pcan_path: 数据文件路径
    :param start_timestamp: 起始时间戳
    :param end_timestamp: 结束时间戳
    :return: 里程（单位：米），如果数据异常返回 0.0
    """
    if pcan_path is None:
        logging.warning("pcan_path 为 None，无法计算里程")
        return 0.0

    try:
        # 读取数据
        df = pd.read_parquet(pcan_path)[[const_key.KEY_CGW_HIGRESOLUTIONTRIPDST, const_key.KEY_TIMESTAMP]]

        # 检查数据是否为空
        if df.empty:
            logging.info(f"里程统计 {pcan_path} 无数据")
            return 0.0

        # 处理数据中的 NaN
        df = df.dropna(subset=[const_key.KEY_CGW_HIGRESOLUTIONTRIPDST, const_key.KEY_TIMESTAMP])
        if df.empty:
            logging.warning(f"里程统计 {pcan_path} 数据异常，所有里程数据为 NaN")
            return 0.0

        # 获取第一帧的值
        if not is_valid_timestamp(start_timestamp):
            first_value = df.iloc[0][const_key.KEY_CGW_HIGRESOLUTIONTRIPDST]
        else:
            # 计算每一行 TIMESTAMP 与目标时间的差值
            df['time_diff_start'] = abs(df[const_key.KEY_TIMESTAMP] - float(start_timestamp))
            # 找到时间差最小的行
            df_closest = df.loc[df['time_diff_start'].idxmin()]
            first_value = df_closest[const_key.KEY_CGW_HIGRESOLUTIONTRIPDST]

        # 获取最后一帧的值
        if not is_valid_timestamp(end_timestamp):
            last_value = df.iloc[-1][const_key.KEY_CGW_HIGRESOLUTIONTRIPDST]
        else:
            # 计算每一行 TIMESTAMP 与目标时间的差值
            df['time_diff_end'] = abs(df[const_key.KEY_TIMESTAMP] - float(end_timestamp))
            # 找到时间差最小的行
            df_closest = df.loc[df['time_diff_end'].idxmin()]
            last_value = df_closest[const_key.KEY_CGW_HIGRESOLUTIONTRIPDST]

        # 检查 first_value 和 last_value 是否为 NaN
        if pd.isna(first_value) or pd.isna(last_value):
            logging.warning(f"里程统计 {pcan_path} 数据异常，first_value 或 last_value 为 NaN")
            return 0.0

        # 计算里程（单位：米）
        miles = abs(last_value - first_value)
        return miles if not pd.isna(miles) else 0.0

    except Exception as e:
        logging.error(f"里程统计 {pcan_path} 发生异常: {e}")
        return 0.0


def get_operator_common_data(params, task_dataset):
    """
    算子结果落库通用字段
    """
    dataset_info = {"task_dataset_id": task_dataset["id"],
                    "dataset_id": task_dataset["dataset_id"],
                    "dataset_name": task_dataset["dataset_name"],
                    "dataset_path": task_dataset["dataset_path"],
                    "data_id": task_dataset["data_id"],
                    "start_timestamp": task_dataset["start_timestamp"],
                    "end_timestamp": task_dataset["end_timestamp"],
                    "start_frame_no": task_dataset["start_frame_no"],
                    "end_frame_no": task_dataset["end_frame_no"]}

    # 拼接回放url
    if "start_timestamp" in dataset_info:
        start_timestamp = dataset_info["start_timestamp"]
    else:
        start_timestamp = 0

    if "end_timestamp" in dataset_info:
        end_timestamp = dataset_info["end_timestamp"]
    else:
        end_timestamp = 0

    dataset_info["playback_url"] = gen_playback_url(start_timestamp, end_timestamp, dataset_info["task_dataset_id"])

    # 车辆软硬件版本信息
    dataset_label_dict = params[const_key.DATASET_LABEL_KEY]
    dataset_info["autopilot_version"] = dataset_label_dict["basic_info"]["autopilot_version"]
    dataset_info["ars_version"] = dataset_label_dict["basic_info"]["ars_version"]
    dataset_info["plate_no"] = dataset_label_dict["basic_info"]["plate_no"]

    # 获取上游数据集标签信息 TODO
    try:
        if "dig_info" in dataset_label_dict.get("data_info", {}):
            dataset_info["data_info_operator_name"] = dataset_label_dict["data_info"]["dig_info"]["operator_name"]
            dataset_info["data_info_task_name"] = dataset_label_dict["data_info"]["dig_info"]["task_name"]
        elif "split_info" in dataset_label_dict.get("data_info", {}):
            dataset_info["data_info_operator_name"] = dataset_label_dict["data_info"]["split_info"]["operator_name"]
            dataset_info["data_info_operator_name"] = dataset_label_dict["data_info"]["split_info"]["task_name"]
        else:
            logging.info("不是切片或场景数据")
    except KeyError:
        logging.info("切片或场景数据上游标签没有operator_name或task_name")

    # 获取场景标签
    tag_road, tag_car_load, tag_region = None, None, None
    tag_path = scene_util.get_tag_path(params[const_key.LOCAL_RAW_DOWNLOAD_PATH_KEY])
    if tag_path is not None:
        tag_road, tag_car_load, tag_region = tags(tag_path)
    source_data = db_util.get_source_data(task_dataset["source_data_ids"].split(",")[0])[0]

    # 白天夜晚统计 TODO 标签
    tag_day_night = tag_day_or_night(source_data["raw_time"])
    logging.info(
        f"统计 {task_dataset['dataset_path']} 标签 道路类型: {tag_road}， 配载类型: {tag_car_load}， 地区: {tag_region} "
        f"白天夜晚: {tag_day_night}")

    # TODO 这块应该从数据源头解决，不要定制化
    if tag_region == "xian":
        tag_region = "西安"
    elif tag_region == "zhizi":
        tag_region = "质子"

    # 算子私有字段
    # weather 早期为string，es不支持类型变更，兼容
    weather = dataset_label_dict["data_info"]["PEGASUS_label_info"]["weather"]
    # 判断 weather 的类型
    if isinstance(weather, list):
        # 如果是列表，转换为逗号分隔的字符串
        weather = ",".join(weather)
    elif not isinstance(weather, str):
        weather = ""

    dataset_label_dict["data_info"]["PEGASUS_label_info"]["weather"] = weather

    operator_info = {"weather": weather, "tag_road": tag_road,
                     "tag_car_load": tag_car_load, "tag_day_night": tag_day_night,
                     "tag_region": tag_region}

    # 通用字段：dataset_info和算子私有字段operator_info有重叠字段是出于统计需要
    # 比如A算子负载统计里程，B算子负载统计接管数，C算子统计白天黑夜数
    # 需求1.要统计榆林地区的百公里接管数量：count(b.take_over_count)/sum(a.mileage) group by dataset_info.tag_region
    # 需求2.统计白天数量：count(c.tag_day_night)，而不能用dataset_info.tag_day_night，因为dataset_info有重复，不准
    dataset_info.update(operator_info)
    return dataset_info, operator_info


def gen_playback_url(scene_start_time, scene_end_time, dataset_id):
    """
    生成回放url
    """

    playback_url = ''
    playback_url += ('<a href="' + current_config.get('playback_page_url') + '?taskDatasetId=' + str(
        dataset_id) + '&sceneStartTime=' + str(scene_start_time) + '&sceneEndTime='
                     + str(scene_end_time) + '">回放时刻</a>&nbsp;&nbsp;&nbsp;')

    return playback_url

