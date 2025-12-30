CREATE TABLE IF NOT EXISTS namespace_pages_current (
    `snapshot_date`         DATE            ,
    `wiki_db`               VARCHAR(255)    ,
    `namespace`             VARCHAR(255)    ,
    `page_count`            BIGINT          ,
    `is_latest`             BOOLEAN         NOT NULL DEFAULT TRUE,
    PRIMARY KEY (`wiki_db`, `namespace`, `snapshot_date`),
    INDEX idx_latest (`is_latest`)
)
ENGINE=InnoDB
;
