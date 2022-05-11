


/****** Object:  Table [custom].[jobvite_full]    Script Date: 3/13/2019 11:07:11 AM ******/
--DROP TABLE [custom].[jobvite_full]
--GO

/****** Object:  Table [custom].[jobvite_full]    Script Date: 3/13/2019 11:07:11 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [custom].[jobvite_full](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[application_eid] [varchar](max) NULL,
	[candidate_eid] [varchar](max) NULL,
	[job_eid] [varchar](max) NULL,
	[workflowState] [varchar](max) NULL,
	[workflowStateEId] [varchar](max) NULL,
	[address] [varchar](max) NULL,
	[address2] [varchar](max) NULL,
	[application_owner] [varchar](max) NULL,
	[formerOrCurrentKIPP] [varchar](max) NULL,
	[KIPPAlumni] [varchar](max) NULL,
	[assigned_work_location] [varchar](max) NULL,
	[city] [varchar](max) NULL,
	[country] [varchar](max) NULL,
	[credentialing_score] [varchar](max) NULL,
	[department] [varchar](max) NULL,
	[disposition] [varchar](max) NULL,
	[validTeacherCert] [varchar](max) NULL,
	[otherLanguageSpeaker] [varchar](max) NULL,
	[spanishSpeaker] [varchar](max) NULL,
	[email] [varchar](max) NULL,
	[equipment_needed] [varchar](max) NULL,
	[firstName] [varchar](max) NULL,
	[desiredSalary] [varchar](max) NULL,
	[fte] [varchar](max) NULL,
	[gender] [varchar](max) NULL,
	[otherKIPPRegions] [varchar](max) NULL,
	[howDidYouHear] [varchar](max) NULL,
	[teachingExperience] [varchar](max) NULL,
	[yrsExperience] [varchar](max) NULL,
	[teacherLicensureProgram] [varchar](max) NULL,
	[jobType] [varchar](max) NULL,
	[jobviteChannel] [varchar](max) NULL,
	[geoPreference] [varchar](max) NULL,
	[lastName] [varchar](max) NULL,
	[lastUpdatedDate] [varchar](max) NULL,
	[likelihood_of_hire] [varchar](max) NULL,
	[location] [varchar](max) NULL,
	[pay_type] [varchar](max) NULL,
	[paycom_job_title] [varchar](max) NULL,
	[gradePref] [varchar](max) NULL,
	[subjectPref] [varchar](max) NULL,
	[otherLanguageSpoken] [varchar](max) NULL,
	[postalCode] [varchar](max) NULL,
	[postingType] [varchar](max) NULL,
	[race] [varchar](max) NULL,
	[requisitionId] [varchar](max) NULL,
	[sharedBayview] [varchar](max) NULL,
	[sharedBayviewES] [varchar](max) NULL,
	[sharedBridgeLower] [varchar](max) NULL,
	[sharedBridgeUpper] [varchar](max) NULL,
	[sharedExcelencia] [varchar](max) NULL,
	[sharedHeartwood] [varchar](max) NULL,
	[sharedHeritage] [varchar](max) NULL,
	[sharedKing] [varchar](max) NULL,
	[sharedSJC] [varchar](max) NULL,
	[sharedNavigate] [varchar](max) NULL,
	[sharedPrize] [varchar](max) NULL,
	[sharedSFBay] [varchar](max) NULL,
	[sharedSFCP] [varchar](max) NULL,
	[sharedSummit] [varchar](max) NULL,
	[sharedValiant] [varchar](max) NULL,
	[sourceType] [varchar](max) NULL,
	[source] [varchar](max) NULL,
	[state] [varchar](max) NULL,
	[title] [varchar](max) NULL,
	[veteranStatus] [varchar](max) NULL,
	[workStartAvailability] [varchar](max) NULL,
	[workStatus] [varchar](max) NULL,
	homePhone               [varchar](max),
    jobcoastcode            [varchar](max),
    position                [varchar](max),
    dept_code               [varchar](max),
    hireDate                [varchar](max),
    work_location_digit     [varchar](max),
    pay_location_digit      [varchar](max),
	[LastMergedDate] [datetime] NULL CONSTRAINT [DF_jobvite_full_LastMergedDate]  DEFAULT (getdate())
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO


