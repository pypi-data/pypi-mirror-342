import importlib.util
import importlib.util
import logging
import os
import shutil
import stat
import sys
import zipfile
from datetime import datetime, timedelta
import json
import base64
from typing import Optional

import ffmpeg
import pymysql
import redis
from minio import Minio
from obs import ObsClient, CompletePart, CompleteMultipartUploadRequest, GetObjectHeader
from obs import PutObjectHeader

from util import nacos_client
import numpy as np
from log_manager import LoggingManager
from util import data_utils

# 通过 get_config() 函数获取配置（懒加载）
current_config = nacos_client.get_config()

bucket_name = current_config.get('bucket_name')
endpoint = current_config.get('endpoint')
ak = current_config.get('ak')
sk = current_config.get('sk')

# 本地暂存目录
containerPath = current_config.get('containerPath')

# mysql配置
mysql_host = current_config.get('mysql_host')
mysql_port = current_config.get('mysql_port')
mysql_user = current_config.get('mysql_user')
mysql_password = current_config.get('mysql_password')
mysql_database = current_config.get('mysql_database')

# 添加当前目录到 Python 路径中
sys.path.append(os.path.dirname(__file__))

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Source:
    def __init__(self, source_type: int, source_id_list: str):
        self.source_type = source_type
        self.source_id_list = source_id_list

    def to_dict(self):
        """将 Source 对象转换为字典"""
        return {
            'source_type': self.source_type,
            'source_id_list': self.source_id_list
        }

    def get_source_id_list(self):
        """将逗号分隔的字符串转换为列表"""
        return self.source_id_list.split(',')

    def set_source_id_list(self, source_id_list):
        """将列表转换为逗号分隔的字符串"""
        self.source_id_list = ','.join(map(str, source_id_list))

    def add_source_id(self, source_id):
        """添加一个新的 source_id 到 source_id_list"""
        source_id_list = self.get_source_id_list()
        source_id_list.append(str(source_id))
        self.set_source_id_list(source_id_list)

    def remove_source_id(self, source_id):
        """从 source_id_list 中移除一个 source_id"""
        source_id_list = self.get_source_id_list()
        source_id_list.remove(str(source_id))
        self.set_source_id_list(source_id_list)

    def __repr__(self):
        return f"Source(source_type={self.source_type}, source_id_list='{self.source_id_list}')"


def change_permissions_and_delete(directory_path):
    # 检查目录是否存在
    if not os.path.exists(directory_path):
        print(f"目录不存在: {directory_path}")
        return

    # 修改目录及其所有子文件和文件夹的权限
    for root, dirs, files in os.walk(directory_path):
        for dir_ in dirs:
            os.chmod(os.path.join(root, dir_), stat.S_IRWXU)  # 为目录添加读、写、执行权限
        for file_ in files:
            os.chmod(os.path.join(root, file_), stat.S_IRWXU)  # 为文件添加读、写、执行权限

    # 删除整个目录
    shutil.rmtree(directory_path)
    print(f"Successfully deleted the directory: {directory_path}")


def parse_date_string(date_str):
    # 将 "Fri Aug 09 02:08:37 pm 2024" 转换为 datetime 对象
    return datetime.strptime(date_str, "%a %b %d %I:%M:%S %p %Y")


def time_to_timestamp(dt):
    """Convert a datetime object to a Unix timestamp."""
    return dt.timestamp()


def convert_to_unix_timestamp(time_input):
    """
    将时间字符串或 datetime 对象转换为 Unix 时间戳（秒.微秒格式）。

    :param time_input: 时间字符串或 datetime 对象
    :return: Unix 时间戳，格式为秒.微秒
    """
    # 如果输入是 datetime 对象，则直接转换为时间戳
    if isinstance(time_input, datetime):
        dt = time_input
    else:
        # 否则，假设输入是时间字符串，按指定格式解析
        time_format = '%Y-%m-%d %H:%M:%S.%f'
        dt = datetime.strptime(time_input, time_format)

    # 获取 Unix 时间戳（秒数）
    timestamp = dt.timestamp()

    # 返回格式化后的 Unix 时间戳，保留6位小数（包括微秒部分）
    return f"{timestamp:.6f}"

