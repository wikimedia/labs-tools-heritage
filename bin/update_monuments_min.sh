#!/bin/bash
#
# Minimal script to update the monuments database
PYWIKIBOT_BIN=/data/project/heritage/pywikibot/pwb.py
ERFGOED_PATH=/data/project/heritage/erfgoedbot

# First have the erfgoed bot update everything in it's config
$PYWIKIBOT_BIN $ERFGOED_PATH/update_database.py -fullupdate

# Update the all monuments table
mysql -h tools-db s51138__heritage_p < $ERFGOED_PATH/sql/fill_table_monuments_all.sql
