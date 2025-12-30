CREATE TABLE IF NOT EXISTS ip_blocks_current (
    `snapshot_date`         DATE            ,
    `wiki_db`               VARCHAR(255)    ,
    `blocked_ip`            VARCHAR(255)    ,
    `blocked_by_user`       VARCHAR(255)    ,
    `block_start_date`      DATE            ,
    `expiry`                VARCHAR(255)    ,
    `is_latest`             BOOLEAN         NOT NULL DEFAULT TRUE,
    PRIMARY KEY (`wiki_db`, `blocked_ip`, `block_start_date`, `snapshot_date`),
    INDEX idx_latest (`is_latest`)
)
ENGINE=InnoDB
;
