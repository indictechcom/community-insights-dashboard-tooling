WITH new_user_edit_counts AS (
    -- Get users who registered in the last 30 days and count ALL their edits
    SELECT 
        u.user_id,
        u.user_registration,
        COALESCE(COUNT(r.rev_id), 0) AS edit_count
    FROM user u
    LEFT JOIN actor a ON u.user_id = a.actor_user
    LEFT JOIN revision r ON a.actor_id = r.rev_actor
    -- Filter to only include users who registered in the last 30 days
    WHERE u.user_registration >= NOW() - INTERVAL 30 DAY
    -- Group by user to count their total edits
    GROUP BY u.user_id, u.user_registration
)
SELECT 
    -- Total number of new users (registered in last 30 days)
    COUNT(*) AS total_new_users,
    -- Count new users who made at least 1 edit
    SUM(CASE WHEN edit_count >= 1 THEN 1 ELSE 0 END) AS new_users_with_1_edit,
    -- Count new users who made at least 5 edits  
    SUM(CASE WHEN edit_count >= 5 THEN 1 ELSE 0 END) AS new_users_with_5_edits,
    -- Calculate activation percentages
    ROUND(
        (SUM(CASE WHEN edit_count >= 1 THEN 1 ELSE 0 END) * 100.0) / COUNT(*), 
        2
    ) AS activation_rate_1_edit_percent
FROM new_user_edit_counts;