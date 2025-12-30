CREATE TABLE IF NOT EXISTS page_length_current (
    `snapshot_date`         DATE            ,
    `wiki_db`               VARCHAR(255)    ,
    `namespace`             VARCHAR(255)    ,
    `page_id`               BIGINT          ,
    `page_title`            VARCHAR(255)    ,
    `page_len`              BIGINT          ,
    `is_latest`             BOOLEAN         NOT NULL DEFAULT TRUE,
    PRIMARY KEY (`wiki_db`, `page_id`, `snapshot_date`),
    INDEX idx_latest (`is_latest`)
)
ENGINE=InnoDB
;
