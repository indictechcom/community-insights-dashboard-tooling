SELECT 
    CURDATE() AS snapshot_date,
    'tewiki' AS wiki_db,
    target.lt_title AS template,
    COUNT(*) AS transclusion_count
FROM 
	templatelinks tl
JOIN 
	linktarget target
    ON tl.tl_target_id = target.lt_id
WHERE
	tl_from_namespace = 0
	AND target.lt_namespace = 10
 GROUP BY
 	snapshot_date,
    wiki_db,
    template
ORDER BY
	transclusion_count DESC
; 