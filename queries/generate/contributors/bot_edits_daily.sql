WITH bot_edits AS (
  SELECT
    CURDATE() AS snapshot_date,
    {DATABASE} AS wiki_db,
    DATE(rev_timestamp) AS date,
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
    ON u.user_id = ug.ug_user
  WHERE
    ug_group = 'bot'
)

SELECT
  snapshot_date,
  wiki_db,
  date,
  COUNT(DISTINCT rev_id) AS edit_count
FROM
  bot_edits
GROUP BY
  snapshot_date,
  wiki_db,
  date
;