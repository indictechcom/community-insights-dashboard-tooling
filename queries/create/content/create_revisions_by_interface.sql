CREATE TABLE IF NOT EXISTS revisions_by_interface_daily (
    `snapshot_date`         DATE            ,
    `wiki_db`               VARCHAR(255)    ,
    `edit_date`             DATE            ,
    `is_main_ns`            BOOLEAN         ,
    `is_page_creation`      BOOLEAN         ,
    `edit_interface`        VARCHAR(255)    ,
    `edit_count`            BIGINT          ,
    PRIMARY KEY (`wiki_db`, `edit_date`, `is_main_ns`, `is_page_creation`, `edit_interface`, `snapshot_date`)
)
ENGINE=InnoDB
;
