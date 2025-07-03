SELECT 
    a.actor_name AS username,
    COUNT(r.rev_id) AS edits
FROM revision r
JOIN actor a ON r.rev_actor = a.actor_id
WHERE 
    STR_TO_DATE(r.rev_timestamp, '%Y%m%d%H%i%s') >= DATE_SUB(NOW(), INTERVAL 3 MONTH)
    AND a.actor_name NOT LIKE '%bot%'  -- exclude usernames like "ExampleBot", "bot123", etc.
GROUP BY a.actor_name
ORDER BY edits DESC
LIMIT 10;