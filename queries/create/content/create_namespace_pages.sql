CREATE TABLE IF NOT EXISTS namespace_pages_current (
    `snapshot_date`         DATE            ,
    `wiki_db`               VARCHAR(255)    ,
    `namespace`             VARCHAR(255)    ,
    `page_count`            BIGINT          ,
    PRIMARY KEY (`wiki_db`, `namespace`, `snapshot_date`)
)
ENGINE=InnoDB
;
