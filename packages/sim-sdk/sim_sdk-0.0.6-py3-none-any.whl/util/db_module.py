from util import nacos_client
from util.db_utils import CustomDBUtils

config = nacos_client.get_config()  # 获取配置

db_config = {
    'host': config.get('mysql_host'),
    'port': config.get('mysql_port'),
    'user': config.get('mysql_user'),
    'password': config.get('mysql_password'),
    'database': config.get('mysql_database'),
    'charset': 'utf8mb4'
}

db_util: CustomDBUtils = CustomDBUtils(db_config)

