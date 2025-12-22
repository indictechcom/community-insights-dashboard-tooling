# Top 25 most used templates
SELECT 
    p.page_title AS template_name,  
    COUNT(*) AS usage_count         
FROM templatelinks tl
JOIN page p 
    ON tl.tl_target_id = p.page_id  
WHERE p.page_namespace = 10         
GROUP BY p.page_title               
ORDER BY usage_count DESC          
LIMIT 25; 