#!/bin/bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $CURRENT_DIR/defaults.sh

set -ex
if [ ! -d $VIRTUAL_ENV_PATH ]; then
    echo "Creating virtual environment..."
    virtualenv --python=python3.7 $VIRTUAL_ENV_PATH --system-site-packages
fi

source $VIRTUAL_ENV_PATH/bin/activate

echo "Upgrade pip to latest..."
pip install --upgrade pip

echo "Installing Python requirements..."
pip install -r $SOURCE_PATH/requirements.txt
