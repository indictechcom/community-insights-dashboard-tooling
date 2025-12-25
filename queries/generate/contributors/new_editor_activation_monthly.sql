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
activated_users AS (
  SELECT DISTINCT
    nu.user_id
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
)
SELECT
  CURDATE() AS snapshot_date,
  {DATABASE} AS wiki_db,
  DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y-%m-01') AS month,
  COUNT(DISTINCT nu.user_id) AS total_new_users,
  COUNT(DISTINCT au.user_id) AS users_with_ns0_edits_24h,
  ROUND(100 * COUNT(DISTINCT au.user_id) / COUNT(DISTINCT nu.user_id), 2) AS activation_rate
FROM
  new_users nu
  LEFT JOIN activated_users au ON au.user_id = nu.user_id
;