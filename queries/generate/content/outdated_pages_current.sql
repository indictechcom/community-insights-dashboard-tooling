WITH page_revisions AS (
  SELECT
    p.page_id,
    CASE
      WHEN p.page_namespace = 0 THEN 'article'
      WHEN p.page_namespace = 118 THEN 'draft'
    END AS namespace,
    COUNT(*) AS rev_count,
    MIN(r.rev_timestamp) AS min_timestamp,
    MAX(r.rev_timestamp) AS max_timestamp
  FROM
    page p
  INNER JOIN
    revision r
    ON r.rev_page = p.page_id
  WHERE
    p.page_namespace IN (0, 118)
    AND p.page_is_redirect = 0
  GROUP BY
    p.page_id,
    p.page_namespace
)
SELECT
  CURDATE() AS snapshot_date,
  {DATABASE} AS wiki_db,
  namespace,
  COUNT(*) AS total_page_count,
  SUM(CASE WHEN rev_count = 1 THEN 1 ELSE 0 END) AS outdated_page_count,
  SUM(CASE WHEN max_timestamp <= min_timestamp + INTERVAL 24 HOUR THEN 1 ELSE 0 END) AS outdated_page_count_post_24h,
  SUM(CASE WHEN max_timestamp <= min_timestamp + INTERVAL 7 DAY THEN 1 ELSE 0 END) AS outdated_page_count_post_1w
FROM
  page_revisions
GROUP BY
  namespace
;