def generate_timestamps_from_video(video_file, frame_rate, timestamp_file):
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


def generate_timestamps_from_asc(asc_file, timestamp_file):
    with open(asc_file, 'r') as f:
        lines = f.readlines()

    timestamps = []
    base_time = None
    base_timestamp = None

    for line in lines:
        line = line.strip()
        if line.startswith("date"):
            date_str = line.split("date", 1)[1].strip()
            base_time = parse_date_string(date_str)
            base_timestamp = time_to_timestamp(base_time)
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


def incr_float(cache_key, increment, expire_time=60):
    try:
        # 使用连接池创建 Redis 连接
        redis_pool = redis.ConnectionPool(host=current_config.get('redis_host'), port=current_config.get('redis_port'), db=current_config.get('redis_db'),
                                          password=current_config.get('redis_password'))
        redis_client = redis.Redis(connection_pool=redis_pool)

        # 使用 INCRBYFLOAT 来进行浮点数累加
        new_value = redis_client.incrbyfloat(cache_key, increment)

        # 设置过期时间，只有在 expire_time 大于 0 的情况下
        if expire_time > 0:
            redis_client.expire(cache_key, expire_time)

        return new_value  # 返回累加后的新值
    except Exception as e:
        logging.exception("增加缓存发生异常")
        return None  # 操作失败时返回 None


def set_str_cache(cache_key, cache_value, expire_time=60):
    try:
        # 使用连接池创建 Redis 连接
        redis_pool = redis.ConnectionPool(host=current_config.get('redis_host'), port=current_config.get('redis_port'),
                                          db=current_config.get('redis_db'),
                                          password=current_config.get('redis_password'))
        redis_client = redis.Redis(connection_pool=redis_pool)

        # 设置键值对，并设置过期时间
        redis_client.set(cache_key, cache_value)
        redis_client.expire(cache_key, expire_time)

        return True  # 操作成功
    except Exception as e:
        logging.exception("设置缓存发生异常")
        return False  # 操作失败


def get_str_cache(cache_key):
    try:
        # 使用连接池创建 Redis 连接
        redis_pool = redis.ConnectionPool(host=current_config.get('redis_host'), port=current_config.get('redis_port'),
                                          db=current_config.get('redis_db'),
                                          password=current_config.get('redis_password'))
        redis_client = redis.Redis(connection_pool=redis_pool)

        # 设置键值对，并设置过期时间
        return redis_client.get(cache_key)
    except Exception as e:
        logging.exception("获取缓存发生异常")
        return None  # 操作失败


def del_str_cache(cache_key):
    try:
        # 使用连接池创建 Redis 连接
        redis_pool = redis.ConnectionPool(host=current_config.get('redis_host'), port=current_config.get('redis_port'),
                                          db=current_config.get('redis_db'),
                                          password=current_config.get('redis_password'))
        redis_client = redis.Redis(connection_pool=redis_pool)

        # 删除键值对
        return redis_client.delete(cache_key)
    except Exception as e:
        logging.exception("删除键值对缓存发生异常")
        return None  # 操作失败


