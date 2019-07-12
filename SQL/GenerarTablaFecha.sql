CREATE TABLE dim_date
(
 [date]       DATE PRIMARY KEY, 
 [year]       AS DATEPART(YEAR,     [date]),
 [month]      AS DATEPART(MONTH,    [date]),
 [MonthName]  AS DATENAME(MONTH,    [date]),
 [day]        AS DATEPART(DAY,      [date]),  
 FirstOfMonth AS CONVERT(DATE, DATEADD(MONTH, DATEDIFF(MONTH, 0, [date]), 0)),  
 FirstOfYear  AS CONVERT(DATE, DATEADD(YEAR,  DATEDIFF(YEAR,  0, [date]), 0)),
 [week]       AS DATEPART(WEEK,     [date]),
 [ISOweek]    AS DATEPART(ISO_WEEK, [date]),
 [DayOfWeek]  AS DATEPART(WEEKDAY,  [date]),
 [quarter]    AS DATEPART(QUARTER,  [date]),    
 [datekey]    AS CONVERT(CHAR(8),   [date], 112),
 [dmy]        AS CONVERT(CHAR(10),  [date], 101)
);

--Procedimiento:

TRUNCATE TABLE dim_dateSET DATEFIRST 7;
SET DATEFORMAT dmy;
SET LANGUAGE Spanish;DECLARE @StartDate DATE = '20180101' 
DECLARE @CutoffDate DATE = GETDATE()+1 INSERT dim_date([date]) 
SELECT d
FROM
(
 SELECT d = DATEADD(DAY, rn - 1, @StartDate)
 FROM 
 (
   SELECT TOP (DATEDIFF(DAY, @StartDate, @CutoffDate)) 
     rn = ROW_NUMBER() OVER (ORDER BY s1.[object_id])
   FROM sys.all_objects AS s1
   CROSS JOIN sys.all_objects AS s2
   -- on my system this would support > 5 million days
   ORDER BY s1.[object_id]
 ) AS x
) AS y;