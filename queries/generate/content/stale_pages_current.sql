# Number of pages that were never edited after creation 
WITH rev_counts AS (
  SELECT rev_page, COUNT(*) AS revs
  FROM revision
  GROUP BY rev_page
),
ns_stats AS (
  SELECT
    p.page_namespace AS ns,
    COUNT(*) AS total_pages,
    SUM(CASE WHEN COALESCE(r.revs, 0) = 1 THEN 1 ELSE 0 END) AS never_edited_pages
  FROM page p
  LEFT JOIN rev_counts r
    ON r.rev_page = p.page_id
  WHERE p.page_namespace IN (0, 118)
    AND p.page_is_redirect = 0 
  GROUP BY p.page_namespace
)
SELECT
  CASE ns WHEN 0 THEN 'main' WHEN 118 THEN 'draft' END AS page_type,
  total_pages,
  never_edited_pages,
  ROUND(100 * never_edited_pages / total_pages, 2) AS pct_never_edited
FROM ns_stats
UNION ALL
SELECT
  'all (main+draft)' AS page_type,
  SUM(total_pages) AS total_pages,
  SUM(never_edited_pages) AS never_edited_pages,
  ROUND(100 * SUM(never_edited_pages) / SUM(total_pages), 2) AS pct_never_edited
FROM ns_stats;