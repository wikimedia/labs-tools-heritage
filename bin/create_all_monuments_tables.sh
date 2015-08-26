#!/bin/bash
# Script to create all the tables from scratch
# The python script expects to be in it's own directory:
cd /data/project/heritage/erfgoedbot
# First create the sql statements
python /data/project/heritage/erfgoedbot/monument_tables.py
for i in `ls /data/project/heritage/erfgoedbot/sql/create_table_monuments*`
do
	echo $i
         mysql -h tools-db s51138__heritage_p < $i
done
for i in `ls /data/project/heritage/erfgoedbot/sql/create_table_wlpa_*`
do
         mysql -h tools-db s51138__heritage_p < $i
done
# Admin tree for browsing ISO codes
mysql -h tools-db s51138__heritage_p < /data/project/heritage/erfgoedbot/sql/create_table_admin_tree.sql
# Something with commonscat
mysql -h tools-db s51138__heritage_p < /data/project/heritage/erfgoedbot/sql/create_table_commonscat.sql
# Tracking the images table
mysql -h tools-db s51138__heritage_p < /data/project/heritage/erfgoedbot/sql/create_table_image.sql