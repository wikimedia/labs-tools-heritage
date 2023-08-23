# -*- coding: utf-8  -*-

import os

import pymysql
import yaml
from pymysql.err import InterfaceError, OperationalError

import pywikibot
from pywikibot import config as pywikibot_config

DEFAULT_CONFIG_FILE_NAME = 'database_config.default.yml'
OVERRIDE_CONFIG_FILE_NAME = 'database_config.yml'


def _get_current_directory():
    """Return the absolute path of the current file."""
    return os.path.dirname(os.path.abspath(__file__))


def _get_database_config_file():
    current_dir = _get_current_directory()
    config_file = os.path.join(current_dir, DEFAULT_CONFIG_FILE_NAME)
    override_config_file = os.path.join(current_dir, OVERRIDE_CONFIG_FILE_NAME)
    if os.path.isfile(override_config_file):
        config_file = override_config_file
    return config_file


def _get_database_config():
    config_file = _get_database_config_file()
    return yaml.safe_load(open(config_file, 'r'))


def get_monuments_database_config():
    return _get_database_config()['monuments_db']


def get_commons_database_config():
    return _get_database_config()['commons_db']


def connect_to_monuments_database():
    """Connect to the mysql monuments database."""
    db_config = get_monuments_database_config()
    username = db_config.get('username', pywikibot_config.db_username)
    password = db_config.get('password', pywikibot_config.db_password)
    conn = pymysql.connect(
        host=db_config['server'], db=db_config['db_name'],
        user=username, passwd=password,
        use_unicode=True, charset='utf8',
        sql_mode='ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION')
    conn.ping(True)
    cursor = conn.cursor()
    return (conn, cursor)


def connect_to_commons_database():
    """Connect to the commons mysql database."""
    db_config = get_commons_database_config()
    username = os.environ.get('DB_USERNAME') or db_config.get('username', pywikibot_config.db_username)
    password = os.environ.get('DB_PASSWORD') or db_config.get('password', pywikibot_config.db_password)
    conn = pymysql.connect(
        host=db_config['server'], db=db_config['db_name'],
        user=username, passwd=password,
        use_unicode=True, charset='latin1')
    cursor = conn.cursor()
    return (conn, cursor)


def close_database_connection(conn, cursor):
    """Close the cursor and commit the current transactions."""
    try:
        conn.commit()
        cursor.close()
    except (InterfaceError, OperationalError) as e:
        pywikibot.error('Looks like MySQL server went away: {}'.format(e))
