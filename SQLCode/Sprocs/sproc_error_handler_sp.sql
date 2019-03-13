

/****** Object:  StoredProcedure [custom].[error_handler_sp]    Script Date: 3/13/2019 11:13:35 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

/**************************************************************************************
Description: Generic error handler for capturing errors in the try catch clause

EXEC custom.[error_handler_sp]

Comments
2019-02-28	MDunn		Created


**************************************************************************************/



CREATE PROCEDURE [custom].[error_handler_sp] AS

DECLARE 
	@errmsg nvarchar(2048),
	@severity tinyint,
	@state tinyint,
	@errno int,
	@proc sysname,
	@lineno int

SELECT @errmsg = error_message(), @severity = ERROR_SEVERITY(),
	@state = ERROR_STATE(), @errno = ERROR_NUMBER(),
	@proc = ERROR_PROCEDURE(), @lineno = ERROR_LINE()

IF @errmsg not like '***%'
BEGIN
	SELECT @errmsg = '*** '+coalesce(QUOTENAME(@proc), '<dynamic SQL>') + ', Line '+ ltrim(str(@lineno)) + '. Errno ' + ltrim(str(@errno)) + ': ' + @errmsg
end

RAISERROR('%s', @severity, @state, @errmsg)


GO


