WITH user_edit_counts AS (
    -- Count the total number of edits per user in the last 30 days
    SELECT a.actor_user AS user_id, COUNT(*) AS edit_count
    FROM revision r
    JOIN actor a ON r.rev_actor = a.actor_id
    -- Filter to only include edits made in the last 30 days
    WHERE r.rev_timestamp >= NOW() - INTERVAL 30 DAY
    -- Group by user to count their total edits
    GROUP BY a.actor_user
)
SELECT 
  
    -- Count users who made at least 1 edit in the last 30 days
    SUM(CASE WHEN edit_count >= 1 THEN 1 ELSE 0 END) AS users_edited_1_edit,

    -- Count users who made at least 5 edits in the last 30 days
    SUM(CASE WHEN edit_count >= 5 THEN 1 ELSE 0 END) AS users_edited_5_edits
FROM user_edit_counts;