"""Unit tests for database_statistics."""
import unittest
import unittest.mock as mock

import custom_assertions  # noqa F401
from erfgoedbot import database_statistics
from report_base_test import TestCreateReportBase


class TestBuildSummaryQuery(unittest.TestCase):

    def test_build_summary_query_simple_field(self):
        result = database_statistics.build_summary_query('foo')
        expected = "SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (foo='' OR foo IS NULL)"
        self.assertEqual(result, expected)

    def test_build_summary_query_complex_field(self):
        result = database_statistics.build_summary_query(('foo', 'bar'))
        expected = "SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (foo='' OR foo IS NULL) AND NOT (bar='' OR bar IS NULL)"
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
            'SELECT DISTINCT(country) FROM monuments_all'
        )

    def test_getLanguages(self):
        database_statistics.getLanguages("at", None, self.mock_cursor)
        self.mock_cursor.execute.assert_called_once_with(
            'SELECT DISTINCT(lang) FROM monuments_all WHERE country=%s',
            ('at', )
        )


class TestGetSummaryStatistics(unittest.TestCase):

    def setUp(self):
        self.mock_cursor = mock.Mock()

    def test_get_summary_statistics(self):
        with mock.patch('erfgoedbot.database_statistics.getCount', autospec=True) as mock_getCount:
            mock_getCount.return_value = 1
            result = database_statistics.get_summary_statistics('ge', 'ka', None, self.mock_cursor)
            self.assertEqual(mock_getCount.call_count, 16)
            self.assertEqual(result['country'], 'ge')
            self.assertEqual(result['lang'], 'ka')
            self.assertEqual(result['all'], 1)
            self.assertEqual(result['name'], 1)


