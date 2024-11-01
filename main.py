import argparse
from datetime import datetime, timedelta
import glob
import json
import logging
import os
import sys
import traceback

from gbq_connector import CloudStorageClient
from job_notifications import create_notifications
from job_notifications import timer
import pandas as pd

from candidate import Candidate
from data_config import custom_application_fields
from job import Job
from jobvite import JobviteAPI
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
    default=None,
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

LOCAL_STORAGE_FOLDER = "./output/"
CANDIDATES_CLOUD_FOLDER = os.getenv("CANDIDATES_CLOUD_FOLDER")
JOBS_CLOUD_FOLDER = os.getenv("JOBS_CLOUD_FOLDER")
BUCKET = os.getenv("BUCKET")

logger = logging.getLogger(__name__)


def get_candidates(jobvite_con, cloud_client):
    results = jobvite_con.candidates(start_date=START_DATE, end_date=END_DATE)
    count = 0
    for result in results:
        data = Candidate(result).__dict__
        create_and_upload_file(data, cloud_client, "candidate_eid", "application_eid", "candidate")
        count += 1
    results = jobvite_con.candidates(start_date=START_DATE, end_date=END_DATE)
    logging.info(f"Retrieved {count} candidate records from Jobvite API")


def get_jobs(jobvite_con, cloud_client):
    results = jobvite_con.jobs()
    count = 0
    for result in results:
        data = Job(result).__dict__
        create_and_upload_file(data, cloud_client, "eId", "requisitionId", "job")
        count += 1
    logging.info(f"Retrieved {count} job records from Jobvite API")


def create_and_upload_file(data, cloud_client, record_id, primary_key, record_type):
        eid = data[record_id]
        pk = data[primary_key]
        file_name = f"{record_type}_{eid}_{pk}.ndjson"
        local_file_path = os.path.join(LOCAL_STORAGE_FOLDER, file_name)
        # Writing file to local dir
        with open(local_file_path, "w") as f:
            f.write(json.dumps(data) + "\n")
        
        # Uploading file from local dir
        with open(local_file_path, "r") as f:
            blob = os.path.join(JOBS_CLOUD_FOLDER, file_name)
            cloud_client.load_file_to_cloud(BUCKET, blob, f)


def cleanup_files():
    files = glob.glob(f"./output/*.ndjson")
    for file in files:
        os.remove(file)


def rename_columns(candidates, jobs):
    candidates.rename(columns=custom_application_fields, inplace=True)
    candidates.index.rename("id", inplace=True)
    jobs.index.rename("id", inplace=True)


@timer("Jobvite")
def main():
    notifications = create_notifications("Jobvite", "mailgun", logs="app.log")
    try:
        jobvite_con = JobviteAPI()
        cloud_client = CloudStorageClient()
        logger.info("Getting candidate data")
        get_candidates(jobvite_con, cloud_client)
        logger.info("Cleaning up candidate files")
        cleanup_files()

        logger.info("Getting job data")
        get_jobs(jobvite_con, cloud_client)
        logger.info("Cleaning up job files")
        cleanup_files()

        notifications.notify()
    except Exception as e:
        logging.exception(e)
        stack_trace = traceback.format_exc()
        notifications.notify(error_message=stack_trace)


if __name__ == "__main__":
    main()
