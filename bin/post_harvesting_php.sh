#!/bin/bash
#
# Post-harvesting steps (in PHP)

set -o errexit
set -o pipefail
set -o nounset

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $CURRENT_DIR/defaults.sh

cd $SOURCE_PATH || exit

# Make more detailed statistics
echo_time "Make more detailed statistics..."
$PHP_BIN $SOURCE_PATH/maintenance/_buildStats.php

# Update admin structure tree
echo_time "Update admin structure tree..."
$PHP_BIN $ERFGOED_PATH/populate_adm_tree.php

echo_time "Done with the PHP post-harvesting steps!"
