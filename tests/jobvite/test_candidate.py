import pytest
import json
from candidate import Candidate


@pytest.fixture(scope="module")
def raw_candidate():
    with open("tests/fixtures/raw_candidate.json") as f:
        return json.loads(f.read())


@pytest.fixture(scope="module")
def parsed(raw_candidate):
    return Candidate(raw_candidate).__dict__


@pytest.fixture(scope="module")
def expected():
    with open("tests/fixtures/flat_candidate.json") as f:
        return json.loads(f.read())


def test_white_space_removal(parsed, expected):
    assert parsed["address"] == expected["address"]


def test_linebreak_removal(parsed, expected):
    assert (
        parsed["please_indicate_the_specific_grade_levels_you_would_like_to_teach"]
        == expected["please_indicate_the_specific_grade_levels_you_would_like_to_teach"]
    )


def test_epoch_datetime_conversion(parsed, expected):
    assert parsed["lastUpdatedDate"] == expected["lastUpdatedDate"]


def test_parsed_matches_expected(parsed, expected):
    assert type(parsed) == type(expected)
    assert len(parsed) == len(expected)
    assert parsed == expected
    for key in parsed.keys():
        assert parsed[key] == expected[key]
