Heritage - tools for Wiki Loves Monuments
=========================================


ErfgoedBot
----------

A Python MediaWiki bot doing mighty things. See [Commons:User:ErfgoedBot](https://commons.wikimedia.org/wiki/User:ErfgoedBot)

By default, the bot connects to the monuments database using the credentials
`pywikibot_config.db_username` and `pywikibot_config.db_password`.
You can override them via the `database_config.yml` file.

To hack on it, use [tox](https://tox.readthedocs.io) to run the tests


Monuments Database and API
--------------------------

A PHP [API](https://commons.wikimedia.org/wiki/Commons:Monuments_database/API) exploiting the [MySQL database](https://commons.wikimedia.org/wiki/Commons:Monuments_database).

To hack on it, use [Composer](https://getcomposer.org/) to run PHP tests and [docker-compose](https://docs.docker.com/compose/) to spin-up a local development environment.

```
sh bin/download_monuments_database_dump.sh
docker-compose up -d
```
