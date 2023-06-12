CREATE PROCEDURE [custom].[sproc_Jobvite_MergeExtract]
AS
/**************************************************************************************
Description: Merges the data from the most recent extract of Jobvite data into the full repository
EXEC dbo.[sproc_Jobvite_MergeExtract]
Comments
2019-02-28      MDunn   Created
2019-03-04      DHess   Change schema for table names.
2019-04-15      DHess   Add source field.
2019-06-12      SXiong  Add 4 new columns for HR account provisioning
2019-08-20      SXiong  Add new school sharing columns
2022-05-11      LMendez Added 7 fields that will be needed for Schoolytics  
  **************************************************************************************/
BEGIN

SET XACT_ABORT ON
SET NOCOUNT ON

BEGIN TRY
SELECT * 
INTO #cache_temp
FROM 
(
SELECT *, ROW_NUMBER() OVER(PARTITION BY job_eid, candidate_eid, application_eid, workflowStateEId ORDER BY lastUpdatedDate DESC) AS row_num
FROM custom.jobvite_cache
) AS part
WHERE row_num = 1


MERGE custom.jobvite_full as jvfull  --Final Destination of the Data
--MERGE [14315-DW.SCHOOLZILLA.COM].Cust14315.custom.jobvite_full as jvfull
USING #cache_temp as cache --Place where are changes are pulled into
ON 
(jvfull.application_eid = cache.application_eid
AND jvfull.candidate_eid = cache.candidate_eid
AND jvfull.job_eid = cache.job_eid
AND jvfull.workflowStateEId = cache.workflowStateEId)
         
                                                                                     

