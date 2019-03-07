from datetime import datetime, timedelta
import json
import logging
import sys
import urllib
import pyodbc
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text as sa_text
from candidate import Candidate
import db
import jobvite
from timer import elapsed


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S%p",
)


if len(sys.argv) > 1:
    MODIFIED_DATE = sys.argv[1]
else:
    MODIFIED_DATE = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")


def get_candidates():
    results = jobvite.JobviteAPI().candidates(modified_date=MODIFIED_DATE)
    candidates = []
    for result in results:
        candidates.append(Candidate(result).__dict__)
    logging.info(f"Retrieved {len(candidates)} candidate records from Jobvite API")
    return candidates


def write_csv(dataframe, delimiter=","):
    datestamp = datetime.now().strftime("%Y%m%d%I%M")
    filename = f"output/candidates_{datestamp}.csv"
    dataframe.to_csv(filename, sep=delimiter, index=False)
    logging.info(f"Wrote {len(dataframe.index)} records to {filename}")


@elapsed
def main():
    try:
        candidates = get_candidates()
        df = pd.DataFrame(candidates)
        connection = db.Connection()
        connection.insert_into("jobvite_cache", df)
        connection.exec_sproc("sproc_Jobvite_MergeExtract")

    except Exception as e:
        logging.critical(e)


if __name__ == "__main__":
    main()
