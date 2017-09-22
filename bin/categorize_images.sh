#!/bin/bash
#
# Script to categorize images

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $CURRENT_DIR/defaults.sh

# Make sure we are in our homedir
cd $HOME_DIR || exit

# Categorize some images
echo_time "Categorize images..."
$PYWIKIBOT_BIN $ERFGOED_PATH/categorize_images.py -log

echo_time "Done with the categorization!"
