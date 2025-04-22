from evaluat.data_init_strategy import DatasetInitStrategy
from evaluat import db_util
from evaluat.const import SCENE
import logging
import label_util
from data_deal_util import convert_to_unix_timestamp


class SenceDatasetInitStrategy(DatasetInitStrategy):
    """
    A strategy for initializing a dataset with dig data.
    """

    def parser_dataset(self, source_id_list, dataset_type):
        # 场景数据
        self.dataset_list = db_util.get_dig_data(source_id_list)
        if not self.dataset_list:
            raise Exception("场景数据不存在 source_id_list:{}".format(source_id_list))

        # # 获取到切片对应元数据
        # source_data_list = db_util.get_source_data(dataset_list[0]["source_data_id"])
        #
        # if not source_data_list:
        #     raise Exception("切片数据集对应的源数据不存在 source_id:{}".format(dataset_list[0]["source_data_id"]))
        # # 获取到车辆信息
        # vehicle = db_util.get_vehicle(source_data_list[0]['plate_no'])[0]
        return self

    def get_dataset_label(self, dataset_id):
        return label_util.selectSceneDataLabelById(dataset_id)

    def init_task_dataset(self, task_id):
        super().init_task_dataset(task_id)
        logging.info("评价场景据集")

        # 提取所有 id 并拼接成逗号分隔的字符串
        dig_data_ids = ",".join(str(item["id"]) for item in self.dataset_list)
        dig_data_list = db_util.get_dig_data(dig_data_ids)

        # 提取每个元素的 id 和 data_id，组成新字典列表
        # 构建字典：{id: data_id}
        id_to_data_id = {item["id"]: item["data_id"] for item in dig_data_list}

        # 一次评价可以选择多个场景数据集
        for dataset in self.dataset_list:
            # source_id = dataset["source_data_id"]
            # 场景的数据集对应的原始数据集
            # source_data = db_util.get_source_data(str(source_id))[0]

            task_dataset_args = [
                self.task_id,
                # TODO 不再维护tag字段，后续删除
                None,
                dataset["id"], # 数据类型数据主表id 比如dig表切片表算数据表
                dataset["source_data_ids"],
                # split data id
                None,
                # Dataset name
                # 不在维护dataset_name字段
                # dataset["task_name"],
                None,
                # 不再维护dataset_path字段
                # source_data["project_name"] + "/" + source_data["plate_no"] + "/" + "raw_" + source_data[
                #     "raw_time"].strftime("%Y%m%d_%H%M%S") + "/",
                None,
                # 元数据时间段为整个数据时间段
                # start_time_stamp
                convert_to_unix_timestamp(dataset["start_time"]),
                # end_time_stamp
                convert_to_unix_timestamp(dataset["end_time"]),
                # start_frame_no
                dataset["start_frame"] if dataset["start_frame"] else None,
                # end_frame_no
                dataset["end_frame"] if dataset["end_frame"] else None,
                # 数据集类型
                SCENE,
                # src_dataset_path
                # 不再维护src_dataset_path字段
                # source_data["project_name"] + "/" + source_data["plate_no"] + "/" + "raw_" + source_data[
                #     "raw_time"].strftime("%Y%m%d_%H%M%S") + "/",
                None,
                id_to_data_id[dataset["id"]],
            ]

            task_dataset_list = [tuple(task_dataset_args)]
            db_util.save_evluate_task_dataset(task_dataset_list)

    def debug_task_dataset(self, task_id, source_id_list):
        """
        为debug模拟数据集
        """
        # 场景数据
        task_dataset_list = db_util.get_dig_data_by_data_id(source_id_list)
        if not task_dataset_list:
            raise Exception("场景数据不存在 source_id_list:{}".format(source_id_list))

        translate_dataset_list = []
        for task_dataset in task_dataset_list:
            dataset = {}
            # 调试任务id任意
            dataset['id'] = 1
            dataset['task_id'] = task_id
            dataset['tag_name'] = None
            dataset['dataset_id'] = task_dataset['id']
            dataset['source_data_ids'] = task_dataset['source_data_ids']
            dataset['dataset_name'] = None
            dataset['dataset_path'] = None
            dataset['start_timestamp'] = convert_to_unix_timestamp(task_dataset["start_time"])
            dataset['end_timestamp'] = convert_to_unix_timestamp(task_dataset["end_time"])
            dataset['start_frame_no'] = task_dataset["start_frame"] if task_dataset["start_frame"] else None
            dataset['end_frame_no'] = task_dataset["end_frame"] if task_dataset["end_frame"] else None
            dataset['dataset_type'] = SCENE
            dataset['data_id'] = task_dataset["data_id"]
            translate_dataset_list.append(dataset)

        return translate_dataset_list


