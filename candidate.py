from datetime import datetime
import pytz
import re

import data_config


class Candidate:
    def __init__(self, candidate):
        self.candidate = candidate
        self._extract_candidate_info()
        delattr(self, "candidate")

    def _remove_whitespace(self, value, sep):
        if value is not None:
            value = str(value).strip().replace("\t", " ")
            value = re.sub('\n\n+','\n',value)
            value = value.replace("\n", sep)
        return value
    
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
        self._extract_custom_application_fields()
        self._extract_custom_job_fields()

    def _extract_candidate_fields(self):
        self.candidate_eid = self.candidate.get("eId")
        for field in data_config.candidate_fields:
            value = self._remove_whitespace(self.candidate.get(field, "")," ")
            setattr(self, field, value)

    def _extract_application_fields(self):
        application = self.candidate.get("application")
        self.application_eid = application.get("eId")
        self.lastUpdatedDate = self._convert_datetime(
            application.get("lastUpdatedDate")
        )
        if application.get("startDate") is not None:
            self.startDate = self._convert_datetime(
                application.get("startDate")
            )
        else:
            self.startDate = None
        for field in data_config.application_fields:
            value = self._remove_whitespace(application.get(field, "")," ")
            setattr(self, field, value)

    def _extract_job_fields(self):
        job = self.candidate.get("application").get("job")
        self.job_eid = job.get("eId")
        for field in data_config.job_fields:
            value = self._remove_whitespace(job.get(field)," ")
            setattr(self, field, value)

    def _extract_custom_job_fields(self):
        custom_job_fields = self.candidate.get("application").get("job").get("customField")
        for f in data_config.custom_job_fields.keys():
            setattr(self, f, "")
            
        if custom_job_fields is not None:
            for field in custom_job_fields:
                key = field.get("fieldCode")
                value = self._remove_whitespace(field.get("value", "")," ")
                if key in data_config.custom_job_fields.keys():
                    setattr(self, key, value)

    def _extract_custom_application_fields(self):
        custom_application_fields = self.candidate.get("application").get("customField")
        for f in data_config.custom_application_fields.keys():
            setattr(self, f, "")

        for field in custom_application_fields:
            key = field.get("fieldCode")
            if key not in data_config.fields_format_newlines:
                value = self._remove_whitespace(field.get("value", "")," ")
            else:
                value = self._remove_whitespace(field.get("value", "")," | ")
            if key in data_config.custom_application_fields.keys():
                setattr(self, key, value)
