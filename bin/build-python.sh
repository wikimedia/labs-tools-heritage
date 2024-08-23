#!/bin/bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $CURRENT_DIR/defaults.sh

set -ex
if [ ! -d $VIRTUAL_ENV_PATH ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VIRTUAL_ENV_PATH
fi

source $VIRTUAL_ENV_PATH/bin/activate

echo "Upgrade pip to latest and add support for the wheel package format..."
pip install --upgrade pip wheel

echo "Installing Python requirements..."
pip install -r $SOURCE_PATH/requirements.txt
