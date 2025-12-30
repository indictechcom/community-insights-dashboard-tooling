CREATE TABLE IF NOT EXISTS top_edited_pages_monthly (
    `snapshot_date`         DATE            ,
    `wiki_db`               VARCHAR(255)    ,
    `month`                 DATE            ,
    `page_id`               BIGINT          ,
    `page_title`            VARCHAR(255)    ,
    `edit_count`            BIGINT          ,
    `page_rank`             INT             ,
    `is_latest`             BOOLEAN         NOT NULL DEFAULT TRUE,
    PRIMARY KEY (`wiki_db`, `month`, `page_rank`, `snapshot_date`),
    INDEX idx_latest (`is_latest`)
)
ENGINE=InnoDB
;
