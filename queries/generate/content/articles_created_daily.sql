SELECT
  CURDATE() AS snapshot_date,
  {DATABASE} AS wiki_db,
    DATE(rev_timestamp) AS date,
    COUNT(DISTINCT rev_id) AS article_count
FROM
	revision r
JOIN
	page p
    ON r.rev_page = p.page_id
WHERE
	rev_parent_id = 0
    AND page_namespace = 0
    AND NOT page_is_redirect
GROUP BY snapshot_date, wiki_db, date
ORDER BY snapshot_date, wiki_db, date