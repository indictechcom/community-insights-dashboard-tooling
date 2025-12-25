SELECT
  CURDATE() AS snapshot_date,
  {DATABASE} AS wiki_db,
  CASE p.page_namespace
    WHEN 0 THEN 'main'
    WHEN 6 THEN 'file'
    WHEN 10 THEN 'template'
    WHEN 14 THEN 'category'
    WHEN 118 THEN 'draft'
  END AS namespace,
  COUNT(*) AS page_count
FROM
  page p
WHERE
  p.page_namespace IN (0, 6, 10, 14, 118)
GROUP BY
  p.page_namespace
ORDER BY
  CASE p.page_namespace
    WHEN 0 THEN 1
    WHEN 6 THEN 2
    WHEN 10 THEN 3
    WHEN 14 THEN 4
    WHEN 118 THEN 5
  END
;