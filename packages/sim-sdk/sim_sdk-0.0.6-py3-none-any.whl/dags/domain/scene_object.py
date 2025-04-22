class SceneObject:
    def __init__(self, source_id, start_time, end_time, start_frame, end_frame):
        self.id = source_id
        self.timePeriod = [{
            "start_time": start_time,
            "end_time": end_time,
            "start_frame": start_frame,
            "end_frame": end_frame
        }]

    def to_dict(self):
        return {
            "source_id": self.id,
            "timePeriod": self.timePeriod
        }