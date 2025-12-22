WITH bot_edits AS (
  SELECT
  	DATE(rev_timestamp) AS rev_date,
  	rev_id
  FROM
  	revision r
  JOIN
	actor a
  	ON r.rev_actor = a.actor_id
  JOIN
  	user u
  	ON a.actor_id = u.user_id
  JOIN
  	user_groups ug
  	On u.user_id = ug.ug_user
  WHERE
  	ug_group = 'bot'
)

SELECT
	rev_date,
    COUNT(DISTINCT rev_id) AS automated_edit_count
FROM
	bot_edits
GROUP BY
	rev_date
;