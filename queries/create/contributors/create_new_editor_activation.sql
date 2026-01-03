CREATE TABLE IF NOT EXISTS new_editor_activation_monthly (
    `snapshot_date`                 DATE            ,
    `wiki_db`                       VARCHAR(255)    ,
    `month`                         DATE            ,
    `total_new_user_count`          BIGINT          ,
    `activated_editor_count_1e`     BIGINT          ,
    `activated_editor_count_5e`     BIGINT          ,
    `activated_editor_pct_1e`       DECIMAL(5,4)    ,
    `activated_editor_pct_5e`       DECIMAL(5,4)    ,
    `is_latest`                     BOOLEAN         NOT NULL DEFAULT TRUE,
    PRIMARY KEY (`wiki_db`, `month`, `snapshot_date`),
    INDEX idx_latest (`is_latest`)
)
ENGINE=InnoDB
;
