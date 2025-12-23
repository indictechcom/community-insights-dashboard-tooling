CREATE TABLE IF NOT EXISTS user_by_editcount_bucket_current (
    `snapshot_date`             DATE            ,
    `wiki_db`                   VARCHAR(255)    ,
    `user_editcount_bucket`     VARCHAR(255)    ,
    `user_count`                BIGINT          ,
    PRIMARY KEY (`wiki_db`, `user_editcount_bucket`, `snapshot_date`)
)
ENGINE=InnoDB
;
