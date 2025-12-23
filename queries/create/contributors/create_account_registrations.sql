CREATE TABLE IF NOT EXISTS account_registrations_daily (
    `snapshot_date`         DATE            ,
    `wiki_db`               VARCHAR(255)    ,
    `registration_date`     DATE            ,
    `user_count`            BIGINT          ,
    PRIMARY KEY (`wiki_db`, `registration_date`, `snapshot_date`)
)
ENGINE=InnoDB
;
