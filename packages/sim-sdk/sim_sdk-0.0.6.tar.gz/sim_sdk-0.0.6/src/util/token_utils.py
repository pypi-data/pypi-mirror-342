import logging

import requests

from util.redis_module import redis_client
from util import nacos_client

current_config = nacos_client.get_config()  # 获取配置
token_key = current_config["token"]["clw_key"]
expire_time = current_config["token"]["expire_time"]
entry = current_config["auth"]["entry"]
password = current_config["auth"]["password"]
username = current_config["auth"]["username"]
clw_domain = current_config["auth"]["domain"]


def get_token():
    """
    查询 Redis 判断是否有未过期 token，如果有直接返回 token，并刷新 Redis 缓存时间。
    """
    value = redis_client.get(token_key)

    if value:
        redis_client.expire(token_key, expire_time)
        return value.decode('utf-8')

    return refresh_token()


def refresh_token():
    """
    如果调用网联平台 401，重新生成 token
    """
    try:
        url = f"{clw_domain}/api/v1.0/authorization/web/loginNoCode"
        params = {
            "entry": entry,
            "password": password,
            "username": username
        }
        response = requests.post(url, json=params)
        response.raise_for_status()

        result = response.json()
        token = result.get("data", {}).get("token")

        if not token:
            raise ValueError("Token not found in response")
    except Exception as e:
        logging.error("获取 token 失败", exc_info=True)
        raise Exception("获取 token 失败") from e

    # 保存 token 到 Redis
    redis_client.set(token_key, token, expire_time)

    return token
