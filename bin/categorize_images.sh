#!/bin/bash
#
# Script to categorize images

set -o errexit
set -o pipefail
set -o nounset

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $CURRENT_DIR/defaults.sh

cd $SOURCE_PATH || exit
source $VIRTUAL_ENV_PATH/bin/activate
export PYTHONPATH=$SOURCE_PATH

# Categorize some images
echo_time "Categorize images..."
$PYWIKIBOT_BIN $ERFGOED_PATH/categorize_images.py -log

echo_time "Done with the categorization!"
