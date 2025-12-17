SELECT
    DATE(r.rev_timestamp) AS Edit_Date,              -- Extracts the date for dashboard filtering
    COUNT(DISTINCT r.rev_id) AS reverted_edits       -- Counts the number of unique reverted edits
FROM
    revision AS r
JOIN
    change_tag AS ct ON r.rev_id = ct.ct_rev_id      -- Links revisions to their associated tags
JOIN
    change_tag_def AS ctd ON ct.ct_tag_id = ctd.ctd_id -- Gets the name of the tag
WHERE
    ctd.ctd_name IN ('mw-reverted', 'mw-rollback', 'mw-undo') -- Filters for specific revert, rollback, and undo tags
GROUP BY
    Edit_Date                                        -- Groups the daily counts
ORDER BY
    Edit_Date;                                       -- Sorts the results chronologically
