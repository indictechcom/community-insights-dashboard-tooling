WITH cohort_users AS (
  SELECT
    u.user_id,
    STR_TO_DATE(CAST(u.user_registration AS CHAR), '%Y%m%d%H%i%S') AS reg_dt
  FROM user u
  WHERE u.user_registration IS NOT NULL
    AND STR_TO_DATE(CAST(u.user_registration AS CHAR), '%Y%m%d%H%i%S') >= DATE_SUB(DATE_FORMAT(CURDATE(), '%Y-%m-01'), INTERVAL 1 MONTH)
    AND STR_TO_DATE(CAST(u.user_registration AS CHAR), '%Y%m%d%H%i%S') <  DATE_FORMAT(CURDATE(), '%Y-%m-01')
),
user_edits_24h AS (
  SELECT
    cu.user_id,
    SUM(
      r.rev_timestamp >= cu.reg_dt
      AND r.rev_timestamp <  cu.reg_dt + INTERVAL 1 DAY
      AND p.page_namespace = 0
    ) AS edits_24h_ns0
  FROM cohort_users cu
  LEFT JOIN actor a
    ON a.actor_user = cu.user_id
  LEFT JOIN revision r
    ON r.rev_actor = a.actor_id
  LEFT JOIN page p
    ON p.page_id = r.rev_page
  GROUP BY cu.user_id
)
SELECT
  CURDATE() AS snapshot_date,
  'tewiki' AS wiki_db,
  DATE_SUB(DATE_FORMAT(CURDATE(), '%Y-%m-01'), INTERVAL 1 MONTH) AS registration_month,
  COUNT(*) AS total_new_users,
  SUM(edits_24h_ns0 >= 1) AS activated_editor_count_1e,
  SUM(edits_24h_ns0 >= 5) AS activated_editor_count_5e,
  ROUND(100 * SUM(edits_24h_ns0 >= 1) / COUNT(*), 2) AS activated_editor_pct_1e,
  ROUND(100 * SUM(edits_24h_ns0 >= 5) / COUNT(*), 2) AS activated_editor_pct_5e
FROM user_edits_24h
;