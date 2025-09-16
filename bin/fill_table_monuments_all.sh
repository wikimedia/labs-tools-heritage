#!/bin/bash
#
# Merge all tables into monuments_all using mysql

set -o errexit
set -o pipefail
set -o nounset

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $CURRENT_DIR/defaults.sh

echo_time "Update the monuments_all table..."
SQL_FILE="$ERFGOED_PATH/sql/fill_table_monuments_all.sql"
$MYSQL_BIN -h $DB_SERVER $DATABASE < $SQL_FILE

echo_time "Triggering Python post-harvesting steps..."
curl -X 'POST' \
    $TOOLFORGE_API_FLAGS \
    $TOOLFORGE_API_JOBS_ENDPOINT \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "cmd": "./bin/post_harvesting_php.sh",
    "filelog": true,
    "filelog_stderr": "logs/post_harvesting_php.err",
    "filelog_stdout": "logs/post_harvesting_php.out",
    "memory": "2G",
    "name": "post-harvesting-php",
    "imagename": "php7.4"
}'

echo_time "Triggering PHP post-harvesting steps..."
curl -X 'POST' \
    $TOOLFORGE_API_FLAGS \
    $TOOLFORGE_API_JOBS_ENDPOINT \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "cmd": "./bin/post_harvesting_python.sh",
    "filelog": true,
    "filelog_stderr": "logs/post_harvesting_python.err",
    "filelog_stdout": "logs/post_harvesting_python.out",
    "memory": "2G",
    "name": "post-harvesting-python",
    "imagename": "python3.9"
}'

echo_time "Triggering categorization job..."
curl -X 'POST' \
    $TOOLFORGE_API_FLAGS \
    $TOOLFORGE_API_JOBS_ENDPOINT \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "cmd": "./bin/categorize_images.sh",
    "filelog": true,
    "filelog_stderr": "logs/categorize_images.err",
    "filelog_stdout": "logs/categorize_images.out",
    "memory": "2G",
    "name": "categorize-images",
    "imagename": "python3.9"
}'

echo_time "Done with fill_table_monuments_all"