def getObject(objectKey, downloadPath):
    if current_config.get('deploy_model') == current_config.get('MODEL_CLOUD'):
        obsClient = ObsClient(access_key_id=ak, secret_access_key=sk, server=endpoint)

        result = obsClient.getObject(bucket_name, objectKey, downloadPath)
        if result is None:
            LoggingManager.logging().error("obs下载文件无响应，objectKey:%s", objectKey)
            return False
        if result.status < 300:
            LoggingManager.logging().info("obs下载文件成功，%s", objectKey)
            return True
        else:
            LoggingManager.logging().error("obs下载文件失败，objectKey:%s, errorCode:%s,errorMsg:%s", objectKey, result.errorCode, result.errorMsg)
            return False
    elif current_config.get('deploy_model') == current_config.get('MODEL_LOCAL'):
        try:
            minio_client = Minio(
                current_config.get('minio_endpoint'),  # MinIO服务器地址和端口
                access_key=current_config.get('minio_access_key'),  # 你的访问密钥
                secret_key=current_config.get('minio_secret_key'),  # 你的密钥
                secure=False  # 如果使用的是HTTP而不是HTTPS，设置为False
            )
            result = minio_client.fget_object(current_config.get('minio_bucket_name'), objectKey, downloadPath)

            if result is None:
                LoggingManager.logging().error("minio下载文件无响应，objectKey:%s", objectKey)
                return False
            return True
        except Exception as e:
            LoggingManager.logging().exception("下载minion数据异常，objectKey:%s", objectKey)
            return False


def getRangeObject(objectKey, startByte, endByte, downloadPath):
    try:
        # 下载对象的附加头域
        headers = GetObjectHeader()
        # 获取对象时，获取在range范围内的对象内容。此处以对象的前1000个字节为例。
        headers.range = startByte + '-' + endByte
        obsClient = ObsClient(access_key_id=ak, secret_access_key=sk, server=endpoint)
        resp = obsClient.getObject(bucket_name, objectKey, downloadPath, headers=headers)
        # 返回码为2xx时，接口调用成功，否则接口调用失败
        if resp.status < 300:
            logging.info('Get Object Succeeded')
            return True
        else:
            logging.error('Get Object Failed, code: %s , message: %s', resp.errorCode, resp.message)
            return False
    except:
        logging.exception("Get Object Failed")
        return False


def getObjectMetadata(obj_key):
    if current_config.get('deploy_model') == current_config.get('MODEL_CLOUD'):
        obsClient = ObsClient(access_key_id=ak, secret_access_key=sk, server=endpoint)
        resp = obsClient.getObjectMetadata(bucket_name, obj_key)

        if resp.status < 300:
            return resp.body.contentLength
        else:
            logging.error('Get Object Metadata Failed, key: %s, status:%s, reason: %s', obj_key, resp.status, resp.reason)
            return None
    elif current_config.get('deploy_model') == current_config.get('MODEL_LOCAL'):
        try:
            minio_client = Minio(
                current_config.get('minio_endpoint'),  # MinIO服务器地址和端口
                access_key=current_config.get('minio_access_key'),  # 你的访问密钥
                secret_key=current_config.get('minio_secret_key'),  # 你的密钥
                secure=False  # 如果使用的是HTTP而不是HTTPS，设置为False
            )

            stat = minio_client.stat_object(current_config.get('minio_bucket_name'), obj_key)
        except Exception as e:
            logging.exception("获取minion meta数据异常，objectKey:%s", obj_key)

        return 0


# 插入数据并获取自增ID的函数
def insert_and_get_id(sql, data):
    connection = pymysql.connect(host=mysql_host,
                                 port=mysql_port,
                                 user=mysql_user,
                                 password=mysql_password,
                                 database=mysql_database)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, data)
            connection.commit()
            return cursor.lastrowid
    except pymysql.MySQLError as e:
        logging.exception("Error in database operation")
        connection.rollback()
        raise
    finally:
        connection.close()


def executemany_sql(sql, values_list):
    cursor = None
    db = None
    try:
        db = pymysql.connect(host=mysql_host,
                             port=mysql_port,
                             user=mysql_user,
                             password=mysql_password,
                             database=mysql_database)
        cursor = db.cursor()
        cursor.executemany(sql, values_list)
        db.commit()
    except Exception as e:
        logging.exception("批量执行sql异常，sql: %s,values_list:%s", sql, values_list)
        raise e

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()


def query_data_one(sql, args=None):
    cursor = None
    db = None
    try:
        db = pymysql.connect(host=mysql_host,
                             port=mysql_port,
                             user=mysql_user,
                             password=mysql_password,
                             database=mysql_database)
        cursor = db.cursor()
        cursor.execute(sql, args=args)
        data = cursor.fetchone()
        return data
    except Exception as e:
        logging.exception("查询数据异常，sql:%s", sql)
        raise e
    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()


