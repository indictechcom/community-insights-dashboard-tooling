SELECT 
    p.page_title, -- Retrives the title of the page
    p.page_len    -- Retrives the length of the page in bytes
FROM 
    page p
JOIN 
    revision r ON r.rev_page = p.page_id    
WHERE 
    p.page_namespace = 0  -- include only pages in the main namespace
    AND r.rev_timestamp >= DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 5 YEAR), '%Y%m%d%H%i%S')
GROUP BY 
    p.page_title, p.page_len;
