import os
import shutil
import sys
from pathlib import Path

import pandas as pd
import pyarrow as pa
from pyarrow import parquet as pq

import data_deal_util

# 添加当前目录到 Python 路径中
sys.path.append(os.path.dirname(__file__))

KEY_TIMESTAMP = 'timestamp'
KEY_MSG_ID = 'msg_id'


def unify_schema(parquet_files):
    """ 读取所有 Parquet 文件，统一 Schema，并保持第一个文件的字段顺序 """
    tables = [pq.read_table(f) for f in parquet_files]

    # 以第一个表的字段顺序为基准
    base_fields = tables[0].schema.names
    all_fields = set(base_fields)

    # 收集所有可能的字段
    field_types = {}  # 存储字段的所有出现类型
    for table in tables:
        all_fields.update(table.schema.names)
        for field in table.schema:
            if field.name not in field_types:
                field_types[field.name] = set()
            field_types[field.name].add(field.type)

    # 确保字段顺序：先按第一个文件的顺序排列，再补充新字段
    all_fields = list(base_fields) + sorted(all_fields - set(base_fields))

    def select_highest_precision_type(types):
        """ 选择字段的最高精度数据类型 """
        if pa.string() in types:
            return pa.string()
        if pa.float64() in types:
            return pa.float64()
        if pa.float32() in types:
            return pa.float32()
        if pa.int64() in types:
            return pa.int64()
        if pa.int32() in types:
            return pa.int32()
        if pa.bool_() in types:
            return pa.bool_()
        return list(types)[0]  # 兜底处理

    # 选择字段的统一类型
    final_field_types = {field: select_highest_precision_type(types) for field, types in field_types.items()}

    # 统一 schema
    new_tables = []
    for table in tables:
        new_columns = []
        for field in all_fields:
            if field in table.schema.names:
                new_columns.append(table.column(field))
            else:
                new_columns.append(pa.array([None] * len(table), type=final_field_types[field]))

        # 重新创建 Table，确保 schema 统一
        new_table = pa.Table.from_arrays(new_columns, names=all_fields)
        new_tables.append(new_table)

    return new_tables


def get_value_from_option(option_str, key):
    # 将字符串按逗号分割成键值对
    pairs = option_str.split(',')

    # 遍历每个键值对
    for pair in pairs:
        k, v = pair.split('=', 1)  # 按第一个等号分割
        if k.strip() == key:  # 检查键是否匹配
            return v.strip()  # 返回对应的值

    return None  # 如果未找到键，返回 None

def get_fusion_path(parquet_path_list=None):
    # prefix = 'Fusion' if current_config.get('env.platform') == 'hr' else 'FD2'
    fusion_path = get_path_by('Fusion', parquet_path_list)
    if fusion_path is None:
        fusion_path = get_path_by('FD2', parquet_path_list)
    return fusion_path


def get_front_camera_data(parquet_path_list=None):
    # prefix = 'Fusion' if current_config.get('env.platform') == 'hr' else 'FD2'
    fusion_path = get_path_by('FD0', parquet_path_list)
    return fusion_path


def get_pcan_path(parquet_path_list=None):
    return get_path_by('PCAN', parquet_path_list)


def get_acan_path(parquet_path_list=None):
    return get_path_by('ACAN', parquet_path_list)

def get_path(search_word, parquet_path_list=None):
    return get_path_by(search_word, parquet_path_list)


def get_tag_path(path_list=None):
    return get_path_by('tag.json', path_list)


def get_path_by(path_key, parquet_path_list=None):
    """根据多个关键字查找包含所有关键字的文件路径"""
    if parquet_path_list is None:
        parquet_path_list = sys.argv[1:]

    # 统一处理为小写关键字列表
    if isinstance(path_key, str):
        keywords = [path_key.lower()]
    else:
        keywords = [k.lower() for k in path_key]

    # 遍历所有文件路径
    for parquet_path in parquet_path_list:
        # 统一转为小写进行比较
        path_lower = parquet_path.lower()

        # 检查是否包含所有关键字
        if all(kw in path_lower for kw in keywords):
            return parquet_path

    return None


