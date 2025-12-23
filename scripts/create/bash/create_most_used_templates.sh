#!/bin/bash

CNF_PATH="$HOME/replica.my.cnf"

SQL_FILE="$HOME/www/python/src/queries/create/content/create_most_used_templates.sql"

DATABASE="s57262__indic_community_insights_p"
HOST="tools.db.svc.wikimedia.cloud"

mariadb --defaults-file="$CNF_PATH" -h "$HOST" "$DATABASE" < "$SQL_FILE" && \
echo "Table most_used_templates_current created in $DATABASE."