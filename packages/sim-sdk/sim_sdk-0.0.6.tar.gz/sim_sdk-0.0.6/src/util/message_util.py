import logging

import requests
from typing import List, Optional

from util import nacos_client
from util import token_utils

current_config = nacos_client.get_config()

DEFAULT_WEBHOOKS = [
    current_config["notify"]["feishu"]["webhook"]
]

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def send_feishu_message(message: str, webhooks: Optional[List[str]] = None) -> bool:
    """
    通过 HTTP 接口发送飞书消息到多个 webhook，支持默认的 webhook 地址。

    :param message: 消息内容
    :param webhooks: 飞书 webhook 地址列表（可选）
    :return: 成功返回 True，全部失败返回 False
    """
    # 使用默认的 webhooks，如果没有传递
    if webhooks is None:
        webhooks = DEFAULT_WEBHOOKS

    all_failed = True  # 默认假设全部失败
    feishu_notify_api = current_config["auth"]["domain"] + current_config["auth"]["messageapi"]
    env = current_config["notify"]["env"]

    for webhook in webhooks:
        data = {
            "message": f'【{env}】' + message,
            "webhook": webhook
        }

        try:
            token = token_utils.get_token()  # 获取 Token
            headers = {"Authorization": f"Bearer {token}"}  # 添加 Token 到请求头

            response = requests.post(feishu_notify_api, data=data, headers=headers)
            response.raise_for_status()  # 如果响应码不是 200，将抛出异常
            all_failed = False  # 如果发送成功，标记为成功
        except Exception as e:
            logging.exception(f"Error sending message to {webhook}: {e}")

    return not all_failed  # 如果所有都失败返回 False，至少有一个成功返回 True

