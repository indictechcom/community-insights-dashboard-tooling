SELECT
  CURDATE() AS snapshot_date,
  'tewiki' AS wiki_db,
  DATE(r.rev_timestamp) AS edit_date,
  CASE p.page_namespace
    WHEN 1 THEN 'article_talk'
    WHEN 3 THEN 'user_talk'
    WHEN 5 THEN 'project_talk'
  END AS namespace,
  COUNT(*) AS edit_count
FROM
  revision r
JOIN
  page p
  ON p.page_id = r.rev_page
WHERE
  p.page_namespace IN (1, 3, 5)
GROUP BY
  DATE(r.rev_timestamp),
  p.page_namespace
ORDER BY
  edit_date,
  namespace
;