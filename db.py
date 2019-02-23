import os
import urllib
import pandas as pd
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.sql import text as sa_text
from data_config import column_map


class Connection:
    def __init__(self, schema, df):
        ip = os.getenv("SERVER_IP")
        db = os.getenv("DB")
        user = os.getenv("USER")
        pwd = os.getenv("PWD")
        driver = f"{{{pyodbc.drivers()[0]}}}"
        params = urllib.parse.quote_plus(
            f"DRIVER={driver};SERVER={ip};DATABASE={db};UID={user};PWD={pwd}"
        )
        self.engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
        self.schema = schema
        self.df = df

    def exec_sproc(self, stored_procedure):
        sql_str = f"EXEC {self.schema}.{stored_procedure}"
        command = sa.text(sql_str).execute_options(autocommit=True)
        self.engine.execute(command)

    def _rename_columns(self):
        self.df.rename(columns=column_map, inplace=True)
        self.df.index.rename("id", inplace=True)

    def insert_into(self, table):
        self._rename_columns()
        self.df.to_sql(
            table, self.engine, schema=self.schema, if_exists="replace", index=True
        )
