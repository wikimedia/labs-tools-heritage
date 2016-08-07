# -*- coding: utf-8  -*-
import MySQLdb
import monuments_config as mconfig
from pywikibot import config


def connect_to_monuments_database():
    """Connect to the mysql monuments database, if it fails, go down in flames."""
    conn = MySQLdb.connect(
        host=mconfig.db_server, db=mconfig.db, user=config.db_username,
        passwd=config.db_password, use_unicode=True, charset='utf8')
    conn.ping(True)
    cursor = conn.cursor()
    return (conn, cursor)


def connect_to_commons_database():
    '''
    Connect to the commons mysql database, if it fails, go down in flames
    '''
    conn = MySQLdb.connect('commonswiki.labsdb', db='commonswiki_p',
                           user=config.db_username, passwd=config.db_password, use_unicode=True, charset='latin1')
    cursor = conn.cursor()
    return (conn, cursor)
