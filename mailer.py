from smtplib import SMTP_SSL
from os import getenv
from email.mime.text import MIMEText


class Mailer:
    def __init__(self):
        self.user = getenv("GMAIL_USER")
        self.password = getenv("GMAIL_PWD")
        self.slack_email = getenv("SLACK_EMAIL")
        self.server = SMTP_SSL("smtp.gmail.com", 465)
        self.from_address = "KIPP Bay Area Job Notification"
        self.to_address = "databot"

    def _subject_line(self):
        subject_type = "Success" if self.success else "Error"
        return f"Jobvite_Connector - {subject_type}"

    def _body_text(self):
        if self.success:
            return f"The Jobvite connector loaded {self.candidates_count} candidate and {self.jobs_count} job changes today."
        else:
            return f"The Jobvite connector encountered an error:\n{self.error_message}"

    def _message(self):
        msg = MIMEText(self._body_text())
        msg["Subject"] = self._subject_line()
        msg["From"] = self.from_address
        msg["To"] = self.to_address
        return msg.as_string()

    def notify(self, candidates_count=None, jobs_count=None, success=True, error_message=None):
        self.candidates_count = candidates_count
        self.jobs_count = jobs_count
        self.success = success
        self.error_message = error_message
        with self.server as s:
            s.login(self.user, self.password)
            msg = self._message()
            s.sendmail(self.user, self.slack_email, msg)
