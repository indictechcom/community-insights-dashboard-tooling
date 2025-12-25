WITH date_params AS (
  SELECT
    DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y%m01000000') AS month_start,
    DATE_FORMAT(CURDATE(), '%Y%m01000000') AS month_end
),
cohort_users AS (
  SELECT
    u.user_id,
    u.user_registration
  FROM
    user u,
    date_params dp
  WHERE
    u.user_registration IS NOT NULL
    AND u.user_registration >= dp.month_start
    AND u.user_registration < dp.month_end
),
user_edits_24h AS (
  SELECT
    cu.user_id,
    COUNT(CASE WHEN p.page_namespace = 0 THEN 1 END) AS edits_24h_ns0
  FROM
    cohort_users cu
  LEFT JOIN
    actor a ON a.actor_user = cu.user_id
  LEFT JOIN
    revision r ON r.rev_actor = a.actor_id
      AND r.rev_timestamp >= cu.user_registration
      AND r.rev_timestamp < DATE_ADD(cu.user_registration, INTERVAL 1 DAY)
  LEFT JOIN
    page p ON p.page_id = r.rev_page
  GROUP BY
    cu.user_id
)
SELECT
  CURDATE() AS snapshot_date,
  {DATABASE} AS wiki_db,
  DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y-%m-01') AS month,
  COUNT(*) AS total_new_user_count,
  SUM(edits_24h_ns0 >= 1) AS activated_editor_count_1e,
  SUM(edits_24h_ns0 >= 5) AS activated_editor_count_5e,
  ROUND(100 * SUM(edits_24h_ns0 >= 1) / COUNT(*), 2) AS activated_editor_pct_1e,
  ROUND(100 * SUM(edits_24h_ns0 >= 5) / COUNT(*), 2) AS activated_editor_pct_5e
FROM
  user_edits_24h
;