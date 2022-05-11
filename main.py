import argparse
from datetime import datetime, timedelta
import logging
import sys
from timer import elapsed
import traceback

import pandas as pd
from sqlsorcery import MSSQL

from candidate import Candidate
from data_config import custom_application_fields
from job import Job
import jobvite
from mailer import Mailer
from transformations import Field_Transformations


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S%p",
)

parser = argparse.ArgumentParser(
    description="Accept start and end date for date window"
)
parser.add_argument(
    "--startdate",
    help="Start Date - format YYYY-MM-DD",
    default=(datetime.now() - timedelta(1)).strftime("%Y-%m-%d"),
)
parser.add_argument(
    "--enddate",
    help="End Date - format YYYY-MM-DD",
    default=(datetime.now()).strftime("%Y-%m-%d"),
)
args = parser.parse_args()
START_DATE = args.startdate
END_DATE = args.enddate


def get_candidates():
    results = jobvite.JobviteAPI().candidates(start_date=START_DATE, end_date=END_DATE)
    candidates = []
    for result in results:
        candidates.append(Candidate(result).__dict__)
    logging.info(f"Retrieved {len(candidates)} candidate records from Jobvite API")
    return pd.DataFrame(candidates)


def get_jobs():
    results = jobvite.JobviteAPI().jobs()
    jobs = []
    for result in results:
        jobs.append(Job(result).__dict__)
    logging.info(f"Retrieved {len(jobs)} job records from Jobvite API")
    return pd.DataFrame(jobs)


def rename_columns(candidates, jobs):
    candidates.rename(columns=custom_application_fields, inplace=True)
    candidates.index.rename("id", inplace=True)
    jobs.index.rename("id", inplace=True)


@elapsed
def main():
    try:
        mailer = Mailer()
        candidates = get_candidates()
        jobs = get_jobs()
        rename_columns(candidates, jobs)
        transformed_candidates = Field_Transformations(candidates).dataframe
        connection = MSSQL()
        connection.insert_into(
            "jobvite_cache", transformed_candidates, if_exists="replace"
        )
        connection.exec_sproc("sproc_Jobvite_MergeExtract", autocommit=True)
        connection.insert_into("jobvite_jobs_cache", jobs, if_exists="replace")
        connection.exec_sproc("sproc_Jobvite_jobs_MergeExtract", autocommit=True)
        mailer.notify(
            candidates_count=len(candidates.index), jobs_count=len(jobs.index)
        )
    except Exception as e:
        logging.exception(e)
        stack_trace = traceback.format_exc()
        mailer.notify(success=False, error_message=stack_trace)


if __name__ == "__main__":
    main()
