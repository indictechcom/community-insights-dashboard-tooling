SELECT
    DATE(r.rev_timestamp) AS edit_date,
    COUNT(DISTINCT r.rev_id) AS affected_edits
FROM revision r
INNER JOIN page p
  	ON r.rev_page = p.page_id
LEFT JOIN change_tag ct
  	ON r.rev_id = ct.ct_rev_id
LEFT JOIN change_tag_def ctd
  	ON ct.ct_tag_id = ctd.ctd_id
WHERE
    ctd.ctd_name IN ('mw-reverted', 'mw-rollback', 'mw-undo')
GROUP BY edit_date
ORDER BY edit_date;