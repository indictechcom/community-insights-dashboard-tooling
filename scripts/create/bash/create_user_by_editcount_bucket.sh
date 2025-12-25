#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

CNF_PATH="$HOME/replica.my.cnf"
SQL_FILE="$REPO_ROOT/queries/create/contributors/create_user_by_editcount_bucket.sql"

DATABASE="s57262__indic_community_insights_p"
HOST="tools.db.svc.wikimedia.cloud"

mariadb --defaults-file="$CNF_PATH" -h "$HOST" "$DATABASE" < "$SQL_FILE" && \
echo "Table user_by_editcount_bucket_current created in $DATABASE."
