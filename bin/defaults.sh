echo_time() {
    echo "$(date +%F_%T) $*"
}

# Paths
: ${HOME_DIR:=/data/project/heritage}
: ${SOURCE_PATH:=$HOME_DIR/heritage}
: ${ERFGOED_PATH:=$SOURCE_PATH/erfgoedbot}

# Database config
: ${DATABASE:=s51138__heritage_p}
: ${DB_SERVER:=tools-db}

# Executables
: ${PYWIKIBOT_BIN:=$HOME_DIR/pywikibot/pwb.py}
: ${PHP_BIN:=php}
: ${MYSQL_BIN:=mysql}
