SELECT 
	EXTRACT(YEAR FROM rev_timestamp) AS year,
    EXTRACT(MONTH FROM rev_timestamp) AS month,
    CASE 
    	WHEN page_namespace = 1 THEN "Article Talk"
        WHEN page_namespace = 3 THEN "User Talk"
        WHEN page_namespace = 5 AND page_title LIKE 'Village_pump%' THEN 'Village Pump'
        WHEN page_namespace = 5 THEN "Project Talk"
       
     END AS talk_page_type,
     count(*) AS edit_count
FROM revision JOIN page 
	on revision.rev_page = page.page_id
WHERE page_namespace in (1,3,5) 
GROUP BY year,month,talk_page_type
 ORDER BY year,month,talk_page_type;