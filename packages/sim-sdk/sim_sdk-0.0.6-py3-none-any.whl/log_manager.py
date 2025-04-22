# log_manager.py
import logging
import os

# 配置默认日志记录器
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')


class LoggingManager:
    """
    日志管理器，用于管理不同 package_id 的日志输出到不同日志文件，同时对外提供统一的日志接口
    也可以作为系统日志的统一出口：比如用LoggingManager.logging().info替换logging.info
    """
    _instance = None
    _loggers = {}  # 存储不同 package_id 的 logger 实例
    _loggers_file_paths = {}
    _current_package_id = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def set_current_package(cls, package_id, log_dir="logs"):
        """
        设置当前 package_id，并创建对应的 logger 实例
        :param package_id: package_id
        :param log_dir: 日志目录
        """
        cls._current_package_id = package_id
        if package_id not in cls._loggers:
            # 确保日志目录存在
            os.makedirs(log_dir, exist_ok=True)
            # 创建 logger 实例
            logger = logging.getLogger(package_id)
            logger.setLevel(logging.INFO)
            # 创建文件 handler，日志文件路径为 log_dir/package_id.log
            log_file_path = f"{log_dir}/{package_id}.log"
            cls._loggers_file_paths[package_id] = log_file_path
            file_handler = logging.FileHandler(log_file_path, mode='a', encoding='utf-8')
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            cls._loggers[package_id] = logger

    @classmethod
    def logging(cls):
        if cls._current_package_id is None:
            return logging
        return cls._loggers[cls._current_package_id]

    @classmethod
    def get_log_file_path(cls):
        if cls._current_package_id is None:
            return logging
        return cls._loggers_file_paths[cls._current_package_id]

    @classmethod
    def release_logger(cls):
        if cls._current_package_id is not None:
            cls.release_logger_by_package_id(cls._current_package_id)


    @classmethod
    def release_logger_by_package_id(cls, package_id):
        """显式关闭并清理指定 package_id 的日志资源"""
        if package_id in cls._loggers:
            logger = cls._loggers[package_id]
            # 关闭所有 handler 并清空
            for handler in logger.handlers[:]:
                handler.close()
                logger.removeHandler(handler)
            del cls._loggers[package_id]
