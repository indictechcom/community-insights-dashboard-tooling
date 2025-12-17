SELECT
    DATE(ar_timestamp) AS Deletion_Date,             -- Extracts the date for dashboard filtering
    COUNT(ar_id) AS deleted_pages                    -- Counts the number of deleted pages per day
FROM
    archive                                          -- Table containing records of deleted pages
GROUP BY
    Deletion_Date                                    -- Groups the counts by day
ORDER BY
    Deletion_Date;                                   -- Sorts the results by date
