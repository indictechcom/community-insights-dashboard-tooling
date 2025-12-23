CREATE TABLE IF NOT EXISTS most_used_templates_current (
    `snapshot_date`         DATE            COMMENT "Date on which the data was last updated on.",
    `wiki_db`               VARCHAR(255)    COMMENT "Database code of the Wikipedia",
    `template`              VARCHAR(255)    COMMENT "Name of the template",
    `transclusion_count`    BIGINT          COMMENT "Number of times the template has been transcluded",
    PRIMARY KEY (`wiki_db`, `template`, `snapshot_date`)
)
ENGINE=InnoDB
COMMENT="List of 100 most used templates by wiki"
;