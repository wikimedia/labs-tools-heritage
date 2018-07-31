"""Unit tests for database_statistics."""
import unittest

import mock

import pywikibot

from erfgoedbot import database_statistics


class TestCreateReportBase(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch(
            'erfgoedbot.database_statistics.common.save_to_wiki_or_local')
        self.mock_save_to_wiki_or_local = patcher.start()
        self.addCleanup(patcher.stop)

        # silence logger
        patcher = mock.patch(
            'erfgoedbot.database_statistics.pywikibot.debug')
        self.mock_debug = patcher.start()
        self.addCleanup(patcher.stop)


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


class TestOutputStatistics(TestCreateReportBase):

    """Test the outputStatistics method."""

    def setUp(self):
        super(TestOutputStatistics, self).setUp()

        self.prefix = (
            u'{| class="wikitable sortable"\n'
            u'! country\n'
            u'! [[:en:List of ISO 639-1 codes|lang]]\n'
            u'! data-sort-type="number"| total\n'
            u'! data-sort-type="number"| name\n'
            u'! data-sort-type="number"| address\n'
            u'! data-sort-type="number"| municipality\n'
            u'! data-sort-type="number"| coordinates\n'
            u'! data-sort-type="number"| image\n'
            u'! data-sort-type="number"| commonscat\n'
            u'! data-sort-type="number"| article\n'
            u'! data-sort-type="number"| wikidata\n'
            u'! data-sort-type="number"| [[:en:ISO 3166-1 alpha-2#Officially assigned code elements|adm0]]\n'
            u'! data-sort-type="number"| [[:en:ISO 3166-2#Current codes|adm1]]\n'
            u'! data-sort-type="number"| adm2\n'
            u'! data-sort-type="number"| adm3\n'
            u'! data-sort-type="number"| adm4\n'
            u'! data-sort-type="number"| source pages\n')

        self.postfix = u'|}\n'

        self.comment = u'Updating monument database statistics'
        commons = pywikibot.Site('commons', 'commons')
        self.page = pywikibot.Page(
            commons, u'Commons:Monuments database/Statistics')

    def bundled_asserts(self, expected_rows,
                        expected_summation_row):
        """The full battery of asserts to do for each test."""
        expected_text = (self.prefix + expected_rows +
                         expected_summation_row + self.postfix)
        self.mock_save_to_wiki_or_local.assert_called_once_with(
            self.page,
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
            u'|-\n'
            u'| [//tools.wmflabs.org/heritage/api/api.php?action=statistics&stcountry=foo&format=html&limit=0 foo] '
            u'|| bar || 100 '
            u'|| 1 <small>(1.0%)</small>'
            u'|| 2 <small>(2.0%)</small>'
            u'|| 3 <small>(3.0%)</small>'
            u'|| 4 <small>(4.0%)</small>'
            u'|| 5 <small>(5.0%)</small>'
            u'|| 6 <small>(6.0%)</small>'
            u'|| 7 <small>(7.0%)</small>'
            u'|| 8 <small>(8.0%)</small>'
            u'|| 9 <small>(9.0%)</small>'
            u'|| [//tools.wmflabs.org/heritage/api/api.php?action=adminlevels&format=json&admtree=foobar 11] <small>(11.0%)</small>'
            u'|| 12 <small>(12.0%)</small>'
            u'|| 13 <small>(13.0%)</small>'
            u'|| 14 <small>(14.0%)</small>'
            u'|| 15\n'
        )
        expected_summation_row = (
            u'|- class="sortbottom"\n'
            u'| '
            u'|| || 100'
            u'|| 1 <small>(1.0%)</small>'
            u'|| 2 <small>(2.0%)</small>'
            u'|| 3 <small>(3.0%)</small>'
            u'|| 4 <small>(4.0%)</small>'
            u'|| 5 <small>(5.0%)</small>'
            u'|| 6 <small>(6.0%)</small>'
            u'|| 7 <small>(7.0%)</small>'
            u'|| 8 <small>(8.0%)</small>'
            u'|| 9 <small>(9.0%)</small>'
            u'|| 11 <small>(11.0%)</small>'
            u'|| 12 <small>(12.0%)</small>'
            u'|| 13 <small>(13.0%)</small>'
            u'|| 14 <small>(14.0%)</small>'
            u'|| 15\n'
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
            u'|-\n'
            u'| [//tools.wmflabs.org/heritage/api/api.php?action=statistics&stcountry=foo&format=html&limit=0 foo] '
            u'|| bar || 100 '
            u'|| 1 <small>(1.0%)</small>'
            u'|| 2 <small>(2.0%)</small>'
            u'|| 3 <small>(3.0%)</small>'
            u'|| 4 <small>(4.0%)</small>'
            u'|| 5 <small>(5.0%)</small>'
            u'|| 6 <small>(6.0%)</small>'
            u'|| 7 <small>(7.0%)</small>'
            u'|| 8 <small>(8.0%)</small>'
            u'|| 9 <small>(9.0%)</small>'
            u'|| [//tools.wmflabs.org/heritage/api/api.php?action=adminlevels&format=json&admtree=foobar 11] <small>(11.0%)</small>'
            u'|| 12 <small>(12.0%)</small>'
            u'|| 13 <small>(13.0%)</small>'
            u'|| 14 <small>(14.0%)</small>'
            u'|| 15\n'
            u'|-\n'
            u'| [//tools.wmflabs.org/heritage/api/api.php?action=statistics&stcountry=foo&format=html&limit=0 foo] '
            u'|| zen || 10 '
            u'|| 10 <small>(100.0%)</small>'
            u'|| 10 <small>(100.0%)</small>'
            u'|| 10 <small>(100.0%)</small>'
            u'|| 10 <small>(100.0%)</small>'
            u'|| 10 <small>(100.0%)</small>'
            u'|| 10 <small>(100.0%)</small>'
            u'|| 10 <small>(100.0%)</small>'
            u'|| 10 <small>(100.0%)</small>'
            u'|| 10 <small>(100.0%)</small>'
            u'|| [//tools.wmflabs.org/heritage/api/api.php?action=adminlevels&format=json&admtree=foozen 10] <small>(100.0%)</small>'
            u'|| 10 <small>(100.0%)</small>'
            u'|| 10 <small>(100.0%)</small>'
            u'|| 10 <small>(100.0%)</small>'
            u'|| 10\n'
            u'|-\n'
            u'| [//tools.wmflabs.org/heritage/api/api.php?action=statistics&stcountry=goo&format=html&limit=0 goo] '
            u'|| zen || 10 '
            u'|| 10 <small>(100.0%)</small>'
            u'|| 10 <small>(100.0%)</small>'
            u'|| 10 <small>(100.0%)</small>'
            u'|| 10 <small>(100.0%)</small>'
            u'|| 10 <small>(100.0%)</small>'
            u'|| 10 <small>(100.0%)</small>'
            u'|| 10 <small>(100.0%)</small>'
            u'|| 10 <small>(100.0%)</small>'
            u'|| 10 <small>(100.0%)</small>'
            u'|| [//tools.wmflabs.org/heritage/api/api.php?action=adminlevels&format=json&admtree=goozen 10] <small>(100.0%)</small>'
            u'|| 10 <small>(100.0%)</small>'
            u'|| 10 <small>(100.0%)</small>'
            u'|| 10 <small>(100.0%)</small>'
            u'|| 10\n'
        )
        expected_summation_row = (
            u'|- class="sortbottom"\n'
            u'| '
            u'|| || 120'
            u'|| 21 <small>(17.5%)</small>'
            u'|| 22 <small>(18.33%)</small>'
            u'|| 23 <small>(19.17%)</small>'
            u'|| 24 <small>(20.0%)</small>'
            u'|| 25 <small>(20.83%)</small>'
            u'|| 26 <small>(21.67%)</small>'
            u'|| 27 <small>(22.5%)</small>'
            u'|| 28 <small>(23.33%)</small>'
            u'|| 29 <small>(24.17%)</small>'
            u'|| 31 <small>(25.83%)</small>'
            u'|| 32 <small>(26.67%)</small>'
            u'|| 33 <small>(27.5%)</small>'
            u'|| 34 <small>(28.33%)</small>'
            u'|| 35\n'
        )

        database_statistics.outputStatistics(statistics)
        self.bundled_asserts(expected_rows, expected_summation_row)
