# Daily deletions within a specific window
SELECT
   CURDATE() AS snapshot_date,
  DATE(STR_TO_DATE(LEFT(log_timestamp, 8), '%Y%m%d')) AS day,
  COUNT(*) AS deleted_page_count
FROM logging
WHERE log_type = 'delete'
  AND log_action IN ('delete','delete_redir')
  AND log_timestamp BETWEEN '20250101000000' AND '20250131235959'
GROUP BY day
ORDER BY day;