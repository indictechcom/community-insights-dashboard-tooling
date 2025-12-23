SELECT
  CURDATE() AS snapshot_date,
  'tewiki' AS wiki_db,
  DATE(user_registration) AS registration_date,
  COUNT(DISTINCT user_id) AS user_count
FROM
  user u
LEFT JOIN
  user_groups ug
  ON u.user_id = ug.ug_user
WHERE
  (ug_group != 'bot' OR ug_group IS NULL)
  AND NOT user_registration IS NULL
GROUP BY
  snapshot_date,
  wiki_db,
  registration_date
;