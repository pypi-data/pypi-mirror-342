import base64
import logging

import requests

from util import nacos_client

# 通过 get_config() 函数获取配置（懒加载）
current_config = nacos_client.get_config()

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_file_str(file_path, bc_name):
    detail_url = current_config.get("git").get("detail_url")
    repo_name = current_config.get("git").get("repo_name")
    url = detail_url % (repo_name, file_path, bc_name)

    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查是否请求成功

        result = response.json()  # 将响应解析为 JSON

        # 检查 'content' 字段是否存在
        base64_content = result.get("content")

        if base64_content:
            # 解码 Base64 内容并返回字符串
            decoded_bytes = base64.b64decode(base64_content)
            return decoded_bytes.decode('utf-8')  # 将字节流转为字符串
        else:
            logging.error("未找到对应的算子文件，filePath：{}，bcName：{}".format(file_path, bc_name))
            return None

    except Exception as e:
        logging.error("获取算子文件异常，filePath：{}，bcName：{}，异常：{}".format(file_path, bc_name, str(e)))
        return None


if __name__ == "__main__":
    get_file_str("src/digscene/obj_cut_in.py", "feature/v1.2.0")