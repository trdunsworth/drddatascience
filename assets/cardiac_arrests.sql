USE Reporting_System;
GO

DECLARE @time1 DATETIME2;

SET @time1 = '2025-01-01 00:00:00.0000000';

SELECT Master_Incident_Number,
    Response_Date,
    Address,
    Time_PhonePickUp,
    Time_FirstCallTakingKeystroke,
    Time_CallEnteredQueue,
    Time_First_Unit_Assigned,
    Time_CallTakingComplete
FROM Response_Master_Incident
WHERE Response_Date BETWEEN DATEADD(YEAR, -5, @time1) AND @time1
    AND Problem LIKE 'CARDIAC ARREST%'
    AND Master_Incident_Number != ''
ORDER BY Response_Date;