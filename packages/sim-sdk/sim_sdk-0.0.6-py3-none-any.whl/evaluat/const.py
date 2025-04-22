progress_percent = {
    '-1': '-1',
    '1': '20',
    '2': '25',
    '3': '30',
    '4': '15',
    '5': '10'
}

progress_title = {
    '-1': '任务失败',
    '1': '任务容器启动',
    '2': '完成回灌数据下载',
    '3': '完成数据回灌',
    '4': '完成结果上传',
    '5': '完成回灌'
}

# 感知回灌每一帧输出文件名前缀
RESULT_FILE_NAME = "icc_result"

SOURCE = 2  # "原始数据集"
SPLIT = 11  # "切片数据集"
CLEAN = 6  # "清洗"
LOGSIM = 7  # "回灌结果数据集"
SCENE = 10  # 场景数据"

SOURCE_TYPE_SOURCE = 1   # "源数据"
SOURCE_TYPE_DATASET = 2  # "数据集"
SOURCE_TYPE_LOGSIM = 16  # "回灌结果数据集"

PERCEPTION = "1"  # "感知"
PNC = "2"  # PNC"
PERCP_PNC = "3"  # "感知+PNC"

# 状态
# 执行中
EXECUTE = 1
# 执行成功
SUCCESS = 2
# 执行失败
FAILED = 3
# 取消
CANCEL = 4
# 异常
ERROR = 5

STR_PASS = "pass"
STR_FAIL = "fail"
STR_ERROR = "error"

# 3小时：单位秒
EXPIRE_24_HOUR = 60 * 60 * 24
EXPIRE_1_HOUR = 60 * 60
PROGRESS_KEY = 'progress:task:eval:'

