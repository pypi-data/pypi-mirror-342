import datetime
import json
import os
import shutil
import subprocess
import sys
import time

import pymysql
import redis
from mcap.reader import make_reader

from mcap_protobuf.writer import Writer
from mcap_protobuf.decoder import DecoderFactory
import obsUtil
import warnings
from data_deal_util import set_str_cache
from util import nacos_client


# 通过 get_config() 函数获取配置（懒加载）
current_config = nacos_client.get_config()


def create_mcap(directory_path_list):
    print(f"[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H_%M_%S.%f')}] Creating mcap: {directory_path_list}")
    Compression = getCompression("playback.normalCompression")

    completed_iterations = 0

    for fileDirectoryPath in directory_path_list:
        # 判断是否存在mcap包
        files = obsUtil.getListOfFiles(fileDirectoryPath)
        mcapFile = ""
        for file in files.get("files"):
            if file.endswith("mcap.mcap"):
                mcapFile = file
        if mcapFile != "":
            # 存在mcap包
            print(f"[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H_%M_%S.%f')}] existMcap: {fileDirectoryPath}")
        else:
            # 不存在mcap包
            print(f"[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H_%M_%S.%f')}] makeMcap: {fileDirectoryPath}")
            makeMcap(fileDirectoryPath, Compression, -1, -1)

        completed_iterations += 1


# 搜索原始文件
def findSourceFiles(fileDirectoryPath, start_frame, end_frame):
    try:
        # 数据集类型：1，原始 2，切片
        dataset_type = 1
        source_path = fileDirectoryPath
        file_directory_path_arr = fileDirectoryPath.split("/")
        if len(file_directory_path_arr) > 4:
            dataset_type = 2
            source_path = f"{file_directory_path_arr[1]}/{file_directory_path_arr[2]}/{file_directory_path_arr[3]}/"
        print(f"---fileDirectoryPath:{fileDirectoryPath}")
        print(f"----len(file_directory_path_arr):{len(file_directory_path_arr)}")
        print(f"---dataset_type:{dataset_type}")

        # 搜索视频文件
        videoPaths = []
        cameraFiles = obsUtil.getListOfFiles(fileDirectoryPath + "camera/")
        for cameraFile in cameraFiles.get("files"):
            if cameraFile.endswith(".mp4") or cameraFile.endswith(".avi"):
                for cameraTimestampFile in cameraFiles.get("files"):
                    if cameraTimestampFile == cameraFile.replace(".mp4", ".timestamp").replace(".avi", ".timestamp"):
                        videoPaths.append([cameraFile, cameraTimestampFile])
                        break

        # 搜索can文件
        canPaths = []
        canFiles = obsUtil.getListOfFiles(fileDirectoryPath + "canbus/")
        for canFile in canFiles.get("files"):
            if canFile.endswith(".parquet"):
                canPaths.append(canFile)

        # 搜索点云文件
        pcdInfo = None
        # 1.搜索原始数据文件夹是否存在unify_dataset
        exist_unify_dataset = False
        sourceFiles = obsUtil.getListOfFiles(source_path + "unify_dataset/")
        for sourceFile in sourceFiles.get("files"):
            if sourceFile.endswith("unify_info.json"):
                exist_unify_dataset = True
                break
        print(f"---source_path:{source_path}")
        print(f"---exist_unify_dataset:{exist_unify_dataset}")
        # 2.获取点云信息
        if exist_unify_dataset:
            pcdNames = []
            unify_info_path = source_path + "unify_dataset/unify_info.json"
            unify_info_download = obsUtil.download(unify_info_path, unify_info_path)
            with open(unify_info_path, 'r') as f_json:
                data = json.load(f_json)
                # 原始数据集获取起始结束帧号
                if dataset_type == 1:
                    start_frame = data["start_frame"]
                    end_frame = data["stop_frame"]
                # 获取雷达名称
                point_cloud = data["point_cloud"]
                for key, value in point_cloud.items():
                    if value:
                        pcdNames.append(key)
            print(f"---unify_info_path:{unify_info_path}")
            print(f"---start_frame:{start_frame}")
            if start_frame != -1:
                pcdInfo = {
                    "start_frame": start_frame,
                    "end_frame": end_frame,
                    "path": source_path + "unify_dataset",
                    "pcdNames": pcdNames
                    }

        # 搜索标定文件
        # calibrationResultFiles = obsUtil.getListOfFiles(source_path + "calibration_result/")

        # 不存在可以回放的文件
        if len(canPaths) == 0 and len(videoPaths) == 0 and pcdInfo == None:
            raise Exception("不存在可以回放的文件")
        return {
            "result": "success",
            "videoPaths": videoPaths,
            "canPaths": canPaths,
            "pcdInfo": pcdInfo
        }
    except Exception as e:
        print(str(e))
        return {
            "result": "error",
            "message": str(e)
        }

