import importlib
import logging
import os
import shutil
import stat
import sys
from datetime import datetime, timedelta
from typing import Union, Optional, List

import ffmpeg
from obs import PutObjectHeader

from util import nacos_client
from util.date_utils import DateUtils
from util.minio_client_singleton import MinioClientSingleton
from util.obs_client_singleton import ObsClientSingleton

# 通过 get_config() 函数获取配置（懒加载）
current_config = nacos_client.get_config()

bucket_name = current_config.get('bucket_name')
endpoint = current_config.get('endpoint')
ak = current_config.get('ak')
sk = current_config.get('sk')

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def listObjects(obs_prefix):
    obsClient = ObsClientSingleton.get_instance(ak, sk, endpoint)
    # 假设是查询目录下文件的元数据
    response = obsClient.listObjects(bucket_name, prefix=obs_prefix)
    if response.status < 300 and 'contents' in response.body:
        return response.body
    else:
        logging.error(f"Error fetching metadata for {obs_prefix}: {response.body}")
        return None


def change_permissions_and_delete(directory_path):
    # 修改目录及其所有子文件和文件夹的权限
    for root, dirs, files in os.walk(directory_path):
        for dir_ in dirs:
            os.chmod(os.path.join(root, dir_), stat.S_IRWXU)  # 为目录添加读、写、执行权限
        for file_ in files:
            os.chmod(os.path.join(root, file_), stat.S_IRWXU)  # 为文件添加读、写、执行权限

    # 删除整个目录
    shutil.rmtree(directory_path)
    print(f"Successfully deleted the directory: {directory_path}")


def list_files_in_directory(directory_prefix):
    if current_config.get('deploy_model') == current_config.get('MODEL_CLOUD'):
        obsClient = ObsClientSingleton.get_instance(ak, sk, endpoint)
        resp = obsClient.listObjects(bucket_name, prefix=directory_prefix)
        if resp.status < 300:
            return [content.key for content in resp.body.contents]
        else:
            logging.error('List Objects Failed, errorCode: %s, errorMessage:%s', resp.errorCode, resp.errorMessage)
            return []
    elif current_config.get('deploy_model') == current_config.get('MODEL_LOCAL'):
        try:
            minio_client = MinioClientSingleton.get_instance(
                current_config.get('minio_endpoint'),
                current_config.get('minio_access_key'),
                current_config.get('minio_secret_key'))
            objects = minio_client.list_objects(current_config.get('minio_bucket_name'), prefix=directory_prefix)
            return [obj.object_name for obj in objects]
        except Exception as e:
            logging.exception("获取minion文件列表异常，directory_prefix:%s", directory_prefix)
            return []


def get_directory(prefix, downloadDir, suffixes: Optional[List[str]] = None) -> bool:
    os.makedirs(downloadDir, exist_ok=True)

    def should_download(file_name: str) -> bool:
        if not suffixes:
            return True
        return any(file_name.lower().endswith(suffix.lower()) for suffix in suffixes)

    if current_config.get('deploy_model') == current_config.get('MODEL_CLOUD'):
        obsClient = ObsClientSingleton.get_instance(ak, sk, endpoint)

        try:
            result = obsClient.listObjects(bucket_name, prefix=prefix)
            if not result or result.status >= 300:
                logging.error("OBS 列取目录失败，prefix:%s, errorCode:%s, errorMsg:%s", prefix, result.errorCode, result.errorMessage)
                return False

            for content in result.body.contents:
                objectKey = content.key
                if not should_download(objectKey):
                    continue

                relative_path = os.path.relpath(objectKey, prefix)
                local_path = os.path.join(downloadDir, relative_path)
                os.makedirs(os.path.dirname(local_path), exist_ok=True)

                download_result = get_object(objectKey, local_path)
                if download_result is False:
                    return False

            return True
        except Exception as e:
            logging.exception("OBS 下载目录异常，prefix:%s", prefix)
            return False

    elif current_config.get('deploy_model') == current_config.get('MODEL_LOCAL'):
        try:
            minio_client = MinioClientSingleton.get_instance(
                current_config.get('minio_endpoint'),
                current_config.get('minio_access_key'),
                current_config.get('minio_secret_key'))

            objects = minio_client.list_objects(current_config.get('minio_bucket_name'), prefix=prefix, recursive=True)
            for obj in objects:
                objectKey = obj.object_name
                if not should_download(objectKey):
                    continue

                relative_path = os.path.relpath(objectKey, prefix)
                local_path = os.path.join(downloadDir, relative_path)
                os.makedirs(os.path.dirname(local_path), exist_ok=True)

                result = minio_client.fget_object(current_config.get('minio_bucket_name'), objectKey, local_path)
                if result is None:
                    logging.error("MinIO 下载失败，objectKey:%s", objectKey)
                    return False
                logging.info("MinIO 下载成功，%s", objectKey)

            return True
        except Exception as e:
            logging.exception("MinIO 下载目录异常，prefix:%s", prefix)
            return False


