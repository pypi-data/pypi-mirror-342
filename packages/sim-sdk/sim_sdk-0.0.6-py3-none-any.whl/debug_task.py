from evaluat import python_main as eval_main
from dags.digscene import dig_scene
import argparse
import sys
import logging
from evaluat.const import SOURCE, SPLIT, SCENE, LOGSIM
import json
from env_manager import env_manager

"""
本地调试工具类：解析命令行参数，组装成成生产环境参数格式
"""

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

buz_dict = {
    "eval": {"dig": SCENE},
    "dig": {"source": SOURCE}
}

def cmd_debug_args():
    """
    命令行本地调试参数
    """
    """
        解析命令行参数，目的是和平台参数组织形式
        """
    # 创建解析器
    parser = argparse.ArgumentParser(description="Process key-value arguments")

    # 添加 key-value 类型的参数
    parser.add_argument('--op_file_name', type=str, help='Operation file name')
    parser.add_argument('--task_id', type=str, help='eval task id')
    parser.add_argument('--logsim_task_id', type=str, help='logsim_task_id')
    # parser.add_argument('--bc_name', type=str, help='BC name')
    parser.add_argument('--config_str', type=str, help='Config string')
    # parser.add_argument('--source_type', type=str, help='Source type')
    parser.add_argument('--buz_type', type=str, help='Business type')
    parser.add_argument('--data_id', type=str, help='Source ID list')

    # 解析命令行参数
    args = parser.parse_args()

    logging.info(f"args:{args}")

    # return args.op_file_name, args.bc_name, args.config_str, args.source_type, args.source_id_list, args.buz_type
    return args.task_id, args.op_file_name, args.data_id, args.buz_type, args.logsim_task_id, args.config_str

def parse_args():
    """
    解析命令行参数，目的是和平台参数组织形式
    """

    # 优先获取cmd命令行参数
    task_id, op_file_name, data_id, buz_type, logsim_task_id, config_str = cmd_debug_args()

    if not op_file_name:
        raise Exception("未获取到参数：op_file_name")

    # if not bc_name:
    #     raise Exception("未获取到参数：bc_name")

    # if not source_type:
    #     raise Exception("未获取到参数：source_type")

    if not data_id:
        raise Exception("未获取到参数：data_id")

    # 打印接收到的参数
    logging.info("Parsed arguments:")
    logging.info(f"op_file_name: {op_file_name}")
    # logging.info(f"bc_name: {bc_name}")
    logging.info(f"config_str: {config_str}")
    # logging.info(f"source_type: {source_type}")
    logging.info(f"data_id: {data_id}")
    logging.info(f"task_id: {task_id}")
    logging.info(f"logsim_task_id: {logsim_task_id}")

    if buz_type not in buz_dict.keys():
        raise Exception(f"buz_type:{buz_type} 目前仅支持 {buz_dict.keys()}")

    param_page_dict = {"op_file_name": op_file_name,
                       "config_str": config_str}

    param_pipeline_dict = {"source_type": SCENE,
                           "source_id_list": data_id,
                           "eval_task_id": task_id,
                           "logsim_task_id": logsim_task_id}

    # 将字典转换为 JSON 字符串形式
    param_page_json = json.dumps(param_page_dict)
    param_pipeline_json = json.dumps(param_pipeline_dict)

    # 假设将这些 JSON 字符串作为 sys.argv 传递给下一个函数
    sys.argv = ['python_main.py', param_page_json, param_pipeline_json]

    return buz_type


def main():
    # 设置环境为debug
    env_manager.set_mode("debug")

    buz_type = parse_args()
    logging.info(f"任务 {buz_type} 开始")
    if buz_type == "eval":
        eval_main.main()
    elif buz_type == "dig":
        dig_scene.dig_data()


if __name__ == '__main__':
    main()
