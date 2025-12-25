#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for script in "$SCRIPT_DIR"/create_*.sh; do
    if [ "$(basename "$script")" != "create_all_tables.sh" ]; then
        bash "$script"
    fi
done
