from datetime import datetime
import pytz
import data_config


class Job:
    def __init__(self, job):
        self.job = job
        self._extract_job_info()
        delattr(self, "job")

    def _remove_whitespace(self, s):
        if s is not None:
            s = str(s)
            s = s.strip().strip("\n").strip("\t")
            s = s.replace("\n", " ").replace("\t", " ")
        return s

    def _convert_datetime(self, unix_timestamp):
        timestamp_without_miliseconds = unix_timestamp / 1000.0
        tz = pytz.timezone("America/Los_Angeles")
        return datetime.fromtimestamp(timestamp_without_miliseconds, tz).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def _extract_job_info(self):
        self._extract_requisition_fields()

    def _extract_requisition_fields(self):
        for field in data_config.requisition_fields:
            value = self._remove_whitespace(self.job.get(field, ""))
            setattr(self, field, value)
