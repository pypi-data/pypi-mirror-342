# -*- coding: utf-8 -*-
import json
import logging
import os
import shutil
import sys
from collections import defaultdict, namedtuple
from dataclasses import asdict, fields
from typing import Dict, Optional, List, Union

import can
import cantools
import cv2
import numpy as np
import pandas as pd
from can import ASCReader
from google.protobuf import descriptor_pb2, descriptor_pool
from google.protobuf.message_factory import GetMessageClass
from mcap_protobuf.writer import Writer
from scipy import interpolate

import label_util
from dags.domain.source_tag import SourceTag
from tag import BusChannelQuality, VideoChannelQuality, DataRecord, PEGASUSLabelInfo
from util import data_utils
from util import message_util
from util import nacos_client
from util.date_utils import DateUtils
from util.db_module import db_util

IS_CLEAN_SUCCESS = 1

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

current_config = nacos_client.get_config()  # 获取配置

TIMESTAMP = "timestamp"
INTERVAL_S = 0.02


def get_single_type(signal):
    # 1-bit 信号作为布尔值
    if signal.length == 1:
        return "bool"

    # 处理浮点数（如果 scale 不是 1 或 0，通常是浮点数）
    if signal.is_float or signal.scale not in [1, 0]:
        return "float32" if signal.length == 32 else "float64"

    # 处理整数类型
    min_value, max_value = signal.minimum, signal.maximum  # DBC 定义的物理值范围

    # **关键调整**：如果最小值是负数，则必须是 **有符号整数**
    if min_value < 0:
        if signal.length <= 8:
            return "int8"
        elif signal.length <= 16:
            return "int16"
        elif signal.length <= 32:
            return "int32"
        else:
            return "int64"
    else:
        # 无符号整数
        if signal.length <= 8:
            return "uint8"
        elif signal.length <= 16:
            return "uint16"
        elif signal.length <= 32:
            return "uint32"
        else:
            return "uint64"


def need_process_meta(project_name, plate_no):
    plate_config = current_config.get('clean_config', {})
    plate_config = plate_config.get(project_name, {})
    plate_config = plate_config.get(plate_no, {})
    if plate_config.get('processMeta', False):
        return True
    return False


def find_dbc_file(matching_file, source_data, sensor_data, local_path_prefix):
    dbc_file = None
    need_check_single = None
    channel_no = sensor_data['no']
    project_name = source_data.get('project_name')
    plate_no = source_data.get('plate_no')
    raw_time = source_data.get('raw_time')
    raw_name = raw_time.strftime("raw_%Y%m%d_%H%M%S")

    vehicle_info_path = f"{project_name}/{plate_no}/{raw_name}/conf/vehicle_info/vehicle_info.json"
    local_vehicle_path = local_path_prefix + vehicle_info_path
    data_utils.get_object(vehicle_info_path, local_vehicle_path)

    sql = f"select * from datacenter_vehicle_sensor_analysis_files where sensor_id = {sensor_data['id']} order by id desc"
    analysis_files = db_util.fetch_all(sql)

    if not os.path.exists(local_vehicle_path) or os.path.getsize(local_vehicle_path) == 0:
        if analysis_files is not None and len(analysis_files) > 0:
            dbc_file, need_check_single = analysis_files[0]['file_url'], analysis_files[0]['check_single']
    else:
        # 打开并读取 JSON 文件
        with open(local_vehicle_path, 'r', encoding='utf-8') as file:
            data = json.load(file)  # 解析 JSON 文件内容

        basic_info = data.get("basic_info", {})
        protocol_version_dirt = get_protocol_version(basic_info)

        if channel_no in protocol_version_dirt:
            dirt_analysis_files = protocol_version_dirt[channel_no]

            for analysis_file in analysis_files:
                if analysis_file['file_name'] in dirt_analysis_files:
                    dbc_file, need_check_single = analysis_file['file_url'], analysis_file['check_single']
            if dbc_file is None and analysis_files is not None and len(analysis_files) > 0:
                logging.info("未找到对应的dbc文件，从车辆配置里找对应的文件。channel_no: %s", channel_no)
                dbc_file, need_check_single = analysis_files[0]['file_url'], analysis_files[0]['check_single']
        else:
            if analysis_files is not None and len(analysis_files) > 0:
                dbc_file, need_check_single = analysis_files[0]['file_url'], analysis_files[0]['check_single']

    dbc_name = matching_file.split("/")[-1].split("_")[0].lower()
    dbc_path = f"{project_name}/{plate_no}/{raw_name}/calibration_result"

    # 列出 dbc_path 目录下的所有文件
    dbc_file_list = data_utils.list_files_in_directory(dbc_path)

    # 查找是否有匹配的 DBC 文件
    for dbcfile in dbc_file_list:
        if dbcfile.endswith(".dbc") and dbc_name in dbcfile.lower():  # 确保匹配
            dbc_file = dbcfile  # 直接使用匹配到的文件名
            break  # 找到第一个匹配项后立即退出

    return dbc_file, need_check_single


# 定义一个简单的消息结构，模拟 ASCReader 返回的 msg 对象
SimpleMsg = namedtuple("SimpleMsg", ["timestamp", "arbitration_id", "data"])


