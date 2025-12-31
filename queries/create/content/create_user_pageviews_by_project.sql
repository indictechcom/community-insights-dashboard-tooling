CREATE TABLE IF NOT EXISTS user_pageviews_by_project (
    `snapshot_date`         DATE            ,
    `wiki_db`               VARCHAR(255)    ,
    `access_type`           VARCHAR(255)         ,
    `date`                  DATE            ,
    `view_count`            BIGINT          ,
    `is_latest`             BOOLEAN         NOT NULL DEFAULT TRUE,
    PRIMARY KEY (`wiki_db`, `date`, `access_type`,`view_count`, `snapshot_date`),
    INDEX idx_latest (`is_latest`)
)
ENGINE=InnoDB
;
