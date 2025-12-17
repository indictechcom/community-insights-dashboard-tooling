SELECT
    DATE(r.rev_timestamp) AS Edit_Date,              -- Extract the date for filtering on the dashboard
    COUNT(DISTINCT r.rev_id) AS Automated_Edits      -- Count distinct edits to avoid duplicates
FROM
    revision AS r
JOIN
    actor AS a ON r.rev_actor = a.actor_id           -- Join to identify the editor (actor)
JOIN
    user_groups AS ug ON a.actor_user = ug.ug_user   -- Join to access user group information
WHERE
    ug.ug_group = 'bot'                              -- Filter for edits made only by bots
GROUP BY
    Edit_Date                                        -- Group results by date
ORDER BY
    Edit_Date;                                       -- Sort the results chronologically
