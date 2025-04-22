import json
import math
import struct
import sys
import time
import zipfile
from io import BytesIO

import pandas as pd
import dpkt
import cv2
from foxglove_schemas_protobuf.Color_pb2 import Color
from foxglove_schemas_protobuf.CompressedImage_pb2 import CompressedImage
from foxglove_schemas_protobuf.CubePrimitive_pb2 import CubePrimitive
from foxglove_schemas_protobuf.TextPrimitive_pb2 import TextPrimitive
from foxglove_schemas_protobuf.LinePrimitive_pb2 import LinePrimitive
from foxglove_schemas_protobuf.PackedElementField_pb2 import PackedElementField
from foxglove_schemas_protobuf.Point3_pb2 import Point3
from foxglove_schemas_protobuf.PointCloud_pb2 import PointCloud
from foxglove_schemas_protobuf.Pose_pb2 import Pose
from foxglove_schemas_protobuf.Quaternion_pb2 import Quaternion
from foxglove_schemas_protobuf.SceneEntity_pb2 import SceneEntity
from foxglove_schemas_protobuf.SceneUpdate_pb2 import SceneUpdate
from foxglove_schemas_protobuf.Vector3_pb2 import Vector3
from google.protobuf.reflection import MakeClass
from mcap_protobuf.writer import Writer

from google.protobuf import timestamp_pb2, descriptor_pb2, descriptor_pool

from util import nacos_client

# 通过 get_config() 函数获取配置（懒加载）
current_config = nacos_client.get_config()

# 写视频数据
def writeVideo(fileDirectoryPath, videoPath, videoTimestapPath, Compression, topic):
    time1 = time.time()
    mcapPath = fileDirectoryPath + topic + '.mcap'
    with open(mcapPath, "wb") as f, Writer(f) as writer:
        videoTimeList = []
        with open(videoTimestapPath, 'r') as file:
            for line in file:
                line_number, float_value = line.strip().split(' ')
                seconds_number, nanos_number = float_value.strip().split('.')
                videoTimeList.append([float_value, seconds_number, nanos_number + '000'])

        cap = cv2.VideoCapture(videoPath)
        width = int(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) / Compression[0])
        height = int(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) / Compression[0])
        dim = (width, height)
        totalLength = len(videoTimeList)
        for i in range(totalLength):
            ret, frame = cap.read()
            # mp4已读完
            if not ret:
                break
            if i % Compression[1] != 0:
                continue
            small_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            temp_frame = list(cv2.imencode(".jpeg", small_frame)[1])
            message = CompressedImage(
                frame_id="base",
                timestamp=timestamp_pb2.Timestamp(seconds=int(videoTimeList[i][1]), nanos=int(videoTimeList[i][2])),
                data=bytes(temp_frame),
                format="jpeg"
            )
            writer.write_message(
                topic=topic,
                message=message,
                log_time=int(float(videoTimeList[i][0]) * 1e9),
                publish_time=int(float(videoTimeList[i][0]) * 1e9),
            )
    time2 = time.time()
    print(f"video:{topic}:{time2 - time1}")


