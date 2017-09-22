#!/bin/bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

. $CURRENT_DIR/build-python.sh

. $CURRENT_DIR/build-php.sh
