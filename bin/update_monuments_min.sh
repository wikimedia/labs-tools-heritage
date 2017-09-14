#!/bin/bash
#
# Minimal script to update the monuments database
PYWIKIBOT_BIN=/data/project/heritage/pywikibot/pwb.py
ERFGOED_PATH=/data/project/heritage/erfgoedbot
DATABASE=s51138__heritage_p

# First have the erfgoed bot update everything in it's config
$PYWIKIBOT_BIN $ERFGOED_PATH/update_database.py -fullupdate

# Update the all monuments table
mysql -h tools-db $DATABASE < $ERFGOED_PATH/sql/fill_table_monuments_all.sql
