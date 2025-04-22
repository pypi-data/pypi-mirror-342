class SourceTag:
    def __init__(self, tag_name: str, start_time: str, end_time: str):
        self.tag_name = tag_name
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return f"SourceTag(tag_name={self.tag_name}, start_time={self.start_time}, end_time={self.end_time})"