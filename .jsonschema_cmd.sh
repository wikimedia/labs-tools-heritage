#!/bin/bash
JSON_PATH=./erfgoedbot/monuments_config

SCHEMA_FILE=$JSON_PATH/monuments_config.schema

echo "Validating schema $SCHEMA_FILE"
if ! check-jsonschema --check-metaschema $SCHEMA_FILE; then
    >&2 echo "ERROR: Invalid schema file: $SCHEMA_FILE"
    exit 1
fi

echo
echo "Processing json configs in $JSON_PATH"
files=$(find $JSON_PATH -name '*.json' -print)

FAIL=0

for f in $files; do
    if [ -e "$f" ]; then
        (check-jsonschema --schemafile=$SCHEMA_FILE "$f" && echo "√ $f") || FAIL=$((FAIL+1))
    fi
done
if [[ $FAIL -ne 0 ]];  then
    echo "$FAIL files with issues"
fi
exit $FAIL
