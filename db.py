from os import getenv
import urllib
import pandas as pd
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.sql import text as sa_text
from data_config import custom_application_fields


class Connection:
    def __init__(self, schema="custom"):
        ip = getenv("SERVER_IP")
        db = getenv("DB")
        user = getenv("USER")
        pwd = getenv("PWD")
        driver = f"{{{pyodbc.drivers()[0]}}}"
        params = urllib.parse.quote_plus(
            f"DRIVER={driver};SERVER={ip};DATABASE={db};UID={user};PWD={pwd}"
        )
        self.engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
        self.schema = schema

    def exec_sproc(self, stored_procedure):
        sql_str = f"EXEC {self.schema}.{stored_procedure}"
        command = sa_text(sql_str).execution_options(autocommit=True)
        return self.engine.execute(command)

    def _rename_columns(self):
        if self.table == "jobvite_cache":
            self.df.rename(columns=custom_application_fields, inplace=True)
        self.df.index.rename("id", inplace=True)

    def insert_into(self, table, df):
        self.df = df
        self.table = table
        self._rename_columns()
        self.df.to_sql(
            table, self.engine, schema=self.schema, if_exists="replace", index=True
        )
