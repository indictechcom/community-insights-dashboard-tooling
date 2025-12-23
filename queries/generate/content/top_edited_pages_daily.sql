SELECT
	CURDATE() AS snapshot_date,
    'tewiki' AS wiki_db,
    DATE(r.rev_timestamp) AS edit_date,
    p.page_id, 
    p.page_title, 
    COUNT(DISTINCT r.rev_id) AS edit_count
FROM revision r
JOIN page p ON r.rev_page = p.page_id
WHERE p.page_namespace = 0
GROUP BY snapshot_date, wiki_db, edit_date, p.page_id, p.page_title
;