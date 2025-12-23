CREATE TABLE IF NOT EXISTS outdated_pages_current (
    `snapshot_date`                     DATE            ,
    `wiki_db`                           VARCHAR(255)    ,
    `namespace`                         VARCHAR(255)    ,
    `total_page_count`                  BIGINT          ,
    `outdated_page_count`               BIGINT          ,
    `outdated_page_count_post_24h`      BIGINT          ,
    `outdated_page_count_post_1w`       BIGINT          ,
    PRIMARY KEY (`wiki_db`, `namespace`, `snapshot_date`)
)
ENGINE=InnoDB
;