# 写点云数据
def writePcap(fileDirectoryPath, pcapPath, pcapTimestapPath, datPath, Compression, topic):
    time1 = time.time()
    mcapPath = fileDirectoryPath + topic + '.mcap'
    with open(mcapPath, "wb") as f, Writer(f) as writer:
        fields = [
            PackedElementField(name="x", offset=0, type=PackedElementField.FLOAT32),
            PackedElementField(name="y", offset=4, type=PackedElementField.FLOAT32),
            PackedElementField(name="z", offset=8, type=PackedElementField.FLOAT32),
            PackedElementField(name="intensity", offset=12, type=PackedElementField.FLOAT32),
        ]
        pose = Pose(
            position=Vector3(x=0, y=0, z=0),
            orientation=Quaternion(w=1, x=0, y=0, z=0),
        )
        # 解析时间戳文件
        pcapTimeList = []
        with open(pcapTimestapPath, 'r') as file:
            for line in file:
                line_number, float_value = line.strip().split(' ')
                seconds_number, nanos_number = float_value.strip().split('.')
                pcapTimeList.append([float_value, seconds_number, nanos_number + '000'])

        # 解析角度矫正文件
        Start_Frame = [22.498203125, 142.747578125, 262.599375]
        Azimuth_Offset = [-2.4, 0.65, -2.4, 0.65, -2.4, 0.65, -2.4, 0.65, -2.4, 0.65, -2.4, 0.65, -2.4, 0.65,
                          -2.4, 0.65, 2.4, -0.65, 2.4, -0.65, 2.4, -0.65, 2.4, -0.65, 2.4, -0.65, 2.4, -0.65,
                          2.4, -0.65, 2.4, -0.65, -2.4, 0.65, -2.4, 0.65, -2.4, 0.65, -2.4, 0.65, -2.4, 0.65,
                          -2.4, 0.65, -2.4, 0.65, -2.4, 0.65, 2.4, -0.65, 2.4, -0.65, 2.4, -0.65, 2.4, -0.65,
                          2.4, -0.65, 2.4, -0.65, 2.4, -0.65, 2.4, -0.65, -2.4, 0.65, -2.4, 0.65, -2.4, 0.65,
                          -2.4, 0.65, -2.4, 0.65, -2.4, 0.65, -2.4, 0.65, -2.4, 0.65, 2.4, -0.65, 2.4, -0.65,
                          2.4, -0.65, 2.4, -0.65, 2.4, -0.65, 2.4, -0.65, 2.4, -0.65, 2.4, -0.65, -2.4, 0.65,
                          -2.4, 0.65, -2.4, 0.65, -2.4, 0.65, -2.4, 0.65, -2.4, 0.65, -2.4, 0.65, -2.4, 0.65,
                          2.4, -0.65, 2.4, -0.65, 2.4, -0.65, 2.4, -0.65, 2.4, -0.65, 2.4, -0.65, 2.4, -0.65,
                          2.4, -0.65]
        Elevation = [12.92828125, 12.72828125, 12.52828125, 12.328359375, 12.128359375, 11.9284375, 11.7284375,
                     11.5284375, 11.328515625, 11.128515625, 10.928515625, 10.72859375, 10.52859375,
                     10.32859375, 10.128671875, 9.928671875, 9.728671875, 9.52875, 9.32875, 9.12875,
                     8.928828125, 8.728828125, 8.52890625, 8.32890625, 8.12890625, 7.928984375, 7.728984375,
                     7.528984375, 7.3290625, 7.1290625, 6.9290625, 6.729140625, 6.529140625, 6.329140625,
                     6.12921875, 5.92921875, 5.72921875, 5.529296875, 5.329296875, 5.129375, 4.929375, 4.729375,
                     4.529453125, 4.329453125, 4.129453125, 3.92953125, 3.72953125, 3.52953125, 3.329609375,
                     3.129609375, 2.929609375, 2.7296875, 2.5296875, 2.3296875, 2.129765625, 1.929765625,
                     1.72984375, 1.52984375, 1.32984375, 1.129921875, 0.929921875, 0.729921875, 0.53, 0.33,
                     0.13, -0.069921875, -0.269921875, -0.469921875, -0.66984375, -0.86984375, -1.06984375,
                     -1.269765625, -1.469765625, -1.6696875, -1.8696875, -2.0696875, -2.269609375, -2.469609375,
                     -2.669609375, -2.86953125, -3.06953125, -3.26953125, -3.469453125, -3.669453125,
                     -3.869453125, -4.069375, -4.269375, -4.469375, -4.669296875, -4.869296875, -5.06921875,
                     -5.26921875, -5.46921875, -5.669140625, -5.869140625, -6.069140625, -6.2690625, -6.4690625,
                     -6.6690625, -6.868984375, -7.068984375, -7.268984375, -7.46890625, -7.66890625,
                     -7.86890625, -8.068828125, -8.268828125, -8.46875, -8.66875, -8.86875, -9.068671875,
                     -9.268671875, -9.468671875, -9.66859375, -9.86859375, -10.06859375, -10.268515625,
                     -10.468515625, -10.668515625, -10.8684375, -11.0684375, -11.2684375, -11.468359375,
                     -11.668359375, -11.86828125, -12.06828125, -12.26828125, -12.468203125]
        if datPath is not None and len(datPath) > 0:
            Start_Frame = []
            Azimuth_Offset = []
            Elevation = []
            with open(datPath, 'rb') as file:
                # 读取整个文件内容
                binary_content = file.read()
                Resolution = binary_content[15]
                for i in range(16, 28, 4):
                    a = int.from_bytes(binary_content[i:i + 4], byteorder='little') * 1.0 * Resolution / 25600
                    Start_Frame.append(a)
                for i in range(40, 552, 4):
                    a = int.from_bytes(binary_content[i:i + 4], byteorder='little')
                    is_negative = (a >> 31) & 1
                    if is_negative:
                        a = a - (1 << 32)
                    a = a * 1.0 * Resolution / 25600
                    Azimuth_Offset.append(a)
                for i in range(552, 1064, 4):
                    a = int.from_bytes(binary_content[i:i + 4], byteorder='little')
                    is_negative = (a >> 31) & 1
                    if is_negative:
                        a = a - (1 << 32)
                    a = a * 1.0 * Resolution / 25600
                    Elevation.append(a)

        # 解析pcap文件
        with open(pcapPath, 'rb') as f:
            pcap = dpkt.pcap.Reader(f)
            index = 0
            frame_index = 0
            h_angel_fuzzy_1_old = 0
            data = BytesIO()
            totalLength = len(pcapTimeList)
            for ts, buf in pcap:
                if index >= totalLength:
                    break
                if index % Compression[2] != 0:
                    index = index + 1
                    continue
                eth = dpkt.ethernet.Ethernet(buf)
                if not isinstance(eth.data, dpkt.ip.IP):
                    index = index + 1
                    continue
                ip = eth.data
                if not isinstance(ip.data, dpkt.udp.UDP):
                    index = index + 1
                    continue
                udp = ip.data
                # if udp.dport != 2368:
                #     index = index + 1
                #     continue
                point_cloud_data = udp.data
                if len(point_cloud_data) != 1118:
                    index = index + 1
                    continue

                # 获取pcap中所需字段
                body = point_cloud_data[12:1046]
                disUnit = point_cloud_data[9]  # 距离单位
                azimuth_1 = int.from_bytes(body[0:2], byteorder='little')  # 码盘角度的低分辨率部分
                fine_azimuth_1 = body[2]  # 码盘角度的高分辨率部分
                block_1 = body[3:515]  # 数据块1

                # 计算镜面修正后的水平角度 h_angel_fuzzy_1
                sorted_angles = sorted(Start_Frame)
                h_angel_fuzzy_1 = 1.0
                a = azimuth_1 * 1.0 / 100 + fine_azimuth_1 * 1.0 / 25600  # 水平角度
                if a >= sorted_angles[0] and a < sorted_angles[1]:
                    h_angel_fuzzy_1 = sorted_angles[0]
                elif a >= sorted_angles[1] and a < sorted_angles[2]:
                    h_angel_fuzzy_1 = sorted_angles[1]
                else:
                    h_angel_fuzzy_1 = sorted_angles[2]
                h_angel_fuzzy_1 = (a - h_angel_fuzzy_1) * 2

                # 如果水平角度为最小，新起一帧
                if h_angel_fuzzy_1_old - h_angel_fuzzy_1 > 120:
                    frame_index = frame_index + 1
                    if frame_index % Compression[3] == 0:
                        message = PointCloud(
                            frame_id="base",
                            pose=pose,
                            timestamp=timestamp_pb2.Timestamp(seconds=int(pcapTimeList[index - 1][1]),
                                                              nanos=int(pcapTimeList[index - 1][2])),
                            point_stride=16,
                            fields=fields,
                            data=data.getvalue(),
                        )
                        writer.write_message(
                            topic=topic,
                            message=message,
                            log_time=int(float(pcapTimeList[index - 1][0]) * 1e9),
                            publish_time=int(float(pcapTimeList[index - 1][0]) * 1e9),
                        )
                    data = BytesIO()
                h_angel_fuzzy_1_old = h_angel_fuzzy_1

                # 解析每个通道的测量数据
                for i in range(0, 128):
                    distance = int.from_bytes(block_1[i * 4:i * 4 + 2], byteorder='little') * disUnit * 0.001  # 距离
                    reflectivity = block_1[i * 4 + 2]  # 反射率
                    confidence = block_1[i * 4 + 3]  # 置信度

                    # 低置信度的点删除
                    if confidence == 1:
                        continue

                    h_angel = h_angel_fuzzy_1 - Azimuth_Offset[i]  # 水平角度
                    v_angel = Elevation[i]  # 垂直角度

                    point_x = distance * math.cos(math.radians(h_angel)) * math.cos(math.radians(v_angel))
                    point_y = distance * math.sin(math.radians(h_angel)) * math.cos(math.radians(v_angel))
                    point_z = distance * math.sin(math.radians(v_angel))

                    data.write(
                        struct.pack(
                            "<ffff",
                            float(point_x),
                            float(point_y),
                            float(point_z),
                            float(reflectivity),
                        )
                    )

                # 数据块2
                azimuth_2 = int.from_bytes(body[515:517], byteorder='little')  # 码盘角度的低分辨率部分
                fine_azimuth_2 = body[517]  # 码盘角度的高分辨率部分
                block_2 = body[518:1030]  # 数据块2

                # 计算镜面修正后的水平角度 h_angel_fuzzy_2
                h_angel_fuzzy_2 = 1.0
                b = azimuth_2 * 1.0 / 100 + fine_azimuth_2 * 1.0 / 25600  # 水平角度
                if b >= sorted_angles[0] and b < sorted_angles[1]:
                    h_angel_fuzzy_2 = sorted_angles[0]
                elif b >= sorted_angles[1] and b < sorted_angles[2]:
                    h_angel_fuzzy_2 = sorted_angles[1]
                else:
                    h_angel_fuzzy_2 = sorted_angles[2]
                h_angel_fuzzy_2 = (b - h_angel_fuzzy_2) * 2

                # 解析每个通道的测量数据 数据块2
                for i in range(0, 128):
                    distance = int.from_bytes(block_2[i * 4:i * 4 + 2], byteorder='little') * disUnit * 0.001  # 距离
                    reflectivity = block_2[i * 4 + 2]  # 反射率
                    confidence = block_2[i * 4 + 3]  # 置信度

                    # 低置信度的点删除
                    if confidence == 1:
                        continue

                    h_angel = h_angel_fuzzy_2 - Azimuth_Offset[i]  # 水平角度
                    v_angel = Elevation[i]  # 垂直角度

                    point_x = distance * math.cos(math.radians(h_angel)) * math.cos(math.radians(v_angel))
                    point_y = distance * math.sin(math.radians(h_angel)) * math.cos(math.radians(v_angel))
                    point_z = distance * math.sin(math.radians(v_angel))

                    data.write(
                        struct.pack(
                            "<ffff",
                            float(point_x),
                            float(point_y),
                            float(point_z),
                            float(reflectivity),
                        )
                    )
                index = index + 1
    time2 = time.time()
    print(f"pcap:{time2 - time1}")



