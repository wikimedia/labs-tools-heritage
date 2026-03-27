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
This should be run with [uv](https://docs.astral.sh/uv/) as:

uv run tox

To spin-up a development environment simulating harvesting a docker setup can be run.

To connect to the commons database, a proxy is setup to connect to the commons database via toolforge. For the config of that the following environment variables are needed:

```
export TOOLFORGE_DB_USERNAME=<username from .my.cnf>
export TOOLFORGE_DB_PASSWORD=<password from .my.cnf>
export SSH_USER=<toolforge username>
```

The openssh inside the docker needs access to your ssh keys. By default that is done via the SSH_AUTH_SOCK variable set by the ssh agent.

If that doesn't work, you can mount your .ssh dir inside the docker instead. For that you need to specify a different docker yml file:

```
export COMPOSE_FILE=docker-compose-sshdir.yml
```

There might be config in your .ssh/config not liked by the openssh inside the docker. If the heritage-db_commons-1 container doesn't show up in docker compose ps, run docker compose logs | grep commons | less for debugging.

A webservice and a database are started, where to can connect to. To set ports different (shown are defaults):

```
export HERITAGE_DBPORT=3306
export HERITAGE_WEBPORT=5000
```

After all this to setup and run docker:

```
# Build Docker images
docker-compose build

# Create database tables
docker-compose run --rm --no-deps --entrypoint python bot -m erfgoedbot.monument_tables
docker-compose run --rm --no-deps --entrypoint python bot -m erfgoedbot.fill_table_monuments_all

# Start the Docker containers
docker-compose up -d

# Ensure a directory for locally written pages
mkdir -p docker_pages

# Run the bot to harvest a country
docker-compose run --rm bot python -m erfgoedbot.update_database -countrycode:ge -langcode:ka -log

# Update the monuments_all table
docker-compose run --rm db mysql -h db s51138__heritage_p --user=heritage --password=password < erfgoedbot/sql/fill_table_monuments_all.sql

# Update the statistics table
docker-compose run --rm web php ../maintenance/_buildStats.php
```

The web interface will be accessible on http://localhost:5000/ or the set port in HERITAGE_WEBPORT.

On port 3306 or the port set in HERITAGE_DBPORT you can connect a local mysql client like dbeaver with username heritage and password password.

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

The web interface will be accessible on http://localhost:5000/

License
--------------------------

With the exception of directories containing their own LICENSE file,
this repository is licensed under the [MIT License](./LICENSE).
