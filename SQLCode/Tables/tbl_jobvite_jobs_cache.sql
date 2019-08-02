/****** Object:  Table [custom].[jobvite_jobs_cache] ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [custom].[jobvite_jobs_cache](
	[category] [varchar](max) NULL,
	[eId] [varchar](max) NULL,
	[requisitionId] [bigint] NULL,
	[title] [varchar](max)
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO