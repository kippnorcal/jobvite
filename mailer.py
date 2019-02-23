import smtplib
import os
from email.mime.text import MIMEText


GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PWD = os.getenv("GMAIL_PWD")
SLACK_EMAIL = os.getenv("SLACK_EMAIL")


def notify(count=None, error=False, error_message=None):
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(GMAIL_USER, GMAIL_PWD)
    if error:
        text = f"The Jobvite connector encountered an error:\n{error_message}"
        msg = MIMEText(text)
        msg["Subject"] = "Jobvite Connector - Error"
        msg["From"] = "KIPP Bay Area Job Notification"
        msg["To"] = "databot"
    else:
        text = f"The Jobvite connector loaded {count} candidate changes today."
        msg = MIMEText(text)
        msg["Subject"] = "Jobvite Connector - Success"
        msg["From"] = "KIPP Bay Area Job Notification"
        msg["To"] = "databot"
    server.sendmail(GMAIL_USER, SLACK_EMAIL, msg.as_string())
    server.quit()
