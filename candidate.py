from datetime import datetime
import pytz
import data_config


class Candidate:
    def __init__(self, candidate):
        self.candidate = candidate
        self._extract_candidate_info()
        delattr(self, "candidate")

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

    def _extract_candidate_info(self):
        self._extract_candidate_fields()
        self._extract_application_fields()
        self._extract_job_fields()
        self._extract_custom_fields()

    def _extract_candidate_fields(self):
        self.candidate_eid = self.candidate.get("eId")
        for field in data_config.candidate_fields:
            value = self._remove_whitespace(self.candidate.get(field, ""))
            setattr(self, field, value)

    def _extract_application_fields(self):
        application = self.candidate.get("application")
        self.application_eid = application.get("eId")
        self.lastUpdatedDate = self._convert_datetime(
            application.get("lastUpdatedDate")
        )
        for field in data_config.application_fields:
            value = self._remove_whitespace(application.get(field, ""))
            setattr(self, field, value)

    def _extract_job_fields(self):
        job = self.candidate.get("application").get("job")
        self.job_eid = job.get("eId")
        for field in data_config.job_fields:
            value = self._remove_whitespace(job.get(field))
            setattr(self, field, value)

    def _extract_custom_fields(self):
        custom_fields = self.candidate.get("application").get("customField")
        for f in data_config.custom_fields:
            setattr(self, f, "")

        for field in custom_fields:
            key = field.get("fieldCode")
            value = self._remove_whitespace(field.get("value", ""))
            if key in data_config.custom_fields:
                setattr(self, key, value)
