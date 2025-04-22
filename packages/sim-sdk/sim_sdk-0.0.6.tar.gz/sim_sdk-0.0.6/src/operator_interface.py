from abc import ABC, abstractmethod
from pandas import (DataFrame)
import pandas as pd
import scene_util
from const_key import (LOCAL_CHANNEL_FILE_INDEX, DATASET_LABEL_KEY, KEY_TIMESTAMP, METRIC_CONFIG, PARAM_PAGE,
                       CONFIG_STR, KEY_DATASET_INFO, KEY_START_TIMESTAMP, KEY_END_TIMESTAMP,
                       LOGSIM_RESULT_ACAN_FILE_NAME, LOGSIM_RESULT_PCAN_FILE_NAME, LOGSIM_RESULT_CAN_FILE_NAME,
                       LOCAL_LOGSIM_RESULT_PATH_KEY, PARQUET_FILE_EXT, LOCAL_CHANNEL_MCAP_FILE_INDEX)
from typing import Union

from util import nacos_client
from util import data_utils
from log_manager import LoggingManager

current_config = nacos_client.get_config()


def append_timestamp_field(field_name_list: list) -> list:
    """
    给信号列表增加时间戳字段，默认读取timestamp字段
    """

    if KEY_TIMESTAMP not in field_name_list:
        field_name_list.append(KEY_TIMESTAMP)

    return field_name_list


