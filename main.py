from datetime import datetime, timedelta
import json
import logging
import os
import sys
import jobvite
from timer import elapsed


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S%p",
)

# TODO: move env vars to api class
JOBVITE_KEY = os.getenv("JOBVITE_API_KEY")
JOBVITE_SECRET = os.getenv("JOBVITE_API_SECRET")

if len(sys.argv) > 1:
    MODIFIED_DATE = sys.argv[1]
else:
    MODIFIED_DATE = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")


def get_candidates():
    api = jobvite.JobviteAPI(JOBVITE_KEY, JOBVITE_SECRET)
    return api.candidates(modified_date=MODIFIED_DATE)


@elapsed
def stream_to_file(candidates_response):
    datestamp = datetime.now().strftime("%Y%m%d%H%M")
    for candidate in candidates_response:
        data = json.dumps(candidate)
        f = open(f"output/candidates_{datestamp}.json", "a")
        f.write(data)


def main():
    try:
        candidates = get_candidates()
        stream_to_file(candidates)

    except Exception as e:
        logging.critical(e)


if __name__ == "__main__":
    main()