# 写点云数据
def writePcd(fileDirectoryPath, topic, pcdName, path, start_frame, end_frame):
    time1 = time.time()
    start_frame = int(start_frame)
    end_frame = int(end_frame)
    mcapPath = fileDirectoryPath + topic + '.mcap'
    true_topic = topic.split("-")[0]
    # 解析时间戳文件
    pcdTimeList = {}
    with open(f"{path}/time_stamp.json", 'r') as f_tjson:
        data = json.load(f_tjson)
        sensor = data["sensor"]
        for key, value in sensor.items():
            for key2, value2 in value.items():
                pcdTimeList[str(int(key2))] = float(value2)
            break

    with open(mcapPath, "wb") as f, Writer(f) as writer:
        pose = Pose(
            position=Vector3(x=0, y=0, z=0),
            orientation=Quaternion(w=1, x=0, y=0, z=0),
        )
        fields = [
            PackedElementField(name="x", offset=0, type=PackedElementField.FLOAT32),
            PackedElementField(name="y", offset=4, type=PackedElementField.FLOAT32),
            PackedElementField(name="z", offset=8, type=PackedElementField.FLOAT32),
            PackedElementField(name="intensity", offset=12, type=PackedElementField.FLOAT32),
        ]
        with zipfile.ZipFile(f"{path}/pcd_{pcdName}.zip", 'r') as zip_ref:
            for i in range(start_frame, end_frame + 1):
                timestamp = pcdTimeList[str(i)]
                pcd_bytes = zip_ref.read(f"{str(i).zfill(6)}_{pcdName}.pcd")
                pcd_content = pcd_bytes.decode('utf-8')
                data = BytesIO()
                lines = pcd_content.strip().split('\n')
                for line in lines:
                    if line.strip():  # 忽略空行
                        parts = line.split()
                        if len(parts) == 4 and parts[0] != 'nan':
                            data.write(struct.pack("<ffff", float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3])))
                message = PointCloud(
                    frame_id="base",
                    pose=pose,
                    timestamp=timestamp_pb2.Timestamp(seconds=int(timestamp),
                                                      nanos=int(
                                                          (timestamp - int(timestamp)) * 1e9)),
                    point_stride=16,
                    fields=fields,
                    data=data.getvalue(),
                )
                writer.write_message(
                    topic=true_topic,
                    message=message,
                    log_time=int(timestamp * 1e9),
                    publish_time=int(timestamp * 1e9),
                )

    time2 = time.time()
    print(f"pcd:{topic}:{time2 - time1}")