WHEN MATCHED
THEN UPDATE
--INSERT THE Full Record into Jobvite
SET jvfull.[workflowState] = cache.[workflowState]
   ,jvfull.[address] = cache.[address]
           ,jvfull.[address2]= cache.[address2]
           ,jvfull.[application_owner]= cache.[application_owner]
           ,jvfull.[formerOrCurrentKIPP]= cache.[formerOrCurrentKIPP]
           ,jvfull.[KIPPAlumni]= cache.[KIPPAlumni]
           ,jvfull.[assigned_pay_location]= cache.[assigned_pay_location]
           ,jvfull.[assigned_work_location]= cache.[assigned_work_location]
           ,jvfull.[city]= cache.[city]
           ,jvfull.[country]= cache.[country]
           ,jvfull.[credentialing_score]= cache.[credentialing_score]
           ,jvfull.[department]= cache.[department]
           ,jvfull.[disposition]= cache.[disposition]
           ,jvfull.[validTeacherCert]= cache.[validTeacherCert]
           ,jvfull.[otherLanguageSpeaker]= cache.[otherLanguageSpeaker]
           ,jvfull.[spanishSpeaker]= cache.[spanishSpeaker]
           ,jvfull.[email]= cache.[email]
           ,jvfull.[equipment_needed]= cache.[equipment_needed]
           ,jvfull.[exempt_status]= cache.[exempt_status]
           ,jvfull.[firstName]= cache.[firstName]
           ,jvfull.[desiredSalary]= cache.[desiredSalary]
           ,jvfull.[fte]= cache.[fte]
           ,jvfull.[gender]= cache.[gender]
           ,jvfull.[otherKIPPRegions]= cache.[otherKIPPRegions]
           ,jvfull.[howDidYouHear]= cache.[howDidYouHear]
           ,jvfull.[teachingExperience]= cache.[teachingExperience]
           ,jvfull.[yrsExperience]= cache.[yrsExperience]
           ,jvfull.[teacherLicensureProgram]= cache.[teacherLicensureProgram]
           ,jvfull.[jobType]= cache.[jobType]
           ,jvfull.[jobviteChannel]= cache.[jobviteChannel]
           ,jvfull.[geoPreference]= cache.[geoPreference]
           ,jvfull.[lastName]= cache.[lastName]
           ,jvfull.[lastUpdatedDate]= cache.[lastUpdatedDate]
           ,jvfull.[likelihood_of_hire]= cache.[likelihood_of_hire]
           ,jvfull.[location]= cache.[location]
           ,jvfull.[pay_type]= cache.[pay_type]
           ,jvfull.[paycom_job_title]= cache.[paycom_job_title]
           ,jvfull.[gradePref]= cache.[gradePref]
           ,jvfull.[subjectPref]= cache.[subjectPref]
           ,jvfull.[offer_1]= cache.[offer_1]
           ,jvfull.[offer_2]= cache.[offer_2]           
           ,jvfull.[offer_3]= cache.[offer_3]           
           ,jvfull.[otherLanguageSpoken]= cache.[otherLanguageSpoken]
           ,jvfull.[postalCode]= cache.[postalCode]
           ,jvfull.[postingType]= cache.[postingType]
           ,jvfull.[race]= cache.[race]
           ,jvfull.[requisitionId]= cache.[requisitionId]
           ,jvfull.[scoutingReportShared]= cache.[scoutingReportShared]
           ,jvfull.[interviewsConductedAt]= cache.[interviewsConductedAt]
           ,jvfull.[offersExtendedFrom]= cache.[offersExtendedFrom]
           ,jvfull.[sharedBayview]= cache.[sharedBayview]
           ,jvfull.[sharedBayviewES]= cache.[sharedBayviewES]
           ,jvfull.[sharedBridgeLower]= cache.[sharedBridgeLower]
           ,jvfull.[sharedBridgeUpper]= cache.[sharedBridgeUpper]
           ,jvfull.[sharedExcelencia]= cache.[sharedExcelencia]
           ,jvfull.[sharedHeartwood]= cache.[sharedHeartwood]
           ,jvfull.[sharedHeritage]= cache.[sharedHeritage]
           ,jvfull.[sharedKing]= cache.[sharedKing]
           ,jvfull.[sharedSJC]= cache.[sharedSJC]
           ,jvfull.[sharedNavigate]= cache.[sharedNavigate]
           ,jvfull.[sharedPrize]= cache.[sharedPrize]
           ,jvfull.[sharedSFBay]= cache.[sharedSFBay]
           ,jvfull.[sharedSFCP]= cache.[sharedSFCP]
           ,jvfull.[sharedSummit]= cache.[sharedSummit]
           ,jvfull.[sharedValiant]= cache.[sharedValiant]
           ,jvfull.[sourceType]= cache.[sourceType]
           ,jvfull.[source]= cache.[source]
           ,jvfull.[state]= cache.[state]
           ,jvfull.[startDate]= cache.[startDate]
           ,jvfull.[title]= cache.[title]
           ,jvfull.[veteranStatus]= cache.[veteranStatus]
           ,jvfull.[workStartAvailability]= cache.[workStartAvailability]
           ,jvfull.[workStatus] = cache.[workStatus]
           ,jvfull.[homePhone] = cache.[homePhone]
           ,jvfull.[position] = cache.[position]
           ,jvfull.[dept_code] = cache.[dept_code]
           ,jvfull.[hireDate] = cache.[hireDate]
           ,jvfull.[pay_location_digit] = cache.[pay_location_digit]
           ,jvfull.[work_location_digit] = cache.[work_location_digit]
           ,jvfull.[Annual_Salary] = cache.[Annual_Salary]
           ,jvfull.[Semi_monthly_Rate] = cache.[Semi_Monthly_Rate]
           ,jvfull.[Hourly_Rate] = cache.[Hourly_Rate]
           ,jvfull.[is_this_a_rehire_promotion_or_internal_transfer] = cache.[is_this_a_rehire_promotion_or_internal_transfer]
           ,jvfull.[LastMergedDate] = getdate()

