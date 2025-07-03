-- Counting the number of actors in different contribution buckets
WITH revision_buckets AS (  --A CTE using WITH
    SELECT COUNT(*), bucket 
    FROM (
        -- Subquery: Categorizing actors based on the number of revisions they made
        SELECT rev_actor,
        CASE 
            WHEN COUNT(rev_id) = 0 THEN '0'               -- No revisions
            WHEN COUNT(rev_id) BETWEEN 1 AND 5 THEN '1-5' -- Between 1 and 5 revisions
            WHEN COUNT(rev_id) BETWEEN 6 AND 99 THEN '6-99' -- Between 6 and 99 revisions
            WHEN COUNT(rev_id) BETWEEN 100 AND 999 THEN '100-999' -- Between 100 and 999 revisions
            WHEN COUNT(rev_id) BETWEEN 1000 AND 4999 THEN '1000-4999' -- Between 1000 and 4999 revisions
            ELSE '5000+' -- More than 5000 revisions
        END AS bucket
        FROM revision
        GROUP BY rev_actor -- Grouping by actor to count their revisions
    )

SELECT 
    bucket,
    COUNT(*) AS number_of_editors   -- Counting the number of actors in each bucket
FROM revision_buckets
GROUP BY bucket
ORDER BY bucket;
