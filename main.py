import argparse
from datetime import datetime
import glob
import json
import logging
import os
import sys
import traceback

from gbq_connector import BigQueryClient
from gbq_connector import CloudStorageClient
from job_notifications import create_notifications
from job_notifications import timer

from candidate import Candidate
from job import Job
from jobvite import JobviteAPI


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

LOCAL_STORAGE_FOLDER = "./output/"
CANDIDATES_CLOUD_FOLDER = os.getenv("CANDIDATES_CLOUD_FOLDER")
JOBS_CLOUD_FOLDER = os.getenv("JOBS_CLOUD_FOLDER")
BUCKET = os.getenv("BUCKET")
CANDIDATE_TABLE = os.getenv("CANDIDATE_TABLE")

logger = logging.getLogger(__name__)


def set_start_date()->str:
    bq_conn = BigQueryClient()
    result = bq_conn.query(f"SELECT MAX(lastUpdatedDate) FROM `{CANDIDATE_TABLE}`")
    times_stamp = result.iloc[0, 0].strftime('%Y-%m-%d')
    return times_stamp


def get_candidates(results, cloud_client: CloudStorageClient) -> None:
    count = 0
    for result in results:
        data = Candidate(result).__dict__
        create_and_upload_file(data, cloud_client, "candidate_eid", "application_eid", "candidate")
        count += 1
    logging.info(f"Retrieved {count} candidate records from Jobvite API")


def get_jobs(results, cloud_client: CloudStorageClient) -> None:
    count = 0
    for result in results:
        data = Job(result).__dict__
        create_and_upload_file(data, cloud_client, "eId", "requisitionId", "job")
        count += 1
    logging.info(f"Retrieved {count} job records from Jobvite API")


def create_and_upload_file(
        data: dict,
        cloud_client: CloudStorageClient,
        record_id:
        str,
        primary_key: str,
        record_type: str
        ) -> None:
        """
        This func helps reduce redundent code by uploading both candidate and job data.
        data: the data of teh record
        cloud_client: connection to Google cloud
        record_id: eId (job) or candidate_eId (candidate)
        primary_key: requisitionId (job) or application_eId (candidate)
        record_type: 'job' or 'candidate'
        """
        if record_type == "jobs":
            cloud_folder = JOBS_CLOUD_FOLDER
        else:
            cloud_folder = CANDIDATES_CLOUD_FOLDER

        eid = data[record_id]
        pk = data[primary_key]
        file_name = f"{record_type}_{eid}_{pk}.ndjson"
        local_file_path = os.path.join(LOCAL_STORAGE_FOLDER, file_name)
        # Writing file to local dir
        with open(local_file_path, "w") as f:
            f.write(json.dumps(data) + "\n")
        
        # Uploading file from local dir
        with open(local_file_path, "r") as f:
            blob = os.path.join(cloud_folder, file_name)
            cloud_client.load_file_to_cloud(BUCKET, blob, f)


def cleanup_files() -> None:
    files = glob.glob(f"./output/*.ndjson")
    for file in files:
        os.remove(file)


@timer("Jobvite")
def main():

    args = parser.parse_args()
    start_date = args.start_date
    end_date = args.end_date

    jobvite_con = JobviteAPI()
    cloud_client = CloudStorageClient()
    if start_date is None:
        start_date = set_start_date()

    logger.info(f"Getting candidate data from {start_date} to {end_date}")
    results = jobvite_con.candidates(start_date=start_date, end_date=end_date)
    get_candidates(results, cloud_client)
    logger.info("Cleaning up candidate files")
    cleanup_files()

    logger.info("Getting job data")
    results = jobvite_con.jobs()
    get_jobs(results, cloud_client)
    logger.info("Cleaning up job files")
    cleanup_files()


if __name__ == "__main__":
    notifications = create_notifications("Jobvite", "mailgun", logs="app.log")
    try:
        main()
    except Exception as e:
        logging.exception(e)
        stack_trace = traceback.format_exc()
        notifications.notify(error_message=stack_trace)
