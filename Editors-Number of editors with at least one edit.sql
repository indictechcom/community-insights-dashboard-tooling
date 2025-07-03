SELECT 
    YEAR(STR_TO_DATE(r.rev_timestamp, '%Y%m%d%H%i%s')) AS edit_year, 
    COUNT(DISTINCT a.actor_user) AS active_editors  -- Count unique editors
FROM revision r
JOIN actor a ON r.rev_actor = a.actor_id  -- Link revisions to users
WHERE STR_TO_DATE(r.rev_timestamp, '%Y%m%d%H%i%s') >= DATE_SUB(NOW(), INTERVAL 1 YEAR)  -- Rolling YoY filter
GROUP BY edit_year
HAVING active_editors >= 1  -- Ensure at least 1 editor
