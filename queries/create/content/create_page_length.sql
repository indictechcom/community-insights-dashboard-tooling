CREATE TABLE IF NOT EXISTS page_length_current (
    `snapshot_date`         DATE            ,
    `wiki_db`               VARCHAR(255)    ,
    `namespace`             VARCHAR(255)    ,
    `length_bucket`         VARCHAR(50)     ,
    `page_count`            BIGINT          ,
    `is_latest`             BOOLEAN         NOT NULL DEFAULT TRUE,
    PRIMARY KEY (`wiki_db`, `namespace`, `length_bucket`, `snapshot_date`),
    INDEX idx_latest (`is_latest`)
)
ENGINE=InnoDB
;
