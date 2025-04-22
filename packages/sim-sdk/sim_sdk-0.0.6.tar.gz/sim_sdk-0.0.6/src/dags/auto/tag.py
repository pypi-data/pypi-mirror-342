from dataclasses import dataclass
from typing import Optional, List


@dataclass
class AutopilotVersion:
    autopilot_function_version: str
    autopilot_hardware_version: str
    autopilot_software_version: str

    def __init__(self):
        self.autopilot_function_version = ""     # 字符串默认 ""
        self.autopilot_hardware_version = ""
        self.autopilot_software_version = ""


@dataclass
class BasicInfo:
    source_data_id: Optional[int]
    project_name: str
    plate_no: str
    collect_time: str
    soc_platform: str
    source: str
    ars_version: str
    data_id: str
    autopilot_version: AutopilotVersion

    def __init__(self):
        self.source_data_id = None       # 数值数据默认为 None
        self.project_name = ""           # 字符串默认为 ""
        self.plate_no = ""
        self.collect_time = ""
        self.soc_platform = ""
        self.source = ""
        self.ars_version = ""
        self.data_id = ""
        self.autopilot_version = AutopilotVersion()  # 嵌套对象自动创建


@dataclass
class PEGASUSLabelInfo:
    animal: str
    cyclist: str
    highway_type: str
    intersection_type: str
    lane_curvature: str
    lane_direction: str
    lane_isolation_status: str
    lane_line_status: str
    lane_slope: str
    light: str
    night: str
    number_of_lanes: str
    number_of_lanes_change: str
    ordinary_lane_line: str
    pedestrians: str
    road_status: str
    road_surface: str
    road_type: str
    small_targets: str
    special_shaped_vehicles: str
    special_events: str
    special_lane_line: str
    special_lighting: str
    special_obstacles: str
    special_right_of_way_vehicles: str
    target_behavior: str
    target_objects: str
    temporary_roadblocks: str
    traffic_signals: str
    traffic_signs: str
    traffic_status: str
    vehicle_behavior: str
    weather: List

    def __init__(self):
        # 所有字符串字段默认 ""
        self.animal = ""
        self.cyclist = ""
        self.highway_type = ""
        self.intersection_type = ""
        self.lane_curvature = ""
        self.lane_direction = ""
        self.lane_isolation_status = ""
        self.lane_line_status = ""
        self.lane_slope = ""
        self.light = ""
        self.night = ""
        self.number_of_lanes = ""
        self.number_of_lanes_change = ""
        self.ordinary_lane_line = ""
        self.pedestrians = ""
        self.road_status = ""
        self.road_surface = ""
        self.road_type = ""
        self.small_targets = ""
        self.special_shaped_vehicles = ""
        self.special_events = ""
        self.special_lane_line = ""
        self.special_lighting = ""
        self.special_obstacles = ""
        self.special_right_of_way_vehicles = ""
        self.target_behavior = ""
        self.target_objects = ""
        self.temporary_roadblocks = ""
        self.traffic_signals = ""
        self.traffic_signs = ""
        self.traffic_status = ""
        self.vehicle_behavior = ""
        self.weather = []


@dataclass
class CleanInfo:
    qualified: Optional[int]

    def __init__(self):
        self.qualified = 0


@dataclass
class DataInfo:
    PEGASUS_label_info: PEGASUSLabelInfo
    clean_info: CleanInfo

    def __init__(self):
        # 自动创建内部对象
        self.PEGASUS_label_info = PEGASUSLabelInfo()
        self.clean_info = CleanInfo()


@dataclass
class BusChannelQuality:
    channel: Optional[int]
    bus_channel_missing: bool
    bus_channel_parse_error: bool
    bus_channel_rolling_counter_error: bool
    bus_channel_rolling_counter_single: List[str]
    bus_channel_single_missing: bool
    bus_channel_missing_singles: str
    bus_channel_frame_loss_rate: Optional[float]
    bus_channel_time_deviation: Optional[float]
    bus_channel_time_error: bool
    bus_channel_parquet_path: str
    bus_channel_error_list: List[str]
    out_of_range_signals: List[str]

    def __init__(self):
        self.channel = None                     # 数值默认为 None
        self.bus_channel_missing = False          # 布尔值默认为 False
        self.bus_channel_parse_error = False
        self.bus_channel_rolling_counter_error = False
        self.bus_channel_rolling_counter_single = []  # 强制初始化列表
        self.bus_channel_single_missing = False
        self.bus_channel_missing_singles = ""
        self.bus_channel_frame_loss_rate = None
        self.bus_channel_time_deviation = None
        self.bus_channel_time_error = False
        self.bus_channel_parquet_path = ""
        self.bus_channel_error_list = []
        self.out_of_range_signals = []


@dataclass
class VideoChannelQuality:
    channel: Optional[int]
    video_missing: bool
    video_parse_error: bool
    video_frame_loss_rate: bool
    video_index_missing: bool
    video_index_parse_error: bool
    video_index_time_deviation: Optional[float]
    video_index_time_error: bool
    video_channel_error_list: List[str]

    def __init__(self):
        self.channel = None                     # 数值默认为 None
        self.video_missing = False              # 布尔值默认为 False
        self.video_parse_error = False
        self.video_frame_loss_rate = False
        self.video_index_missing = False
        self.video_index_parse_error = False
        self.video_index_time_deviation = None
        self.video_index_time_error = False
        self.video_channel_error_list = []


@dataclass
class MetaKeyDataMissing:
    weather: bool
    highway_type: bool
    lighting: bool
    location: bool
    basic_info: bool

    def __init__(self):
        self.weather = False
        self.highway_type = False
        self.lighting = False
        self.location = False
        self.basic_info = False


@dataclass
class MetaTagQuality:
    meta_tag_missing: bool
    meta_key_data_missing: MetaKeyDataMissing

    def __init__(self):
        self.meta_tag_missing = False           # 布尔值默认为 False
        self.meta_key_data_missing = MetaKeyDataMissing()


@dataclass
class DataQuality:
    bus_data_quality: List[BusChannelQuality]
    video_data_quality: List[VideoChannelQuality]
    meta_tag_quality: MetaTagQuality

    def __init__(self):
        # 强制初始化列表
        self.bus_data_quality = []
        self.video_data_quality = []
        self.meta_tag_quality = MetaTagQuality()


@dataclass
class Quality:
    data_quality: DataQuality

    def __init__(self):
        self.data_quality = DataQuality()


@dataclass
class DataRecord:
    basic_info: BasicInfo
    data_info: DataInfo
    quality: Quality

    def __init__(self):
        # 构造所有嵌套对象，确保每个字段都存在
        self.basic_info = BasicInfo()
        self.data_info = DataInfo()
        self.quality = Quality()

