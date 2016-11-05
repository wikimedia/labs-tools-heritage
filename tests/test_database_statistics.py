"""Unit tests for database_statistics."""

# from pywikibot.site import APISite
# from pywikibot.exceptions import NoPage
import unittest
import mock
from erfgoedbot import database_statistics


class TestGetMethods(unittest.TestCase):

    def setUp(self):
        self.mock_cursor = mock.Mock()

    def test_getCount(self):
        self.mock_cursor.fetchone.return_value = (42,)
        result = database_statistics.getCount("SELECT X", self.mock_cursor)
        self.assertEqual(result, 42)
        self.mock_cursor.execute.assert_called_once_with("SELECT X")
        self.mock_cursor.fetchone.assert_called_once_with()

    def test_getCountries(self):
        database_statistics.getCountries(None, self.mock_cursor)
        self.mock_cursor.execute.assert_called_once_with(
            u'SELECT DISTINCT(country) FROM monuments_all'
        )

    def test_getLanguages(self):
        database_statistics.getLanguages("at", None, self.mock_cursor)
        self.mock_cursor.execute.assert_called_once_with(
            u"SELECT DISTINCT(lang) FROM monuments_all WHERE country='at'"
        )
