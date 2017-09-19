#!/bin/bash
# Script to create all the tables from scratch

ERFGOED_PATH=/data/project/heritage/erfgoedbot
DATABASE=s51138__heritage_p

# The python script expects to be in it's own directory:
cd $ERFGOED_PATH || exit
# First create the sql statements
python $ERFGOED_PATH/monument_tables.py
python $ERFGOED_PATH/fill_table_monuments_all.py
for i in $ERFGOED_PATH/sql/create_table_monuments*; do
    echo "$i"
    mysql -h tools-db $DATABASE < "$i"
done
for i in $ERFGOED_PATH/sql/create_table_wlpa_*; do
    echo "$i"
    mysql -h tools-db $DATABASE < "$i"
done
# Admin tree for browsing ISO codes
mysql -h tools-db $DATABASE < $ERFGOED_PATH/sql/create_table_admin_tree.sql
# Something with commonscat
mysql -h tools-db $DATABASE < $ERFGOED_PATH/sql/create_table_commonscat.sql
# Tracking the images table
mysql -h tools-db $DATABASE < $ERFGOED_PATH/sql/create_table_image.sql
