CREATE TABLE IF NOT EXISTS editor_user_counts_by_project_daily (
    `snapshot_date`         DATE            ,
    `wiki_db`               VARCHAR(255)    ,
    `date`                  DATE            ,
    `page_type`             VARCHAR(255)     ,
    `activity_level`        VARCHAR(255)     ,
    `editor_count`          BIGINT          ,
    `is_latest`             BOOLEAN         NOT NULL DEFAULT TRUE,
    PRIMARY KEY (`wiki_db`, `date`, `page_type`, `activity_level`, `snapshot_date`),
    INDEX idx_latest (`is_latest`)
)
ENGINE=InnoDB
;