# Number of pages by namespace (Main, File, Template, Category, Draft)
WITH ns_map AS (
  SELECT 0 AS ns, 'main' AS page_type, 1 AS sort_order
  UNION ALL SELECT 6,   'file', 2
  UNION ALL SELECT 10,  'template', 3
  UNION ALL SELECT 14,  'category', 4
  UNION ALL SELECT 118, 'draft', 5
),
agg AS (
  SELECT
    p.page_namespace AS ns,
    COUNT(*) AS total_pages
  FROM page p
  WHERE p.page_namespace IN (0,6,10,14,118)
  GROUP BY p.page_namespace
)
SELECT
  m.page_type,
  COALESCE(a.total_pages, 0) AS total_pages
FROM ns_map m
LEFT JOIN agg a
  ON a.ns = m.ns
ORDER BY m.sort_order;