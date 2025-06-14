/* For getting number of edits we use revision table 
   For getting number of deleted pages we use archieve table 
   Used timestamp for filtering between specific dates */

SELECT 
    (SELECT COUNT(*) 
     FROM revision -- For edits we use revision table 
     WHERE LEFT(rev_timestamp, 8) BETWEEN '20240101' AND '20240301') AS total_edits, -- Filtered between specific dates
     
    (SELECT COUNT(*) 
     FROM archive -- For deleted pages we use archive tale 
     WHERE LEFT(ar_timestamp, 8) BETWEEN '20240101' AND '20240301') AS deleted_pages; -- Filtered between specific dates 