# 写asc数据
def writeSimpleProtoMessage(fileDirectoryPath, parquetPath, topic, ascType):
    # protoc --python_out=. can_message.proto
    time1 = time.time()
    mcapPath = fileDirectoryPath + topic + '.mcap'

    with open(mcapPath, "wb") as f, Writer(f) as writer:
        df = pd.read_parquet(parquetPath)
        column_names_list = df.columns.tolist()

        descriptor_proto = descriptor_pb2.FileDescriptorProto()
        descriptor_proto.name = f'{ascType}.proto'
        message_descriptor = descriptor_proto.message_type.add()
        message_descriptor.name = ascType
        pool = descriptor_pool.Default()
        number = 1
        for column_name in column_names_list:
            field_descriptor = message_descriptor.field.add()
            field_descriptor.name = column_name.replace('.', '__')
            field_descriptor.json_name = column_name.replace('.', '__')
            field_descriptor.number = number
            field_descriptor.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING
            field_descriptor.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
            number = number + 1
        pool.Add(descriptor_proto)
        for index, row in df.iterrows():
            timestamp = index
            # 使用消息工厂从描述符池中创建消息类
            message_class = MakeClass(pool.FindMessageTypeByName(ascType))
            message = message_class()

            for column_name in column_names_list:
                setattr(message, column_name.replace('.', '__'), str(row[column_name]))

            writer.write_message(
                topic=f'{topic}',
                message=message,
                log_time=int(float(timestamp) * 1e9),
                publish_time=int(float(timestamp) * 1e9),
            )
    time2 = time.time()
    print(f"{ascType}:{topic}:{time2 - time1}")

