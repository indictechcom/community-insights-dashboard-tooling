# Top edited content pages for the selected time range
SELECT 
    DATE(r.rev_timestamp) AS edit_date,
    p.page_id, 
    p.page_title, 
    COUNT(DISTINCT r.rev_id) AS edit_count
FROM revision r
JOIN page p ON r.rev_page = p.page_id
WHERE p.page_namespace = 0
GROUP BY DATE(r.rev_timestamp), p.page_id, p.page_title
ORDER BY edit_count DESC, edit_date DESC
LIMIT 10;
