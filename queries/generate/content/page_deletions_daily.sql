SELECT
  CURDATE() AS snapshot_date,
  'tewiki' AS wiki_db,
  DATE(log_timestamp) AS deletion_date,
  DATE(ar_timestamp) AS page_creation_date,
  COUNT(DISTINCT ar_page_id) AS deleted_page_count
FROM
  logging
JOIN
  archive
  ON log_title = ar_title
  AND log_timestamp > ar_timestamp
WHERE
  log_type = 'delete'
  AND log_action = 'delete'
  AND ar_parent_id = 0
  AND ar_namespace = 0
GROUP BY
  snapshot_date,
  wiki_db,
  deletion_date,
  page_creation_date
;