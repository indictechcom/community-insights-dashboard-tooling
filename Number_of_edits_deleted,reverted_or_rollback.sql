
/* For getting deleted edits we use archieve table 
   For getting reverted or rollback edits we use comment table in that comment_text contains the strings revert or rollback */

SELECT 
    (SELECT COUNT(*) 
     FROM archive -- For deleted edits we use archieve table 
     WHERE LEFT(ar_timestamp, 8) BETWEEN '20230301' AND '20231212') AS deleted_edits,  -- Filtering between specific dates 

    (SELECT COUNT(*) 
     FROM revision r -- For reverted or rollback edits we use comment table
     JOIN comment c ON r.rev_comment_id = c.comment_id
     WHERE LEFT(r.rev_timestamp, 8) BETWEEN '20230301' AND '20231212' -- Filtering between specific dates 
       AND (c.comment_text LIKE '%revert%' 
         OR c.comment_text LIKE '%rollback%' 
         OR c.comment_text LIKE '%undid%')) AS reverted_edits; -- Comparing strings i.e revert or rollback with column comment_text