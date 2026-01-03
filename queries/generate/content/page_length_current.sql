SELECT
  CURDATE() AS snapshot_date,
  {DATABASE} AS wiki_db,
  CASE
    WHEN page_namespace = 0 THEN 'article'
    WHEN page_namespace = 1 THEN 'article_talk'
    WHEN page_namespace = 118 THEN 'draft'
    WHEN page_namespace = 119 THEN 'draft_talk'
  END AS namespace,
  CASE
    WHEN page_len BETWEEN 0 AND 2000 THEN '0-2000'
    WHEN page_len BETWEEN 2001 AND 5000 THEN '2001-5000'
    WHEN page_len BETWEEN 5001 AND 10000 THEN '5001-10000'
    WHEN page_len BETWEEN 10001 AND 20000 THEN '10001-20000'
    WHEN page_len BETWEEN 20001 AND 30000 THEN '20001-30000'
    WHEN page_len BETWEEN 30001 AND 40000 THEN '30001-40000'
    WHEN page_len BETWEEN 40001 AND 50000 THEN '40001-50000'
    WHEN page_len BETWEEN 50001 AND 75000 THEN '50001-75000'
    WHEN page_len BETWEEN 75001 AND 100000 THEN '75001-100000'
    WHEN page_len > 100000 THEN '100000+'
  END AS length_bucket,
  COUNT(*) AS page_count
FROM
  page
WHERE
  page_namespace IN (0, 1, 118, 119)
GROUP BY
  wiki_db,
  namespace,
  length_bucket
ORDER BY
  wiki_db,
  CASE namespace
    WHEN 'article' THEN 1
    WHEN 'article_talk' THEN 2
    WHEN 'draft' THEN 3
    WHEN 'draft_talk' THEN 4
  END,
  CASE length_bucket
    WHEN '0-2000' THEN 1
    WHEN '2001-5000' THEN 2
    WHEN '5001-10000' THEN 3
    WHEN '10001-20000' THEN 4
    WHEN '20001-30000' THEN 5
    WHEN '30001-40000' THEN 6
    WHEN '40001-50000' THEN 7
    WHEN '50001-75000' THEN 8
    WHEN '75001-100000' THEN 9
    WHEN '100000+' THEN 10
  END
;