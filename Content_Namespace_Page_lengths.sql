SELECT 
    p.page_len AS page_length
FROM 
    page p
JOIN 
    revision r ON r.rev_page = p.page_id
WHERE 
    p.page_namespace = 0 
    AND r.rev_timestamp >= DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 5 YEAR), '%Y%m%d%H%i%S')
GROUP BY 
    p.page_len;
