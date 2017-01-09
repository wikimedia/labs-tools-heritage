"""Unit tests for database_statistics."""

# from pywikibot.site import APISite
# from pywikibot.exceptions import NoPage
import unittest
import mock
from erfgoedbot import database_statistics


class TestBuildQuery(unittest.TestCase):

    def test_build_query_simple_field(self):
        result = database_statistics.build_query('foo')
        expected = u"SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (foo='' OR foo IS NULL)"
        self.assertEqual(result, expected)

    def test_build_query_complex_field(self):
        result = database_statistics.build_query(('foo', 'bar'))
        expected = u"SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (foo='' OR foo IS NULL) AND NOT (bar='' OR bar IS NULL)"
        self.assertEqual(result, expected)


class TestComputePercentage(unittest.TestCase):

    def test_compute_percentage(self):
        result = database_statistics.compute_percentage(2, 8)
        self.assertEqual(result, 25)

    def test_compute_percentage_with_rounding(self):
        result = database_statistics.compute_percentage(1, 3)
        self.assertEqual(result, 33.33)

    def test_compute_percentage_with_zero(self):
        result = database_statistics.compute_percentage(0, 0)
        self.assertEqual(result, 0.0)


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


class TestGetStatistics(unittest.TestCase):

    def setUp(self):
        self.mock_cursor = mock.Mock()

    def test_getStatistics(self):
        with mock.patch('erfgoedbot.database_statistics.getCount', autospec=True) as mock_getCount:
            mock_getCount.return_value = 1
            result = database_statistics.getStatistics('ge', 'ka', None, self.mock_cursor)
            self.assertEqual(mock_getCount.call_count, 16)
            self.assertEqual(result['country'], 'ge')
            self.assertEqual(result['lang'], 'ka')
            self.assertEqual(result['all'], 1)
            self.assertEqual(result['name'], 1)
            self.assertEqual(result['namePercentage'], 100)
