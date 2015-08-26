#!/bin/bash
#
# Script to make a full update of the monuments databse and run a bunch of tasks

# Make sure we are in our homedir
cd /data/project/heritage/

# First have the erfgoed bot update everything in it's config
echo "Full database update..."
/data/project/heritage/pywikibot/pwb.py /data/project/heritage/erfgoedbot/update_database.py -fullupdate

# Update the all monuments table
echo "Update all monuments table..."
mysql -h tools-db s51138__heritage_p < /data/project/heritage/erfgoedbot/sql/fill_table_monuments_all.sql

## Update the image table. Is now another job
# echo "Update image table..."
# /data/project/heritage/pywikibot/pwb.py /data/project/heritage/erfgoedbot/populate_image_table.py

# Update admin structure tree
echo "Update admin structure tree..."
php ./erfgoedbot/populate_adm_tree.php

# Make statistics
echo "Make statistics..."
/data/project/heritage/pywikibot/pwb.py /data/project/heritage/erfgoedbot/database_statistics.py

# Make more detailed statistics
echo "Make more detailed statistics..."
php ./public_html/maintenance/_buildStats.php

# Update the list of unused monuments
echo "Update unused images list..."
/data/project/heritage/pywikibot/pwb.py /data/project/heritage/erfgoedbot/unused_monument_images.py

# Make a list of missing commonscat links
echo "Make a list of missing commonscat links..."
/data/project/heritage/pywikibot/pwb.py /data/project/heritage/erfgoedbot/missing_commonscat_links.py

# Dump database to a file so people can play around with it
cd ./public_html

# Keep the last dump around just in case
ln -f monuments_db.sql.gz monuments_db-old.sql.gz

# Dump the database
echo "Dump database..."
mysqldump --host=tools-db --single-transaction s51138__heritage_p > monuments_db-new.sql
nice gzip monuments_db-new.sql

# Atomically replace the provided file
echo "Replace atomically the file..."
mv -f monuments_db-new.sql.gz monuments_db.sql.gz
cd ..

# Refill prox_search table. Which will be used by layar server.
echo "Refill prox_search table..."
php ./prox_search/fill_table_prox_search.php

# Categorize some images
echo "Categorize images..."
/data/project/heritage/pywikibot/pwb.py /data/project/heritage/erfgoedbot/categorize_images.py
