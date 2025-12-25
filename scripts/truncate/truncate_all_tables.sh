#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

CNF_PATH="$HOME/replica.my.cnf"
SQL_FILE="$REPO_ROOT/queries/truncate/truncate_all_tables.sql"

DATABASE="s57262__indic_community_insights_p"
HOST="tools.db.svc.wikimedia.cloud"

echo "warning: this will delete all data from all the tables."
echo "database: $DATABASE"
echo ""
read -p "are you sure you want to continue? (yes/no): " response

if [ "$response" = "yes" ]; then
    mariadb --defaults-file="$CNF_PATH" -h "$HOST" "$DATABASE" < "$SQL_FILE" && \
    echo "all tables truncated successfully in $DATABASE."
else
    echo "truncation cancelled."
fi
