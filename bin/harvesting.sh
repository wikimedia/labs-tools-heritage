#!/bin/bash
#
# Running harvesting and invoking the merge into monuments_all

set -o errexit
set -o pipefail
set -o nounset

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $CURRENT_DIR/defaults.sh

cd $SOURCE_PATH || exit
source $VIRTUAL_ENV_PATH/bin/activate
export PYTHONPATH=$SOURCE_PATH

echo_time "Starting harvesting..."
$PYWIKIBOT_BIN $ERFGOED_PATH/update_database.py $UPDATE_MONUMENTS_ARGS

echo_time "Triggering fill_table_monuments_all..."
FILL_TABLE_MONUMENTS_ALL_JOB=$(
    cat <<EOF
{
    "cmd": "./bin/fill_table_monuments_all.sh",
    "filelog": true,
    "filelog_stderr": "logs/fill_table_monuments_all.err",
    "filelog_stdout": "logs/fill_table_monuments_all.out",
    "memory": "2G",
    "name": "fill-table-monuments-all",
    "imagename": "mariadb"
}
EOF
)
curl -X 'POST' \
    $TOOLFORGE_API_FLAGS \
    $TOOLFORGE_API_JOBS_ENDPOINT \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d "$FILL_TABLE_MONUMENTS_ALL_JOB"

echo_time "Done harvesting"
