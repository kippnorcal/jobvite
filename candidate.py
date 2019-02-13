class Candidate:
    def __init__(self, candidate):
        self.candidate = candidate
        self._extract_candidate_info()
        delattr(self, "candidate")

    def _extract_candidate_info(self):
        self._extract_candidate_fields()
        self._extract_application_fields()
        self._extract_job_fields()
        self._extract_custom_fields()

    def _extract_candidate_fields(self):
        self.candidate_eid = self.candidate.get("eId")
        fields = [
            "address",
            "address2",
            "city",
            "state",
            "country",
            "postalCode",
            "email",
            "firstName",
            "lastName",
            "workStatus",
        ]
        for field in fields:
            value = self.candidate.get(field)
            setattr(self, field, value)

    def _extract_application_fields(self):
        application = self.candidate.get("application")
        self.application_eid = application.get("eId")
        fields = [
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
        for field in fields:
            value = application.get(field)
            setattr(self, field, value)

    def _extract_job_fields(self):
        job = self.candidate.get("application").get("job")
        self.job_eid = job.get("eId")
        fields = [
            "department",
            "jobType",
            "location",
            "postingType",
            "requisitionId",
            "title",
        ]
        for field in fields:
            value = job.get(field)
            setattr(self, field, value)

    def _extract_custom_fields(self):
        custom_fields = self.candidate.get("application").get("customField")
        fields = [
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
        for field in custom_fields:
            key = field.get("fieldCode")
            value = field.get("value")
            if key in fields:
                setattr(self, key, value)
