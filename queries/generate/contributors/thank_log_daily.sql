SELECT
	CURDATE() AS snapshot_date,
    'tewiki' AS wiki_db,
	DATE(log_timestamp) AS log_date,
	COUNT(DISTINCT log_id) AS thank_count
FROM 
	logging
WHERE 
	log_type = 'thanks'
GROUP BY
	log_date
;