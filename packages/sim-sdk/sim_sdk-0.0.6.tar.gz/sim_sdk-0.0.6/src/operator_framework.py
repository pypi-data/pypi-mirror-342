from pathlib import Path
import importlib.util
from operator_interface import Operator
import logging
from util import nacos_client
import const_key
import sys

current_config = nacos_client.get_config()

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

class OperatorFramework:
    """
    算子框架，用于加载、执行算子和保存算子结果。
    """

    def __init__(self):
        # 算子字典，键为算子名称，值为算子类
        self.operators = {}

    def load_common(self, script_local_path_list: list):
        """
        从给定路径列表加载模块，并将其注册到框架中。
        @param script_local_path_list: 算子完成路径及名称列表：["/src/a.py", "/src/b.py"]
        """
        for script_local_path in script_local_path_list:
            self.load_module(script_local_path)

    def load_multiple_operators(self, script_local_path_list: list):
        """
        从给定路径列表加载算子模块，并将其注册到框架中。
        @param script_local_path_list: 算子完成路径及名称列表：["/operator/lane/aeb_operator.py",
            "/operator/lane/brake_operator.py"]
        """
        for script_local_path in script_local_path_list:
            self.load_operator(script_local_path)

    def load_operator(self, script_local_path: str):
        """
        从给定路径加载算子模块，并将其注册到框架中。
        @param script_local_path: 算子文件完整路径：/operator/lane/aeb_operator.py
        """
        # 在指定目录下加载自定义的算子脚本
        module = self.load_module(script_local_path)

        # 从算子脚本中加载算子类：这里约定算子脚本名和算子类名相同custom_operator.py中有声明同名类 class custom_operator
        class_name = script_local_path.rsplit('/', 1)[-1].replace(".py", "")
        # 获取最后一个部分
        operator_class = getattr(module, class_name, None)

        # 注册算子到框架中
        if operator_class and issubclass(operator_class, Operator):
            # operator_name = operator_class.__name__
            self.operators[script_local_path] = operator_class

    def load_module(self, script_local_path):
        """
        从给定路径加载模块。
        @param script_local_path: 算子文件完整路径：operator/lane/aeb_operator.py
        """
        src_dir = current_config.get('containerPath') + '/src'
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)

        # 动态加载模块
        spec = importlib.util.spec_from_file_location("module_operator", Path(script_local_path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def execute_multiple_operators(self, script_local_path_list: list, params: dict, save_result_method=None,
                                   save_middle_files_method=None) -> dict:
        """
        执行指定名称的算子，并将结果保存到ES。
        @param script_local_path_list: 算子完成路径及名称列表：["/operator/lane/aeb_operator.py",
            "/operator/lane/brake_operator.py"]
        @param params: 算子参数
        @param save_result_method: 算子结果保存方法，不是必须
        @param save_middle_files_method: 保存中间结果文件方法，不是必须
        @param cus_logging: 自定义日志记录器`

        @return: 各个算子结果
        """
        # 各个算子的执行结果
        operator_result_dic = {}
        # 各个算子的配置版本信息
        operator_version_dict = {}

        # 算子计算过程中产生的一些计算数据
        operators_cvs_df_list = []
        operators_topic_df_list = []

        # 执行各个算子
        for script_local_path in script_local_path_list:
            operator_name, operator_result, cvs_df, topic_df, operator_version = self.execute_operator(
                                                                                     script_local_path, params,
                                                                                     save_result_method)
            operator_version_dict[operator_name] = operator_version
            # 统一处理成数组
            if operator_result:
                if isinstance(operator_result, dict):
                    operator_result_dic[operator_name] = [operator_result]
                else:
                    operator_result_dic[operator_name] = operator_result

            # 处理中间结果
            if cvs_df is not None and not cvs_df.empty:
                operators_cvs_df_list.append(cvs_df)
            if topic_df is not None and not topic_df.empty:
                operators_topic_df_list.append(topic_df)

        return operator_result_dic, operators_cvs_df_list, operators_topic_df_list, operator_version_dict

    def execute_operator(self, script_local_path: str, params: dict, save_result_method=None):
        """
        执行指定名称的算子，并将结果保存到ES。
        @param script_local_path: 算子文件完整路径：/operator/lane/aeb_operator.py
        @param params: 算子参数
        @param save_result_method: 算子结果保存方法，不是必须
        @param cus_logging: 日志记录器
        """
        if script_local_path in self.operators:
            operator_class = self.operators[script_local_path]

            # 创建算子实例并执行
            operator_instance = operator_class()
            # 把算子参数传递给算子实例
            operator_instance.set_params(params)
            operator_instance.set_logging(logging)

            logging.info(f"execute_operator params: %s", params)
            # 执行算子
            operator_result = operator_instance.compute()
            logging.info(f"execute_operator {operator_class.__name__} auto result: {operator_result}")

            # 算子json每个算子的配置dict
            metric_config = operator_instance.get_config()
            operator_version = None
            if "version" in metric_config:
                operator_version = metric_config["version"]

            # 是否需要保存结果
            if save_result_method is not None:
                # 使用外部传入的 save_result 方法保存自动结果
                save_result_method(operator_class.__name__, operator_result, metric_config, params,
                                   operator_instance.index_name(), params[const_key.DATASET_LABEL_KEY])

                # 手动保存的结果
                manual_table_name, manual_result = operator_instance.get_manual_save_result()
                logging.info(f"execute_operator {operator_class.__name__} manual {manual_table_name} "
                             f"result: {manual_result}")

                save_result_method(operator_class.__name__, manual_result, metric_config, params,
                                   manual_table_name, params[const_key.DATASET_LABEL_KEY])

            # 中间结果数据，后续concat后保存到文件
            cvs_df = operator_instance.get_csv_df()
            topic_df = operator_instance.get_topic_df()

            # 返回算子名称和算子结果
            return operator_class.__name__, operator_result, cvs_df, topic_df, operator_version
        else:
            raise ValueError(f"Operator {script_local_path} not found.")
