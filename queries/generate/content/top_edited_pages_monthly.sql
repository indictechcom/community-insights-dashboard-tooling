WITH monthly_edits AS (
  SELECT
    DATE_FORMAT(r.rev_timestamp, '%Y-%m-01') AS month,
    p.page_id,
    p.page_title,
    COUNT(DISTINCT r.rev_id) AS edit_count
  FROM
    revision r
  JOIN
    page p ON r.rev_page = p.page_id
  WHERE
    p.page_namespace = 0
    AND r.rev_timestamp >= '20150101000000'
  GROUP BY
    month,
    p.page_id,
    p.page_title
),
ranked_pages AS (
  SELECT
    month,
    page_id,
    page_title,
    edit_count,
    ROW_NUMBER() OVER (PARTITION BY month ORDER BY edit_count DESC) AS page_rank
  FROM
    monthly_edits
)
SELECT
  CURDATE() AS snapshot_date,
  {DATABASE} AS wiki_db,
  month,
  page_id,
  page_title,
  edit_count,
  page_rank
FROM
  ranked_pages
WHERE
  page_rank <= 10
ORDER BY
  month,
  page_rank
;