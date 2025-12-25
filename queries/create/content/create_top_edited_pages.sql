CREATE TABLE IF NOT EXISTS top_edited_pages_monthly (
    `snapshot_date`         DATE            ,
    `wiki_db`               VARCHAR(255)    ,
    `edit_month`            DATE            ,
    `page_id`               BIGINT          ,
    `page_title`            VARCHAR(255)    ,
    `edit_count`            BIGINT          ,
    `page_rank`             INT             ,
    PRIMARY KEY (`wiki_db`, `edit_month`, `page_rank`, `snapshot_date`)
)
ENGINE=InnoDB
;
