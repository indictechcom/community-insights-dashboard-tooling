CREATE TABLE IF NOT EXISTS user_edits_daily (
    `snapshot_date`         DATE            ,
    `wiki_db`               VARCHAR(255)    ,
    `is_anon`               BOOLEAN         ,
    `rev_date`              DATE            ,
    `edit_count`            BIGINT          ,
    PRIMARY KEY (`wiki_db`, `rev_date`, `is_anon`, `snapshot_date`)
)
ENGINE=InnoDB
;