def query_data_all(sql, args=None):
    cursor = None
    db = None
    try:
        db = pymysql.connect(host=mysql_host,
                             port=mysql_port,
                             user=mysql_user,
                             password=mysql_password,
                             database=mysql_database)
        cursor = db.cursor()
        cursor.execute(sql, args=args)
        data = cursor.fetchall()
        # 获取列名
        columns = [desc[0] for desc in cursor.description]
        # 将结果转换为字典的列表
        result = [dict(zip(columns, row)) for row in data]
        return result
    except Exception as e:
        logging.exception("查询数据异常，sql:%s", sql)
        raise e
    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()


def execute_sql(sql_statements, values_list):
    cursor = None
    db = None
    try:
        db = pymysql.connect(host=mysql_host,
                             port=mysql_port,
                             user=mysql_user,
                             password=mysql_password,
                             database=mysql_database)

        cursor = db.cursor()

        for sql, values in zip(sql_statements, values_list):
            cursor.execute(sql, values)

        db.commit()
    except Exception as e:
        logging.exception("更新数据库出现异常, sql:%s, val:%s", sql_statements, values_list)
        db.rollback()  # 如果出现异常，回滚事务
        raise e
    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()


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


def upload_to_obs_part(object_key, local_file_path):
    obsClient = ObsClient(access_key_id=ak, secret_access_key=sk, server=endpoint)
    try:
        # 对象的MIME类型
        contentType = 'text/plain'
        # 初始化分段上传任务
        resp = obsClient.initiateMultipartUpload(bucket_name, object_key, contentType=contentType)
        # 获取初始化上传任务的uploadId
        uploadId = resp.body["uploadId"]
        # 上传段大小
        partSize = 9 * 1024 * 1024
        # 段号
        partNum = 1
        # 指明object字段是否代表文件路径，默认为False、此处为True
        isFile = True
        # 本地要上传的对象文件
        filepath = local_file_path
        contentLength = os.path.getsize(filepath)
        # 源文件中某一分段的起始偏移大小。
        offset = 0
        etags = {}

        while offset < contentLength:
            partSize = min(partSize, (contentLength - offset))
            # 用于上传段
            resp1 = obsClient.uploadPart(bucket_name, object_key, partNum, uploadId, filepath, isFile, partSize, offset)
            if resp1.status < 300:
                logging.info('Upload Part %s Succeeded', partNum)
                etags[partNum] = resp1.body.etag
            else:
                logging.error('Upload Part %s Failed', partNum)
            offset = offset + partSize
            partNum = partNum + 1

        completes = []
        for i in range(1, partNum):
            completes.append(CompletePart(i, etags[i]))
        # 用于合并段
        completeMultipartUploadRequest = CompleteMultipartUploadRequest(parts=completes)
        resp = obsClient.completeMultipartUpload(bucket_name, object_key, uploadId, completeMultipartUploadRequest)
        # 返回码为2xx时，接口调用成功，否则接口调用失败
        if resp.status < 300:
            logging.info('Upload File Succeeded')
        else:
            logging.error('Upload File Failed,errorCode :%s, errorMessage:%s ', resp.errorCode, resp.errorMessage)
    except BaseException as e:
        logging.exception('multiPartsUpload Failed')


def upload_to_obs(object_key, local_file_path):
    if current_config.get('deploy_model') == current_config.get('MODEL_CLOUD'):
        obsClient = ObsClient(access_key_id=ak, secret_access_key=sk, server=endpoint)

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
        minio_client = Minio(
            current_config.get('minio_endpoint'),  # MinIO服务器地址和端口
            access_key=current_config.get('minio_access_key'),  # 你的访问密钥
            secret_key=current_config.get('minio_secret_key'),  # 你的密钥
            secure=False  # 如果使用的是HTTP而不是HTTPS，设置为False
        )
        minio_client.fput_object(current_config.get('minio_bucket_name'), object_key, local_file_path)


