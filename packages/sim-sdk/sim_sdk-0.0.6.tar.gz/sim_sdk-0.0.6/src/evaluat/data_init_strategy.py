class DatasetInitStrategy:
    def __init__(self):
        self.task_id = None
        self.dataset_list = None

    def parser_dataset(self, source_id_list, dataset_type):
        """
        解析到任务数据
        @param source_id_list 数据id集合，逗号分隔
        @param dataset_type 数据类型 场景、切片、原始数据、回灌任务
        """
        return self

    def get_dataset_label(self, dataset_id):
        """
        获取数据标签
        """
        pass

    def init_task_dataset(self, task_id):
        self.task_id = task_id

    def debug_task_dataset(self, task_id, source_id_list):
        pass
