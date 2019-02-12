from datetime import datetime, timedelta
import json
import logging
import os
import sys
import jobvite
from timer import elapsed
import pandas as pd


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
    return api.candidates(modified_date=MODIFIED_DATE, limit=5)


def stream_data():
    candidates = get_candidates()
    response = []
    for candidate in candidates:
        response.append(candidate)
    return response


def extract_candidate_data(record):
    candidate_columns = [
        "address",
        "address2",
        "city",
        "state",
        "country",
        "postalCode",
        "location",
        "email",
        "firstName",
        "lastName",
        "workStatus",
    ]
    data = {}
    for key, value in record.items():
        if key in candidate_columns:
            data[key] = value
        if key == "eId":
            data["candidate_eId"] = value
    return data


def extract_application_data(record):
    application_columns = [
        "disposition",
        "gender",
        "jobviteChannel",
        "lastUpdatedDate",
        "race",
        "sourceType",
        "veteranStatus",
        "workflowState",
        "workflowStateEId",
    ]
    data = {}
    for key, value in record["application"].items():
        if key in application_columns:
            data[key] = value
        if key == "eId":
            data["application_eId"] = value
    return data


def extract_job_data(record):
    job_columns = [
        "department",
        "jobType",
        "location",
        "postingType",
        "requisitionId",
        "title",
    ]
    data = {}
    for key, value in record["application"]["job"].items():
        if key in job_columns:
            data[key] = value
        if key == "eId":
            data["job_eId"] = value
    return data


def extract_custom_fields(record):
    custom_columns = [
        "when_are_you_available_to_begin_work",
        "how_did_you_hear_about_kipp",
        "are_you_a_former_or_current_kipp_employee",
        "are_you_an_alumnus_of_a_kipp_school",
        "how_many_years_of_fulltime_classroom_teaching_experience_do_you_have_not_including_student_teaching_internships_tutoring_or_volunteer_work",
        "for_your_next_position_what_would_be_your_desired_salary_range",
        "if_you_have_completed_a_teacher_licensure_program_please_indicate_what_type_of_program",
        "kipp_has_schools_located_in_different_parts_of_the_bay_area__please_select_your_geographic_preferences",
        "please_indicate_the_specific_grade_levels_you_would_like_to_teach",
        "please_indicate_the_specific_subject_areas_you_would_like_to_teach",
        "do_you_hold_a_valid_teacher_certification",
        "do_you_speak_spanish",
        "do_you_speak_a_language_other_than_english_or_spanish",
        "application_owner",
        "paycom_job_title",
        "pay_type",
        "fte",
        "assigned_work_location",
        "have_you_applied_to_other_kipp_regions_besides_the_bay_area",
    ]
    # TODO: Add likelihood of hire, shared fields, credential score, and fulltime work experience
    data = {}
    for field in record["application"]["customField"]:
        key = field["fieldCode"]
        value = field["value"]
        if key in custom_columns:
            data[key] = value
    return data


@elapsed
def stream_to_file():
    datestamp = datetime.now().strftime("%Y%m%d%H%M")
    candidates = get_candidates()
    response = []
    for candidate in candidates:
        data = json.dumps(candidate)
        response.append(data)
    return response


def main():
    try:
        # results = stream_to_file()
        # print(results)
        results = stream_data()
        clean = []
        for result in results:
            candidate_fields = extract_candidate_data(result)
            application_fields = extract_application_data(result)
            job_fields = extract_job_data(result)
            custom_fields = extract_custom_fields(result)
            clean.append(
                {
                    **candidate_fields,
                    **application_fields,
                    **job_fields,
                    **custom_fields,
                }
            )

        df = pd.DataFrame(clean)
        print(df.head())

    except Exception as e:
        logging.critical(e)


if __name__ == "__main__":
    main()
