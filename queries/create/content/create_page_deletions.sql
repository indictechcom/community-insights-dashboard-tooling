CREATE TABLE IF NOT EXISTS page_deletions_daily (
    `snapshot_date`         DATE            ,
    `wiki_db`               VARCHAR(255)    ,
    `deletion_date`         DATE            ,
    `page_creation_date`    DATE            ,
    `deleted_page_count`    BIGINT          ,
    PRIMARY KEY (`wiki_db`, `deletion_date`, `page_creation_date`, `snapshot_date`)
)
ENGINE=InnoDB
;