def get_object(objectKey, downloadPath) -> bool:
    if os.path.exists(downloadPath):
        return True

    if current_config.get('deploy_model') == current_config.get('MODEL_CLOUD'):
        obsClient = ObsClientSingleton.get_instance(ak, sk, endpoint)

        result = obsClient.getObject(bucket_name, objectKey, downloadPath)
        if result is None:
            logging.error("obs下载文件无响应，objectKey:%s", objectKey)
            return False
        if result.status < 300:
            logging.info("obs下载文件成功，%s", objectKey)
            return True
        else:
            logging.error("obs下载文件失败，objectKey:%s, errorCode:%s,errorMsg:%s", objectKey, result.errorCode, result.errorMsg)
            return False
    elif current_config.get('deploy_model') == current_config.get('MODEL_LOCAL'):
        try:
            minio_client = MinioClientSingleton.get_instance(
                current_config.get('minio_endpoint'),
                current_config.get('minio_access_key'),
                current_config.get('minio_secret_key'))

            result = minio_client.fget_object(current_config.get('minio_bucket_name'), objectKey, downloadPath)

            if result is None:
                logging.error("minio下载文件无响应，objectKey:%s", objectKey)
                return False
            return True
        except Exception as e:
            logging.exception("下载minion数据异常，objectKey:%s", objectKey)
            return False


def upload_object(object_key, local_file_path):
    if current_config.get('deploy_model') == current_config.get('MODEL_CLOUD'):
        obsClient = ObsClientSingleton.get_instance(ak, sk, endpoint)

        # 上传对象的附加头域
        headers = PutObjectHeader()
        # # 【可选】待上传对象的MIME类型
        # headers.contentType = 'text/plain'
        bucketName = bucket_name
        # 对象名，即上传后的文件名
        objectKey = object_key
        # 待上传文件/文件夹的完整路径，如aa/bb.txt，或aa/
        file_path = local_file_path
        # 上传文件的自定义元数据
        metadata = {}
        # 文件上传
        resp = obsClient.putFile(bucketName, objectKey, file_path, metadata, headers)
        # 返回码为2xx时，接口调用成功，否则接口调用失败
        if resp.status < 300:
            logging.info('Put File Succeeded')
        else:
            logging.error('Put File Failed, errorCode: %s, errorMessage:%s', resp.errorCode, resp.errorMessage)
    elif current_config.get('deploy_model') == current_config.get('MODEL_LOCAL'):
        minio_client = MinioClientSingleton.get_instance(
            current_config.get('minio_endpoint'),
            current_config.get('minio_access_key'),
            current_config.get('minio_secret_key'))
        minio_client.fput_object(current_config.get('minio_bucket_name'), object_key, local_file_path)


def get_object_metadata(obj_key: str) -> Union[int, None]:
    if current_config.get('deploy_model') == current_config.get('MODEL_CLOUD'):
        obsClient = ObsClientSingleton.get_instance(ak, sk, endpoint)
        resp = obsClient.getObjectMetadata(bucket_name, obj_key)

        if resp.status < 300:
            return resp.body.contentLength
        else:
            logging.error('Get Object Metadata Failed, key: %s, status:%s, reason: %s', obj_key, resp.status, resp.reason)
            raise ValueError(f"获取obs meta数据异常，objectKey:{obj_key}")
    elif current_config.get('deploy_model') == current_config.get('MODEL_LOCAL'):
        try:
            minio_client = MinioClientSingleton.get_instance(
                current_config.get('minio_endpoint'),
                current_config.get('minio_access_key'),
                current_config.get('minio_secret_key'))
            stat = minio_client.stat_object(current_config.get('minio_bucket_name'), obj_key)
        except Exception as e:
            logging.exception("获取minion meta数据异常，objectKey:%s", obj_key)
            raise ValueError(f"获取minion meta数据异常，objectKey:{obj_key}")
        return 0


