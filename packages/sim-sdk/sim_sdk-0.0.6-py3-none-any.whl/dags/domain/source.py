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