def read_df_by_msg_id(acan_path, msg_id_value, dest_field_key):
    # where 条件，根据 msg_id 查询
    # filters = [[(KEY_MSG_ID, '=', msg_id_value)]]
    # 指定需要加载的列
    if isinstance(dest_field_key, list):
        columns_to_load = [KEY_TIMESTAMP, KEY_MSG_ID] + dest_field_key
    else:
        columns_to_load = [KEY_TIMESTAMP, KEY_MSG_ID, dest_field_key]

    msg_signal_filter = {
        msg_id_value: columns_to_load
    }

    df_protobuf = data_deal_util.protobuf_to_dataframe_filtered(acan_path, msg_signal_filter)
    return df_protobuf


def df_merge(df_left, df_right):
    """
    按时间错对齐合并两个DataFrame
    """
    # 确保DataFrame按时间戳排序（在这个例子中它们已经是排序的）
    df_left.sort_values(KEY_TIMESTAMP, inplace=True)
    df_right.sort_values(KEY_TIMESTAMP, inplace=True)

    # 假设你想用前一个非空值来填充（注意：这可能会引入偏差）
    df_left[KEY_TIMESTAMP].fillna(method='ffill', inplace=True)
    df_right[KEY_TIMESTAMP].fillna(method='ffill', inplace=True)

    df_left["timestamp_tmp"] = df_left[KEY_TIMESTAMP].astype(float) * 1000000
    df_right["timestamp_tmp"] = df_right[KEY_TIMESTAMP].astype(float) * 1000000

    # 使用merge_asof合并DataFrame
    merged_df = pd.merge_asof(df_left, df_right, on="timestamp_tmp", direction='nearest')

    # 删除临时列
    merged_df.drop('timestamp_tmp', axis=1, inplace=True)
    merged_df.drop('timestamp_y', axis=1, inplace=True)
    # 保留做列 timestamp
    merged_df = merged_df.rename(columns={"timestamp_x": "timestamp"})

    return merged_df


def apply_conditions(df, conditions, operator='and'):
    """
    根据条件列表应用条件。

    参数:
    df (pd.DataFrame): 数据 DataFrame。
    conditions (list of tuples): 条件列表，每个条件由 (列名, 操作符, 条件值) 组成。
    operator('and' or 'or'): 条件列表的条件运算符。

    返回:
    pd.Series: 布尔 Series，表示每行是否满足所有条件。
    """
    condition_met = pd.Series([True] * len(df))
    if operator == 'and':
        for col, op, values in conditions:
            if op == '==':
                condition_met &= df[col] == values
            elif op == '!=':
                condition_met &= df[col] != values
            elif op == '>':
                condition_met &= df[col] > values
            elif op == '<':
                condition_met &= df[col] < values
            elif op == '>=':
                condition_met &= df[col] >= values
            elif op == '<=':
                condition_met &= df[col] <= values
            elif op == 'in':
                condition_met &= df[col].isin(values)
            elif op == 'not in':
                condition_met &= ~df[col].isin(values)
    elif operator == 'or':
        condition_met = pd.Series([False] * len(df))
        for col, op, values in conditions:
            if op == '==':
                condition_met |= df[col] == values
            elif op == '!=':
                condition_met |= df[col] != values
            elif op == '>':
                condition_met |= df[col] > values
            elif op == '<':
                condition_met |= df[col] < values
            elif op == '>=':
                condition_met |= df[col] >= values
            elif op == '<=':
                condition_met |= df[col] <= values
            elif op == 'in':
                condition_met |= df[col].isin(values)
            elif op == 'not in':
                condition_met |= ~df[col].isin(values)
    return condition_met



