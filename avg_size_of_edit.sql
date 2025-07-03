SELECT
  CASE
    WHEN user_edits.edit_count BETWEEN 1 AND 10 THEN '1–10'
    WHEN user_edits.edit_count BETWEEN 11 AND 50 THEN '11–50'
    WHEN user_edits.edit_count BETWEEN 51 AND 100 THEN '51–100'
    WHEN user_edits.edit_count BETWEEN 101 AND 500 THEN '101–500'
    WHEN user_edits.edit_count BETWEEN 501 AND 1000 THEN '501–1000'
    ELSE '1001+'
  END AS edit_count_bucket,
  AVG(ABS(CAST(r.rev_len AS SIGNED) - CAST(p.rev_len AS SIGNED))) AS avg_edit_size
FROM revision r
JOIN revision p ON r.rev_parent_id = p.rev_id
JOIN (
  SELECT rev_actor, COUNT(*) AS edit_count   # number of edits done by user
  FROM revision
  GROUP BY rev_actor
) AS user_edits ON r.rev_actor = user_edits.rev_actor
GROUP BY edit_count_bucket
;
