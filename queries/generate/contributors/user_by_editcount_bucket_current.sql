WITH bucketing AS (
  SELECT
    CURDATE() AS snapshot_date,
    {DATABASE} AS wiki_db,
    user_id,
    CASE
      WHEN user_editcount = 0 THEN '0'
      WHEN user_editcount BETWEEN 1 AND 5 THEN '1-5'
      WHEN user_editcount BETWEEN 6 AND 99 THEN '6-99'
      WHEN user_editcount BETWEEN 100 AND 999 THEN '100-999'
      WHEN user_editcount BETWEEN 1000 AND 4999 THEN '1000-4999'
      WHEN user_editcount >= 5000 THEN '5000+'
    END AS user_editcount_bucket
  FROM
    user u
  LEFT JOIN
    user_groups ug
    ON u.user_id = ug.ug_user
  WHERE
    (ug_group != 'bot' OR ug_group IS NULL)
)

SELECT
  snapshot_date,
  wiki_db,
  user_editcount_bucket,
  COUNT(DISTINCT user_id) AS user_count
FROM
  bucketing
GROUP BY
  snapshot_date,
  wiki_db,
  user_editcount_bucket
ORDER BY
  CASE
    WHEN user_editcount_bucket = '0' THEN 1
    WHEN user_editcount_bucket = '1-5' THEN 2
    WHEN user_editcount_bucket = '6-99' THEN 3
    WHEN user_editcount_bucket = '100-999' THEN 4
    WHEN user_editcount_bucket = '1000-4999' THEN 5
    WHEN user_editcount_bucket = '5000+' THEN 6
  END
;