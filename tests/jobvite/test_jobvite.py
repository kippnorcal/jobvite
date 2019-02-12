import pytest


def test_jobvite_api_limit_request(jobvite_api):
    candidates = list(jobvite_api.candidates(limit=10))
    assert len(candidates) == 10


def test_jobvite_api_batched_limit_request(jobvite_api):
    candidates = list(jobvite_api.candidates(batch_size=40, limit=20))
    assert len(candidates) == 20
