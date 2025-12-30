SELECT
  CURDATE() AS snapshot_date,
  {DATABASE} AS wiki_db,
  DATE(rev_timestamp) AS date,
  COUNT(DISTINCT rev_id) AS revert_count
FROM
  revision r
JOIN
  page p
  ON r.rev_page = p.page_id
JOIN
  change_tag ct
  ON r.rev_id = ct.ct_rev_id
JOIN
  change_tag_def ctd
  ON ct.ct_tag_id = ctd.ctd_id
WHERE
  ctd.ctd_name IN ('mw-rollback', 'mw-undo')
  AND page_namespace = 0
GROUP BY
  snapshot_date,
  wiki_db,
  date
ORDER BY
  snapshot_date,
  wiki_db,
  date
;