WHEN NOT MATCHED
THEN  
INSERT ([application_eid],[candidate_eid],[job_eid],[workflowState],[workflowStateEId],[address],[address2]
,[application_owner],[formerOrCurrentKIPP],[KIPPAlumni],[assigned_pay_location],[assigned_work_location],[city],[country],[credentialing_score]
,[department],[disposition],[validTeacherCert],[otherLanguageSpeaker],[spanishSpeaker],[email],[equipment_needed]
,[exempt_status],[firstName],[desiredSalary],[fte],[gender],[otherKIPPRegions],[howDidYouHear],[teachingExperience],[yrsExperience]
,[teacherLicensureProgram],[jobType],[jobviteChannel],[geoPreference],[lastName],[lastUpdatedDate],[likelihood_of_hire]
,[location],[pay_type],[paycom_job_title],[gradePref],[subjectPref],[offer_1],[offer_2],[offer_3],[otherLanguageSpoken],[postalCode]
,[postingType],[race],[requisitionId],[scoutingReportShared],[interviewsConductedAt],[offersExtendedFrom],[sharedBayview],[sharedBayviewES],[sharedBridgeLower],[sharedBridgeUpper]
,[sharedExcelencia],[sharedHeartwood],[sharedHeritage],[sharedKing],[sharedSJC],[sharedNavigate],[sharedPrize]
,[sharedSFBay],[sharedSFCP],[sharedSummit],[sharedValiant],[sourceType],[source],[state],[startDate],[title],[veteranStatus]
,[workStartAvailability],[workStatus], [homePhone],[position],[dept_code], [hireDate], [pay_location_digit], [work_location_digit], [Annual_Salary]
,[Semi_Monthly_Rate], [Hourly_Rate],[is_this_a_rehire_promotion_or_internal_transfer], [LastMergedDate])
VALUES (cache.[application_eid],cache.[candidate_eid],cache.[job_eid],cache.[workflowState],cache.[workflowStateEId],cache.[address],cache.[address2]
,cache.[application_owner],cache.[formerOrCurrentKIPP],cache.[KIPPAlumni],cache.[assigned_pay_location],cache.[assigned_work_location],cache.[city],cache.[country],cache.[credentialing_score]
,cache.[department],cache.[disposition],cache.[validTeacherCert],cache.[otherLanguageSpeaker],cache.[spanishSpeaker],cache.[email],cache.[equipment_needed]
,cache.[exempt_status],cache.[firstName],cache.[desiredSalary],cache.[fte],cache.[gender],cache.[otherKIPPRegions],cache.[howDidYouHear],cache.[teachingExperience],cache.[yrsExperience]
,cache.[teacherLicensureProgram],cache.[jobType],cache.[jobviteChannel],cache.[geoPreference],cache.[lastName],cache.[lastUpdatedDate],cache.[likelihood_of_hire]
,cache.[location],cache.[pay_type],cache.[paycom_job_title],cache.[gradePref],cache.[subjectPref],cache.[offer_1],cache.[offer_2],cache.[offer_3],cache.[otherLanguageSpoken],cache.[postalCode]
,cache.[postingType],cache.[race],cache.[requisitionId],cache.[scoutingReportShared],cache.[interviewsConductedAt],cache.[offersExtendedFrom],cache.[sharedBayview],cache.[sharedBayviewES],cache.[sharedBridgeLower],cache.[sharedBridgeUpper]
,cache.[sharedExcelencia],cache.[sharedHeartwood],cache.[sharedHeritage],cache.[sharedKing],cache.[sharedSJC],cache.[sharedNavigate],cache.[sharedPrize]
,cache.[sharedSFBay],cache.[sharedSFCP],cache.[sharedSummit],cache.[sharedValiant],cache.[sourceType],cache.[source],cache.[state],cache.[startDate],cache.[title],cache.[veteranStatus]
,cache.[workStartAvailability],cache.[workStatus], cache.[homePhone],[position],[dept_code], [hireDate], [pay_location_digit], [work_location_digit]
,[Annual_Salary], [Semi_Monthly_Rate], [Hourly_Rate], [is_this_a_rehire_promotion_or_internal_transfer], GETDATE())

/*Probably going to do nothing
WHEN NOT MATCHED BY Delta 
THEN         
DELETE*/
;   

DROP TABLE #cache_temp

END TRY
BEGIN CATCH
	EXEC custom.error_handler_sp
	RETURN -1
END CATCH

TRUNCATE TABLE custom.jobvite_cache

END
go
