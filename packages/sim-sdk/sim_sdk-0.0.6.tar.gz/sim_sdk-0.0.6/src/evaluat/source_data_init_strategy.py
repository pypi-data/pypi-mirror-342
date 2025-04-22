from evaluat.data_init_strategy import DatasetInitStrategy
from evaluat import db_util
from evaluat.const import SOURCE
import logging
import label_util

class SourceDatasetInitStrategy(DatasetInitStrategy):
    """
    A strategy for initializing a dataset with clean data.
    """

    def parser_dataset(self, source_id_list, dataset_type):
        # 原始源数
        self.dataset_list = db_util.get_source_data(source_id_list)
        if not self.dataset_list:
            raise Exception("原始数据不存在 source_id_list:{}".format(source_id_list))

        return self

    def get_dataset_label(self, dataset_id):
        # 原始源数
        return label_util.selectSourceDataLabelById(dataset_id)

    def init_task_dataset(self, task_id):
        super().init_task_dataset(task_id)
        logging.info("评价源据集")

        # 提取所有 id 并拼接成逗号分隔的字符串
        source_data_ids = ",".join(str(item["id"]) for item in self.dataset_list)
        source_data_list = db_util.get_source_data(source_data_ids)

        # 提取每个元素的 id 和 data_id，组成新字典列表

        id_to_data_id = {item["id"]: item["data_id"] for item in source_data_list}

        # 一次评价可以选择多个源数据集
        # 每个源数据和任务id对应一个任务数据集
        for source_data in self.dataset_list:
            task_dataset_args = [
                self.task_id,
                # TODO 不再维护tag字段，后续删除
                None,
                source_data["id"],
                source_data["id"],
                # split data id
                None,
                # Dataset name
                "raw_" + source_data["raw_time"].strftime("%Y%m%d_%H%M%S"),
                source_data["project_name"] + "/" + source_data["plate_no"] + "/" + "raw_"
                + source_data["raw_time"].strftime("%Y%m%d_%H%M%S") + "/",
                # 元数据时间段为整个数据时间段
                # start_time_stamp
                "0",
                # end_time_stamp
                "0",
                # start_frame_no
                0,
                # end_frame_no
                0,
                # 数据集类型
                SOURCE,
                # src_dataset_path
                source_data["project_name"] + "/" + source_data["plate_no"] + "/" + "raw_"
                + source_data["raw_time"].strftime("%Y%m%d_%H%M%S") + "/",
                # data_id
                id_to_data_id[source_data["id"]]
            ]

            task_dataset_list = [tuple(task_dataset_args)]
            db_util.save_evluate_task_dataset(task_dataset_list)
