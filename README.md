Heritage - tools for Wiki Loves Monuments
=========================================


ErfgoedBot
----------

A Python MediaWiki bot doing mighty things. See [Commons:User:ErfgoedBot](https://commons.wikimedia.org/wiki/User:ErfgoedBot)

By default, the bot connects to the monuments database using the credentials
`pywikibot_config.db_username` and `pywikibot_config.db_password`.
You can override them via the `database_config.yml` file.

To hack on it, use [tox](https://tox.readthedocs.io) to run the tests

To spin-up a development environement simulating harvesting:

```
# Create database tables
python erfgoedbot/monument_tables.py
python erfgoedbot/fill_table_monuments_all.py

# Build and start the Docker containers
docker-compose -f docker-compose-bot.yml up --build -d

# Run the bot to harvest a country
docker-compose -f docker-compose-bot.yml run --rm bot python erfgoedbot/update_database.py -countrycode:ge -langcode:ka -log

# Update the monuments_all table
docker-compose -f docker-compose-bot.yml run --rm db mysql -h db s51138__heritage_p --user=heritage --password=password < erfgoedbot/sql/fill_table_monuments_all.sql
```

The web interface will be accessible on http://localhost:8000/


Monuments Database and API
--------------------------

A PHP [API](https://commons.wikimedia.org/wiki/Commons:Monuments_database/API) exploiting the [MySQL database](https://commons.wikimedia.org/wiki/Commons:Monuments_database).

To hack on it, use [Composer](https://getcomposer.org/) to run PHP tests and [docker-compose](https://docs.docker.com/compose/) to spin-up a local development environment.

```
./bin/download_monuments_database_dump.sh
docker-compose up -d
```

The web interface will be accessible on http://localhost:8000/
