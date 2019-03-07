import pytest
import json
from db import Connection
from sqlalchemy import create_engine
from sqlalchemy.sql.elements import TextClause
from pandas import DataFrame
import data_config


@pytest.fixture(scope="module")
def data_frame():
    with open("tests/fixtures/flat_candidate.json") as f:
        candidate = [json.loads(f.read())]
        return DataFrame(candidate)


def test_connection():
    connection = Connection()
    assert connection.schema == "custom"
    connection = Connection("dbo")
    assert connection.schema == "dbo"


def test_exec_sproc(monkeypatch):
    def mock_execute(command):
        return command

    connection = Connection()
    monkeypatch.setattr(connection.engine, "execute", mock_execute)
    sproc_call = connection.exec_sproc("sproc_do_a_thing")
    assert type(sproc_call) == TextClause
    assert str(sproc_call) == "EXEC custom.sproc_do_a_thing"


def test__rename_columns(data_frame):
    connection = Connection()
    connection.df = data_frame
    df_before = list(data_frame)
    assert data_frame.index.name != "id"
    connection._rename_columns()
    df_after = list(connection.df)
    assert connection.df.index.name == "id"
    assert df_before != df_after
    for k, v in data_config.column_map.items():
        assert k in df_before
        assert v in df_after