#写fusion中的车道线与目标物
def writeFusion(fileDirectoryPath, fusionPath, topic):
    time1 = time.time()
    mcapPath = fileDirectoryPath + topic + '.mcap'
    SEN_LAN_NAME_LIST = ['Left', 'Right', 'Next_Left', 'Next_Right']
    SEN_OBJ_NAME_LIST = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                         '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']

    # 自车框(写死：翼三6*4牵引 长宽高7375×2550×3360)
    self_width = 2.55
    self_length = 7.375
    self_height = 3.36
    ego_front_offset = 6.65
    ego_pose_x = ego_front_offset - self_length / 2
    cube_primitive_self = CubePrimitive(
        pose=Pose(position=Vector3(x=ego_pose_x, y=0, z=self_height / 2),
                  orientation=Quaternion(w=0, x=1, y=0, z=0)),
        size=Vector3(x=self_length, y=self_width, z=self_height),
        color=Color(r=1, g=0.3, b=0.6, a=0.5)
    )
    cubes_self = []
    cubes_self.append(cube_primitive_self)
    scene_entity_obj_self = SceneEntity(
        frame_id="base",
        cubes=cubes_self
    )
    message_obj_self = SceneUpdate(
        entities=[scene_entity_obj_self]
    )

    with open(mcapPath, "wb") as f, Writer(f) as writer:
        df = pd.read_parquet(fusionPath)
        start_timestamp = df.index[0]
        # 车道线与目标物
        for index, row in df.iterrows():
            lines = []
            cubes = []
            texts = []
            # 时间戳
            timestamp = index
            # 车道线
            for line_name in SEN_LAN_NAME_LIST:
                # 车道线类型
                # 0=Unknown
                # 1=Solid 实线
                # 2=Road Edge 道路边缘
                # 3=Dashed 虚线
                # 4=Double Lane(Left Dashed, Right Solid) 双车道（左虚线，右实线）
                # 5=Double Lane(Left Solid, Right Dashed) 双车道（左实线，右虚线）
                # 6=Double Lane(Double Dashed) 双车道（双虚线）
                # 7=Double Lane(Double Solid) 双车道（双实心）
                # 8=Line Ramp(Solid) 线路斜坡（实线）
                # 9=Line Ramp(Dashed) 线路斜坡（虚线）
                # 10=ShadedArea 阴影区域
                # 11=DecelerationSolidLine 减速实线
                # 12=DecelerationDashedLine 减速线
                # 13=LaneVirtualMarking 车道路线标记
                # 15=Invalid 无效

                # 车道线颜色
                # 0=Unknown
                # 1=White
                # 2=Yellow_Orange_Red
                # 3=Blue_Green
                SEN_LAN_Type = row[f'SEN_LAN_{line_name}_A.SEN_LAN_{line_name}_Type']  # 车道线类型
                if SEN_LAN_Type is None:
                    continue
                SEN_LAN_Color = row[f'SEN_LAN_{line_name}_A.SEN_LAN_{line_name}_Color']  # 车道线颜色
                SEN_LAN_Crossing = row[f'SEN_LAN_{line_name}_A.SEN_LAN_{line_name}_Crossing']  # 跨越道线标志位
                SEN_LAN_RangeStart = row[f'SEN_LAN_{line_name}_A.SEN_LAN_{line_name}_RangeStart']  # 车道线检测起始距离
                SEN_LAN_RangeEnd = row[f'SEN_LAN_{line_name}_A.SEN_LAN_{line_name}_RangeEnd']  # 车道线检测终止距离
                SEN_LAN_C0 = row[f'SEN_LAN_{line_name}_B.SEN_LAN_{line_name}_C0']  # 车道线C0
                SEN_LAN_C1 = row[f'SEN_LAN_{line_name}_B.SEN_LAN_{line_name}_C1']  # 车道线C1
                SEN_LAN_C2 = row[f'SEN_LAN_{line_name}_B.SEN_LAN_{line_name}_C2']  # 车道线C2
                SEN_LAN_C3 = row[f'SEN_LAN_{line_name}_B.SEN_LAN_{line_name}_C3']  # 车道线C3

                if math.isnan(SEN_LAN_Type) or math.isnan(SEN_LAN_C0):
                    continue

                # 车道线颜色
                color = Color(r=1, g=1, b=1, a=1)
                if SEN_LAN_Color == 2:
                    color = Color(r=1, g=1, b=0, a=1)
                elif SEN_LAN_Color == 3:
                    color = Color(r=0, g=0, b=1, a=1)

                # 根据车道线类型,获得宽度，单双，实虚，间宽
                type_center = LinePrimitive.LINE_STRIP
                type_left = LinePrimitive.LINE_STRIP
                type_right = LinePrimitive.LINE_STRIP
                thickness = 0.15
                pitch = 0.2
                double_flag = 0
                if SEN_LAN_Type == 1:
                    type_center = LinePrimitive.LINE_STRIP
                    thickness = 0.15
                    double_flag = 0
                elif SEN_LAN_Type == 2:
                    type_center = LinePrimitive.LINE_STRIP
                    thickness = 0.1
                    double_flag = 0
                elif SEN_LAN_Type == 3:
                    type_center = LinePrimitive.LINE_LIST
                    thickness = 0.15
                    double_flag = 0
                elif SEN_LAN_Type == 4:
                    type_left = LinePrimitive.LINE_LIST
                    type_right = LinePrimitive.LINE_STRIP
                    thickness = 0.15
                    pitch = 0.2
                    double_flag = 1
                elif SEN_LAN_Type == 5:
                    type_left = LinePrimitive.LINE_STRIP
                    type_right = LinePrimitive.LINE_LIST
                    thickness = 0.15
                    pitch = 0.2
                    double_flag = 1
                elif SEN_LAN_Type == 6:
                    type_left = LinePrimitive.LINE_LIST
                    type_right = LinePrimitive.LINE_LIST
                    thickness = 0.15
                    pitch = 0.2
                    double_flag = 1
                elif SEN_LAN_Type == 7:
                    type_left = LinePrimitive.LINE_STRIP
                    type_right = LinePrimitive.LINE_STRIP
                    thickness = 0.15
                    pitch = 0.2
                    double_flag = 1

                if double_flag == 0:
                    points = []
                    for x in range(int(SEN_LAN_RangeStart), int(SEN_LAN_RangeEnd)):
                        y = SEN_LAN_C0 + SEN_LAN_C1 * x + SEN_LAN_C2 * x * x + SEN_LAN_C3 * x * x * x
                        point = Point3(x=x, y=y, z=0)
                        points.append(point)

                    line_primitive = LinePrimitive(
                        type=type_center,
                        thickness=thickness,
                        points=points,
                        color=color
                    )
                    lines.append(line_primitive)
                else:
                    points_left = []
                    points_right = []
                    for x in range(int(SEN_LAN_RangeStart), int(SEN_LAN_RangeEnd)):
                        y = SEN_LAN_C0 + SEN_LAN_C1 * x + SEN_LAN_C2 * x * x + SEN_LAN_C3 * x * x * x
                        point_left = Point3(x=x, y=y - (pitch + thickness) / 2, z=0)
                        point_right = Point3(x=x, y=y + (pitch + thickness) / 2, z=0)
                        points_left.append(point_left)
                        points_right.append(point_right)

                    line_primitive_left = LinePrimitive(
                        type=type_left,
                        pose=Pose(position=Vector3(x=0, y=0, z=0), orientation=Quaternion(w=1, x=0, y=0, z=0)),
                        thickness=thickness,
                        points=points_left,
                        color=color
                    )
                    line_primitive_right = LinePrimitive(
                        type=type_right,
                        pose=Pose(position=Vector3(x=0, y=0, z=0), orientation=Quaternion(w=1, x=0, y=0, z=0)),
                        thickness=thickness,
                        points=points_right,
                        color=color
                    )
                    lines.append(line_primitive_left)
                    lines.append(line_primitive_right)

            scene_entity_lines = SceneEntity(
                frame_id="base",
                lines=lines
            )
            message_lines = SceneUpdate(
                entities=[scene_entity_lines]
            )
            writer.write_message(
                topic=f'{topic}_LAN',
                message=message_lines,
                log_time=int(float(timestamp) * 1e9),
                publish_time=int(float(timestamp) * 1e9),
            )

            # 目标物
            for obj_name in SEN_OBJ_NAME_LIST:
                # CAMERA对于车辆类型的分类
                # 0=Unknown
                # 1=Bus
                # 2=Small_Medium_Car
                # 3=Trucks
                # 4=Motors(Tri-cycle)
                # 5=Special_vehicle
                # 6=Tiny_car
                # 7=Lorry

                SEN_Obj_Distance_X = row[f'SEN_Obj_{obj_name}_A.SEN_Obj_{obj_name}_Distance_X']  # 融合目标的纵向距离
                if SEN_Obj_Distance_X is None:
                    continue
                SEN_Obj_Distance_Y = row[f'SEN_Obj_{obj_name}_A.SEN_Obj_{obj_name}_Distance_Y']  # 融合目标的横向距离
                SEN_Obj_BoxSize_X = row[f'SEN_Obj_{obj_name}_B.SEN_Obj_{obj_name}_BoxSize_X']  # 融合目标的长度
                SEN_Obj_BoxSize_Y = row[f'SEN_Obj_{obj_name}_B.SEN_Obj_{obj_name}_BoxSize_Y']  # 融合目标的宽度
                SEN_Obj_BoxAngle = row[f'SEN_Obj_{obj_name}_B.SEN_Obj_{obj_name}_BoxAngle']  # 融合目标的航向角
                SEN_Obj_Veh_Subtype_C = row[f'SEN_Obj_{obj_name}_C.SEN_Obj_{obj_name}_Veh_Subtype_C']  # CAMERA对于车辆类型的分类
                SEN_Obj_Velocity_X = row[f'SEN_Obj_{obj_name}_A.SEN_Obj_{obj_name}_Velocity_X']  # 融合目标的纵向相对速度 m/s
                SEN_Obj_Velocity_Y = row[f'SEN_Obj_{obj_name}_A.SEN_Obj_{obj_name}_Velocity_Y']  # 融合目标的横向相对速度 m/s
                SEN_Obj_Acceleration_X = row[f'SEN_Obj_{obj_name}_A.SEN_Obj_{obj_name}_Acceleration_X']  # 融合目标的纵向绝对加速度 m/s^2
                SEN_Obj_CIPV_Flag_C = row[f'SEN_Obj_{obj_name}_C.SEN_Obj_{obj_name}_CIPV_Flag_C']  # 是否是CIPV
                SEN_Obj_Cutin_Flag_C = row[f'SEN_Obj_{obj_name}_C.SEN_Obj_{obj_name}_Cutin_Flag_C']  # 是否是cutin
                SEN_Obj_ID_Camera = row[f'SEN_Obj_{obj_name}_C.SEN_Obj_{obj_name}_ID_Camera']  # CameraId
                SEN_Obj_ID_Radar = row[f'SEN_Obj_{obj_name}_C.SEN_Obj_{obj_name}_ID_Radar']  # RadarId
                SEN_Obj_ID = obj_name  # ID

                if math.isnan(SEN_Obj_Distance_X) or math.isnan(SEN_Obj_BoxSize_X) or math.isnan(SEN_Obj_Veh_Subtype_C):
                    continue

                pose_x = SEN_Obj_Distance_X
                pose_y = SEN_Obj_Distance_Y
                size_x = SEN_Obj_BoxSize_X
                size_y = SEN_Obj_BoxSize_Y
                orientation_w, orientation_x, orientation_y, orientation_z = euler_to_quaternion(SEN_Obj_BoxAngle, 0, 0)

                # 高度 颜色
                size_z = 1.8
                color = Color(r=1, g=1, b=1, a=0.5)
                if SEN_Obj_Veh_Subtype_C == 1:
                    size_z = 3.5
                    color = Color(r=1, g=0, b=0, a=0.5)
                elif SEN_Obj_Veh_Subtype_C == 2:
                    size_z = 1.5
                    color = Color(r=0, g=1, b=1, a=0.5)
                elif SEN_Obj_Veh_Subtype_C == 3:
                    size_z = 4.5
                    color = Color(r=1, g=0, b=0, a=0.5)
                elif SEN_Obj_Veh_Subtype_C == 4:
                    size_z = 1.8
                    color = Color(r=0, g=0, b=1, a=0.5)
                elif SEN_Obj_Veh_Subtype_C == 5:
                    size_z = 4.0
                    color = Color(r=1, g=0, b=0, a=0.5)
                elif SEN_Obj_Veh_Subtype_C == 6:
                    size_z = 1.5
                    color = Color(r=0, g=1, b=1, a=0.5)
                elif SEN_Obj_Veh_Subtype_C == 7:
                    size_z = 4.5
                    color = Color(r=1, g=0, b=0, a=0.5)

                # 车辆框数据
                cube_primitive = CubePrimitive(
                    pose=Pose(position=Vector3(x=pose_x, y=pose_y, z=size_z / 2),
                              orientation=Quaternion(w=orientation_w, x=orientation_x, y=orientation_y,
                                                     z=orientation_z)),
                    size=Vector3(x=size_x, y=size_y, z=size_z),
                    color=color
                )
                cubes.append(cube_primitive)

                # 车辆文字数据
                test_str = (f"ID={SEN_Obj_ID}/{int(SEN_Obj_ID_Camera)}/{int(SEN_Obj_ID_Radar)}\n"
                            f"Velocity={round(float(SEN_Obj_Velocity_X), 2)}/{round(float(SEN_Obj_Velocity_Y), 2)}\n"
                            f"Acceleration_X={round(float(SEN_Obj_Acceleration_X), 2)}\n"
                            f"CIPV_Flag={int(SEN_Obj_CIPV_Flag_C)}\n"
                            f"Cutin_Flag={int(SEN_Obj_Cutin_Flag_C)}")
                text_primitive = TextPrimitive(
                    pose=Pose(position=Vector3(x=pose_x, y=pose_y, z=size_z),
                              orientation=Quaternion(w=orientation_w, x=orientation_x, y=orientation_y,
                                                     z=orientation_z)),
                    billboard=True,
                    font_size=12,
                    scale_invariant=True,
                    color=color,
                    text=test_str
                )
                texts.append(text_primitive)

            # mcap 写车辆框与车辆文字数据
            scene_entity_obj = SceneEntity(
                frame_id="base",
                cubes=cubes
            )
            message_obj = SceneUpdate(
                entities=[scene_entity_obj]
            )
            writer.write_message(
                topic=f'{topic}_OBJ',
                message=message_obj,
                log_time=int(float(timestamp) * 1e9),
                publish_time=int(float(timestamp) * 1e9),
            )

            scene_entity_text = SceneEntity(
                frame_id="base",
                texts=texts
            )
            message_text = SceneUpdate(
                entities=[scene_entity_text]
            )
            writer.write_message(
                topic=f'{topic}_OBJ_TEXT',
                message=message_text,
                log_time=int(float(timestamp) * 1e9),
                publish_time=int(float(timestamp) * 1e9),
            )

            # mcap 写自车框
            writer.write_message(
                topic=f'EGO_OBJ',
                message=message_obj_self,
                log_time=int(float(timestamp) * 1e9),
                publish_time=int(float(timestamp) * 1e9),
            )

    time2 = time.time()
    print(f"CANFD:{topic}:{time2 - time1}")

