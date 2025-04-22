import logging
import os

import nacos
import yaml

# 全局配置变量，确保配置和客户端只会初始化一次
_current_config = None
_nacos_client = None  # 用于存储 NacosClient 实例

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def _initialize_nacos_client():
    """初始化 NacosClient 单例"""
    global _nacos_client

    # 如果客户端还没有初始化，进行初始化
    if _nacos_client is None:
        SERVER_ADDRESSES = os.getenv('NACOS_SERVER_ADDRESSES')
        NAMESPACE = os.getenv('NACOS_NAMESPACE')

        # 初始化 Nacos 客户端
        _nacos_client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE)
        logging.info("Nacos Client initialized.")
    return _nacos_client


def _load_config():
    """从 Nacos 加载配置并返回配置字典"""
    global _current_config

    # 如果配置已经加载，则直接返回
    if _current_config is not None:
        return _current_config

    # 从环境变量读取 Nacos 配置
    DATA_ID = os.getenv('NACOS_DATA_ID')
    GROUP = os.getenv('NACOS_GROUP')

    logging.info("DATA_ID: %s", DATA_ID)
    logging.info("GROUP: %s", GROUP)

    # 获取 Nacos 客户端（确保只有一个实例）
    client = _initialize_nacos_client()

    # 从 Nacos 获取配置
    config_data = client.get_config(DATA_ID, GROUP, 30)

    # 解析 YAML 格式的配置
    _current_config = yaml.safe_load(config_data) if config_data else {}

    logging.info("配置加载成功")

    return _current_config


def get_config():
    """提供对配置的访问，必要时加载"""
    return _load_config()
