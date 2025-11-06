echo_time() {
    echo "$(date +%F_%T) $*"
}

create_toolforge_job() {
    local json_payload="$1"
    curl -X 'POST' \
        "$TOOLFORGE_API_FLAGS" \
        "$TOOLFORGE_API_JOBS_ENDPOINT" \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d "$json_payload"
}

# Paths
: ${TOOL_NAME:=heritage}
: ${HOME_DIR:=/data/project/$TOOL_NAME}
: ${SOURCE_PATH:=$HOME_DIR/$TOOL_NAME}
: ${ERFGOED_PATH:=$SOURCE_PATH/erfgoedbot}
: ${PUBLIC_HTML_PATH:=$HOME_DIR/public_html/}
: ${VIRTUAL_ENV_PATH:=$HOME_DIR/.venv}
: ${LOGS_PATH:=$HOME_DIR/logs}

# Database config
: ${DATABASE:=s51138__heritage_p}
: ${DB_SERVER:=tools-db}

# Toolforge API
: ${TOOLFORGE_API_URL:=https://api.svc.tools.eqiad1.wikimedia.cloud:30003}
: ${TOOLFORGE_API_KEY:=$HOME_DIR/.toolskube/client.key}
: ${TOOLFORGE_API_CERT:=$HOME_DIR/.toolskube/client.crt}
: ${TOOLFORGE_API_JOBS_ENDPOINT:=$TOOLFORGE_API_URL/jobs/v1/tool/$TOOL_NAME/jobs/}
: ${TOOLFORGE_API_FLAGS:=--insecure --cert $TOOLFORGE_API_CERT --key $TOOLFORGE_API_KEY}
: ${TOOLFORGE_PYTHON_IMAGE:=python3.9}
: ${TOOLFORGE_PHP_IMAGE:=php7.4}
: ${TOOLFORGE_MARIADB_IMAGE:=mariadb}

# Executables
: ${PYWIKIBOT_BIN:=python}
: ${PHP_BIN:=php}
: ${MYSQL_BIN:=mysql}
: ${MYSQLDUMP_BIN:=mysqldump}

: ${UPDATE_MONUMENTS_ARGS:=-fullupdate -log}
: ${CATEGORIZATION_JOB_NAME:=categorize_images}

# Conditionals
: ${RECREATE_TABLES:=true}