def get_time_range_from_asc(asc_file: str):
    with open(asc_file, 'r') as f:
        lines = f.readlines()

    # 处理前几行，获取基准时间
    base_time = None
    base_timestamp = None
    for line in lines[:5]:  # 只读取前五行，假设文件头部包含日期信息
        line = line.strip()
        if line.startswith("date"):
            date_str = line.split("date", 1)[1].strip()
            base_time = DateUtils.parse_date_string(date_str)
            base_timestamp = base_time.timestamp()
            break  # 找到基准时间后退出循环

    if base_timestamp is None:
        raise ValueError("Failed to find base timestamp in the file.")

    # 获取最后一行数据
    last_line = lines[-1].strip()
    parts = last_line.split()
    if parts[0].replace('.', '', 1).isdigit():
        relative_time = float(parts[0])
        last_timestamp = base_timestamp + relative_time
    else:
        raise ValueError("Invalid time format in the last line.")

    # 返回时间范围（第一个时间戳和最后一个时间戳）
    first_timestamp = base_timestamp  # 假设第一行就是文件的开始时间
    return first_timestamp, last_timestamp


def generate_timestamps_from_asc(asc_file: str, timestamp_file: str):
    with open(asc_file, 'r') as f:
        lines = f.readlines()

    timestamps = []
    base_time = None
    base_timestamp = None

    for line in lines:
        line = line.strip()
        if line.startswith("date"):
            date_str = line.split("date", 1)[1].strip()
            base_time = DateUtils.parse_date_string(date_str)
            base_timestamp = base_time.timestamp()
        elif line.startswith("base") or line.startswith("Begin Triggerblock"):
            continue
        elif line and base_time:
            parts = line.split()
            if parts[0].replace('.', '', 1).isdigit():
                try:
                    relative_time = float(parts[0])
                    timestamp = base_timestamp + relative_time
                    timestamps.append((len(timestamps), timestamp))
                except ValueError:
                    continue  # Skip lines where conversion fails

    with open(timestamp_file, 'w') as f:
        for i, ts in timestamps:
            f.write(f"{i} {ts}\n")

    return timestamps


def generate_timestamps_from_video(video_file: str, frame_rate: int, timestamp_file: str):
    # 获取视频时长和起始时间
    probe = ffmpeg.probe(video_file)
    duration = float(probe['format']['duration'])
    filename = os.path.basename(video_file)

    start_time_str = filename.split('_')[-1].split('.')[0]
    start_time = datetime.strptime(start_time_str, '%Y%m%d%H%M%S')

    timestamps = []
    current_time = start_time
    frame_duration = timedelta(seconds=1 / frame_rate)
    frame_number = 0

    while current_time < start_time + timedelta(seconds=duration):
        timestamps.append((frame_number, current_time.timestamp()))
        current_time += frame_duration
        frame_number += 1

    # 写入时间戳文件
    with open(timestamp_file, "w") as f:
        for frame_number, timestamp in timestamps:
            f.write(f"{frame_number} {timestamp}\n")

    return timestamps


def execute_python_script(script_path, *args, option=None):
    try:
        # 获取脚本的模块名称
        module_name = os.path.basename(script_path).replace('.py', '')

        # 通过 importlib 加载模块
        spec = importlib.util.spec_from_file_location(module_name, script_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # 构建传递给 main 函数的参数
        arg_list = list(args)

        # 假设目标脚本中定义了一个 main() 函数，可以执行并传入参数
        if hasattr(module, 'main'):
            result = module.main(*arg_list, option=option)
        else:
            raise AttributeError(f"No 'main' function found in {script_path}")

        return result

    except Exception as e:
        logging.exception(f"An error occurred: {str(e)}")
        return None