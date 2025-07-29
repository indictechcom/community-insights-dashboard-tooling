SELECT 
    YEAR(STR_TO_DATE(r.rev_timestamp, '%Y%m%d%H%i%s')) AS edit_year, 
    COUNT(DISTINCT a.actor_user) AS active_editors  -- Count unique editors
FROM revision r
JOIN actor a ON r.rev_actor = a.actor_id -- Link revisions to users
GROUP BY edit_year
HAVING edit_year >= YEAR(DATE_SUB(NOW(), INTERVAL 3 YEAR))  -- Rolling YoY filter
ORDER BY edit_year DESC;
