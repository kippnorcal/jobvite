import argparse
from datetime import datetime, timedelta
import logging
import sys
import traceback

from job_notifications import create_notifications
from job_notifications import timer
import pandas as pd
from sqlsorcery import MSSQL

from candidate import Candidate
from data_config import custom_application_fields
from job import Job
import jobvite
from transformations import Field_Transformations


logging.basicConfig(
    handlers=[
        logging.FileHandler(filename="app.log", mode="w+"),
        logging.StreamHandler(sys.stdout),
    ],
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S%p %Z",
)

parser = argparse.ArgumentParser(
    description="Accept start and end date for date window"
)
parser.add_argument(
    "--start-date",
    help="Start Date - format YYYY-MM-DD",
    dest="start_date",
    default=(datetime.now() - timedelta(1)).strftime("%Y-%m-%d"),
)
parser.add_argument(
    "--end-date",
    help="End Date - format YYYY-MM-DD",
    dest="end_date",
    default=(datetime.now()).strftime("%Y-%m-%d"),
)

args = parser.parse_args()
START_DATE = args.start_date
END_DATE = args.end_date

logger = logging.getLogger(__name__)


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


@timer("Jobvite")
def main():
    notifications = create_notifications("Jobvite", "mailgun", logs="app.log")
    try:
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
        logger.info(f"Loaded {len(candidates.index)} candidates")
        logger.info(f"Loaded {len(jobs.index)} jobs")
        notifications.notify()
    except Exception as e:
        logging.exception(e)
        stack_trace = traceback.format_exc()
        notifications.notify(error_message=stack_trace)


if __name__ == "__main__":
    main()
