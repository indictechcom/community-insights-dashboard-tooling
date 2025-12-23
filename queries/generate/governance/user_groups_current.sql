SELECT
    CURDATE() AS snapshot_date,
    'tewiki' AS wiki_db,
    ug_group AS user_right,
    COUNT(DISTINCT ug_user) AS unique_users
FROM 
	user_groups
GROUP BY 
	ug_group
ORDER BY 
	unique_users DESC
;