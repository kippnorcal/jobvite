import pytest
from smtplib import SMTP_SSL
import mailer
from os import getenv


@pytest.fixture(scope="module")
def inbox():
    return []


def test_notify(inbox, monkeypatch):
    def mock_login(user, password, initial_response_ok=True):
        return user, password

    def mock_sendmail(obj, from_address, to_address, full_message):
        inbox.append({"from": from_address, "to": to_address, "message": full_message})
        return inbox

    monkeypatch.setattr(SMTP_SSL, "login", mock_login)
    monkeypatch.setattr(SMTP_SSL, "sendmail", mock_sendmail)
    mailer.notify(1)
    assert len(inbox) == 1
    assert inbox[0]["to"] == getenv("SLACK_EMAIL")
