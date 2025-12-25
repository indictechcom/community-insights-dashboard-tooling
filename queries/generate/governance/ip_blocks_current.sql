SELECT
  CURDATE() AS snapshot_date,
  {DATABASE} AS wiki_db,
  CASE
    WHEN bt.bt_range_start IS NOT NULL THEN
      CONCAT(
        INET_NTOA(CAST(CONV(bt.bt_range_start, 16, 10) AS UNSIGNED)),
        ' - ',
        INET_NTOA(CAST(CONV(bt.bt_range_end, 16, 10) AS UNSIGNED))
      )
    ELSE
      INET_NTOA(CAST(CONV(bt.bt_ip_hex, 16, 10) AS UNSIGNED))
  END AS blocked_ip,
  a.actor_name AS blocked_by_user,
  DATE(b.bl_timestamp) AS block_start_date,
  CASE
  	WHEN b.bl_expiry = 'infinity' THEN bl_expiry
    ELSE DATE(b.bl_expiry)
   END AS expiry
FROM 
	block AS b
JOIN 
	block_target AS bt 
    ON b.bl_target = bt.bt_id
LEFT JOIN 
	actor AS a 
    ON a.actor_id = b.bl_by_actor
WHERE 
	bt.bt_user IS NULL
  	AND (bt.bt_ip_hex != 0 OR bt.bt_range_start != 0)
  	AND (b.bl_expiry = 'infinity' OR b.bl_expiry > NOW())
ORDER BY 
	b.bl_timestamp;