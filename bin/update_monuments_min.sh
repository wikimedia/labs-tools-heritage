#!/bin/bash
#
# Minimal script to update the monuments database

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $CURRENT_DIR/defaults.sh

# First have the erfgoed bot update everything in it's config
$PYWIKIBOT_BIN $ERFGOED_PATH/update_database.py -fullupdate

# Update the all monuments table
$MYSQL_BIN -h $DB_SERVER $DATABASE < $ERFGOED_PATH/sql/fill_table_monuments_all.sql