class TestOutputStatistics(TestCreateReportBase):

    """Test the outputStatistics method."""

    def setUp(self):
        self.class_name = 'erfgoedbot.database_statistics'
        super(TestOutputStatistics, self).setUp()

        self.prefix = 'prefix'
        patcher = mock.patch(
            'erfgoedbot.categorize_images.common.table_header_row')
        self.mock_table_header_row = patcher.start()
        self.mock_table_header_row.return_value = self.prefix
        self.addCleanup(patcher.stop)

        self.postfix = '|}\n'

        self.comment = 'Updating monument database statistics'
        self.pagename = 'Commons:Monuments database/Statistics'

    def bundled_asserts(self, expected_rows,
                        expected_summation_row):
        """The full battery of asserts to do for each test."""
        expected_text = (self.prefix + expected_rows +
                         expected_summation_row + self.postfix)
        self.mock_site.assert_called_once_with('commons', 'commons')
        self.mock_page.assert_called_once_with(
            self.mock_site.return_value, self.pagename)
        self.mock_save_to_wiki_or_local.assert_called_once_with(
            self.mock_page.return_value,
            self.comment,
            expected_text
        )

    def test_output_statistics_single_complete(self):
        statistics = {'foo_country': {'bar_lang': {
            'country': 'foo',
            'lang': 'bar',
            'all': 100,
            'name': 1,
            'address': 2,
            'municipality': 3,
            'coordinates': 4,
            'image': 5,
            'commonscat': 6,
            'article': 7,
            'wikidata': 8,
            'adm0': 9,
            'adm1': 11,
            'adm2': 12,
            'adm3': 13,
            'adm4': 14,
            'adm0iso': 'foobar',
            'source': 15
        }}}

        expected_rows = (
            '|-\n'
            '| [//tools.wmflabs.org/heritage/api/api.php?action=statistics&stcountry=foo&format=html&limit=0 foo] '
            '|| bar || 100 '
            '|| 1 <small>(1.0%)</small> '
            '|| 2 <small>(2.0%)</small> '
            '|| 3 <small>(3.0%)</small> '
            '|| 4 <small>(4.0%)</small> '
            '|| 5 <small>(5.0%)</small> '
            '|| 6 <small>(6.0%)</small> '
            '|| 7 <small>(7.0%)</small> '
            '|| 8 <small>(8.0%)</small> '
            '|| 9 <small>(9.0%)</small> '
            '|| [//tools.wmflabs.org/heritage/api/api.php?action=adminlevels&format=json&admtree=foobar 11] <small>(11.0%)</small> '
            '|| 12 <small>(12.0%)</small> '
            '|| 13 <small>(13.0%)</small> '
            '|| 14 <small>(14.0%)</small> '
            '|| 15 \n'
        )
        expected_summation_row = (
            '|- class="sortbottom"\n'
            '| '
            '|| || 100 '
            '|| 1 <small>(1.0%)</small> '
            '|| 2 <small>(2.0%)</small> '
            '|| 3 <small>(3.0%)</small> '
            '|| 4 <small>(4.0%)</small> '
            '|| 5 <small>(5.0%)</small> '
            '|| 6 <small>(6.0%)</small> '
            '|| 7 <small>(7.0%)</small> '
            '|| 8 <small>(8.0%)</small> '
            '|| 9 <small>(9.0%)</small> '
            '|| 11 <small>(11.0%)</small> '
            '|| 12 <small>(12.0%)</small> '
            '|| 13 <small>(13.0%)</small> '
            '|| 14 <small>(14.0%)</small> '
            '|| 15 \n'
        )

        database_statistics.outputStatistics(statistics)
        self.bundled_asserts(expected_rows, expected_summation_row)

    def test_output_statistics_multiple_complete(self):
        statistics = {}
        statistics['foo_country'] = {}
        statistics['foo_country']['bar_lang'] = {
            'country': 'foo',
            'lang': 'bar',
            'all': 100,
            'name': 1,
            'address': 2,
            'municipality': 3,
            'coordinates': 4,
            'image': 5,
            'commonscat': 6,
            'article': 7,
            'wikidata': 8,
            'adm0': 9,
            'adm1': 11,
            'adm2': 12,
            'adm3': 13,
            'adm4': 14,
            'adm0iso': 'foobar',
            'source': 15
        }
        statistics['foo_country']['zen_lang'] = {
            'country': 'foo',
            'lang': 'zen',
            'all': 10,
            'name': 10,
            'address': 10,
            'municipality': 10,
            'coordinates': 10,
            'image': 10,
            'commonscat': 10,
            'article': 10,
            'wikidata': 10,
            'adm0': 10,
            'adm1': 10,
            'adm2': 10,
            'adm3': 10,
            'adm4': 10,
            'adm0iso': 'foozen',
            'source': 10
        }
        statistics['goo_country'] = {
            'zen_lang': {
                'country': 'goo',
                'lang': 'zen',
                'all': 10,
                'name': 10,
                'address': 10,
                'municipality': 10,
                'coordinates': 10,
                'image': 10,
                'commonscat': 10,
                'article': 10,
                'wikidata': 10,
                'adm0': 10,
                'adm1': 10,
                'adm2': 10,
                'adm3': 10,
                'adm4': 10,
                'adm0iso': 'goozen',
                'source': 10
            }
        }

        expected_rows = (
            '|-\n'
            '| [//tools.wmflabs.org/heritage/api/api.php?action=statistics&stcountry=foo&format=html&limit=0 foo] '
            '|| bar || 100 '
            '|| 1 <small>(1.0%)</small> '
            '|| 2 <small>(2.0%)</small> '
            '|| 3 <small>(3.0%)</small> '
            '|| 4 <small>(4.0%)</small> '
            '|| 5 <small>(5.0%)</small> '
            '|| 6 <small>(6.0%)</small> '
            '|| 7 <small>(7.0%)</small> '
            '|| 8 <small>(8.0%)</small> '
            '|| 9 <small>(9.0%)</small> '
            '|| [//tools.wmflabs.org/heritage/api/api.php?action=adminlevels&format=json&admtree=foobar 11] <small>(11.0%)</small> '
            '|| 12 <small>(12.0%)</small> '
            '|| 13 <small>(13.0%)</small> '
            '|| 14 <small>(14.0%)</small> '
            '|| 15 \n'
            '|-\n'
            '| [//tools.wmflabs.org/heritage/api/api.php?action=statistics&stcountry=foo&format=html&limit=0 foo] '
            '|| zen || 10 '
            '|| 10 <small>(100.0%)</small> '
            '|| 10 <small>(100.0%)</small> '
            '|| 10 <small>(100.0%)</small> '
            '|| 10 <small>(100.0%)</small> '
            '|| 10 <small>(100.0%)</small> '
            '|| 10 <small>(100.0%)</small> '
            '|| 10 <small>(100.0%)</small> '
            '|| 10 <small>(100.0%)</small> '
            '|| 10 <small>(100.0%)</small> '
            '|| [//tools.wmflabs.org/heritage/api/api.php?action=adminlevels&format=json&admtree=foozen 10] <small>(100.0%)</small> '
            '|| 10 <small>(100.0%)</small> '
            '|| 10 <small>(100.0%)</small> '
            '|| 10 <small>(100.0%)</small> '
            '|| 10 \n'
            '|-\n'
            '| [//tools.wmflabs.org/heritage/api/api.php?action=statistics&stcountry=goo&format=html&limit=0 goo] '
            '|| zen || 10 '
            '|| 10 <small>(100.0%)</small> '
            '|| 10 <small>(100.0%)</small> '
            '|| 10 <small>(100.0%)</small> '
            '|| 10 <small>(100.0%)</small> '
            '|| 10 <small>(100.0%)</small> '
            '|| 10 <small>(100.0%)</small> '
            '|| 10 <small>(100.0%)</small> '
            '|| 10 <small>(100.0%)</small> '
            '|| 10 <small>(100.0%)</small> '
            '|| [//tools.wmflabs.org/heritage/api/api.php?action=adminlevels&format=json&admtree=goozen 10] <small>(100.0%)</small> '
            '|| 10 <small>(100.0%)</small> '
            '|| 10 <small>(100.0%)</small> '
            '|| 10 <small>(100.0%)</small> '
            '|| 10 \n'
        )
        expected_summation_row = (
            '|- class="sortbottom"\n'
            '| '
            '|| || 120 '
            '|| 21 <small>(17.5%)</small> '
            '|| 22 <small>(18.33%)</small> '
            '|| 23 <small>(19.17%)</small> '
            '|| 24 <small>(20.0%)</small> '
            '|| 25 <small>(20.83%)</small> '
            '|| 26 <small>(21.67%)</small> '
            '|| 27 <small>(22.5%)</small> '
            '|| 28 <small>(23.33%)</small> '
            '|| 29 <small>(24.17%)</small> '
            '|| 31 <small>(25.83%)</small> '
            '|| 32 <small>(26.67%)</small> '
            '|| 33 <small>(27.5%)</small> '
            '|| 34 <small>(28.33%)</small> '
            '|| 35 \n'
        )

        database_statistics.outputStatistics(statistics)
        self.bundled_asserts(expected_rows, expected_summation_row)

    def test_output_statistics_single_empty(self):
        statistics = {'foo_country': {'bar_lang': {}}}

        expected_rows = (
            '|-\n'
            '|| foo_country || bar_lang'
            '|| colspan="15" | Datasource [//tools.wmflabs.org/heritage/monuments_config/foo_country_bar_lang.json (foo_country, bar_lang)] is configured, but no monuments are in the database.\n'
        )
        expected_summation_row = (
            '|- class="sortbottom"\n'
            '| '
            '|| || 0 '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 \n'
        )

        database_statistics.outputStatistics(statistics)
        self.bundled_asserts(expected_rows, expected_summation_row)

    def test_output_statistics_multiple_empty(self):
        statistics = {
            'foo_country': {
                'bar_lang': {},
                'zen_lang': {}
            },
            'goo_country': {
                'zen_lang': {}
            }
        }

        expected_rows = (
            '|-\n'
            '|| foo_country || bar_lang'
            '|| colspan="15" | Datasource [//tools.wmflabs.org/heritage/monuments_config/foo_country_bar_lang.json (foo_country, bar_lang)] is configured, but no monuments are in the database.\n'
            '|-\n'
            '|| foo_country || zen_lang'
            '|| colspan="15" | Datasource [//tools.wmflabs.org/heritage/monuments_config/foo_country_zen_lang.json (foo_country, zen_lang)] is configured, but no monuments are in the database.\n'
            '|-\n'
            '|| goo_country || zen_lang'
            '|| colspan="15" | Datasource [//tools.wmflabs.org/heritage/monuments_config/goo_country_zen_lang.json (goo_country, zen_lang)] is configured, but no monuments are in the database.\n'
        )
        expected_summation_row = (
            '|- class="sortbottom"\n'
            '| '
            '|| || 0 '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 <small>(0.0%)</small> '
            '|| 0 \n'
        )

        database_statistics.outputStatistics(statistics)
        self.bundled_asserts(expected_rows, expected_summation_row)

    def test_output_statistics_mixed(self):
        statistics = {
            'foo_country': {
                'bar_lang': {
                    'country': 'foo',
                    'lang': 'bar',
                    'all': 100,
                    'name': 1,
                    'address': 2,
                    'municipality': 3,
                    'coordinates': 4,
                    'image': 5,
                    'commonscat': 6,
                    'article': 7,
                    'wikidata': 8,
                    'adm0': 9,
                    'adm1': 11,
                    'adm2': 12,
                    'adm3': 13,
                    'adm4': 14,
                    'adm0iso': 'foobar',
                    'source': 15
                }
            },
            'goo_country': {
                'zen_lang': {}
            }
        }

        expected_rows = (
            '|-\n'
            '| [//tools.wmflabs.org/heritage/api/api.php?action=statistics&stcountry=foo&format=html&limit=0 foo] '
            '|| bar || 100 '
            '|| 1 <small>(1.0%)</small> '
            '|| 2 <small>(2.0%)</small> '
            '|| 3 <small>(3.0%)</small> '
            '|| 4 <small>(4.0%)</small> '
            '|| 5 <small>(5.0%)</small> '
            '|| 6 <small>(6.0%)</small> '
            '|| 7 <small>(7.0%)</small> '
            '|| 8 <small>(8.0%)</small> '
            '|| 9 <small>(9.0%)</small> '
            '|| [//tools.wmflabs.org/heritage/api/api.php?action=adminlevels&format=json&admtree=foobar 11] <small>(11.0%)</small> '
            '|| 12 <small>(12.0%)</small> '
            '|| 13 <small>(13.0%)</small> '
            '|| 14 <small>(14.0%)</small> '
            '|| 15 \n'
            '|-\n'
            '|| goo_country || zen_lang'
            '|| colspan="15" | Datasource [//tools.wmflabs.org/heritage/monuments_config/goo_country_zen_lang.json (goo_country, zen_lang)] is configured, but no monuments are in the database.\n'
        )
        expected_summation_row = (
            '|- class="sortbottom"\n'
            '| '
            '|| || 100 '
            '|| 1 <small>(1.0%)</small> '
            '|| 2 <small>(2.0%)</small> '
            '|| 3 <small>(3.0%)</small> '
            '|| 4 <small>(4.0%)</small> '
            '|| 5 <small>(5.0%)</small> '
            '|| 6 <small>(6.0%)</small> '
            '|| 7 <small>(7.0%)</small> '
            '|| 8 <small>(8.0%)</small> '
            '|| 9 <small>(9.0%)</small> '
            '|| 11 <small>(11.0%)</small> '
            '|| 12 <small>(12.0%)</small> '
            '|| 13 <small>(13.0%)</small> '
            '|| 14 <small>(14.0%)</small> '
            '|| 15 \n'
        )

        database_statistics.outputStatistics(statistics)
        self.bundled_asserts(expected_rows, expected_summation_row)
