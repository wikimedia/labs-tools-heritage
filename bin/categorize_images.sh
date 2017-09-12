#!/bin/bash
#
# Script to categorize images

echo_time() {
    echo "$(date +%F_%T) $*"
}

PYWIKIBOT_BIN=/data/project/heritage/pywikibot/pwb.py
ERFGOED_PATH=/data/project/heritage/erfgoedbot

# Make sure we are in our homedir
cd /data/project/heritage/ || exit

# Categorize some images
echo_time "Categorize images..."
$PYWIKIBOT_BIN $ERFGOED_PATH/categorize_images.py -log

echo_time "Done with the categorization!"
