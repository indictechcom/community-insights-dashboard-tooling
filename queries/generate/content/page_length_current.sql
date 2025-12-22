SELECT
    CURDATE() AS snapshot_date,
    'tewiki' AS wiki_db,
    CASE
    	WHEN page_namespace = 0 THEN 'article'
        WHEN page_namespace = 1 THEN 'article_talk'
        WHEN page_namespace = 118 THEN 'draft'
        WHEN page_namespace = 119 THEN 'draft_talk'
    END AS ns_label,
    page_id,
    page_title,
    page_len    
FROM 
	page
WHERE
	page_namespace IN (0, 1, 118, 119) 
;