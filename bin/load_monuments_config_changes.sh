#!/bin/bash
#
# Recreate SQL statements for all tables (in Python)

set -o errexit
set -o pipefail
set -o nounset

CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. $CURRENT_DIR/defaults.sh

cd $SOURCE_PATH || exit
source $VIRTUAL_ENV_PATH/bin/activate
export PYTHONPATH=$SOURCE_PATH

echo_time "Recreate SQL for monument tables..."
$PYWIKIBOT_BIN $ERFGOED_PATH/monument_tables.py -log

echo_time "Recreate SQL for fill_monuments_all..."
$PYWIKIBOT_BIN $ERFGOED_PATH/fill_table_monuments_all.py -log

echo_time "Done with the SQL statement recreation!"
