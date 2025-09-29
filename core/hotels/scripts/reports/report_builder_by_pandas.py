import os

from ...config import bucket
from .executor_list import executors_list


class ReportBuilder:
    _builders = {
        "EXECUTORS_LIST": executors_list,
    }

    def __init__(self, report_type, path, time_zone_offset):
        self.func = __class__._builders.get(report_type, None)
        self.path = path
        self.time_zone_offset = time_zone_offset

        self.file_path = os.path.join("/usr/local/share/minio", bucket, self.path)

        if os.path.isfile(os.path.join(self.file_path)):
            os.remove(os.path.join(self.file_path))
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def process(self, tasks, period):
        return self.func(tasks, period, self.time_zone_offset, self.file_path)