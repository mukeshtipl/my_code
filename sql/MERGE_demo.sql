-- Demo for MERGE command
MERGE INTO IGACORE.IGIRETRYEVENTAUDIT as ar
USING (SELECT *
FROM (VALUES
                (627113)) t1 (EVENTID)
WHERE 1 = 1) as dm on (dm.eventid=ar.eventid )
WHEN NOT MATCHED THEN 
INSERT (EVENTID, CREATEDATE, STATE, LASTMODIFIEDDATE,SOURCETYPE) 
VALUES (627113,CURRENT_TIMESTAMP, 'Unprocessed',CURRENT_TIMESTAMP,'testfile3.txt');

