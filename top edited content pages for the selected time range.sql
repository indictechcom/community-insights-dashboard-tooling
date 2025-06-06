SELECT 
    p.page_id, 
    p.page_title, 
    COUNT(*) AS edit_count
FROM revision r
JOIN page p ON r.rev_page = p.page_id
WHERE r.rev_timestamp >= NOW() - INTERVAL 30 DAY
AND p.page_namespace = 0  -- Filters for content pages (namespace 0)
GROUP BY p.page_id, p.page_title
ORDER BY edit_count DESC
LIMIT 10;  -- Get the top 10 most edited pages
