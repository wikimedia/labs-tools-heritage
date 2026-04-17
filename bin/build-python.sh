#!/bin/bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $CURRENT_DIR/defaults.sh

set -ex
# Probe `import pip` to detect a stale venv left over from a previous
# python3 (e.g. after a 3.9 -> 3.11 image bump); recreate if broken.
if [ ! -d "$VIRTUAL_ENV_PATH" ] \
   || ! "$VIRTUAL_ENV_PATH/bin/$PYWIKIBOT_BIN" -c 'import pip' >/dev/null 2>&1; then
    echo "Creating/refreshing virtual environment..."
    python3 -m venv --clear "$VIRTUAL_ENV_PATH"
fi

source $VIRTUAL_ENV_PATH/bin/activate

echo "Upgrade pip to latest and add support for the wheel package format..."
pip install --upgrade pip wheel

echo "Installing Python requirements..."
pip install -r $SOURCE_PATH/requirements.txt
