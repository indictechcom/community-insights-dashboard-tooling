CREATE TABLE IF NOT EXISTS reverts_daily (
    `snapshot_date`         DATE            ,
    `wiki_db`               VARCHAR(255)    ,
    `date`                  DATE            ,
    `revert_count`          BIGINT          ,
    `is_latest`             BOOLEAN         NOT NULL DEFAULT TRUE,
    PRIMARY KEY (`wiki_db`, `date`, `snapshot_date`),
    INDEX idx_latest (`is_latest`)
)
ENGINE=InnoDB
;
