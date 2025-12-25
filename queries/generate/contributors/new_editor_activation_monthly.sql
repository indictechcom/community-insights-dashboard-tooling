WITH date_params AS (
  SELECT
    DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y%m01000000') AS month_start,
    DATE_FORMAT(CURDATE(), '%Y%m01000000') AS month_end
),
new_users AS (
  SELECT
    u.user_id,
    u.user_registration,
    DATE_FORMAT(DATE_ADD(u.user_registration, INTERVAL 1 DAY), '%Y%m%d%H%i%s') AS reg_plus_24h
  FROM
    user u,
    date_params dp
  WHERE
    u.user_registration >= dp.month_start
    AND u.user_registration < dp.month_end
    AND u.user_registration IS NOT NULL
),
user_edit_counts AS (
  SELECT
    nu.user_id,
    COUNT(r.rev_id) AS edit_count
  FROM
    new_users nu
  JOIN
    actor a ON a.actor_user = nu.user_id
  JOIN
    revision r ON r.rev_actor = a.actor_id
  JOIN
    page p ON p.page_id = r.rev_page
  WHERE
    p.page_namespace = 0
    AND r.rev_timestamp >= nu.user_registration
    AND r.rev_timestamp < nu.reg_plus_24h
  GROUP BY
    nu.user_id
)
SELECT
  CURDATE() AS snapshot_date,
  {DATABASE} AS wiki_db,
  DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y-%m-01') AS month,
  COUNT(DISTINCT nu.user_id) AS total_new_user_count,
  COUNT(DISTINCT CASE WHEN uec.edit_count >= 1 THEN uec.user_id END) AS activated_editor_count_1e,
  COUNT(DISTINCT CASE WHEN uec.edit_count >= 5 THEN uec.user_id END) AS activated_editor_count_5e,
  ROUND(100 * COUNT(DISTINCT CASE WHEN uec.edit_count >= 1 THEN uec.user_id END) / COUNT(DISTINCT nu.user_id), 2) AS activated_editor_pct_1e,
  ROUND(100 * COUNT(DISTINCT CASE WHEN uec.edit_count >= 5 THEN uec.user_id END) / COUNT(DISTINCT nu.user_id), 2) AS activated_editor_pct_5e
FROM
  new_users nu
  LEFT JOIN user_edit_counts uec ON uec.user_id = nu.user_id
;