# 下载原始文件
def downloadSourceFiles(sourceFiles):
    # 待下载数据
    downloadFiles = []

    for videoPath in sourceFiles.get("videoPaths"):
        downloadFiles.append(videoPath[0])
        downloadFiles.append(videoPath[1])

    for canPath in sourceFiles.get("canPaths"):
        downloadFiles.append(canPath)

    if sourceFiles.get("pcdInfo") != None:
        pcd_path = sourceFiles.get("pcdInfo").get("path")
        downloadFiles.append(pcd_path + "/time_stamp.json")
        for pcd_name in sourceFiles.get("pcdInfo").get("pcdNames"):
            downloadFiles.append(pcd_path + "/pcd_" + pcd_name + ".zip")

    # 下载数据
    for downloadFile in downloadFiles:
        result = obsUtil.download(downloadFile, downloadFile)
        if result.get("result") != "success":
            return False
    return True


# 制作原始数据mcap包
def makeMcap(fileDirectoryPath, Compression, start_frame, end_frame):
    try:
        r = redis.Redis(host=current_config.get('redis_host'), port=current_config.get('redis_port'), db=current_config.get('redis_db'), password=current_config.get('redis_password'))
        r.set(f'makeMcapProgress:{fileDirectoryPath}', 0)
        r.persist(f'makeMcapProgress:{fileDirectoryPath}')
        # 下载所有文件
        print(f"[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H_%M_%S.%f')}] findSourceFiles: {fileDirectoryPath} {start_frame} {end_frame}")
        sourceFiles = findSourceFiles(fileDirectoryPath, start_frame, end_frame)
        if sourceFiles.get("result") != "success":
            r.set(f'makeMcapError:{fileDirectoryPath}', '文件搜索失败，文件不存在或不完整')
            r.delete(f'makeMcapProgress:{fileDirectoryPath}')
            return
        r.set(f'makeMcapProgress:{fileDirectoryPath}', 10)

        print(f"[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H_%M_%S.%f')}] downloadSourceFiles: {sourceFiles}")
        if downloadSourceFiles(sourceFiles) == False:
            shutil.rmtree(fileDirectoryPath)
            r.set(f'makeMcapError:{fileDirectoryPath}', '文件下载失败')
            r.delete(f'makeMcapProgress:{fileDirectoryPath}')
            return
        r.set(f'makeMcapProgress:{fileDirectoryPath}', 30)

        print(f"[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H_%M_%S.%f')}] makeSubMcapStart")
        time1 = time.time()
        mcapPath = fileDirectoryPath + "mcap.mcap"
        argsArr = []
        processArr = []

        videoPaths = sourceFiles.get("videoPaths")
        for i in range(len(videoPaths)):
            argsArr.append(["1", fileDirectoryPath, f"/video_{i + 1}", videoPaths[i][0], videoPaths[i][1], str(Compression[0]), str(Compression[1]), str(Compression[2]), str(Compression[3])])

        pcdInfo = sourceFiles.get("pcdInfo")
        if pcdInfo != None:
            for i in range(len(pcdInfo.get("pcdNames"))):
                # 获取文件的大小（单位为字节）
                file_size = os.stat(f"{pcdInfo.get('path')}/pcd_{pcdInfo.get('pcdNames')[i]}.zip").st_size
                # 大于1G的数据，分包制作子mcap包
                if file_size > 1024 * 1024 * 1024:
                    split_mcap_count = 5
                    pcdInfo_start_frame = int(pcdInfo.get("start_frame"))
                    pcdInfo_end_frame = int(pcdInfo.get("end_frame"))
                    avg_frame = int((pcdInfo_end_frame - pcdInfo_start_frame) // split_mcap_count)
                    for j in range(split_mcap_count):
                        sf = pcdInfo_start_frame + j * avg_frame
                        ef = sf + avg_frame - 1
                        if j == split_mcap_count - 1:
                            ef = pcdInfo_end_frame
                        argsArr.append(["5", fileDirectoryPath, f"/point_cloud_{i + 1}-{j + 1}", pcdInfo.get("pcdNames")[i],
                                        pcdInfo.get("path"), str(sf), str(ef)])
                else:
                    # 不大于1G的数据，直接制作子mcap包
                    argsArr.append(["5", fileDirectoryPath, f"/point_cloud_{i + 1}", pcdInfo.get("pcdNames")[i], pcdInfo.get("path"), str(pcdInfo.get("start_frame")), str(pcdInfo.get("end_frame"))])

        canPaths = sourceFiles.get("canPaths")
        cans_index = {}
        fusion_index = 1
        for i in range(len(canPaths)):
            asc_type = canPaths[i].split("/")[-1].split("_")[0]
            if asc_type in cans_index.keys():
                can_index = cans_index[asc_type]
                argsArr.append(["3", fileDirectoryPath, f"/{asc_type}_{can_index}", canPaths[i], asc_type])
                cans_index[asc_type] = can_index + 1
                break
            else:
                cans_index[asc_type] = 2
                argsArr.append(["3", fileDirectoryPath, f"/{asc_type}_1", canPaths[i], asc_type])
            if canPaths[i].split("/")[-1].startswith('Fusion') or canPaths[i].split("/")[-1].startswith('FD2'):
                argsArr.append(["4", fileDirectoryPath, f"/CANFD_{fusion_index}", canPaths[i]])
                fusion_index = fusion_index + 1

        # 多进程生成各个通道的mcap文件
        for args in argsArr:
            process = subprocess.Popen([sys.executable, 'writeMessage.py'] + args)
            processArr.append(process)
        for process in processArr:
            process.wait()

        print(f"[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H_%M_%S.%f')}] makeSubMcapEnd")

        # 将各个通道的mcap文件信息写在一起
        warnings.filterwarnings("ignore")
        r.set(f'makeMcapProgress:{fileDirectoryPath}', 80)
        with open(mcapPath, "wb") as f, Writer(f) as writer:
            for args in argsArr:
                sub_mcap_path = args[1] + args[2] + '.mcap'
                with open(sub_mcap_path, "rb") as f2:
                    reader = make_reader(f2, decoder_factories=[DecoderFactory()])
                    for schema, channel, message, proto_msg in reader.iter_decoded_messages():
                        writer.write_message(
                            topic=channel.topic,
                            log_time=message.log_time,
                            message=proto_msg,
                            publish_time=message.log_time,
                        )

        time2 = time.time()
        print(f"Time: {time2 - time1}")
        print(f"[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H_%M_%S.%f')}] makeMcapEnd")

        # 制作mcap配置文件
        mcapConfigFile = mcapPath.replace('.mcap', '_config.json')
        ## 写入json文件
        json_config = {
            'Compression': Compression
        }
        with open(mcapConfigFile, "w") as f:
            json.dump(json_config, f)

        print("mcap制作完成，正在上传至OBS")
        mcapUpload = obsUtil.upload(mcapPath, mcapPath)
        configUpload = obsUtil.upload(mcapConfigFile, mcapConfigFile)
        if mcapUpload.get("result") == "success" and configUpload.get("result") == "success":
            r.delete(f'makeMcapProgress:{fileDirectoryPath}')
            updatePlaybackFlag(fileDirectoryPath)
            print(f"[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H_%M_%S.%f')}] mcapUploadEnd")
        else:
            r.set(f'makeMcapError:{fileDirectoryPath}', 'mcap上传失败')
            r.delete(f'makeMcapProgress:{fileDirectoryPath}')
        shutil.rmtree(fileDirectoryPath)
    except BaseException as e:
        r = redis.Redis(host=current_config.get('redis_host'), port=current_config.get('redis_port'),
                        db=current_config.get('redis_db'), password=current_config.get('redis_password'))
        r.set(f'makeMcapError:{fileDirectoryPath}', str(e))
        r.delete(f'makeMcapProgress:{fileDirectoryPath}')


def getCompression(config_key):
    conn = pymysql.connect(host=current_config.get('mysql_host'), port=current_config.get('mysql_port'),
                           user=current_config.get('mysql_user'),
                           passwd=current_config.get('mysql_password'), db=current_config.get('mysql_database'),
                           charset="utf8")
    cursor = conn.cursor()
    cursor.execute(
        "select config_value from sys_config where config_key = '{}'".format(config_key))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    arr = str(data[0]).split(",")
    return [int(arr[0]), int(arr[1]), int(arr[2]), int(arr[3])]


# 更新回放状态为已回放
def updatePlaybackFlag(fileDirectoryPath):
    arr = fileDirectoryPath.split("/")
    # 原始数据
    if len(arr) == 4:
        project_name = arr[0]
        plate_no = arr[1]
        date_time_str = arr[2][4:]
        year = date_time_str[:4]
        month = date_time_str[4:6]
        day = date_time_str[6:8]
        hour = date_time_str[9:11]
        minute = date_time_str[11:13]
        second = date_time_str[13:15]
        raw_time = f"{year}-{month}-{day} {hour}:{minute}:{second}"
        # 查询是否有需要更新的数据
        conn = pymysql.connect(host=current_config.get('mysql_host'), port=current_config.get('mysql_port'),
                               user=current_config.get('mysql_user'),
                               passwd=current_config.get('mysql_password'), db=current_config.get('mysql_database'),
                               charset="utf8")
        cursor = conn.cursor()
        cursor.execute(
            "select id from datacenter_source_data WHERE playback_flag=0 and project_name='{}' and plate_no='{}' and raw_time='{}'".format(project_name, plate_no, raw_time))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        # 更新状态
        if len(data) > 0:
            conn = pymysql.connect(host=current_config.get('mysql_host'), port=current_config.get('mysql_port'),
                                   user=current_config.get('mysql_user'),
                                   passwd=current_config.get('mysql_password'), db=current_config.get('mysql_database'),
                                   charset="utf8")
            cursor = conn.cursor()
            cursor.execute("UPDATE datacenter_source_data SET playback_flag=1 WHERE project_name=%s and plate_no=%s and raw_time=%s",
                           (project_name, plate_no, raw_time))
            conn.commit()
            cursor.close()
            conn.close()


if __name__ == "__main__":
    fun_type = sys.argv[1]
    if fun_type == "makeMcap":
        makeMcap(sys.argv[2], [int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])], sys.argv[7], sys.argv[8])