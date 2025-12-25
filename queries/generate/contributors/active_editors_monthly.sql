SELECT
  CURDATE() AS snapshot_date,
  {DATABASE} AS wiki_db,
  CONCAT(
    edit_year, '-',
    IF(edit_month < 10, CONCAT('0', edit_month), edit_month),
    '-01'
  ) AS month,
  COUNT(DISTINCT actor_user) AS active_editor_count
FROM (
  SELECT
    YEAR(r.rev_timestamp) AS edit_year,
    MONTH(r.rev_timestamp) AS edit_month,
    a.actor_user
  FROM
    revision r
  JOIN
    page p
    ON p.page_id = r.rev_page
  JOIN
    actor a
    ON a.actor_id = r.rev_actor
  JOIN
    user u
    ON u.user_id = a.actor_user
  WHERE
    p.page_namespace = 0
    AND a.actor_user IS NOT NULL
    AND r.rev_timestamp >= DATE_SUB(NOW(), INTERVAL 1 YEAR)
    AND NOT EXISTS (
      SELECT 1
      FROM user_groups ug
      WHERE ug.ug_user = u.user_id
        AND ug.ug_group = 'bot'
    )
  GROUP BY
    YEAR(r.rev_timestamp),
    MONTH(r.rev_timestamp),
    a.actor_user
  HAVING
    COUNT(*) >= 5
) AS filtered_editors
GROUP BY
  CONCAT(
    edit_year, '-',
    IF(edit_month < 10, CONCAT('0', edit_month), edit_month),
    '-01'
  )
ORDER BY
  month
;