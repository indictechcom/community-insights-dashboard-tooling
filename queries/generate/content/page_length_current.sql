# Distribution of page lengths in content namespace
WITH type_map AS (
  SELECT 0 AS ns, 'main' AS page_type, 1 AS sort_order
  UNION ALL SELECT 1, 'talk', 2
  UNION ALL SELECT 118, 'draft', 3
  UNION ALL SELECT 119, 'draft talk', 4
),
first_rev AS (
  SELECT rev_page, MIN(rev_timestamp) AS creation_ts
  FROM revision
  GROUP BY rev_page
),
agg AS (
  SELECT
    p.page_namespace AS ns,
    COUNT(DISTINCT p.page_id) AS unique_pages,
    COUNT(DISTINCT p.page_title) AS unique_titles,
    SUM(p.page_len) AS total_page_len,
    AVG(p.page_len) AS avg_page_len,
    MIN(p.page_len) AS min_page_len,
    MAX(p.page_len) AS max_page_len
  FROM page p
  JOIN first_rev fr
    ON fr.rev_page = p.page_id
  WHERE p.page_is_redirect = 0
    AND fr.creation_ts BETWEEN '20250101000000' AND '20250131235959'
    AND p.page_namespace IN (0,1,118,119)
  GROUP BY p.page_namespace
)
SELECT
  tm.page_type,
  COALESCE(a.total_page_len, 0) AS total_page_len,
  COALESCE(a.unique_pages, 0) AS unique_pages,
  COALESCE(a.unique_titles, 0) AS unique_titles,
  a.avg_page_len,
  a.min_page_len,
  a.max_page_len
FROM type_map tm
LEFT JOIN agg a
  ON a.ns = tm.ns
ORDER BY tm.sort_order;