#!/bin/bash
# wait-for-db.sh

set -e

function wait_for_database {
    set +e
    for try in {1..60} ; do
        python -c "from erfgoedbot.database_connection import connect_to_monuments_database; connect_to_monuments_database()" > /dev/null 2>&1 && break
        echo "Waiting for database to respond..."
        sleep 1
    done
}

wait_for_database

exec "$@"
