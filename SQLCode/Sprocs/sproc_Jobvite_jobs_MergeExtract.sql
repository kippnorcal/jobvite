/****** Object:  StoredProcedure [custom].[sproc_Jobvite_jobs_MergeExtract] ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


/**************************************************************************************
Description: Merges the data from the most recent extract of Jobvite jobs data into the full repository

EXEC dbo.[sproc_Jobvite_jobs_MergeExtract]

Comments
2019-07-22      sxiong  Initial version

**************************************************************************************/
ALTER PROCEDURE [custom].[sproc_Jobvite_jobs_MergeExtract]
AS
BEGIN

SET XACT_ABORT ON
SET NOCOUNT ON

BEGIN TRY
SELECT * 
INTO #cache_temp
FROM 
(
SELECT *, ROW_NUMBER() OVER(PARTITION BY eId ORDER BY eId) AS row_num
FROM custom.jobvite_jobs_cache
) AS part
WHERE row_num = 1


MERGE custom.jobvite_jobs_full as jvfull  --Final Destination of the Data
USING #cache_temp as cache --Place where are changes are pulled into
ON 
(jvfull.eId = cache.eId
AND jvfull.title = cache.title)


WHEN MATCHED
THEN UPDATE
SET jvfull.[category] = cache.[category]
    ,jvfull.[eId]= cache.[eId]
    ,jvfull.[requisitionId] = cache.[requisitionId]
    ,jvfull.[title] = cache.[title]
    ,jvfull.[LastMergedDate] = getdate()

WHEN NOT MATCHED
THEN  
INSERT ([category],[eId],[requisitionId],[title],[LastMergedDate])
VALUES (cache.[category],cache.[eId],cache.[requisitionId],cache.[title],GETDATE())

;   

DROP TABLE #cache_temp

END TRY
BEGIN CATCH
	EXEC custom.error_handler_sp
	RETURN -1
END CATCH

TRUNCATE TABLE custom.jobvite_jobs_cache

END


GO