def iterate_asc_messages(canbus_file, is_blf_file):
    if is_blf_file:
        with open(canbus_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 4 or parts[2] != "#":
                    continue
                try:
                    timestamp = float(parts[0])
                    arbitration_id = int(parts[1], 16)  # 十六进制转整数
                    data = bytes(int(byte, 16) for byte in parts[3:])
                    yield SimpleMsg(timestamp, arbitration_id, data)
                except (ValueError, IndexError):
                    continue
    else:
        with ASCReader(canbus_file, relative_timestamp=False) as asc:
            for msg in asc:
                yield msg


def analysis_asc_file(sensor_type, source_file, protocol_file, need_check_single, busChannelQuality, error_feishu_message, is_blf_file):
    single_list = [s.strip() for s in need_check_single.split(",")] if need_check_single else []
    signal_presence = {signal: False for signal in single_list}

    # 使用 cantools 加载 DBC 文件
    db = cantools.db.load_file(protocol_file)

    total_distance = 0.0
    prev_timestamp = None
    prev_speed = None  # 记录上一帧的速度（单位：m/s）
    analysis_file_paths = []

    raw_data = {}
    timestamp_min = None
    timestamp_max = None
    last_rolling_counters = {}  # 用于存储每个消息的上一个 Rolling Counter 值
    skip_rolling_counter_check = set()  # 记录已经丢帧的信号
    single_types = {}  # 用于存储每个信号的类型

    dir_path, filename = os.path.split(source_file)
    file_ext = os.path.splitext(filename)[0]
    parquet_file_path = dir_path + '/' + file_ext + '.parquet'
    mcap_file_path = dir_path + '/' + file_ext + '.mcap'
    channel_no = file_ext.split("_")[1]
    asc_type = f"{sensor_type}_{channel_no}"

    message_id_list = db._frame_id_to_message.keys()
    out_of_range_signals = set()  # 用于存储超出范围的信号

    for index, msg in enumerate(iterate_asc_messages(source_file, is_blf_file)):
        if msg.arbitration_id not in message_id_list:
            continue
        # 增加asc文件中某些msg没有在dbc中定义的处理
        frame = db._frame_id_to_message[msg.arbitration_id]
        try:
            message = frame.decode(msg.data, False)
        except Exception as e:
            logging.error(f"Error decoding message: {e}")
            continue

        message[TIMESTAMP] = msg.timestamp
        # 更新最大信号长度
        if timestamp_min is None:
            timestamp_min = msg.timestamp
            timestamp_max = msg.timestamp

        if msg.timestamp > timestamp_max:
            timestamp_max = msg.timestamp

        for signal_name, value in message.items():
            if frame.name not in raw_data:
                raw_data[frame.name] = {}
            if signal_name not in raw_data[frame.name]:
                raw_data[frame.name][signal_name] = []
            raw_data[frame.name][signal_name].append(value)
            if signal_name == TIMESTAMP:
                continue

            signal_key = f"{frame.name}.{signal_name}"
            signal = frame.get_signal_by_name(signal_name)

            # 收集信号类型
            single_types[signal_key] = get_single_type(signal)

            # 检查是否信号丢失
            if signal_name in single_list:
                signal_presence[signal_name] = True
            # 检查信号是否超出范围
            if signal_key not in out_of_range_signals:
                min_value = signal.minimum
                max_value = signal.maximum

                if (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
                    out_of_range_signals.add(signal_key)

                    error_msg = (f"{source_file} 信号 {signal_key} 超出范围: "
                                 f"当前值 {value}, 允许范围 [{min_value}, {max_value}]")
                    logging.error(error_msg)
                    error_feishu_message.append(error_msg)

                    # 记录超出范围的信号
                    busChannelQuality.out_of_range_signals.append(signal_key)

            # 统计里程 速度信号名为 "VCU_VehSpd"（单位：km/h）
            if signal_name == "VCU_VehSpd":
                speed_mps = value / 3.6  # 转换为 m/s

                if prev_timestamp is not None and prev_speed is not None:
                    time_diff = msg.timestamp - prev_timestamp
                    if time_diff > 0:
                        total_distance += prev_speed * time_diff

                # 更新上一次的时间戳和速度
                prev_timestamp = msg.timestamp
                prev_speed = speed_mps

            # 检查是否存在 Rolling Counter
            if "RollingCounter" in signal_name:
                if frame.name in skip_rolling_counter_check:
                    continue
                # 获取 Rolling Counter 的位宽信息
                rolling_counter_max = (2 ** signal.length) - 1  # 计算最大值

                # 如果是第一次遇到该消息，初始化
                if frame.name not in last_rolling_counters:
                    last_rolling_counters[frame.name] = value
                else:
                    # 判断是否连续，考虑循环范围
                    expected_value = (last_rolling_counters[frame.name] + 1) % (rolling_counter_max + 1)
                    if value != expected_value:
                        # 如果不连续，打印日志并退出
                        logging.error(f"{source_file} 检查Rolling Counter 出现丢帧，信号： {frame.name} (Line {index + 1}): "
                                      f"last {last_rolling_counters[frame.name]}, current {value}")
                        error_feishu_message.append(f"{source_file} 检查Rolling Counter 出现丢帧，信号： {frame.name} (Line {index + 1}): "
                                                         f"last {last_rolling_counters[frame.name]}, current {value}")
                        busChannelQuality.bus_channel_rolling_counter_error = True
                        skip_rolling_counter_check.add(frame.name)
                    last_rolling_counters[frame.name] = value
    if skip_rolling_counter_check:
        busChannelQuality.bus_channel_rolling_counter_single = list(skip_rolling_counter_check)

    # 检查是否有缺失的信号
    missing_signals = [signal for signal, present in signal_presence.items() if not present]
    if missing_signals:
        logging.error(f"Missing signals: {', '.join(missing_signals)}")
        busChannelQuality.bus_channel_single_missing = True
        busChannelQuality.bus_channel_missing_singles = ', '.join(missing_signals)
        error_feishu_message.append(f"{source_file} 检查Single 出现丢信号： {', '.join(missing_signals)}")

    if len(raw_data) == 0:
        logging.error("No valid CAN messages found.")
    else:
        timestamp_index = np.arange((timestamp_min // INTERVAL_S) * INTERVAL_S,
                                    (timestamp_max // INTERVAL_S) * INTERVAL_S,
                                    INTERVAL_S)

        descriptor_proto = descriptor_pb2.FileDescriptorProto()
        descriptor_proto.name = f'{asc_type}.proto'
        pool = descriptor_pool.Default()

        for message_name in raw_data:
            message_descriptor = descriptor_proto.message_type.add()
            message_descriptor.name = f'{asc_type}_{message_name}'
            number = 1
            for signal in raw_data[message_name]:
                if signal == TIMESTAMP:
                    continue
                field_descriptor = message_descriptor.field.add()
                field_descriptor.name = signal
                field_descriptor.json_name = signal
                field_descriptor.number = number
                field_descriptor.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL

                signal_key = f"{message_name}.{signal}"
                signal_type = single_types[signal_key]

                if signal_type == "float32" or signal_type == "float64":
                    field_descriptor.type = descriptor_pb2.FieldDescriptorProto.TYPE_FLOAT
                elif signal_type.startswith("int"):
                    if signal_type == "int8":
                        field_descriptor.type = descriptor_pb2.FieldDescriptorProto.TYPE_INT32  # Protobuf doesn't have int8, use int32
                    elif signal_type == "int16":
                        field_descriptor.type = descriptor_pb2.FieldDescriptorProto.TYPE_INT32  # Protobuf doesn't have int16, use int32
                    elif signal_type == "int32":
                        field_descriptor.type = descriptor_pb2.FieldDescriptorProto.TYPE_INT32
                    else:
                        field_descriptor.type = descriptor_pb2.FieldDescriptorProto.TYPE_INT64
                elif signal_type.startswith("uint"):
                    if signal_type == "uint8":
                        field_descriptor.type = descriptor_pb2.FieldDescriptorProto.TYPE_UINT32  # Protobuf doesn't have uint8, use uint32
                    elif signal_type == "uint16":
                        field_descriptor.type = descriptor_pb2.FieldDescriptorProto.TYPE_UINT32  # Protobuf doesn't have uint16, use uint32
                    elif signal_type == "uint32":
                        field_descriptor.type = descriptor_pb2.FieldDescriptorProto.TYPE_UINT32
                    else:
                        field_descriptor.type = descriptor_pb2.FieldDescriptorProto.TYPE_UINT64
                elif signal_type == "bool":
                    field_descriptor.type = descriptor_pb2.FieldDescriptorProto.TYPE_BOOL

                number = number + 1
        pool.Add(descriptor_proto)

        with open(mcap_file_path, "wb") as f, Writer(f) as writer:
            for message_name, signals in raw_data.items():
                topic_name = f"{asc_type}/{message_name}"
                message_class = GetMessageClass(pool.FindMessageTypeByName(f'{asc_type}_{message_name}'))

                timestamps = raw_data[message_name][TIMESTAMP]
                # 写入 MCAP，只存原始数据
                for i, timestamp in enumerate(timestamps):
                    mcap_msg = message_class()
                    for s in signals:
                        if s != TIMESTAMP:
                            setattr(mcap_msg, s, raw_data[message_name][s][i])

                    writer.write_message(
                        topic=topic_name,
                        message=mcap_msg,
                        log_time=int(float(timestamp) * 1e9),
                        publish_time=int(float(timestamp) * 1e9),
                    )

        raw_df = {}
        for message_name in raw_data:
            for signal in raw_data[message_name]:
                if signal == TIMESTAMP:
                    continue
                new_signal = f"{message_name}.{signal}"
                interp = interpolate.interp1d(raw_data[message_name][TIMESTAMP],
                                              raw_data[message_name][signal],
                                              kind="nearest",
                                              fill_value="extrapolate")
                dtype = single_types.get(new_signal, "float32")  # 默认 float32
                np_dtype = np.bool_ if dtype == "bool" else getattr(np, dtype)

                raw_df[new_signal] = interp(timestamp_index).astype(np_dtype)
        df = pd.DataFrame(raw_df, index=timestamp_index)
        # 添加 timestamp 列
        df['timestamp'] = df.index
        df.to_parquet(parquet_file_path, engine="pyarrow", compression="snappy")

        analysis_file_paths.append(parquet_file_path)
        analysis_file_paths.append(mcap_file_path)

    return analysis_file_paths, total_distance, timestamp_min, timestamp_max


def clean_nul_and_save_from_end(file_path):
    # 读取原文件内容
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 用来存放有效的行和它之前的所有行
    valid_lines = []

    found_illegal_line = False

    # 反向遍历行，找到第一个不包含 NUL 字符的行
    for i in range(len(lines) - 1, -1, -1):
        if '\x00' not in lines[i]:
            # 一旦找到有效行，保留从第一个有效行之前的所有行
            valid_lines = lines[:i + 1]
            break  # 找到有效行后停止
        else:
            found_illegal_line = True

    if found_illegal_line:
        # 如果找到了有效行，写回文件
        if valid_lines:
            with open(file_path, 'w') as file:
                file.writelines(valid_lines)
            logging.info("Cleaned data written back to the file.")
        else:
            raise ValueError("No valid data found.")


def get_protocol_version(basic_info):
    protocol_version = basic_info.get("protocol_version")

    if protocol_version is None:  # 判断是否为 None
        logging.error("protocol_version 不存在")
        return {}  # 返回空字典

    if isinstance(protocol_version, dict):
        if not protocol_version:  # 判断是否为空字典
            logging.error("protocol_version 为空字典")
            return {}
        return protocol_version  # 直接返回字典
    else:
        logging.error("protocol_version 格式未知")
        return {}  # 返回空字典


def canbus_check(sensor_type, obs_path_prefix, local_canbus_file, dbc_file, need_check_single, source_data, busChannelQuality, error_feishu_message, local_path_prefix, channel_no, is_blf_file):
    local_dbc_file = local_path_prefix + dbc_file

    # 下载dbc文件
    data_utils.get_object(dbc_file, local_dbc_file)

    if not is_blf_file:
        clean_nul_and_save_from_end(local_canbus_file)

    # 校验canbus文件是否有丢帧
    frame_loss_rate = get_frame_loss_rate(local_canbus_file, local_dbc_file, is_blf_file)

    if frame_loss_rate > current_config.get('frameLossRate'):
        logging.info("canbus文件丢帧率过大，frame_loss_rate: %s", frame_loss_rate)
        error_feishu_message.append(f"canbus文件丢帧率过大，canbus_file: {local_canbus_file}, frame_loss_rate: {frame_loss_rate}")

    busChannelQuality.bus_channel_frame_loss_rate = frame_loss_rate

    # 获取ASC文件的开始时间
    start_time = get_asc_start_time(local_canbus_file, is_blf_file)

    busChannelQuality.bus_channel_time_deviation = float(start_time)

    raw_time = source_data['raw_time']
    raw_timestamp = raw_time.timestamp()

    if busChannelQuality.bus_channel_time_deviation < raw_timestamp or busChannelQuality.bus_channel_time_deviation - raw_timestamp > current_config.get('canBustimeDeviation'):
        logging.info(f"文件：{local_canbus_file} CAN数据时间偏差过大，偏差为{busChannelQuality.bus_channel_time_deviation - raw_timestamp}")
        error_feishu_message.append(
            f"文件：{local_canbus_file} CAN数据时间偏差过大，偏差为{busChannelQuality.bus_channel_time_deviation - raw_timestamp}"
        )
        busChannelQuality.bus_channel_time_error = True

    # 执行canbus校验
    analysis_file_path, total_distance, timestamp_min, timestamp_max = analysis_asc_file(sensor_type, local_canbus_file, local_dbc_file, need_check_single, busChannelQuality, error_feishu_message, is_blf_file)

    if analysis_file_path is not None and len(analysis_file_path) > 0:
        parquet_key = obs_path_prefix + '/canbus/' + sensor_type + '_' + str(channel_no) + '.parquet'
        data_utils.upload_object(parquet_key, analysis_file_path[0])
        logging.info('upload complete, parquet file path: %s', parquet_key)

        mcap_key = obs_path_prefix + '/canbus/' + sensor_type + '_' + str(channel_no) + '.mcap'
        data_utils.upload_object(mcap_key, analysis_file_path[1])
        logging.info('upload complete, mcap file path: %s', mcap_key)

        busChannelQuality.bus_channel_parquet_path = parquet_key

    if total_distance > 0:
        total_distance_km = round(total_distance / 1000, 2)
        sql = f"update datacenter_source_data set mileage_kilometers = {total_distance_km} where id = {source_data['id']}"
        db_util.execute_single_sql(sql)

    if timestamp_min is not None:
        sql = f"""
            UPDATE datacenter_source_data
            SET start_time = CASE
                WHEN start_time IS NULL THEN FROM_UNIXTIME({timestamp_min})
                WHEN start_time > FROM_UNIXTIME({timestamp_min}) THEN FROM_UNIXTIME({timestamp_min})
                ELSE start_time
            END
            WHERE id = {source_data['id']}
        """
        db_util.execute_single_sql(sql)
    if timestamp_max is not None:
        sql = f"""
            UPDATE datacenter_source_data
            SET end_time = CASE
                WHEN end_time IS NULL THEN FROM_UNIXTIME({timestamp_max})
                WHEN end_time < FROM_UNIXTIME({timestamp_max}) THEN FROM_UNIXTIME({timestamp_max})
                ELSE end_time
            END
            WHERE id = {source_data['id']}
        """
        db_util.execute_single_sql(sql)

    return busChannelQuality


def get_asc_start_time(canbus_file, is_blf_file):
    if is_blf_file:
        # 简化版 ASC，按行读取第一条合法数据的 timestamp
        with open(canbus_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 4 or parts[2] != "#":
                    continue
                try:
                    return float(parts[0])
                except ValueError:
                    continue
        return 0.0  # 没读到任何合法时间戳
    else:
        # 标准 ASC 格式，用 ASCReader 读取第一条消息
        with ASCReader(canbus_file, relative_timestamp=False) as asc:
            for index, msg in enumerate(asc):
                if index == 0:
                    return msg.timestamp
        return 0.0  # 没有读取到任何消息


def get_frame_loss_rate(canbus_file, dbc_file, is_blf_file):
    db = cantools.db.load_file(dbc_file)

    timestamps = []
    first_message_id = None

    try:
        if is_blf_file:
            # 简化版 ASC（按行解析）
            with open(canbus_file, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) < 4 or parts[2] != "#":
                        continue  # 跳过格式异常的行

                    timestamp = float(parts[0])
                    arbitration_id = int(parts[1], 16)

                    if first_message_id is None:
                        first_message_id = arbitration_id

                    if arbitration_id == first_message_id:
                        timestamps.append(timestamp)
        else:
            # 标准 Vector ASC（用 ASCReader）
            with ASCReader(canbus_file, relative_timestamp=False) as asc:
                iterator = iter(asc)
                first_msg = next(iterator, None)
                if first_msg is None:
                    logging.error(f"标准 ASC 文件为空：{canbus_file}")
                    return float(1.0)

                first_message_id = first_msg.arbitration_id
                if first_message_id is None:
                    logging.error("未能解析出首条消息的 ID")
                    return float(1.0)

            with ASCReader(canbus_file, relative_timestamp=False) as asc:
                for msg in asc:
                    if msg.arbitration_id == first_message_id:
                        timestamps.append(msg.timestamp)

    except Exception as e:
        logging.error(f"读取 CAN 文件失败: {e}")
        return float(1.0)

    if not timestamps:
        logging.error(f"找不到 ID 为 {first_message_id} 的任何报文")
        return float(1.0)

    # 获取该消息的第一条和最后一条消息的时间戳
    start_time = timestamps[0]
    end_time = timestamps[-1]
    total_time = end_time - start_time

    # 获取 DBC 中定义的帧率（cycle_time 是毫秒，需要转换）
    if first_message_id in db._frame_id_to_message:
        cycle_time = db._frame_id_to_message[first_message_id].cycle_time
        frame_rate = 1000 / cycle_time if cycle_time else 0  # 确保 frame_rate 以 Hz 计算
    else:
        frame_rate = 0  # DBC 里没有这个 ID，设为 0，避免后续计算出错

    # 计算预计的总帧数
    expected_frame_count = int(frame_rate * total_time)

    # 计算实际的帧数
    actual_frame_count = len(timestamps)

    # 计算丢帧率
    if expected_frame_count > 0:
        frame_loss_rate = (expected_frame_count - actual_frame_count) / expected_frame_count
    else:
        frame_loss_rate = 0  # 如果理论帧数为 0，丢帧率设为 0

    return float(frame_loss_rate)


def get_video_fps(video_obs_path, videoChannelQuality):
    cap = None
    try:
        # 打开视频流
        cap = cv2.VideoCapture(video_obs_path)

        # 检查视频流是否成功打开
        if not cap.isOpened():
            logging.error("Error: Could not open video stream: %s", video_obs_path)
            videoChannelQuality.video_parse_error = True
            return float(0)
        else:
            # 获取视频帧率
            fps = cap.get(cv2.CAP_PROP_FPS)
            logging.info("Frame Rate: %s", fps)

            return float(fps)
    except Exception as e:
        logging.exception("检查视频出现异常。")
        videoChannelQuality.video_parse_error = True
        return float(0)
    finally:
        # 释放视频对象
        if cap is not None:
            cap.release()


def check_video_data_quality(path_prefix, source_data, sensor_data, channel_no, local_path_prefix):
    videoChannelQuality = VideoChannelQuality()
    videoChannelQuality.channel = channel_no
    logging.info("检查视频数据质量，channel_no: %s", channel_no)
    error_msg = []
    try:
        video_path = path_prefix + "/camera/"
        all_files = data_utils.list_files_in_directory(video_path)

        if all_files is None:
            logging.error("camera目录下未找到任何文件")
            error_msg.append(f"camera目录下未找到任何文件")
            videoChannelQuality.video_missing = True
            videoChannelQuality.video_index_missing = True
            return videoChannelQuality
        video_files = [file for file in all_files if file.endswith('.mp4')]
        if not video_files:
            logging.error("未找到任何.mp4 文件")
            error_msg.append(f"未找到任何.mp4 文件")
            videoChannelQuality.video_missing = True
        else:
            channel_numbers = [os.path.basename(file).split("_")[1] for file in video_files]
            if str(channel_no) not in channel_numbers:
                logging.error("未找到通道号为 %s 的视频文件", channel_no)
                error_msg.append(
                    f"未找到通道号为 {channel_no} 的视频文件")
                videoChannelQuality.video_missing = True
            else:
                matching_file = next(file for file in video_files if os.path.basename(file).split("_")[1] == str(channel_no))
                contentLength = data_utils.get_object_metadata(matching_file)

                if contentLength == 0:
                    logging.error("视频文件为空")
                    error_msg.append(f"视频文件为空")
                    videoChannelQuality.video_missing = True
                else:
                    # 检查视频文件丢帧率
                    fps_video = get_video_fps(current_config.get('obs_host') + matching_file, videoChannelQuality)
                    if sensor_data['frame_rate'] - fps_video > current_config.get('frameRateThreshold'):
                        logging.error("视频：%s，帧率：%s 与配置帧率 %s，相差过大", matching_file, fps_video, sensor_data['frame_rate'])
                        error_msg.append(
                            f"视频：{matching_file}，帧率：{fps_video} 与配置帧率 {sensor_data['frame_rate']}，相差过大")
                        videoChannelQuality.video_frame_loss_rate = True

        video_index_files = [file for file in all_files if file.endswith('.timestamp')]
        if not video_index_files:
            logging.error("未找到任何.timestamp 文件")
            error_msg.append(f"未找到任何.timestamp 文件")
            videoChannelQuality.video_index_missing = True
            return videoChannelQuality

        channel_numbers = [os.path.basename(file).split("_")[1] for file in video_index_files]
        if str(channel_no) not in channel_numbers:
            logging.error("未找到通道号为 %s 的视频索引文件", channel_no)
            error_msg.append(
                f"未找到通道号为 {channel_no} 的视频索引文件")
            videoChannelQuality.video_index_missing = True
            return videoChannelQuality

        matching_file = next(
            file for file in video_index_files if os.path.basename(file).split("_")[1] == str(channel_no))
        contentLength = data_utils.get_object_metadata(matching_file)

        if contentLength == 0:
            logging.error("视频索引文件为空")
            error_msg.append(f"视频索引文件为空")
            videoChannelQuality.video_index_missing = True
            return videoChannelQuality

        local_index_file = local_path_prefix + matching_file
        data_utils.get_object(matching_file, local_index_file)

        try:
            with open(local_index_file, "r") as file:
                first_line = file.readline().strip()  # 读取第一行并去除空白字符

            # 提取时间戳（空格分隔后取第二个元素）
            timestamp = float(first_line.split()[1])
            videoChannelQuality.video_index_time_deviation = timestamp

            raw_time = source_data['raw_time']
            raw_timestamp = raw_time.timestamp()

            if videoChannelQuality.video_index_time_deviation < raw_timestamp or videoChannelQuality.video_index_time_deviation - raw_timestamp > current_config.get('videoTimeDeviation'):
                logging.error(f"{raw_time}, 文件：{matching_file} 视频索引时间偏差过大，偏差为{videoChannelQuality.video_index_time_deviation - raw_timestamp}")
                error_msg.append(
                    f"{raw_time}, 通道：{matching_file} 视频索引时间偏差过大，偏差为{videoChannelQuality.video_index_time_deviation - raw_timestamp}"
                )
                videoChannelQuality.video_index_time_error = True

            return videoChannelQuality
        except Exception as e:
            logging.exception("检查视频索引出现异常。")
            error_msg.append(f"检查视频索引出现异常 ，文件：{matching_file}")
            videoChannelQuality.video_index_parse_error = True
            return videoChannelQuality

    except Exception as e:
        logging.exception("检查视频出现异常。")
        error_msg.append(f"检查视频出现异常 ，通道：{channel_no}")
        videoChannelQuality.video_parse_error = True
        return videoChannelQuality
    finally:
        videoChannelQuality.video_channel_error_list = error_msg
        return videoChannelQuality


def check_bus_data_quality(obs_path_prefix, source_data, sensor_data, channel_no, local_path_prefix, is_blf_file):
    busChannelQuality = BusChannelQuality()
    busChannelQuality.channel = channel_no
    logging.info("开始检查bus数据，channel_no: %s", channel_no)
    error_msg = []
    try:
        can_bus_path = local_path_prefix + "canbus/"
        all_files = [f for f in os.listdir(can_bus_path) if os.path.isfile(os.path.join(can_bus_path, f))]

        if all_files is None:
            logging.error("canbus目录下未找到任何文件")
            error_msg.append(f"canbus目录下未找到任何文件")
            busChannelQuality.bus_channel_missing = True
            return busChannelQuality
        # 筛选出以 .asc 结尾的文件
        asc_files = [file for file in all_files if file.endswith('.asc')]
        if not asc_files:
            logging.error("未找到任何 .asc 文件")
            error_msg.append(f"未找到任何.asc 文件")
            busChannelQuality.bus_channel_missing = True
        else:
            # 提取通道号
            channel_numbers = [os.path.basename(file).split("_")[1] for file in asc_files]
            if str(channel_no) not in channel_numbers:
                logging.error("未找到通道号为 %s 的文件", channel_no)
                error_msg.append(
                    f"未找到通道号为 {channel_no} 的文件")
                busChannelQuality.bus_channel_missing = True
            else:
                matching_file = next(
                    file for file in asc_files if os.path.basename(file).split("_")[1] == str(channel_no))
                dbc_file, need_check_single = find_dbc_file(matching_file, source_data, sensor_data, local_path_prefix)
                if dbc_file is None:
                    logging.error("未找到通道：%s, 对应的dbc文件", channel_no)
                    error_msg.append(
                        f"未找到通道：{channel_no}, 对应的dbc文件")
                    busChannelQuality.bus_channel_missing = True
                else:
                    # 执行canbus校验
                    local_canbus_file = can_bus_path + matching_file
                    canbus_check(sensor_data['type'], obs_path_prefix, local_canbus_file, dbc_file, need_check_single, source_data, busChannelQuality, error_msg, local_path_prefix, channel_no, is_blf_file)
    except Exception as e:
        logging.exception(f"检查bus数据出现异常， channel_no: {channel_no}")
        error_msg.append(f"检查bus数据出现异常， channel_no: {channel_no}")
        busChannelQuality.bus_channel_parse_error = True
    finally:
        busChannelQuality.bus_channel_error_list = error_msg
        return busChannelQuality


def check_channel_data(source_data, sensor_data, local_path_prefix, is_blf_file):
    project_name = source_data['project_name']
    plate_no = source_data['plate_no']
    raw_time = source_data['raw_time']
    raw_name = raw_time.strftime("raw_%Y%m%d_%H%M%S")

    obs_path_prefix = f"{project_name}/{plate_no}/{raw_name}"

    data_type = sensor_data['type']
    channel_no = sensor_data['no']

    vin_config = current_config.get('clean_config', {}).get(project_name, {}).get(plate_no, {})
    process_set = set(vin_config.get('processChannels', []))
    if channel_no not in process_set:
        logging.info("通道：%s 未配置需要处理，跳过", channel_no)
        return None

    if data_type == 'CAN' or data_type == 'CANFD' or data_type == 'Ethernet':
        return check_bus_data_quality(obs_path_prefix, source_data, sensor_data, channel_no, local_path_prefix, is_blf_file)
    elif data_type == 'CAMERA':
        return check_video_data_quality(obs_path_prefix, source_data, sensor_data, channel_no, local_path_prefix)
    else:
        logging.error("不支持的数据类型：%s", data_type)
        return None


def check_station_not_empty(data):
    for item in data:
        if not item.get("station"):  # 检查 station 是否为空或不存在
            return False
    return True


def check_required_tag(data, required_tag):
    for item in data:
        if item.get("sectionTag", {}).get("tagName") == required_tag:
            return True
    return False


def extract_tag_names(data: dict) -> str:
    """递归提取 tagName"""
    tag_names = []
    extract_tag_names_recursive(data, tag_names)
    return "-".join(tag_names)


def extract_tag_names_recursive(data: dict, tag_names: list):
    if "tagName" in data:
        tag_names.append(data["tagName"])
    if "children" in data:
        extract_tag_names_recursive(data["children"], tag_names)


def get_source_tag(tag_json: list) -> Optional[List[SourceTag]]:
    if not tag_json:
        logging.error("标签不存在")
        return None

    tag_list = []
    try:
        for tag_obj in tag_json:
            tag_mode = tag_obj.get("tagMode")

            if tag_mode == "section":
                tag_name = extract_tag_names(tag_obj.get("sectionTag", {}))
                start_time = tag_obj.get("tagBeginTime", "")
                end_time = tag_obj.get("tagEndTime", "")
                tag_list.append(SourceTag(tag_name, start_time, end_time))

            elif tag_mode == "event":
                event_tags = tag_obj.get("eventTag", [])
                for event in event_tags:
                    tag_name = extract_tag_names(event)
                    start_time = tag_obj.get("tagBeginTime", "")
                    end_time = tag_obj.get("tagEndTime", "")
                    tag_list.append(SourceTag(tag_name, start_time, end_time))

        return tag_list
    except Exception as e:
        logging.error(f"解析标签数据异常，tag_list: {tag_list}, 错误: {e}")
        return None


def get_english_names(tag_names: List[str]) -> Dict[str, Union[str, List[str]]]:
    chinese_names = set()

    # 提取标签中文名（倒数第二部分）
    for tag_name in tag_names:
        parts = tag_name.split('-')
        if len(parts) > 1:
            chinese_name = parts[-2]
            chinese_names.add(chinese_name)

    # 如果没有中文名，直接返回空字典
    if not chinese_names:
        return {}

    # 构造 SQL 查询语句（FIND_IN_SET 不能使用占位符）
    query_conditions = " OR ".join([f"FIND_IN_SET('{val}', mapping_name)" for val in chinese_names])
    sql_query = f"SELECT * FROM datacenter_dataset_label WHERE {query_conditions};"

    # 执行查询
    results = db_util.fetch_all(sql_query)

    # 构建英文名到 tag_name-后部分 的映射
    english_name_map = {}

    for result in results:
        english_name = result.get('key_name')
        mapping_names = result.get('mapping_name')

        # 拆分 mapping_name 并和 chinese_names 交叉对比
        for name in mapping_names.split(','):
            if name in chinese_names:
                english_name_map[name] = english_name

    # 构建最终返回的字典
    temp_map = defaultdict(list)

    for tag_name in tag_names:
        parts = tag_name.split('-')
        if len(parts) > 1:
            value = parts[-1]  # 取 tag_name 的后部分作为 value
            chinese_name = parts[-2]
            english_name = english_name_map.get(chinese_name, "")

            if english_name:
                temp_map[english_name].append(value)

    # 处理返回值：
    final_map = {}
    for key, values in temp_map.items():
        if key == "weather":
            final_map[key] = values  # weather 直接返回 list
        else:
            final_map[key] = ",".join(values)  # 其他 key 用 , 连接成字符串

    return final_map


def update_label_info(label_info: PEGASUSLabelInfo, english_name_map: dict):
    for field in fields(label_info):
        field_name = field.name
        if field_name in english_name_map:
            setattr(label_info, field_name, english_name_map[field_name])


def process_meta_info(source_data, dataRecord, error_feishu_message, local_path_prefix):
    project_name = source_data['project_name']
    plate_no = source_data['plate_no']
    raw_time = source_data['raw_time']
    raw_name = raw_time.strftime("raw_%Y%m%d_%H%M%S")
    data_id = source_data['data_id']

    quality = dataRecord.quality
    metaTagQuality = quality.data_quality.meta_tag_quality
    basic_info = dataRecord.basic_info
    basic_info.source_data_id = source_data['id']
    basic_info.project_name = project_name
    basic_info.plate_no = plate_no
    basic_info.data_id = data_id
    basic_info.collect_time = DateUtils.convert_to_timestamp_millis(str(raw_time))

    path_prefix = f"{project_name}/{plate_no}/{raw_name}"

    vehicle_info_path = f"{path_prefix}/conf/vehicle_info/vehicle_info.json"
    data_utils.get_object(vehicle_info_path, local_path_prefix + vehicle_info_path)

    file_path = f"{local_path_prefix}{vehicle_info_path}"
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        logging.error("车辆信息文件为空")
        error_feishu_message.append(f"车辆信息文件为空")
        metaTagQuality.meta_tag_missing = True
    else:
        # 打开并读取 JSON 文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)  # 解析 JSON 文件内容

        # 获取基本信息
        basic_info_file = data.get("basic_info")
        if basic_info_file is None:
            logging.error("车辆信息文件中缺少basic_info")
            error_feishu_message.append(f"车辆信息文件中缺少basic_info")
            metaTagQuality.meta_key_data_missing["basic_info"] = True
        else:
            ars_version = basic_info_file.get("ars_version")

            if ars_version is None:
                logging.error("车辆信息文件中缺少ars_version")
                error_feishu_message.append(f"车辆信息文件中缺少ars_version")
                metaTagQuality.meta_key_data_missing["basic_info"] = True
            else:
                basic_info.ars_version = ars_version

                autopilot_version = basic_info_file.get("autopilot_version")

                if autopilot_version is None:
                    logging.error("车辆信息文件中缺少autopilot_version")
                    error_feishu_message.append(f"车辆信息文件中缺少autopilot_version")
                    metaTagQuality.meta_key_data_missing["basic_info"] = True
                else:
                    autopilot_hardware_version = autopilot_version.get("autopilot_hardware_version")
                    autopilot_function_version = autopilot_version.get("autopilot_function_version")
                    autopilot_software_version = autopilot_version.get("autopilot_software_version")

                    soc_platform = basic_info_file.get("soc_platform")
                    source = basic_info_file.get("source")

                    if autopilot_hardware_version is None or autopilot_function_version is None or autopilot_software_version is None or soc_platform is None or source is None:
                        logging.error("车辆信息文件中缺少autopilot_hardware_version,autopilot_function_version,autopilot_software_version,protocol_version_dirt,soc_platform,source")
                        error_feishu_message.append(f"车辆信息文件中缺少autopilot_hardware_version,autopilot_function_version,autopilot_software_version,protocol_version_dirt,soc_platform,source")
                        metaTagQuality.meta_key_data_missing.basic_info = True
                    else:
                        basic_info.soc_platform = soc_platform
                        basic_info.source = source
                        basic_info.autopilot_version.autopilot_hardware_version = autopilot_hardware_version
                        basic_info.autopilot_version.autopilot_function_version = autopilot_function_version
                        basic_info.autopilot_version.autopilot_software_version = autopilot_software_version

    tag_path = f"{path_prefix}/tag.json"
    local_tag_path = local_path_prefix + tag_path
    data_utils.get_object(tag_path, local_tag_path)

    if not os.path.exists(local_tag_path) or os.path.getsize(local_tag_path) == 0:
        metaTagQuality.meta_key_data_missing.weather = True
        metaTagQuality.meta_key_data_missing.road_type = True
        metaTagQuality.meta_key_data_missing.lighting = True
        metaTagQuality.meta_key_data_missing.location = True
        logging.error("标签文件为空")
        error_feishu_message.append(f"标签文件为空")
    else:
        with open(local_tag_path, 'r', encoding='utf-8') as file:
            data = json.load(file)  # 解析 JSON 文件内容

        source_tag_list = get_source_tag(data)

        if source_tag_list is not None:
            tag_names = [tag.tag_name for tag in source_tag_list]
            english_name_map = get_english_names(tag_names)
            update_label_info(dataRecord.data_info.PEGASUS_label_info, english_name_map)

        if not check_required_tag(data, "天气"):
            metaTagQuality.meta_key_data_missing.weather = True
            logging.error("标签文件中缺少天气标签")
            error_feishu_message.append(f"标签文件中缺少天气标签")

        if not check_station_not_empty(data):
            metaTagQuality.meta_key_data_missing.location = True
            logging.error("标签文件中缺少location")
            error_feishu_message.append(f"标签文件中缺少station")

        if not check_required_tag(data, "行车场景"):
            metaTagQuality.meta_key_data_missing.highway_type = True
            logging.error("标签文件中缺少行车场景标签")
            error_feishu_message.append(f"标签文件中缺少行车场景标签")

        if not check_required_tag(data, "光照条件"):
            metaTagQuality.meta_key_data_missing.lighting = True
            logging.error("标签文件中缺少光照条件标签")
            error_feishu_message.append(f"标签文件中缺少光照条件标签")

    return dataRecord


def is_dirty_bus_data_quality(busChannelQuality, source_data):
    if busChannelQuality.bus_channel_parse_error:
        return True

    if busChannelQuality.bus_channel_missing:
        return True

    if busChannelQuality.bus_channel_frame_loss_rate > current_config.get('frameLossRate'):
        return True

    raw_time = source_data['raw_time']
    raw_timestamp = raw_time.timestamp()

    if busChannelQuality.bus_channel_time_deviation < raw_timestamp or busChannelQuality.bus_channel_time_deviation - raw_timestamp > current_config.get('canBustimeDeviation'):
        return True

    if busChannelQuality.bus_channel_rolling_counter_error:
        return True

    if busChannelQuality.bus_channel_single_missing:
        return True
    return False


def is_dirty_video_data_quality(videoChannelQuality, source_data):
    if videoChannelQuality.video_missing:
        return True
    if videoChannelQuality.video_parse_error:
        return True
    if videoChannelQuality.video_frame_loss_rate:
        return True
    if videoChannelQuality.video_index_missing:
        return True
    if videoChannelQuality.video_index_parse_error:
        return True

    raw_time = source_data['raw_time']
    raw_timestamp = raw_time.timestamp()

    if videoChannelQuality.video_index_time_deviation < raw_timestamp or videoChannelQuality.video_index_time_deviation - raw_timestamp > current_config.get('videoTimeDeviation'):
        return True

    return False


def is_dirty_quality(quality, source_data):
    if quality.data_quality.meta_tag_quality.meta_tag_missing or any(vars(quality.data_quality.meta_tag_quality.meta_key_data_missing).values()):
        return True
    for videoChannelQuality in quality.data_quality.video_data_quality:
        if is_dirty_video_data_quality(videoChannelQuality, source_data):
            return True
    for busChannelQuality in quality.data_quality.bus_data_quality:
        if is_dirty_bus_data_quality(busChannelQuality, source_data):
            return True
    return False


def convert_blf_to_asc(blf_file_path, output_dir):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 创建一个字典存储文件句柄，用于每个通道写入不同文件
    channel_files = {}

    with can.BLFReader(blf_file_path) as reader:
        for msg in reader:
            if msg.channel not in channel_files:
                output_file_path = os.path.join(output_dir, f"channel_{msg.channel}_canbus.asc")
                channel_files[msg.channel] = open(output_file_path, 'w')

            timestamp = f"{msg.timestamp:.6f}"
            can_id = f"{msg.arbitration_id:X}"
            data_hex = " ".join(f"{b:02X}" for b in msg.data)

            channel_files[msg.channel].write(f"{timestamp} {can_id} # {data_hex}\n")

    # 关闭所有打开的文件
    for file in channel_files.values():
        file.close()

    logging.info(f"转换完成，文件保存为: {output_dir}")


def list_blf_files(directory):
    """
    列出目录下所有的 .blf 文件
    """
    return [file for file in os.listdir(directory) if file.endswith('.blf')]


def process_source_data(sourceDataId):
    logging.info(f"开始处理 source_data_id: {sourceDataId}")
    sql = f"select * from datacenter_source_data where id = {sourceDataId}"
    source_data = db_util.fetch_one(sql)

    if source_data is None:
        logging.error("未找到对应的原始数据")
        raise ValueError(f"未找到对应的原始数据")
    local_path_prefix = current_config.get('containerPath') + sourceDataId + "/"
    error_feishu_message = []
    try:
        sql = f"select * from datacenter_vehicle_sensor where vin = '{source_data['vin']}' and type in('CAN', 'CANFD', 'CAMERA')"
        sensor_data_list = db_util.fetch_all(sql)
        if not sensor_data_list:
            logging.error("车辆未配置任何通道，project_name: %s, plate_no：%s", source_data['project_name'], source_data['plate_no'])
            raise ValueError(f"车辆未配置任何通道，source_data_id: {sourceDataId}")

        dataRecord = DataRecord()

        if need_process_meta(source_data['project_name'], source_data['plate_no']):
            logging.info("Meta数据配置为需要处理")
            # 处理Meta数据
            process_meta_info(source_data, dataRecord, error_feishu_message, local_path_prefix)
        else:
            logging.info("Meta数据配置为不需要处理")
        quality = dataRecord.quality

        bus_data_quality = quality.data_quality.bus_data_quality
        video_data_quality = quality.data_quality.video_data_quality

        project_name = source_data['project_name']
        plate_no = source_data['plate_no']
        raw_time = source_data['raw_time']
        raw_name = raw_time.strftime("raw_%Y%m%d_%H%M%S")

        path_prefix = f"{project_name}/{plate_no}/{raw_name}/canbus"

        local_canbus_path = local_path_prefix + "canbus/"
        suffixes = [".blf", ".asc"]
        data_utils.get_directory(path_prefix, local_canbus_path, suffixes)

        is_blf_file = False
        blf_files = list_blf_files(local_canbus_path)
        if not blf_files:
            logging.error("未找到任何 .blf 文件。")
        else:
            is_blf_file = True
            # 解析每一个 BLF 文件
            for blf_file in blf_files:
                blf_path = os.path.join(local_canbus_path, blf_file)
                convert_blf_to_asc(blf_path, local_canbus_path)

        for sensor_data in sensor_data_list:
            result = check_channel_data(source_data, sensor_data, local_path_prefix, is_blf_file)
            # 结果分类并存储
            if isinstance(result, BusChannelQuality):
                bus_data_quality.append(result)
                if result.bus_channel_error_list:
                    error_feishu_message.extend(result.bus_channel_error_list)
            elif isinstance(result, VideoChannelQuality):
                video_data_quality.append(result)
                if result.video_channel_error_list:
                    error_feishu_message.extend(result.video_channel_error_list)

        logging.info("数据处理完成，开始校验质量")
        data_quality = is_dirty_quality(quality, source_data)

        sql_statements = []
        values_list = []
        if data_quality is False:  # 数据质量正常
            sql = "UPDATE datacenter_source_data SET is_clean = " + str(IS_CLEAN_SUCCESS) + ", update_time = now() WHERE id = %s"
            sql_statements.append(sql)
            values_list.append(sourceDataId)
            db_util.execute_sql(sql_statements, values_list)
            dataRecord.data_info.clean_info.qualified = 1

            data_record_json = json.dumps(asdict(dataRecord), indent=4)
            if need_process_meta(source_data['project_name'], source_data['plate_no']):
                label_util.saveSourceDataLabel(sourceDataId, data_record_json)
        else:
            sql = "UPDATE datacenter_source_data SET fail_reason = '数据质量有误，请检查日志', update_time = now() WHERE id = %s"
            sql_statements.append(sql)
            values_list.append(sourceDataId)
            db_util.execute_sql(sql_statements, values_list)
            dataRecord.data_info.clean_info.qualified = 0

            quality_json = json.dumps(asdict(dataRecord), indent=4)
            if need_process_meta(source_data['project_name'], source_data['plate_no']):
                label_util.saveSourceDataLabel(sourceDataId, quality_json)
    except Exception as e:
        error_message = str(e)
        error_feishu_message.append(error_message)
        sql_statements = ["UPDATE datacenter_source_data SET fail_reason = %s, update_time = now() WHERE id = %s"]
        values_list = [(error_message, sourceDataId)]
        db_util.execute_sql(sql_statements, values_list)
        logging.exception(f"清洗数据出现异常，结束操作。:{error_message}")
    finally:
        if os.path.exists(local_path_prefix):
            shutil.rmtree(local_path_prefix)

    if error_feishu_message:
        raw_time = source_data['raw_time']
        raw_name = raw_time.strftime("raw_%Y%m%d_%H%M%S")
        message = f"检查原始数据项目名称：{source_data['project_name']},车牌号：{source_data['plate_no']}, 包名：{raw_name} 出现异常，异常列表如下：\n" + "\n".join(
            [f"{i + 1}. {error}" for i, error in enumerate(error_feishu_message)]
        )
        message_util.send_feishu_message(message)
    logging.info(f"处理 source_data_id: {sourceDataId} 结束。")


def clean_tag():
    source_data_id = sys.argv[1]

    process_source_data(source_data_id)

    logging.info("auto clean and tag data end.")

    return 'Success'


if __name__ == '__main__':
    clean_tag()

