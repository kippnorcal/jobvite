/****** Object:  Table [custom].[jobvite_jobs_full] ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [custom].[jobvite_jobs_full](
	[category] [varchar](max) NULL,
	[eId] [varchar](max) NULL,
	[requisitionId] [bigint] NULL,
	[title] [varchar](max) NULL,
	[LastMergedDate] [datetime] NULL CONSTRAINT [DF_jobvite_jobs_full_LastMergedDate] DEFAULT GETDATE()
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO