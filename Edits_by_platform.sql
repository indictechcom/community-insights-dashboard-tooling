SELECT 
    -- Categorize the edits based on the platform: desktop, mobile web, mobile app
    CASE 
        WHEN ctd.ctd_name IN ('mobile app edit', 'android app edit', 'ios app edit', 'advanced app edit') THEN 'mobile app'
        WHEN ctd.ctd_name = 'mobile edit' THEN 'mobile web'
        ELSE 'desktop'
    END AS platform,
    COUNT(DISTINCT r.rev_id) AS edit_count   -- Count number of edits per platform
FROM 
    change_tag ct
JOIN 
    change_tag_def ctd ON ct.ct_tag_id = ctd.ctd_id    -- Link tags with their definitions
LEFT JOIN
    revision r ON ct.ct_rev_id = r.rev_id
WHERE 
    ctd.ctd_name IN ('mobile edit', 'mobile app edit', 'android app edit', 'ios app edit', 'advanced app edit', 'visual editor', 'visualeditor-wikitext', 'wikieditor')
GROUP BY 
    platform
