from datetime import datetime, timedelta
import json
import logging
import os
import sys
import jobvite
from timer import elapsed
import pandas as pd
from candidate import Candidate


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


def main():
    try:
        results = jobvite.JobviteAPI().candidates(modified_date=MODIFIED_DATE)
        candidates = []
        for result in results:
            candidates.append(Candidate(result).__dict__)

        df = pd.DataFrame(candidates)
        datestamp = datetime.now().strftime("%Y%m%d%I%M")
        df.to_csv(f"output/candidates_{datestamp}.csv", sep=",", index=False)

    except Exception as e:
        logging.critical(e)


if __name__ == "__main__":
    main()
