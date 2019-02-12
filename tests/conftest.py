import pytest


@pytest.fixture(scope="session")
def jobvite_api():
    from jobvite import JobviteAPI
    from os import environ

    return JobviteAPI()