def download_folder_from_obs(remote_prefix, local_folder, filter_file_subfix_tuple=None, filter_dir_tuple=None):
    """
     下载文件夹：次方法会下载指定目录下的所有子、孙目录和文件：结构内容和云端1:1下载还原
     参数样例
     remote_prefix = "datacenter/jin-A00004/raw_20240613_200139"
     local_folder = r"d:/home/raw_20240613_200139"

     return: True 下载成功 False 下载失败

     调用方式
     download_folder("datacenter/jin-A00004/raw_20240613_200139", r"d:/home/raw_20240613_200139")
    """

    obsClient = ObsClient(access_key_id=ak, secret_access_key=sk, server=endpoint)

    failed_list = []
    local_path_list = []
    remote_prefix = remote_prefix if remote_prefix.endswith("/") else remote_prefix + "/"
    prefix_length = len(remote_prefix)
    object_list = obsClient.listObjects(bucket_name, prefix=remote_prefix, encoding_type="url")
    while True:
        for obs_object in object_list.body["contents"]:
            object_key = obs_object["key"]

            # 过滤目录：按目录名
            if filter_dir_tuple is not None and not filter_dir_tuple not in (object_key, ):
                continue

            # 过滤文件：按文件名
            if filter_file_subfix_tuple is not None and not object_key.endswith(filter_file_subfix_tuple):
                continue

            # 将 OBS 中的对象名转换为本地路径
            download_file_path = os.path.join(local_folder, object_key[prefix_length:].replace("/", os.sep))
            LoggingManager.logging().info("Start to download object [%s] to [%s]" % (object_key, download_file_path))
            try:
                obsClient.downloadFile(bucket_name, object_key, taskNum=10, downloadFile=download_file_path)
                local_path_list.append(download_file_path)
            except Exception as e:
                # 目录不下载，值记录文件下载
                if object_key.endswith("/") is False:
                    LoggingManager.logging().info("Failed to download %s" % object_key)
                    failed_list.append(object_key)

        # 如果 is_truncated 为 True 则说明全部列举完成，没有剩余
        if not object_list.body["is_truncated"]:
            break
        # 使用上次返回的 next_marker 作为下次列举的 marker
        object_list = obsClient.listObjects(bucket_name, prefix=remote_prefix,
                                            encoding_type="url", marker=object_list.body["next_marker"])
    for i in failed_list:
        LoggingManager.logging().info("Failed to download %s, please try again" % i)

    return len(failed_list) == 0, local_path_list


def download_files_by_extension(obs_prefix, local_path, extension=".parquet"):
    obs_body = data_utils.listObjects(obs_prefix)

    if obs_body is None:
        logging.error("下载文件失败：%s", obs_prefix)
        raise Exception("下载文件失败")

    objects = obs_body['contents']
    parquet_files = [obj['key'] for obj in objects if obj['key'].endswith(extension)]

    downloaded_files = []
    LoggingManager.logging().info(f"Start to download {extension} object")
    for obs_file in parquet_files:
        local_file = local_path + "/" + os.path.basename(obs_file)
        data_utils.get_object(obs_file, local_file)
        downloaded_files.append(local_file)
        LoggingManager.logging().info(f"download one {extension} object [%s] to [%s]" % (obs_file, local_file))

    return downloaded_files


def unzip_file(zip_path, extract_path=None):
    """
    解压ZIP文件

    :param zip_path: ZIP文件的路径
    :param extract_path: 解压到的目标文件夹路径，如果为None，则解压到ZIP文件所在目录
    """
    # 如果未指定解压路径，则默认为ZIP文件所在目录
    if extract_path is None:
        extract_path = os.path.dirname(zip_path)

        # 确保解压路径存在
    if not os.path.exists(extract_path):
        os.makedirs(extract_path)

        # 使用with语句打开ZIP文件，确保文件正确关闭
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # 解压ZIP文件到指定目录
        zip_ref.extractall(extract_path)

    logging.info(f"文件已从 {zip_path} 解压到 {extract_path}")


