#!/bin/bash
JSON_PATH=./erfgoedbot/monuments_config

files=$(find $JSON_PATH -name '*.json' -print)

FAIL=0

for f in $files; do
    if [ -e "$f" ]; then
        (jsonschema -i  "$f" $JSON_PATH/monuments_config.schema && echo "√ $f") || FAIL=$((FAIL+1))
    fi
done
if [[ $FAIL -ne 0 ]];  then
    echo "$FAIL files with issues"
fi
exit $FAIL
