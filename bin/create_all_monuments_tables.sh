#!/bin/bash
# Script to create all the tables from scratch

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $CURRENT_DIR/defaults.sh

# The python script expects to be in it's own directory:
cd $ERFGOED_PATH || exit

# First create the sql statements
python $ERFGOED_PATH/monument_tables.py
python $ERFGOED_PATH/fill_table_monuments_all.py
for i in $ERFGOED_PATH/sql/create_table_monuments*; do
    echo "$i"
    $MYSQL_BIN -h $DB_SERVER $DATABASE < "$i"
done
for i in $ERFGOED_PATH/sql/create_table_wlpa_*; do
    echo "$i"
    $MYSQL_BIN -h $DB_SERVER $DATABASE < "$i"
done
# Admin tree for browsing ISO codes
$MYSQL_BIN -h $DB_SERVER $DATABASE < $ERFGOED_PATH/sql/create_table_admin_tree.sql
# Something with commonscat
$MYSQL_BIN -h $DB_SERVER $DATABASE < $ERFGOED_PATH/sql/create_table_commonscat.sql
# Tracking the images table
$MYSQL_BIN -h $DB_SERVER $DATABASE < $ERFGOED_PATH/sql/create_table_image.sql
