#!/bin/bash

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

find "$REPO_ROOT/scripts" -type f \( -name "*.sh" -o -name "*.py" \) -exec chmod +x {} \;
