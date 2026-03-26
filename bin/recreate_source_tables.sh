#!/bin/bash
#
# Recreate the source tables

set -o errexit
set -o pipefail
set -o nounset

CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. $CURRENT_DIR/defaults.sh

count=$(ls -1 $ERFGOED_PATH/sql/create_table_monuments* | wc -l)

if [ "$RECREATE_TABLES" = true ]; then
    echo_time "Recreating the $count source tables..."
    for i in $ERFGOED_PATH/sql/create_table_monuments*; do
        $MYSQL_BIN -h $DB_SERVER $DATABASE <"$i"
    done
    echo_time "Done recreating $count source tables!"
else
    echo_time "Skipping recreation of $count source tables."
fi