def to_int(value):
    """
    Convert a value to an integer if possible.

    Parameters:
    value (Any): The value to convert.

    Returns:
    int: The integer representation of the value.

    Raises:
    ValueError: If the value cannot be converted to an integer.
    """
    if isinstance(value, int):
        # If the value is already an integer, return it
        return value
    elif isinstance(value, np.integer):
        return int(value)
    elif isinstance(value, float):
        # If the value is a float, convert it to an integer (truncating)
        return int(value)
    elif isinstance(value, bool):
        # If the value is a boolean, convert it to an integer (True -> 1, False -> 0)
        return int(value)
    elif isinstance(value, str):
        # If the value is a string, try to convert it to an integer
        try:
            return int(value)
        except ValueError:
            # If the string cannot be converted to an integer, raise a ValueError
            raise ValueError(f"Cannot convert string '{value}' to integer")
    else:
        # If the value is of an unsupported type, raise a ValueError
        raise ValueError(f"Cannot convert type {type(value).__name__} to integer")


def to_float(value):
    """
    Convert a value to a floating-point number.

    Parameters:
    value (Any): The value to convert.

    Returns:
    float: The floating-point representation of the value.

    Raises:
    ValueError: If the value cannot be converted to a float.
    """
    if isinstance(value, (int, float)):
        return float(value)
    elif isinstance(value, (np.integer, np.floating)):
        return float(value)
    elif isinstance(value, bool):
        return float(value)  # True becomes 1.0, False becomes 0.0
    elif isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"Cannot convert string '{value}' to float")
    else:
        raise ValueError(f"Cannot convert type {type(value).__name__} to float")


def to_str(value):
    """
    Convert a value to a string.

    Parameters:
    value (Any): The value to convert.

    Returns:
    str: The string representation of the value.
    """
    try:
        # Attempt to convert the value to a string using the built-in str() function
        return str(value)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Cannot convert value of type {type(value).__name__} to string: {e}")


def get_logging(log_path):
    """
    获取日志记录器
    """
    # 检查目录是否存在，如果不存在则创建
    log_dir = os.path.dirname(log_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)  # 创建目录

    # 配置 a.py 的日志记录器
    logger = logging.getLogger('logger_operator')
    logger.setLevel(logging.INFO)  # 设置日志级别

    # 创建文件处理器，输出到 a.log
    file_handler_a = logging.FileHandler(log_path, mode='a', encoding='utf-8')
    file_handler_a.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s'))

    # 添加处理器到记录器
    logger.addHandler(file_handler_a)

    return logger


def close_logger_handler(cus_logger):
    """
    关闭日志记录器的文件句柄
    """
    for handler in cus_logger.handlers:
        if isinstance(handler, logging.FileHandler):
            # 确保先刷新缓冲区
            handler.flush()
            handler.close()
            cus_logger.removeHandler(handler)
    # 确保关闭所有日志资源
    logging.shutdown()  # 只需调用一次 logging.shutdown()


def generate_local_op_file(op_strs: str, local_path_prefix: Optional[str] = None):
    """
    将字符串转换为文件,并保持在本地
    """
    if local_path_prefix:
        logging.info(f"使用路径前缀：{local_path_prefix}")
    else:
        logging.info("未提供路径前缀，使用默认路径")
        local_path_prefix = current_config.get('containerPath')
    data = json.loads(op_strs)
    # 存储文件路径的列表
    file_paths = []

    for key, value in data.items():
        file_path = local_path_prefix + "src/" + key

        # 确保目录存在，如果不存在则创建
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # 保存 value 字符串到文件
        with open(file_path, "w", encoding='utf-8') as file:
            decoded_str = base64.b64decode(value).decode('utf-8')
            file.write(decoded_str)

        # 将文件路径加入列表
        file_paths.append(file_path)

    return file_paths

