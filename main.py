from datetime import datetime, timedelta
import json
import logging
import os
import sys
import urllib
import jobvite
from timer import elapsed
import pyodbc
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text as sa_text
from candidate import Candidate

# Connect to Database
drivers = pyodbc.drivers()
driver = "{" + drivers[0] + "}"
ip = os.getenv("SERVER_IP")
db = os.getenv("DB")
user = os.getenv("USER")
pwd = os.getenv("PWD")
params = urllib.parse.quote_plus(
    f"DRIVER={driver};SERVER={ip};DATABASE={db};UID={user};PWD={pwd}"
)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")


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


def exec_sproc(schema, stored_procedure):
    sql_str = f"EXEC {schema}.{stored_procedure}"
    command = sa.text(sql_str).execute_options(autocommit=True)
    engine.execute(command)


@elapsed
def main():
    try:
        candidates = get_candidates()
        df = pd.DataFrame(candidates)
        column_map = {
            "are_you_a_former_or_current_kipp_employee": "formerOrCurrentKIPP",
            "are_you_an_alumnus_of_a_kipp_school": "KIPPAlumni",
            "do_you_hold_a_valid_teacher_certification": "validTeacherCert",
            "do_you_speak_a_language_other_than_english_or_spanish": "otherLanguageSpeaker",
            "do_you_speak_spanish": "spanishSpeaker",
            "for_your_next_position_what_would_be_your_desired_salary_range": "desiredSalary",
            "have_you_applied_to_other_kipp_regions_besides_the_bay_area": "otherKIPPRegions",
            "how_did_you_hear_about_kipp": "howDidYouHear",
            "how_many_years_of_fulltime_classroom_teaching_experience_do_you_have_not_including_student_teaching_internships_tutoring_or_volunteer_work": "teachingExperience",
            "how_many_years_of_fulltime_work_experience_do_you_have": "yrsExperience",
            "if_you_have_completed_a_teacher_licensure_program_please_indicate_what_type_of_program": "teacherLicensureProgram",
            "kipp_has_schools_located_in_different_parts_of_the_bay_area__please_select_your_geographic_preferences": "geoPreference",
            "please_indicate_the_specific_grade_levels_you_would_like_to_teach": "gradePref",
            "please_indicate_the_specific_subject_areas_you_would_like_to_teach": "subjectPref",
            "please_specify_which_language": "otherLanguageSpoken",
            "when_are_you_available_to_begin_work": "workStartAvailability",
            "shared_with_kipp_bayview_academy_middle": "sharedBayview",
            "shared_with_kipp_bayview_elementary": "sharedBayviewES",
            "shared_with_kipp_bridge__middle": "sharedBridgeUpper",
            "shared_with_kipp_excelencia": "sharedExcelencia",
            "shared_with_kipp_heartwood": "sharedHeartwood",
            "shared_with_kipp_heritage": "sharedHeritage",
            "shared_with_kipp_king": "sharedKing",
            "shared_with_sf_college_prep": "sharedSFCP",
            "shared_with_ksjc": "sharedSJC",
            "shared_with_summit": "sharedSummit",
            "shared_with_valiant": "sharedValiant",
            "shared_with_kipp_bridge__elementary": "sharedBridgeLower",
            "shared_with_navigate": "sharedNavigate",
            "shared_with_sf_bay": "sharedSFBay",
            "shared_with_prize": "sharedPrize",
        }
        df.rename(columns=column_map, inplace=True)
        df.index.rename("id", inplace=True)
        df.to_sql(
            "jobvite_cache", engine, schema="custom", if_exists="replace", index=True
        )
        # TODO: Create SQL stored procedure
        # exec_sproc("custom", "sproc_merge_jobvite")

    except Exception as e:
        logging.critical(e)


if __name__ == "__main__":
    main()
