#!/bin/bash
#
# Script to make a full update of the monuments databse and run a bunch of tasks

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $CURRENT_DIR/defaults.sh

echo_time "Starting full monument update."

# Make sure we are in our homedir
cd $HOME_DIR || exit

# Use a virtual environment with our requirements
source $VIRTUAL_ENV_PATH/bin/activate

# Load any config changes into the source tables
echo_time "Load changes to monuments_config..."
$PYWIKIBOT_BIN $ERFGOED_PATH/monument_tables.py -log
$PYWIKIBOT_BIN $ERFGOED_PATH/fill_table_monuments_all.py -log

# Recreate the source tables
count=$(ls -1 $ERFGOED_PATH/sql/create_table_monuments* | wc -l)

if [ "$RECREATE_TABLES" = true ] ; then
    echo_time "Recreating the $count source tables..."
    for i in $ERFGOED_PATH/sql/create_table_monuments*; do
        $MYSQL_BIN -h $DB_SERVER $DATABASE < "$i"
    done
else
    echo_time "Skipping recreation of $count source tables."
fi

# Update all of the source tables
echo_time "Full source database update..."
$PYWIKIBOT_BIN $ERFGOED_PATH/update_database.py $UPDATE_MONUMENTS_ARGS

echo_time "Stop categorization job as next stage locks the database..."
jstop $CATEGORIZATION_JOB_NAME

# Update the all monuments table
echo_time "Update monuments_all table..."
$MYSQL_BIN -h $DB_SERVER $DATABASE < $ERFGOED_PATH/sql/fill_table_monuments_all.sql

echo_time "Restart the categorization job..."
jsub -l release=trusty -mem 1000m -once -j y -o $LOGS_PATH/categorize_images.log -N $CATEGORIZATION_JOB_NAME $SOURCE_PATH/bin/categorize_images.sh >> $LOGS_PATH/crontab.log

## Update the image table. Is now another job
# echo_time "Update image table..."
# PYWIKIBOT_BIN $ERFGOED_PATH/populate_image_table.py

# Make statistics
echo_time "Make statistics..."
$PYWIKIBOT_BIN $ERFGOED_PATH/database_statistics.py -log -skip_wd

# Make more detailed statistics
echo_time "Make more detailed statistics..."
$PHP_BIN $SOURCE_PATH/maintenance/_buildStats.php

# Update the list of unused monuments
echo_time "Update unused images list..."
$PYWIKIBOT_BIN $ERFGOED_PATH/unused_monument_images.py -log

# Make a list of missing commonscat links
echo_time "Make a list of missing commonscat links..."
$PYWIKIBOT_BIN $ERFGOED_PATH/missing_commonscat_links.py -log

# Make a list of images without id
echo_time "Make a list of images without id..."
$PYWIKIBOT_BIN $ERFGOED_PATH/images_of_monuments_without_id.py -log

# Dump database to a file so people can play around with it
cd $PUBLIC_HTML_PATH || exit

# Keep the last dump around just in case
ln -f monuments_db.sql.gz monuments_db-old.sql.gz

# Dump the database
echo_time "Dump database..."
$MYSQLDUMP_BIN --host=$DB_SERVER --single-transaction $DATABASE > monuments_db-new.sql
nice gzip monuments_db-new.sql

# Atomically replace the provided file
echo_time "Replace the sql file atomically..."
mv -f monuments_db-new.sql.gz monuments_db.sql.gz

cd $HOME_DIR || exit

# Refill prox_search table. Which will be used by layar server.
echo_time "Refill prox_search table..."
$PHP_BIN $SOURCE_PATH/prox_search/fill_table_prox_search.php

# Update admin structure tree
echo_time "Update admin structure tree..."
$PHP_BIN $ERFGOED_PATH/populate_adm_tree.php

echo_time "Done with the update!"
