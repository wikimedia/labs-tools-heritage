Heritage - tools for Wiki Loves Monuments
=========================================


ErfgoedBot
----------

A Python MediaWiki bot doing mighty things. See [Commons:User:ErfgoedBot](https://commons.wikimedia.org/wiki/User:ErfgoedBot)

By default, the bot connects to the monuments database using the credentials
`pywikibot_config.db_username` and `pywikibot_config.db_password`.
You can override them via the `database_config.yml` file.

### Development

To hack on it, use [tox](https://tox.readthedocs.io) to run the tests

To spin-up a development environement simulating harvesting:

```
# Build Docker images
docker-compose build

# Create database tables
docker-compose run --rm --no-deps --entrypoint python bot erfgoedbot/monument_tables.py
docker-compose run --rm --no-deps --entrypoint python bot erfgoedbot/fill_table_monuments_all.py

# Start the Docker containers
docker-compose up -d

# Ensure a directory for locally written pages
mkdir -p docker_pages

# Run the bot to harvest a country
docker-compose run --rm bot python erfgoedbot/update_database.py -countrycode:ge -langcode:ka -log

# Update the monuments_all table
docker-compose run --rm db mysql -h db s51138__heritage_p --user=heritage --password=password < erfgoedbot/sql/fill_table_monuments_all.sql

# Update the statistics table
docker-compose run --rm web php ../maintenance/_buildStats.php
```

The web interface will be accessible on http://localhost:8000/

### Toolforge

This tool is meant to run on [Toolforge](https://wikitech.wikimedia.org/wiki/Toolforge).

Dependencies are installed in a Python virtual environment (via `bin/build-python.sh`). In order to run Python scripts, you may want to use the Shell scripts in the `bin` directory:
```
./bin/run_erfgoedbot_script.sh erfgoedbot/update_database.py -countrycode:ge -langcode:ka -log

```

Monuments Database and API
--------------------------

A PHP [API](https://commons.wikimedia.org/wiki/Commons:Monuments_database/API) exploiting the [MySQL database](https://commons.wikimedia.org/wiki/Commons:Monuments_database).

To hack on it, use [Composer](https://getcomposer.org/) to run PHP tests and [docker-compose](https://docs.docker.com/compose/) to spin-up a local development environment.

```
./bin/download_monuments_database_dump.sh
docker-compose -f docker-compose-dump.yml up -d
```

The web interface will be accessible on http://localhost:8000/
