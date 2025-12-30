CREATE TABLE IF NOT EXISTS user_by_editcount_bucket_current (
    `snapshot_date`             DATE            ,
    `wiki_db`                   VARCHAR(255)    ,
    `user_editcount_bucket`     VARCHAR(255)    ,
    `user_count`                BIGINT          ,
    `is_latest`                 BOOLEAN         NOT NULL DEFAULT TRUE,
    PRIMARY KEY (`wiki_db`, `user_editcount_bucket`, `snapshot_date`),
    INDEX idx_latest (`is_latest`)
)
ENGINE=InnoDB
;
