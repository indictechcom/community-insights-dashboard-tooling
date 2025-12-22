-- Top 10 non-bot registered users for the selected time period last 3 months
SELECT 
	a.actor_name AS username, 
    COUNT(*) AS edit_count
FROM recentchanges rc
JOIN actor a ON rc.rc_actor = a.actor_id
WHERE rc.rc_bot = 0  
AND rc.rc_timestamp >= DATE_FORMAT(NOW() - INTERVAL 3 MONTH, '%Y%m%d%H%i%s')
GROUP BY a.actor_name
ORDER BY edit_count DESC
LIMIT 10;