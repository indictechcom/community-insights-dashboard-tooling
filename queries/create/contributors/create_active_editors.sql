CREATE TABLE IF NOT EXISTS active_editors_monthly (
    `snapshot_date`         DATE            ,
    `wiki_db`               VARCHAR(255)    ,
    `month`                 DATE            ,
    `active_editor_count`   BIGINT          ,
    `is_latest`             BOOLEAN         NOT NULL DEFAULT TRUE,
    PRIMARY KEY (`wiki_db`, `month`, `snapshot_date`),
    INDEX idx_latest (`is_latest`)
)
ENGINE=InnoDB
;