def extract_pre_events(df, current_conditions, previous_conditions=None, time_threshold=2, operator='and'):
    """
    提取满足条件的时间段的时间点。

    参数:
    df (pd.DataFrame): 包含数据的 DataFrame。
    current_conditions (list of tuples): 当前帧条件，每个条件由 (列名, 操作符, 条件值) 组成。
    previous_conditions (list of tuples, optional): 前几秒的条件，每个条件由 (列名, 操作符, 条件值) 组成。默认为 None。
    time_threshold (int): 时间阈值（秒），用于检查前几秒的条件。负值表示后几秒，正值表示前几秒。
    operator('and' or 'or'): 条件列表的条件运算符。


    返回:
    list: 包含事件的开始时间和结束时间的时间段列表。
    """
    if df.empty:
        return []

    if previous_conditions is not None:
        # 计算前几秒的值
        df['previous_timestamp'] = df['timestamp'] - pd.Timedelta(seconds=time_threshold)

        # 对于没有前几秒或后几秒数据的情况，进行边界处理
        previous_columns = [col for col, _, _ in previous_conditions]
        merged_df = pd.merge_asof(df, df[['timestamp'] + previous_columns],
                                  left_on='previous_timestamp', right_on='timestamp',
                                  suffixes=('', '_previous'), direction='backward' if time_threshold > 0 else 'forward')

        # 处理没有对应时间的数据
        for col in previous_columns:
            merged_df[f'{col}_previous'].fillna(method='bfill' if time_threshold > 0 else 'ffill', inplace=True)

    else:
        merged_df = df.copy()

    # 计算当前条件是否满足
    merged_df['current_condition_met'] = apply_conditions(merged_df, current_conditions, operator=operator)

    if previous_conditions is not None:
        # 计算前几秒或后几秒条件是否满足
        merged_df['previous_condition_met'] = apply_conditions(merged_df,
                                                               [(f'{col}_previous', op, values) for col, op, values
                                                                in previous_conditions], operator=operator)
        # 判断事件
        merged_df['is_event'] = merged_df['current_condition_met'] & merged_df['previous_condition_met']
    else:
        merged_df['is_event'] = merged_df['current_condition_met']

    merged_df['prev_is_event'] = merged_df['is_event'].shift(1, fill_value=False)
    events = merged_df[merged_df['is_event'] & ~merged_df['prev_is_event']]
    start_times = events['timestamp'].tolist()

    if start_times:
        return [(start_time, start_time) for start_time in start_times]
    else:
        return []


def extract_periods(df, current_conditions, previous_conditions=None, operator='and'):
    """
    提取满足条件的时间段的开始时间和结束时间。

    参数:
    df (pd.DataFrame): 包含数据的 DataFrame。
    current_conditions (list of tuples): 当前帧条件，每个条件由 (列名, 操作符, 条件值列表) 组成。
    previous_conditions (list of tuples, optional): 前一帧条件，每个条件由 (列名, 操作符, 条件值列表) 组成。默认为 None。
    operator('and' or 'or'): 条件列表的条件运算符。

    返回:
    list: 包含开始时间和结束时间的时间段列表。
    """
    if df.empty:
        return []

    if previous_conditions is not None:
        # 计算前一行的值
        for col, _, _ in previous_conditions:
            df[f'prev_{col}'] = df[col].shift(1)

    # 计算条件是否满足
    current_condition_met = apply_conditions(df, current_conditions, operator=operator)

    if not current_condition_met.any():
        return []

    if previous_conditions is not None:
        prev_condition_met = apply_conditions(df, [(f'prev_{col}', op, values) for col, op, values in previous_conditions], operator=operator)
        df['condition_met'] = current_condition_met & prev_condition_met
    else:
        df['condition_met'] = current_condition_met

    # 计算段的开始
    df['segment_start'] = (~df['condition_met'].shift(1, fill_value=False) & df['condition_met']).cumsum()

    # 过滤满足条件的行
    condition_periods = df[df['condition_met']]

    # 如果没有满足条件的行，返回空列表
    if condition_periods.empty:
        return []

    # 分组并提取开始和结束时间
    periods = condition_periods.groupby('segment_start').agg(start=('timestamp', 'first'),
                                                             end=('timestamp', 'last')).reset_index()

    # 转换为列表
    periods_list = periods[['start', 'end']].to_records(index=False).tolist()

    return periods_list


def extract_periods(df, current_conditions=None, operator='and', operator_method=None):
    return extract_periods_one_frame(df, current_conditions=current_conditions, operator=operator, operator_method=operator_method)


