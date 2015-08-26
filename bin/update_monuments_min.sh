#!/bin/bash
#
# Minimal script to update the monuments database

# First have the erfgoed bot update everything in it's config
/data/project/heritage/pywikibot/pwb.py /data/project/heritage/erfgoedbot/update_database.py -fullupdate

# Update the all monuments table
mysql -h tools-db s51138__heritage_p sql < /data/project/heritage/erfgoedbot/sql/fill_table_monuments_all.sql
