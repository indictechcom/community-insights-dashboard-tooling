SELECT
	CURDATE() AS snapshot_date,
    {DATABASE} AS wiki_db,
    CASE
    	WHEN actor_user IS NULL THEN TRUE
        ELSE FALSE
    END AS is_anon,
    DATE(rev_timestamp) AS date,
    COUNT(DISTINCT rev_id) AS edit_count
FROM
	revision r
JOIN
	actor a
    ON r.rev_actor = a.actor_id
LEFT JOIN
	user u
    ON a.actor_user = u.user_id
LEFT JOIN
	user_groups ug
    ON u.user_id = ug.ug_user
WHERE
    NOT EXISTS (
      SELECT 1
      FROM user_groups ug
      WHERE ug.ug_user = u.user_id
        AND ug.ug_group = 'bot'
    )
GROUP BY
	snapshot_date,
    wiki_db,
    date,
    is_anon
;