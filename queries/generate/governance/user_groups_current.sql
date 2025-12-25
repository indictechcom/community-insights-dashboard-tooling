SELECT
  CURDATE() AS snapshot_date,
  {DATABASE} AS wiki_db,
  ug_group AS user_right,
  COUNT(DISTINCT ug_user) AS user_count
FROM
  user_groups
GROUP BY
  snapshot_date,
  wiki_db,
  ug_group
ORDER BY
  user_count DESC
;