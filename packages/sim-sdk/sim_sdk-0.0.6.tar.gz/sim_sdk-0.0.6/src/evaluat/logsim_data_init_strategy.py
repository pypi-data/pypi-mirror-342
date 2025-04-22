from evaluat.data_init_strategy import DatasetInitStrategy
from evaluat import db_util
from evaluat.const import LOGSIM, SCENE, SPLIT, SOURCE
import logging
import label_util


class LogsimDatasetInitStrategy(DatasetInitStrategy):
    """
    A strategy for initializing a dataset with clean data.
    """

    def parser_dataset(self, dataset_ids, dataset_type):
        # 获取到所有任务
        # son_task_list = db_util.get_logsim_son_task_by_main_task_id(main_task_id_list)

        # 获取到所有
        # son_task_id_list = ",".join(str(task["id"]) for task in son_task_list)
        # 回灌任务数据
        self.dataset_list = db_util.get_logsim_task_result(dataset_ids)
        if not self.dataset_list:
            raise Exception("回灌任务结果数据不存在 dataset_ids:{}".format(dataset_ids))
        return self

    def get_dataset_label(self, dataset_id):
        # 回灌一个数据包的结果数据
        # logsim_result_dataset = db_util.get_logsim_task_dataset(dataset_id)[0]
        # 回灌一个输入数据包
        logsim_source_dataset = db_util.get_logsim_task_dataset(dataset_id)[0]
        data_type = logsim_source_dataset["dataset_type"]
        dataset_id = logsim_source_dataset["dataset_id"]
        if LOGSIM == data_type:
            logging.error(f"回灌结果数据集 {dataset_id} 的数据类型 {data_type} 不是源数据表、切片表、场景表数据类型")
            return {}

        if data_type == SCENE:
            return label_util.selectSceneDataLabelById(dataset_id)

        elif data_type == SPLIT:
            return label_util.selectSplitDataLabelById(dataset_id)

        elif data_type == SOURCE:
            # 原始源数
            return label_util.selectSourceDataLabelById(dataset_id)


    def init_task_dataset(self, task_id):
        super().init_task_dataset(task_id)

        logging.info("评价回灌结果集")

        # 回灌源数据类型
        logsim_source_dataset_type = db_util.get_logsim_task_dataset(self.dataset_list[0]["parent_id"])[0]["dataset_type"]

        # 提取所有 id 并拼接成逗号分隔的字符串
        logsim_source_data_ids = ",".join(str(item["dataset_id"]) for item in self.dataset_list)
        if logsim_source_dataset_type == SOURCE:
            logsim_source_data_list = db_util.get_source_data(logsim_source_data_ids)
        else:
            logsim_source_data_list = db_util.get_dig_data(logsim_source_data_ids)

        # 构建字典：{id: data_id}
        id_to_data_id = {item["id"]: item["data_id"] for item in logsim_source_data_list}

        # 一次评价可以选择多个源数据集
        # 每个源数据和任务id对应一个任务数据集
        for logsim_result_data in self.dataset_list:

            # 获取到执行任务时的回灌任务数据集
            logsim_task_dataset = db_util.get_logsim_task_dataset(logsim_result_data["parent_id"])[0]

            task_dataset_args = [
                self.task_id,
                # TODO 不再维护tag字段，后续删除
                None,
                logsim_result_data["id"],
                # 不再维护source_data_id
                logsim_task_dataset["source_data_ids"],
                # split data id
                None,
                # Dataset name
                logsim_result_data["dataset_name"],
                logsim_result_data["result_path"],
                # 元数据时间段为整个数据时间段
                # start_time_stamp
                logsim_task_dataset["start_timestamp"],
                # end_time_stamp
                logsim_task_dataset["end_timestamp"],
                # start_frame_no
                logsim_task_dataset["start_frame_no"],
                # end_frame_no
                logsim_task_dataset["end_frame_no"],
                # 数据集类型
                LOGSIM,
                # src_dataset_path
                logsim_result_data["dataset_path"],
                id_to_data_id[logsim_result_data["dataset_id"]],
            ]

            task_dataset_list = [tuple(task_dataset_args)]
            db_util.save_evluate_task_dataset(task_dataset_list)


    def debug_task_dataset(self, logsim_task_id, data_id):
        """
        为debug模拟数据集
        """
        # 场景数据
        # dig_dataset = db_util.get_dig_data_by_data_id(data_id)
        # 获取到所有子任务id
        # 获取到所有
        dataset_list = db_util.get_logsim_task_result_by(logsim_task_id, data_id)
        if not dataset_list:
            raise Exception(f"回灌任务结果数据不存在 logsim_task_id:{logsim_task_id} data_id: {data_id}")

        translate_dataset_list = []
        for logsim_result_data in dataset_list:
            # 获取到执行任务时的回灌任务数据集
            logsim_task_dataset = db_util.get_logsim_task_dataset(logsim_result_data["parent_id"])[0]
            dataset_tmp = {}
            # 调试任务id任意
            dataset_tmp['id'] = 1
            dataset_tmp['task_id'] = 1
            dataset_tmp['tag_name'] = None
            dataset_tmp['dataset_id'] = logsim_result_data['id']
            dataset_tmp['source_data_ids'] = logsim_task_dataset['source_data_ids']
            dataset_tmp['dataset_name'] = logsim_result_data['dataset_name']
            dataset_tmp['dataset_path'] = logsim_result_data["result_path"]
            dataset_tmp['start_timestamp'] = logsim_task_dataset['start_timestamp']
            dataset_tmp['end_timestamp'] = logsim_task_dataset['end_timestamp']
            dataset_tmp['start_frame_no'] = logsim_task_dataset['start_frame_no']
            dataset_tmp['end_frame_no'] = logsim_task_dataset['end_frame_no']
            dataset_tmp['dataset_type'] = LOGSIM
            dataset_tmp['src_dataset_path'] = logsim_result_data['dataset_path']
            dataset_tmp['data_id'] = data_id
            translate_dataset_list.append(dataset_tmp)

        return translate_dataset_list
