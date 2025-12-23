WITH edits AS (
  SELECT
    CURDATE() AS snapshot_date,
    'tewiki' AS wiki_db,
    DATE(rev_timestamp) AS edit_date,
    rev_id,
    CASE
      WHEN page_namespace = 0 THEN TRUE
      ELSE FALSE
    END AS is_main_ns,
    CASE
      WHEN rev_parent_id = 0 THEN TRUE
      ELSE FALSE
    END AS is_page_creation
  FROM
    revision r
  JOIN
    page p
    ON r.rev_page = p.page_id
  JOIN
    actor a
    ON r.rev_actor = a.actor_id
  LEFT JOIN
    user u
    ON a.actor_id = u.user_id
  LEFT JOIN
    user_groups ug
    ON u.user_id = ug.ug_user
  WHERE
    (ug_group != 'bot' OR ug_group IS NULL)
    AND rev_parent_id != 0
),

tags AS (
  SELECT
    e.*,
    CASE
      WHEN ctd_name = 'wikitext' THEN 'wikitext-2010'
      WHEN ctd_name = 'visualeditor-wikitext' THEN 'wikitext-2017'
      WHEN ctd_name = 'visualeditor' THEN 'visualeditor'
      WHEN ctd_name = 'mobile web edit' THEN 'mobile-web'
      WHEN ctd_name = 'mobile app edit' THEN 'mobile-app'
      WHEN ctd_name = 'mobile edit' THEN 'mobile-other'
      WHEN ctd_name = 'AWB' THEN 'auto-wiki-browser'
      WHEN ctd_name = 'twinkle' THEN 'twinkle'
      WHEN ctd_name IN ('contenttranslation', 'contenttranslation-v2') THEN 'content-translation'
      WHEN ctd_name = 'sectiontranslation' THEN 'section-translation'
      WHEN (ctd_name = 'discussiontools' OR ctd_name LIKE '%discussiontools%') THEN 'discussiontools'
      ELSE 'other'
    END AS edit_interface
  FROM
    edits e
  LEFT JOIN
    change_tag ct
    ON e.rev_id = ct.ct_rev_id
  LEFT JOIN
    change_tag_def ctd
    ON ct.ct_tag_id = ctd.ctd_id
)

SELECT
  snapshot_date,
  wiki_db,
  edit_date,
  is_main_ns,
  is_page_creation,
  edit_interface,
  COUNT(DISTINCT rev_id) AS edit_count
FROM
  tags
GROUP BY
  snapshot_date,
  wiki_db,
  edit_date,
  is_main_ns,
  is_page_creation,
  edit_interface
;