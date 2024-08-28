#!/bin/bash
#
# Post-harvesting steps (in Python)

set -o errexit
set -o pipefail
set -o nounset

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $CURRENT_DIR/defaults.sh

cd $SOURCE_PATH || exit
source $VIRTUAL_ENV_PATH/bin/activate
export PYTHONPATH=$SOURCE_PATH

# Make statistics
echo_time "Make statistics..."
$PYWIKIBOT_BIN $ERFGOED_PATH/database_statistics.py -log

# Update the list of unused monuments
echo_time "Update unused images list..."
$PYWIKIBOT_BIN $ERFGOED_PATH/unused_monument_images.py -log

# Make a list of missing commonscat links
echo_time "Make a list of missing commonscat links..."
$PYWIKIBOT_BIN $ERFGOED_PATH/missing_commonscat_links.py -log

# Make a list of images without id
echo_time "Make a list of images without id..."
$PYWIKIBOT_BIN $ERFGOED_PATH/images_of_monuments_without_id.py -log

echo_time "Done with the Python post-harvesting steps!"
