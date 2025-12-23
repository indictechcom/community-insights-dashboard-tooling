CREATE TABLE IF NOT EXISTS thank_log_daily (
    `snapshot_date`         DATE            ,
    `wiki_db`               VARCHAR(255)    ,
    `log_date`              DATE            ,
    `thank_count`           BIGINT          ,
    PRIMARY KEY (`wiki_db`, `log_date`, `snapshot_date`)
)
ENGINE=InnoDB
;
