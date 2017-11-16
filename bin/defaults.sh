echo_time() {
    echo "$(date +%F_%T) $*"
}

# Paths
: ${HOME_DIR:=/data/project/heritage}
: ${SOURCE_PATH:=$HOME_DIR/heritage}
: ${ERFGOED_PATH:=$SOURCE_PATH/erfgoedbot}
: ${VIRTUAL_ENV_PATH:=$HOME_DIR/.venv}
: ${LOGS_PATH:=$SOURCE_PATH/logs}

# Database config
: ${DATABASE:=s51138__heritage_p}
: ${DB_SERVER:=tools-db}

# Executables
: ${PYWIKIBOT_BIN:=python}
: ${PHP_BIN:=php}
: ${MYSQL_BIN:=mysql}