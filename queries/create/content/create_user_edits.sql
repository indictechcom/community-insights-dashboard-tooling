CREATE TABLE IF NOT EXISTS user_edits_daily (
    `snapshot_date`         DATE            ,
    `wiki_db`               VARCHAR(255)    ,
    `is_anon`               BOOLEAN         ,
    `date`                  DATE            ,
    `edit_count`            BIGINT          ,
    `is_latest`             BOOLEAN         NOT NULL DEFAULT TRUE,
    PRIMARY KEY (`wiki_db`, `date`, `is_anon`, `snapshot_date`),
    INDEX idx_latest (`is_latest`)
)
ENGINE=InnoDB
;
