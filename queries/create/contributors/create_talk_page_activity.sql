CREATE TABLE IF NOT EXISTS talk_page_activity_daily (
    `snapshot_date`         DATE            ,
    `wiki_db`               VARCHAR(255)    ,
    `edit_date`             DATE            ,
    `namespace`             VARCHAR(255)    ,
    `edit_count`            BIGINT          ,
    PRIMARY KEY (`wiki_db`, `edit_date`, `namespace`, `snapshot_date`)
)
ENGINE=InnoDB
;
