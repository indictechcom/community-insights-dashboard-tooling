CREATE TABLE IF NOT EXISTS user_groups_current (
    `snapshot_date`         DATE            ,
    `wiki_db`               VARCHAR(255)    ,
    `user_right`            VARCHAR(255)    ,
    `user_count`            BIGINT          ,
    `is_latest`             BOOLEAN         NOT NULL DEFAULT TRUE,
    PRIMARY KEY (`wiki_db`, `user_right`, `snapshot_date`),
    INDEX idx_latest (`is_latest`)
)
ENGINE=InnoDB
;
