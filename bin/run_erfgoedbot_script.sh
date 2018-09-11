#!/bin/bash
#
# Script to run arbitrary Erfgoed Python script

if [ -z "$*" ]; then
    echo "Please provide a Python script to run."
    exit
fi

SCRIPT=$1
shift

if [ ! -f "$SCRIPT" ]; then
    echo "No such script $SCRIPT!"
    exit
fi

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $CURRENT_DIR/defaults.sh

# Use a virtual environment with our requirements
source $VIRTUAL_ENV_PATH/bin/activate

# Make sure we are in our homedir
cd $HOME_DIR || exit

# Executing script
echo_time "Running script $SCRIPT..."

$PYWIKIBOT_BIN "$SCRIPT" "$@"

echo_time "Done with $SCRIPT!"
