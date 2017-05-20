#!/bin/bash
#
# Script to make a full update of the monuments databse and run a bunch of tasks

echo_time() {
    echo "$(date +%F_%T) $*"
}

PYWIKIBOT_BIN=/data/project/heritage/pywikibot/pwb.py
ERFGOED_PATH=/data/project/heritage/erfgoedbot

echo_time "Starting full monument update."

# Make sure we are in our homedir
cd /data/project/heritage/ || exit

# Load any config changes into the source tables
echo_time "Load changes to monuments_config..."
$PYWIKIBOT_BIN $ERFGOED_PATH/monument_tables.py -log
$PYWIKIBOT_BIN $ERFGOED_PATH/fill_table_monuments_all.py -log

# Recreate the source tables
echo_time "Recreating the source tables..."
for i in $ERFGOED_PATH/sql/create_table_monuments*
do
    mysql -h tools-db s51138__heritage_p < "$i"
done

# Update all of the source tables
echo_time "Full source database update..."
$PYWIKIBOT_BIN $ERFGOED_PATH/update_database.py -fullupdate -log

# Update the all monuments table
echo_time "Update monuments_all table..."
mysql -h tools-db s51138__heritage_p < $ERFGOED_PATH/sql/fill_table_monuments_all.sql

## Update the image table. Is now another job
# echo_time "Update image table..."
# PYWIKIBOT_BIN $ERFGOED_PATH/populate_image_table.py

# Update admin structure tree
echo_time "Update admin structure tree..."
php ./erfgoedbot/populate_adm_tree.php

# Make statistics
echo_time "Make statistics..."
$PYWIKIBOT_BIN $ERFGOED_PATH/database_statistics.py -log

# Make more detailed statistics
echo_time "Make more detailed statistics..."
php ./public_html/maintenance/_buildStats.php

# Update the list of unused monuments
echo_time "Update unused images list..."
$PYWIKIBOT_BIN $ERFGOED_PATH/unused_monument_images.py -log

# Make a list of missing commonscat links
echo_time "Make a list of missing commonscat links..."
$PYWIKIBOT_BIN $ERFGOED_PATH/missing_commonscat_links.py -log

# Dump database to a file so people can play around with it
cd ./public_html || exit

# Keep the last dump around just in case
ln -f monuments_db.sql.gz monuments_db-old.sql.gz

# Dump the database
echo_time "Dump database..."
mysqldump --host=tools-db --single-transaction s51138__heritage_p > monuments_db-new.sql
nice gzip monuments_db-new.sql

# Atomically replace the provided file
echo_time "Replace the sql file atomically..."
mv -f monuments_db-new.sql.gz monuments_db.sql.gz
cd ..

# Refill prox_search table. Which will be used by layar server.
echo_time "Refill prox_search table..."
php ./prox_search/fill_table_prox_search.php

# Categorize some images
echo_time "Categorize images..."
$PYWIKIBOT_BIN $ERFGOED_PATH/categorize_images.py -log

echo_time "Done with the update!"
