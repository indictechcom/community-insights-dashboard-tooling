CREATE TABLE IF NOT EXISTS top_edited_pages_daily (
    `snapshot_date`         DATE            ,
    `wiki_db`               VARCHAR(255)    ,
    `edit_date`             DATE            ,
    `page_id`               BIGINT          ,
    `page_title`            VARCHAR(255)    ,
    `edit_count`            BIGINT          ,
    PRIMARY KEY (`wiki_db`, `edit_date`, `page_id`, `snapshot_date`)
)
ENGINE=InnoDB
;
