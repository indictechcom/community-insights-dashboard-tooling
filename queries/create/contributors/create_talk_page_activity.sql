CREATE TABLE IF NOT EXISTS talk_page_activity_daily (
    `snapshot_date`         DATE            ,
    `wiki_db`               VARCHAR(255)    ,
    `date`                  DATE            ,
    `namespace`             VARCHAR(255)    ,
    `edit_count`            BIGINT          ,
    `is_latest`             BOOLEAN         NOT NULL DEFAULT TRUE,
    PRIMARY KEY (`wiki_db`, `date`, `namespace`, `snapshot_date`),
    INDEX idx_latest (`is_latest`)
)
ENGINE=InnoDB
;
