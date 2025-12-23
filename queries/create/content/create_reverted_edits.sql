CREATE TABLE IF NOT EXISTS reverted_edits_daily (
    `snapshot_date`         DATE            ,
    `wiki_db`               VARCHAR(255)    ,
    `edit_date`             DATE            ,
    `reverted_edit_count`   BIGINT          ,
    PRIMARY KEY (`wiki_db`, `edit_date`, `snapshot_date`)
)
ENGINE=InnoDB
;
