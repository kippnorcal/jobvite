import pytest
from smtplib import SMTP_SSL
from os import getenv
from mailer import Mailer


@pytest.fixture(scope="module")
def inbox():
    return []


@pytest.fixture(autouse=True)
def mock_login(monkeypatch):
    def mockreturn(user, password, initial_response_ok=True):
        return user, password

    monkeypatch.setattr(SMTP_SSL, "login", mockreturn)


@pytest.fixture(autouse=True)
def mock_sendmail(monkeypatch, inbox):
    def mockreturn(obj, from_address, to_address, full_message):
        inbox.append({"from": from_address, "to": to_address, "message": full_message})
        return inbox

    monkeypatch.setattr(SMTP_SSL, "sendmail", mockreturn)


def test_mailer_success(inbox):
    inbox.clear()
    success = Mailer()
    success.notify(count=1)
    assert len(inbox) == 1
    assert inbox[0]["to"] == getenv("SLACK_EMAIL")
    assert "Success" in inbox[0]["message"]
    assert "changes" in inbox[0]["message"]


def test_mailer_error(inbox):
    inbox.clear()
    error = Mailer()
    error.notify(success=False, error_message="it failed")
    assert len(inbox) == 1
    assert inbox[0]["to"] == getenv("SLACK_EMAIL")
    assert "Error" in inbox[0]["message"]
    assert "it failed" in inbox[0]["message"]