class Operator(ABC):
    """
    算子接口，所有算子需要继承该接口。
    """

    def __init__(self):
        # 算子参数
        self.params = None
        # 算子结果：手动结果
        self.manual_result = None
        # 算子结果：自动结果 return返回的
        self.manual_table_name = None
        # 日志记录器
        self.logging = None
        # 中间数据
        self.topic_df = None
        # 分析数据
        self.analysis_df = None

    def index_name(self) -> str:
        """
        获取算子索引名称，默认为"idx_operator"，子类可以重写该方法，修改算子索引名称
        自动保存结果时会使用该索引名称作为表名

        返回:
        - str: 索引名称
        """
        return "idx_operator"

    def manual_save_result(self, table_name: str, result: Union[dict, list]):
        """
        手动保存算子结果，

        参数:
        - result: 需要保存的算子结果，是一个dict或list[dict]
        - table_name: 保存到的表
        """

        self.manual_result = result
        self.manual_table_name = table_name

    def get_manual_save_result(self):
        """
        手获取动保存算子结果，

        参数:
        - result: 需要保存的算子结果，是一个dict或list[dict]
        - table_name: 保存到的表
        """

        return self.manual_table_name, self.manual_result

    def append_csv_df(self, df: pd.DataFrame):
        """
        将传入的 DataFrame 内容追加到当前的 `data` 中

        :param df: 需要追加的 DataFrame
        """
        self.analysis_df = pd.concat([self.analysis_df, df], ignore_index=True)

    def get_csv_df(self):
        """
        返回csv DataFrame
        """
        return self.analysis_df

    def append_topic_df(self, df: pd.DataFrame):
        """
        将传入的 DataFrame 内容追加到当前的 `data` 中

        :param df: 需要追加的 DataFrame
        """
        self.topic_df = pd.concat([self.topic_df, df], ignore_index=True)

    def get_topic_df(self):
        """
        返回topic DataFrame
        """
        return self.topic_df

    def set_params(self, new_params):
        """
        设置算子参数

        参数:
        - new_params: 新的参数，是一个dict
        """
        self.params = new_params

    def set_logging(self, logging):
        """
        设置日志记录器

        参数:
        - logging: 日志记录器
        """
        self.logging = logging

    @abstractmethod
    def compute(self) -> Union[dict, list]:
        """
        执行算子并返回结果，结果需要是一个dict，最终会被序列化为JSON

        参数:

        返回:
        {
          "table1_key": [{
            key: value
          }],

          "table2_key": [{
            key: value
          }],
        }
        框架最终会在表（算子类名+table1_key）中插入 table1_key对应的数据，在表（算子类名+table2_key）中插入 table2_key 对应的数据
        插入行数分别由对应表list条数决定，字段由对应表dict key决定
        """
        pass

    def has_can_data(self, can_name) -> bool:
        """
        判断是否有CAN数据

        返回:
        - bool: True 有CAN数据 False 无CAN数据
        """
        local_channel_file_index = self.params[LOCAL_CHANNEL_FILE_INDEX]

        if local_channel_file_index is None:
            return False

        can_data = local_channel_file_index.get(can_name, None)
        if can_data is None:
            return False

        return True

    def has_acan_data(self) -> bool:
        """
        判断是否有ACAN数据

        返回:
        - bool: True 有ACAN数据 False 无ACAN数据
        """
        return self.has_can_data('acan')

    def has_pcan_data(self) -> bool:
        """
        判断是否有PCAN数据

        返回:
        - bool: True 有PCAN数据 False 无PCAN数据
        """
        return self.has_can_data('pcan')

    def has_acan_data_from_logsim_result(self) -> bool:
        """
        判断是否有回灌结果ACAN数据

        返回:
        - bool: True 有回灌结果ACAN数据 False 无回灌结果ACAN数据
        """
        return scene_util.get_path_by([LOGSIM_RESULT_ACAN_FILE_NAME, PARQUET_FILE_EXT],
                                      self.params[LOCAL_LOGSIM_RESULT_PATH_KEY]) is not None

    def has_pcan_data_from_logsim_result(self) -> bool:
        """
        判断是否有回灌结果PCAN数据

        返回:
        - bool: True 有回灌结果PCAN数据 False 无回灌结果PCAN数据
        """
        return scene_util.get_path_by([LOGSIM_RESULT_PCAN_FILE_NAME, PARQUET_FILE_EXT],
                                      self.params[LOCAL_LOGSIM_RESULT_PATH_KEY]) is not None

    def has_can_data_from_logsim_result(self) -> bool:
        """
        判断是否有回灌结果CAN数据

        返回:
        - bool: True 有回灌结果CAN数据 False 无回灌结果CAN数据
        """
        return scene_util.get_path_by(LOGSIM_RESULT_CAN_FILE_NAME,
                                      self.params[LOCAL_LOGSIM_RESULT_PATH_KEY]) is not None

    def has_fusion_data(self) -> bool:
        """
        判断是否有融合数据
        返回:
        - bool: True 有融合数据 False 无融合数据
        """
        return self.has_can_data('fusion') or self.has_can_data('fd2')

    def has_front_camera_data(self) -> bool:
        """
        判断是否有J3 前置摄像头融合数据
        返回:
        - bool: True 有融合数据 False 无融合数据
        """
        return self.has_can_data('fd0')

    def has_data_from_logsim_result(self, search_word: str) -> bool:
        """
        判断是否有具体can数据
        @:search_word: 查询词，可以是ACAN、PCAN、Fusion debugcan
        返回:
        - bool: True 有具体can数据 False 无具体can数据
        """
        return scene_util.get_path(search_word, self.params[LOCAL_LOGSIM_RESULT_PATH_KEY]) is not None

    def get_data_path(self, search_word: str):
        """
        获取路径包含关键字search_word的文件完整路径
        @:search_word: 查询词，可以是ACAN、PCAN、Fusion debugcan
        返回:
        - 文件路径
        """
        local_channel_file_index = self.params[LOCAL_CHANNEL_FILE_INDEX]

        if local_channel_file_index is None:
            return None

        can_data = local_channel_file_index.get(search_word, None)
        if can_data is None:
            return None

        # 处理路径列表
        for path in can_data:
            # 分割路径并去掉最后两个部分（日期部分和文件名）
            path_parts = path.split('/')

            # 去掉最后两部分（日期部分和文件名）
            path_parts = path_parts[:-2]

            # 提取文件名并去掉时间戳部分（例如 ACAN_2_20240622130513.parquet -> ACAN_2.parquet）
            file_name = path_parts[-1].split('_')[0]  # 获取文件名前缀部分

            # 拼接新的路径，包括文件名前缀（去掉时间戳）
            new_path = '/'.join(path_parts) + '/' + file_name + '.parquet'

            return new_path  # 返回去掉日期部分的路径和文件名

        return None  # 如果没有找到合适的路径

    def get_data_path_from_logsim_result(self, search_word: str) -> bool:
        """
        获取路径包含关键字search_word的文件完整路径，仅查询回灌结果文件
        @:search_word: 查询词，可以是ACAN、PCAN、Fusion debugcan
        返回:
        - 文件路径
        """
        return scene_util.get_path(search_word, self.params[LOCAL_LOGSIM_RESULT_PATH_KEY])

    def get_data_path_from_mcap_path(self, search_word: str) -> bool:
        """
        获取路径包含关键字search_word的文件完整路径，仅查询mcap文件
        @:search_word: 查询词，可以是ACAN、PCAN、Fusion debugcan
        返回:
        - 文件路径
        """
        local_channel_file_index = self.params[LOCAL_CHANNEL_MCAP_FILE_INDEX]

        if local_channel_file_index is None:
            return None

        return local_channel_file_index.get(search_word, None)

    def get_acan_mcap_data_path(self) -> bool:
        """
        判断是否有ACAN数据

        返回:
        - bool: True 有ACAN数据 False 无ACAN数据
        """
        return self.get_data_path_from_mcap_path('acan')

    def get_pcan_mcap_data_path(self) -> bool:
        """
        判断是否有ACAN数据

        返回:
        - bool: True 有ACAN数据 False 无ACAN数据
        """
        return self.get_data_path_from_mcap_path('pcan')

    def get_fusion_mcap_data_path(self) -> bool:
        """
        判断是否有融合数据
        返回:
        - bool: True 有融合数据 False 无融合数据
        """
        return self.get_data_path_from_mcap_path('fusion') or self.get_data_path_from_mcap_path('fd2')

    def get_front_camera_mcap_data_path(self) -> bool:
        """
        判断是否有J3 前置摄像头融合数据
        返回:
        - bool: True 有融合数据 False 无融合数据
        """
        return self.get_data_path_from_mcap_path('fd0')

    def read_can_data(self, channel, signals, start_time=None, end_time=None):
        """
        读取并合并指定通道的 Parquet 文件，确保数据类型一致
        :param channel: 通道名称，例如 "pcan"
        :param signals: 需要的信号列表，例如 ["VCU_VehInfoB.VCPU_VehSpd"]
        :param start_time: 需要的起始时间戳（可选）
        :param end_time: 需要的结束时间戳（可选）
        :return: DataFrame，包含 timestamp 和 需要的信号
        """
        local_channel_file_index = self.params[LOCAL_CHANNEL_FILE_INDEX]

        if channel not in local_channel_file_index:
            raise ValueError(f"通道 {channel} 不存在索引中")

        files = local_channel_file_index[channel]

        if not files:
            print(f"⚠️ 通道 {channel} 没有可用的 Parquet 文件")
            return pd.DataFrame(columns=list(set(["timestamp"] + signals)))

        data_frames = []

        for file in files:
            try:
                # 只加载 `timestamp` 和需要的信号列
                df = pd.read_parquet(file, columns=list(set(["timestamp"] + signals)))

                # 确保每个 DataFrame 都有完整的信号列
                missing_columns = set(signals) - set(df.columns)
                for col in missing_columns:
                    df[col] = None  # 对缺失的列填充 NaN（或 None）

                # 处理时间范围过滤
                if start_time is not None and end_time is not None:
                    df = df[(df["timestamp"] >= start_time) & (df["timestamp"] <= end_time)]
                elif start_time is not None:
                    df = df[df["timestamp"] >= start_time]
                elif end_time is not None:
                    df = df[df["timestamp"] <= end_time]

                data_frames.append(df)

            except Exception as e:
                print(f"❌ 读取 {file} 失败: {e}")

        # 合并多个文件的数据
        if data_frames:
            result_df = pd.concat(data_frames).sort_values(by="timestamp").reset_index(drop=True)
            return result_df
        else:
            print(f"⚠️ 没有找到符合条件的数据 {channel}")
            return pd.DataFrame(columns=["timestamp"] + signals)

    def read_acan_data(self, field_name_list: list) -> DataFrame:
        """
        读取ACAN数据，并返回结果，结果需要是一个DataFrame

        参数:
        - field_name_params：信号字段名

        返回:
        - pd.DataFrame: 包含 'timestamp' 和指定列的信号结果。
        """
        df = self.read_can_data('acan', field_name_list)

        # 读取时间区间内的数据
        if self.has_time_period():
            df = scene_util.df_filter_by_timestamp(df, self.params[KEY_DATASET_INFO][KEY_START_TIMESTAMP],
                                                   self.params[KEY_DATASET_INFO][KEY_END_TIMESTAMP])
        return df

    def read_pcan_data(self, field_name_list: list) -> DataFrame:
        """
        读取PCAN数据，并返回结果，结果需要是一个DataFrame

        参数:
        - field_name_params：信号字段名

        返回:
        - pd.DataFrame: 包含 'timestamp' 和指定列的信号结果。
        """

        df = self.read_can_data('pcan', field_name_list)
        # 读取时间区间内的数据
        if self.has_time_period():
            df = scene_util.df_filter_by_timestamp(df, self.params[KEY_DATASET_INFO][KEY_START_TIMESTAMP],
                                                   self.params[KEY_DATASET_INFO][KEY_END_TIMESTAMP])
        return df

    def read_acan_data_from_logsim_result(self, field_name_list: list) -> DataFrame:
        """
        读取回灌结果ACAN数据，结果需要是一个DataFrame

        参数:
        - field_name_params：信号字段名

        返回:
        - pd.DataFrame: 包含 'timestamp' 和指定列的信号结果。
        """

        df = pd.read_parquet(scene_util.get_path([LOGSIM_RESULT_ACAN_FILE_NAME, PARQUET_FILE_EXT],
                                                 self.params[LOCAL_LOGSIM_RESULT_PATH_KEY]))[
            append_timestamp_field(field_name_list)]
        return df

    def read_pcan_data_from_logsim_result(self, field_name_list: list) -> DataFrame:
        """
        读取回灌结果PCAN数据，结果需要是一个DataFrame

        参数:
        - field_name_params：信号字段名

        返回:
        - pd.DataFrame: 包含 'timestamp' 和指定列的信号结果。
        """

        df = pd.read_parquet(scene_util.get_path_by([LOGSIM_RESULT_PCAN_FILE_NAME, PARQUET_FILE_EXT],
                                                    self.params[LOCAL_LOGSIM_RESULT_PATH_KEY]))[
            append_timestamp_field(field_name_list)]
        return df

    def read_can_data_from_logsim_result(self, field_name_list: list) -> DataFrame:
        """
        读取回灌结果CAN数据，结果需要是一个DataFrame

        参数:
        - field_name_params：信号字段名

        返回:
        - pd.DataFrame: 包含 'timestamp' 和指定列的信号结果。
        """

        df = pd.read_parquet(scene_util.get_path_by(LOGSIM_RESULT_CAN_FILE_NAME,
                                                    self.params[LOCAL_LOGSIM_RESULT_PATH_KEY]))[
            append_timestamp_field(field_name_list)]
        return df

    def read_fusion_data(self, field_name_list: list) -> DataFrame:
        """
        读取ACAN数据，并返回结果，结果需要是一个DataFrame

        参数:
        - field_name_params：信号字段名

        返回:
        - pd.DataFrame: 包含 'timestamp' 和指定列的信号结果。
        """
        df = None
        try:
            df = self.read_can_data('fusion', field_name_list)
        except Exception as e:
            LoggingManager.logging().error(f"读fusion取融合数据失败: {e}")

        if df is None or df.empty:
            df = self.read_can_data('fd2', field_name_list)

        # 读取时间区间内的数据
        if self.has_time_period():
            df = scene_util.df_filter_by_timestamp(df, self.params[KEY_DATASET_INFO][KEY_START_TIMESTAMP],
                                                   self.params[KEY_DATASET_INFO][KEY_END_TIMESTAMP])

        return df

    def read_front_camera_data(self, field_name_list: list) -> DataFrame:
        """
        读取J3 前置摄像头融合数据，结果需要是一个DataFrame

        参数:
        - field_name_params：信号字段名

        返回:
        - pd.DataFrame: 包含 'timestamp' 和指定列的信号结果。
        """

        df = self.read_can_data('fd0', field_name_list)
        # 读取时间区间内的数据
        if self.has_time_period():
            df = scene_util.df_filter_by_timestamp(df, self.params[KEY_DATASET_INFO][KEY_START_TIMESTAMP],
                                                   self.params[KEY_DATASET_INFO][KEY_END_TIMESTAMP])

        return df

    def read_data(self, search_word, field_name_list: list) -> DataFrame:
        """
        读取ACAN数据，并返回结果，结果需要是一个DataFrame

        参数:
        - search_word: 查询词，可以是ACAN、PCAN、Fusion debugcan
        - field_name_params：信号字段名

        返回:
        - pd.DataFrame: 包含 'timestamp' 和指定列的信号结果。
        """
        df = self.read_can_data(search_word, field_name_list)
        # 读取时间区间内的数据
        if self.has_time_period():
            df = scene_util.df_filter_by_timestamp(df, self.params[KEY_DATASET_INFO][KEY_START_TIMESTAMP],
                                                   self.params[KEY_DATASET_INFO][KEY_END_TIMESTAMP])
        return df

    def read_data_from_logsim_result(self, search_word, field_name_list: list) -> DataFrame:
        """
        读取ACAN数据，并返回结果，结果需要是一个DataFrame

        参数:
        - search_word: 查询词，可以是ACAN、PCAN、Fusion debugcan
        - field_name_params：信号字段名

        返回:
        - pd.DataFrame: 包含 'timestamp' 和指定列的信号结果。
        """
        df = pd.read_parquet(scene_util.get_path(search_word, self.params[LOCAL_LOGSIM_RESULT_PATH_KEY]))[
            append_timestamp_field(field_name_list)]
        return df

    def has_time_period(self) -> bool:
        """
        判断是否有时间区间
        返回:
        - bool: 是否有时间区间
        """
        return (KEY_DATASET_INFO in self.params and self.params[KEY_DATASET_INFO] is not None
                and KEY_START_TIMESTAMP in self.params[KEY_DATASET_INFO]
                and KEY_END_TIMESTAMP in self.params[KEY_DATASET_INFO])

    def get_time_period(self) -> tuple:
        """
        获取时间区间
        返回:
        - tuple: 时间区间
        """
        if self.has_time_period():
            return self.params[KEY_DATASET_INFO][KEY_START_TIMESTAMP], self.params[KEY_DATASET_INFO][KEY_END_TIMESTAMP]
        return None, None

    def get_label(self) -> dict:
        """
        读取标签数据，并返回结果，结果需要是一个dict

        返回:
        - dict: 对应标签字段
        """
        return self.params[DATASET_LABEL_KEY]

    def read_label(self) -> dict:
        """
        读取标签数据，并返回结果，结果需要是一个dict

        返回:
        - dict: 对应标签字段
        """
        return self.params[DATASET_LABEL_KEY]

    def get_env(self) -> dict:
        """
        读取算子文件配置项(a=1,b=1,c=1...)，结果是一个dict

        返回:
        - dict: 对应标签字段
        """
        env = {}

        if CONFIG_STR not in self.params[PARAM_PAGE]:
            return {}

        config_str = self.params[PARAM_PAGE][CONFIG_STR]

        if config_str is not None and config_str != '':
            pairs = config_str.split(',')

            # 构造字典
            for pair in pairs:
                key, value = pair.split('=')
                env[key] = value

        return env

    def get_config(self):
        """
        读取json文件算子对应的配置，结果是一个dict
        json 文件内容为
            "metric_info":{
                "enabled_metric_list": ["eval/operator/test/test_x_operator.py","eval/operator/test/test_y_operator.py"],
                "disabled_metric_list":["eval/operator/test/test_z_operator.py"],
                "metric_config":{
                    "eval/operator/test/test_x_operator.py":{
                        "threshold" : 2
                    },
                    "eval/operator/test/test_y_operator.py":{
                        "threshold" : 1.5
                    },
                    "eval/operator/test/test_z_operator.py":{
                        "threshold" : [1,2]
                    }
                }
            }
        返回: json文件内容的metric_config内容
        - dict: 对应标签字段
        """
        operator_name = self.__class__.__name__
        for path, value in self.params[METRIC_CONFIG].items():
            if operator_name in path:  # 判断文件名是否在路径中
                return value
        return None

    def save_forecast_data(self, forecast_data: str, file_name: str):
        env = self.params
        obs_prefix = env.get('obs_prefix')
        """
        保存预测数据
        """
        local_path = current_config.get('containerPath') + "/" + file_name
        # 打开文件，如果文件不存在则创建文件
        with open(local_path, 'w') as file:
            # 将字符串写入文件
            file.write(forecast_data)

        obs_path = obs_prefix + "forecast_data/"

        obs_key = obs_path + file_name

        print("obs_key:", obs_key)

        data_utils.upload_object(obs_key, local_path)
