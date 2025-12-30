CREATE TABLE IF NOT EXISTS page_deletions_daily (
    `snapshot_date`         DATE            ,
    `wiki_db`               VARCHAR(255)    ,
    `date`                  DATE            ,
    `page_creation_date`    DATE            ,
    `deleted_page_count`    BIGINT          ,
    `is_latest`             BOOLEAN         NOT NULL DEFAULT TRUE,
    PRIMARY KEY (`wiki_db`, `date`, `page_creation_date`, `snapshot_date`),
    INDEX idx_latest (`is_latest`)
)
ENGINE=InnoDB
;
