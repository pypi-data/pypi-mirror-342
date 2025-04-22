class LabelObject:
    def __init__(self, label_id, start_time, end_time):
        self.id = label_id
        self.timePeriod = [{
            "start_time": start_time,
            "end_time": end_time
        }]

    def to_dict(self):
        return {
            "label_id": self.id,
            "timePeriod": self.timePeriod
        }