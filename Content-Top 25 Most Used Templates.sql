SELECT 
    p.page_title AS template_name,  -- Select the template's name
    COUNT(*) AS usage_count         -- Count how many times each template is used
FROM templatelinks tl
JOIN page p 
    ON tl.tl_target_id = p.page_id  -- Join with the 'page' table using the template's page ID
WHERE p.page_namespace = 10         -- Filter to include only pages in the 'Template' namespace (10)
GROUP BY p.page_title               -- Group by template name to count occurrences
ORDER BY usage_count DESC          
LIMIT 25;  