# 角度转四元数
def euler_to_quaternion(yaw, pitch, roll):
    yaw = math.radians(yaw)
    pitch = math.radians(pitch)
    roll = math.radians(roll)
    # 将角度从弧度转换为正弦和余弦值
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)

    # 使用ZYX欧拉角顺序
    w = cy * cp * cr + sy * sp * sr
    x = cy * cp * sr - sy * sp * cr
    y = cy * sp * cr + sy * cp * sr
    z = sy * cp * cr - cy * sp * sr

    return w, x, y, z

if __name__ == "__main__":
    arg_type = sys.argv[1]
    fileDirectoryPath = sys.argv[2]
    topic = sys.argv[3]
    if arg_type == "1":
        writeVideo(fileDirectoryPath, sys.argv[4], sys.argv[5], [int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8]), int(sys.argv[9])], topic)
    # elif arg_type == "2":
    #     writePcap(fileDirectoryPath, sys.argv[4], sys.argv[5], sys.argv[6], [int(sys.argv[7]), int(sys.argv[8]), int(sys.argv[9]), int(sys.argv[10])], topic)
    elif arg_type == "3":
        writeSimpleProtoMessage(fileDirectoryPath, sys.argv[4], topic, sys.argv[5])
    elif arg_type == "4":
        writeFusion(fileDirectoryPath, sys.argv[4], topic)
    elif arg_type == "5":
        writePcd(fileDirectoryPath, topic, sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])