def extract_periods_one_frame(df, current_conditions=None, operator='and', operator_method=None):
    """
    新增一列warning：1 激活 0 未激活
    差分warning列，如果连续为1，则记录开始和结束时间戳
    返回时间戳区间列表
    """
    # 计算条件
    if operator_method is not None:
        df['warning'] = df.apply(operator_method, axis=1)
    else:
        current_condition_met = apply_conditions(df, current_conditions, operator=operator)
        df['warning'] = (current_condition_met).astype(int)

    # 处理 start_indices（包括首行逻辑）
    start_indices = df[
        (df['warning'] == 1) &
        ((df['warning'].shift(1) == 0) | (df.index == df.index[0]))  # 处理首行逻辑
    ]['timestamp']

    # 处理 end_indices（包括尾行逻辑）
    end_indices = df[
        (df['warning'] == 1) &
        (df['warning'].shift(-1) == 0)  # 找到结束点
    ]['timestamp']

    # 如果尾行 warning == 1，补充最后的结束时间戳
    if df.iloc[-1]['warning'] == 1 and (len(end_indices) == 0 or df.iloc[-1]['timestamp'] != end_indices.iloc[-1]):
        end_indices = pd.concat([end_indices, pd.Series([df.iloc[-1]['timestamp']])], ignore_index=True)

    # 验证数量匹配
    if len(start_indices) != len(end_indices):
        raise ValueError(f"Start indices 和 End indices 数量不匹配: {len(start_indices)} != {len(end_indices)}")

    # 构造时间戳区间
    timestamp_ranges = [(start, end) for start, end in zip(start_indices, end_indices)]

    return timestamp_ranges

def marge_different_msg(df, primary_msg_id, other_msg_ids):
    """
    合并不同消息到主消息中

    参数:
    df (pd.DataFrame): 包含数据的 DataFrame。
    primary_msg_id (number): 主消息msg_id。
    other_msg_ids (list of number): 被合并的msg_id。

    返回:
    pd.DataFrame: 合并后的DataFrame。
    """
    # 初始化一个空字典来存储合并后的数据
    merged_data = {}
    last_primary_index = None

    # 遍历DataFrame的行
    columns = df.columns
    for index, row in df.iterrows():
        msg_id = row['msg_id']
        if msg_id == primary_msg_id:
            if last_primary_index is not None:
                for column in columns:
                    if pd.isnull(merged_data[last_primary_index][column]):
                        del merged_data[last_primary_index]
                        break
            merged_data[index] = row.to_dict()
            last_primary_index = index
        elif msg_id in other_msg_ids:
            # 如果找到了other_msg_ids中的行，则合并到上一个primary_msg_id的字典中
            if last_primary_index is not None:
                for column in columns:
                    if pd.isnull(merged_data[last_primary_index][column]):
                        merged_data[last_primary_index][column] = row[column]

    # 创建一个新的DataFrame
    merged_df = pd.DataFrame(merged_data).T.reset_index(drop=True)
    return merged_df


def df_filter_by_timestamp(df, start_timestamp, end_timestamp):
    """
    通过时间戳过滤df
    @param df
    @param start_timestamp 开始时间 1720773866.3188682 单位秒
    @param end_timestamp 结束时间 1720773881.618885 单位秒
    @return 过滤后的filter
    """
    if df is None or df.empty:
        return df

    start_timestamp = float(start_timestamp)
    end_timestamp = float(end_timestamp)

    # 如果 start_timestamp 或 end_timestamp 为 0，则跳过对应的过滤条件
    if start_timestamp == 0 and end_timestamp == 0:
        return df  # 如果两个时间戳都为 0，返回原始数据
    elif start_timestamp == 0:
        # 如果 start_timestamp 为 0，只过滤 end_timestamp
        filtered_df = df[df['timestamp'] <= end_timestamp]
    elif end_timestamp == 0:
        # 如果 end_timestamp 为 0，只过滤 start_timestamp
        filtered_df = df[df['timestamp'] >= start_timestamp]
    else:
        # 正常的时间戳区间过滤
        filtered_df = df[(df['timestamp'] >= start_timestamp) & (df['timestamp'] <= end_timestamp)]
    return filtered_df


def remove_files(local_path_list):
    # 遍历列表中的每个文件路径
    for path in local_path_list:
        # 检查文件是否存在
        if os.path.exists(path):
            # 删除文件
            os.remove(path)


def remove_dirs(local_dir_list):
    # 遍历列表中的每个文件路径
    for dir_path in local_dir_list:
        # 检查文件是否存在
        if not os.path.exists(dir_path):
            continue

        # 检查目录是否为空
        if os.listdir(dir_path):
            shutil.rmtree(dir_path)
        else:
            # 删除文件目录
            os.rmdir(dir_path)


def list_file_names(directory):
    # 使用 pathlib 获取目录下的所有文件
    dir_path = Path(directory)
    # 获取文件名列表（只包含文件名）
    file_names = [file.name for file in dir_path.iterdir() if file.is_file()]
    return file_names

