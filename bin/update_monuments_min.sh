#!/bin/bash
#
# Minimal script to update the monuments database

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $CURRENT_DIR/defaults.sh

# Use a virtual environment with our requirements
source $VIRTUAL_ENV_PATH/bin/activate

# First have the erfgoed bot update everything in it's config
$PYWIKIBOT_BIN $ERFGOED_PATH/update_database.py -fullupdate

# Update the all monuments table
$MYSQL_BIN -h $DB_SERVER $DATABASE < $ERFGOED_PATH/sql/fill_table_monuments_all.sql
