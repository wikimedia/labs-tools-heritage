"""Unit tests for database_connection."""

import os
import unittest
import unittest.mock as mock

from pymysql.connections import Connection

import custom_assertions  # noqa F401
from erfgoedbot import database_connection


class TestGetDatabaseConfigFile(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch('erfgoedbot.database_connection._get_current_directory')
        self.mock_current_dir = patcher.start()
        self.mock_current_dir.return_value = '/foo/bar'
        self.addCleanup(patcher.stop)

    def test_get_database_config_file_return_default_file(self):
        expected_file = os.path.join('/foo/bar', database_connection.DEFAULT_CONFIG_FILE_NAME)
        config_file = database_connection._get_database_config_file()
        self.assertEqual(config_file, expected_file)


class TestGetConfigContents(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch('erfgoedbot.database_connection._get_database_config')
        self.mock_database_config = patcher.start()
        self.mock_database_config.return_value = {
            'monuments_db': 'fake_monuments_db',
            'commons_db': 'fake_commons_db',
        }
        self.addCleanup(patcher.stop)

    def test_get_monuments_database_config(self):
        result = database_connection.get_monuments_database_config()
        self.assertEqual(result, 'fake_monuments_db')

    def test_get_commons_database_config(self):
        result = database_connection.get_commons_database_config()
        self.assertEqual(result, 'fake_commons_db')


class TestConnectToMonumentsDatabase(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch('erfgoedbot.database_connection.get_monuments_database_config')
        self.mock_database_config = patcher.start()
        self.addCleanup(patcher.stop)
        self.mock_connection = mock.Mock(spec=Connection)
        patcher = mock.patch('erfgoedbot.database_connection.pymysql.connect')
        self.mock_connect = patcher.start()
        self.mock_connect.return_value = self.mock_connection
        self.addCleanup(patcher.stop)

    def test_connect_to_monuments_database(self):
        self.mock_database_config.return_value = {
            'server': 'fake_server',
            'db_name': 'fake_db_name',
        }
        result = database_connection.connect_to_monuments_database()
        self.mock_connect.assert_called_once_with(
            db='fake_db_name', host='fake_server',
            user='', passwd='',
            charset='utf8', use_unicode=True,
            sql_mode='ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'
        )
        self.mock_connection.ping.assert_called_once_with(True)
        self.assertEqual(result, (self.mock_connection, self.mock_connection.cursor()))

    def test_connect_to_monuments_database_with_overriden_credentials(self):
        self.mock_database_config.return_value = {
            'server': 'fake_server',
            'db_name': 'fake_db_name',
            'username': 'fake_username',
            'password': 'fake_password',
        }
        result = database_connection.connect_to_monuments_database()
        self.mock_connect.assert_called_once_with(
            db='fake_db_name', host='fake_server',
            user='fake_username', passwd='fake_password',
            charset='utf8', use_unicode=True,
            sql_mode='ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'
        )
        self.mock_connection.ping.assert_called_once_with(True)
        self.assertEqual(result, (self.mock_connection, self.mock_connection.cursor()))


class TestConnectToCommonsDatabase(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch('erfgoedbot.database_connection.get_commons_database_config')
        self.mock_database_config = patcher.start()
        self.mock_database_config.return_value = {
            'server': 'fake_server',
            'db_name': 'fake_db_name',
        }
        self.addCleanup(patcher.stop)
        self.mock_connection = mock.Mock(spec=Connection)
        patcher = mock.patch('erfgoedbot.database_connection.pymysql.connect')
        self.mock_connect = patcher.start()
        self.mock_connect.return_value = self.mock_connection
        self.addCleanup(patcher.stop)

    def test_connect_to_commons_database(self):
        result = database_connection.connect_to_commons_database()
        self.mock_connect.assert_called_once_with(
            db='fake_db_name', host='fake_server',
            user='', passwd='',
            charset='latin1', use_unicode=True
        )
        self.mock_connection.ping.assert_not_called()
        self.assertEqual(result, (self.mock_connection, self.mock_connection.cursor()))

    def test_connect_to_commons_database_with_overriden_credentials(self):
        self.mock_database_config.return_value = {
            'server': 'fake_server',
            'db_name': 'fake_db_name',
            'username': 'fake_username',
            'password': 'fake_password',
        }
        result = database_connection.connect_to_commons_database()
        self.mock_connect.assert_called_once_with(
            db='fake_db_name', host='fake_server',
            user='fake_username', passwd='fake_password',
            charset='latin1', use_unicode=True
        )
        self.mock_connection.ping.assert_not_called()
        self.assertEqual(result, (self.mock_connection, self.mock_connection.cursor()))
