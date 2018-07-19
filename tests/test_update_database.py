"""Unit tests for update_database."""

import unittest
from collections import Counter

import mock

import pywikibot

from erfgoedbot import update_database


class TestUpdateDatabaseBase(unittest.TestCase):

    def setUp(self):
        self.country_config = {
            'primkey': u'id',
            'table': 'dummy_table',
            'fields': [
                {
                    'source': u'id',
                    'dest': u'id',
                },
                {
                    'source': u'name',
                    'dest': u'name',
                }
            ],
        }
        self.mock_page = mock.create_autospec(
            update_database.pywikibot.Page,
        )
        self.mock_page.title.return_value = "MockPageTitle"
        self.mock_cursor = mock.Mock()
        self.source = 'DummySource'


class TestProcessMonumentNoPrimkey(TestUpdateDatabaseBase):

    def setUp(self):
        super(TestProcessMonumentNoPrimkey, self).setUp()
        self.country_config['primkey'] = None
        self.header_defaults = {}

    def test_process_monument_with_empty_params_returns_empty_unknown_fields(self):
        params = {}
        unknown_fields = {}
        with self.assertRaises(update_database.NoPrimkeyException):
            update_database.process_monument(
                params, self.source, self.country_config, None, None,
                self.mock_page, self.header_defaults, unknown_fields)
        self.assertEqual(unknown_fields, {})

    def test_process_monument_with_one_unknown_param_correctly_returns_unknown_fields(self):
        params = [
            u'id=1234',
            u'name=A Monument Name',
            u'some_unknown_field=An unknown field value'
        ]
        unknown_fields = {}
        expected_unknown = Counter({self.mock_page: 1})
        with self.assertRaises(update_database.NoPrimkeyException):
            update_database.process_monument(
                params, self.source, self.country_config, None, None,
                self.mock_page, self.header_defaults, unknown_fields)
        self.assertEqual(
            unknown_fields,
            {u'some_unknown_field': expected_unknown}
        )


class TestProcessMonumentWithPrimkey(TestUpdateDatabaseBase):

    def test_process_monument_with_empty_primkey_value(self):
        params = [u'id=', u'name=A Monument Name']
        header_defaults = {}
        unknown_fields = {}

        with self.assertRaises(update_database.NoPrimkeyException):
            update_database.process_monument(
                params, self.source, self.country_config, None,
                self.mock_cursor, self.mock_page, header_defaults,
                unknown_fields)
        self.assertEqual(unknown_fields, {})

    def test_process_monument_calls_update_monument_and_returns_unknown_fields(self):
        params = [
            u'id=1234',
            u'name=A Monument Name',
            u'some_unknown_field=An unknown field value'
        ]
        header_defaults = {}
        unknown_fields = {}

        expected_contents = {
            'title': 'MockPageTitle',
            u'id': u'1234',
            u'name': u'A Monument Name',
            'source': 'DummySource'
        }
        expected_unknown = Counter({self.mock_page: 1})

        with mock.patch('erfgoedbot.update_database.update_monument', autospec=True) as mock_update_monument:
            update_database.process_monument(
                params, self.source, self.country_config, None,
                self.mock_cursor, self.mock_page, header_defaults,
                unknown_fields)
            mock_update_monument.assert_called_once_with(
                expected_contents, 'DummySource', self.country_config, None,
                self.mock_cursor, self.mock_page)
        self.assertEqual(
            unknown_fields,
            {u'some_unknown_field': expected_unknown}
        )


class TestUpdateMonument(TestUpdateDatabaseBase):

    def test_update_monument_executes_database_replace(self):
        source = 'DummySource'
        contents = {
            'title': 'MockPageTitle',
            u'id': u'1234',
            u'name': u'A Monument Name',
            'source': source
        }
        update_database.update_monument(contents, source, self.country_config, None, self.mock_cursor, self.mock_page)
        expected_query = u'REPLACE INTO `dummy_table` (`source`, `id`, `name`) VALUES (%s, %s, %s)'
        expected_query_params = ['DummySource', u'1234', u'A Monument Name']
        self.mock_cursor.execute.assert_called_once_with(expected_query, expected_query_params)


class TestProcessHeader(TestUpdateDatabaseBase):

    def test_process_header_parses_correct_fields_and_skips_unknowns(self):
        params = [u'id=1234', u'name=A Monument Name', u'some_unknown_field=An unknown field value']
        result = update_database.process_header(params, self.country_config)
        expected_contents = {
            u'id': u'1234',
            u'name': u'A Monument Name',
        }
        self.assertEqual(result, expected_contents)


class TestLookupSourceField(TestUpdateDatabaseBase):

    def setUp(self):
        super(TestLookupSourceField, self).setUp()
        self.country_config['fields'].append(
            {
                'source': u'source-name',
                'dest': u'dest-name',
            }
        )

    def test_lookup_source_field_on_unknown_field_return_none(self):
        result = update_database.lookup_source_field("unknown", self.country_config)
        self.assertEqual(result, None)

    def test_lookup_source_field_on_known_field_return_source(self):
        result = update_database.lookup_source_field(u'dest-name', self.country_config)
        self.assertEqual(result, 'source-name')


class TestProcessPage(TestUpdateDatabaseBase):

    def setUp(self):
        super(TestProcessPage, self).setUp()
        self.mock_template = mock.create_autospec(
            update_database.pywikibot.Page,
        )
        self.mock_template.title.return_value = "MockTemplate"

        self.mock_page.templatesWithParams.return_value = [
            (self.mock_template, ['a', 'b'])
        ]

    def test_process_page_calls_process_header(self):
        self.country_config['headerTemplate'] = 'MockTemplate'
        with mock.patch('erfgoedbot.update_database.process_header', autospec=True) as mock_process_header:
            update_database.process_page(self.mock_page, self.source, self.country_config, None, None)
            mock_process_header.assert_called_once_with(['a', 'b'], self.country_config)

    def test_process_page_calls_process_monument(self):
        self.country_config['rowTemplate'] = 'MockTemplate'
        with mock.patch('erfgoedbot.update_database.process_monument', autospec=True) as mock_process_monument:
            update_database.process_page(self.mock_page, self.source, self.country_config, None, None)
            mock_process_monument.assert_called_once_with(
                ['a', 'b'],
                self.source,
                self.country_config,
                None, None, self.mock_page, {}, unknown_fields={}
            )

#    # awaiting solution to T147752
#    def test_process_page_warning_on_NoPrimkeyException(self):
#        self.country_config['rowTemplate'] = 'MockTemplate'
#        ## two templates to ensure count works
#        self.mock_page.templatesWithParams.return_value = [
#            (self.mock_template, ['a', 'b']),
#            (self.mock_template, ['a', 'b'])
#        ]
#
#        warning_patcher = mock.patch('erfgoedbot.update_database.pywikibot.warning', autospec=True)
#        mock_warning = warning_patcher.start()
#        self.addCleanup(warning_patcher.stop)
#
#        with mock.patch('erfgoedbot.update_database.process_monument', autospec=True,
#                        side_effect=update_database.NoPrimkeyException):
#            update_database.process_page(
#                self.mock_page, self.source, self.country_config, None, None)
#            mock_warning.assert_called_once_with(
#                u"2 primkey(s) missing on MockPageTitle (dummy_table)")


class TestCountryBboxRequireLatLon(TestUpdateDatabaseBase):

    def setUp(self):
        super(TestCountryBboxRequireLatLon, self).setUp()
        self.country_config['countryBbox'] = u'8.5,10.5,28.0,60.0'
        self.monument_key = 'some-key'
        self.contents = {
            'title': 'MockPageTitle',
            u'id': self.monument_key,
            u'name': u'A Monument Name',
            'source': self.source
        }

    def test_countryBbox_calls_check(self):
        expected_fieldnames = [u'source', u'id', u'name']
        with mock.patch('erfgoedbot.update_database.check_lat_with_lon', autospec=True) as mock_check_lat_with_lon:
            update_database.update_monument(self.contents, self.source, self.country_config, None, self.mock_cursor, self.mock_page)
            mock_check_lat_with_lon.assert_called_once_with(expected_fieldnames, self.monument_key, self.mock_page)

    def test_countryBbox_calls_check_with_lon(self):
        self.country_config['fields'].append(
            {
                'source': u'lon',
                'dest': u'lon',
            }
        )
        self.contents['lon'] = '123'
        expected_fieldnames = [u'source', u'id', u'name', 'lon']
        with mock.patch('erfgoedbot.update_database.check_lat_with_lon', autospec=True) as mock_check_lat_with_lon:
            update_database.update_monument(self.contents, self.source, self.country_config, None, self.mock_cursor, self.mock_page)
            mock_check_lat_with_lon.assert_called_once_with(expected_fieldnames, self.monument_key, self.mock_page)


class TestTriggerConversion(TestUpdateDatabaseBase):

    def test_call_convert_field(self):
        new_field = {
            'source': u'source-name',
            'dest': u'dest-name',
            'conv': 'some-converter',
        }
        self.country_config['fields'].append(new_field)
        source = 'DummySource'
        contents = {
            'title': 'MockPageTitle',
            u'id': u'1234',
            u'name': u'A Monument Name',
            'source-name': u'Some value',
            'source': source
        }

        with mock.patch('erfgoedbot.update_database.convert_field', autospec=True) as mock_convert_field:
            update_database.update_monument(contents, source, self.country_config, None, self.mock_cursor, self.mock_page)
            mock_convert_field.assert_called_once_with(new_field, contents, self.country_config)


class TestTriggerChecks(TestUpdateDatabaseBase):

    def setUp(self):
        super(TestTriggerChecks, self).setUp()
        self.monument_key = 'some-key'
        self.contents = {
            'title': 'MockPageTitle',
            u'id': self.monument_key,
            u'name': u'A Monument Name',
            'source': self.source
        }

    def test_trigger_checkLat(self):
        self.country_config['fields'].append(
            {
                'source': u'lat',
                'dest': u'lat',
                'check': u'checkLat',
            }
        )
        lat = '13.37'
        self.contents[u'lat'] = lat

        with mock.patch('erfgoedbot.update_database.checkLat', autospec=True) as mock_checkLat:
            update_database.update_monument(self.contents, self.source, self.country_config, None, self.mock_cursor, self.mock_page)
            mock_checkLat.assert_called_once_with(lat, self.monument_key, self.country_config, self.mock_page)

    def test_trigger_checkLon(self):
        self.country_config['fields'].append(
            {
                'source': u'lon',
                'dest': u'lon',
                'check': u'checkLon',
            }
        )
        lon = '-13.37'
        self.contents[u'lon'] = lon

        with mock.patch('erfgoedbot.update_database.checkLon', autospec=True) as mock_checkLon:
            update_database.update_monument(self.contents, self.source, self.country_config, None, self.mock_cursor, self.mock_page)
            mock_checkLon.assert_called_once_with(lon, self.monument_key, self.country_config, self.mock_page)

    def test_trigger_checkWD(self):
        self.country_config['fields'].append(
            {
                'source': u'wd_item',
                'dest': u'wd_item',
                'check': u'checkWD',
            }
        )
        wd_item = 'Q123'
        self.contents[u'wd_item'] = wd_item

        with mock.patch('erfgoedbot.update_database.check_wikidata', autospec=True) as mock_check_wikidata:
            update_database.update_monument(self.contents, self.source, self.country_config, None, self.mock_cursor, self.mock_page)
            mock_check_wikidata.assert_called_once_with(wd_item, self.monument_key, self.mock_page)

    def test_trigger_unknown_check(self):
        self.country_config['fields'].append(
            {
                'source': u'source-field',
                'dest': u'dest-field',
                'check': u'unknown',
            }
        )
        val = 'something'
        self.contents[u'source-field'] = val

        with self.assertRaises(pywikibot.Error) as cm:
            update_database.update_monument(self.contents, self.source, self.country_config, None, self.mock_cursor, self.mock_page)
            self.assertEqual(cm.exception, 'Un-defined check in config for dummy_table: unknown')

    def test_trigger_problematic_check(self):
        # It is a known bug that any function can be triggered using a check
        self.country_config['fields'].append(
            {
                'source': u'source-field',
                'dest': u'dest-field',
                'check': u'connectDatabase',
            }
        )
        val = 'something'
        self.contents[u'source-field'] = val

        with self.assertRaises(pywikibot.Error) as cm:
            update_database.update_monument(self.contents, self.source, self.country_config, None, self.mock_cursor, self.mock_page)
            self.assertEqual(cm.exception, 'Un-defined check in config for dummy_table: connectDatabase')


class TestFormatSourceField(unittest.TestCase):

    def setUp(self):
        self.commons = pywikibot.Site('commons', 'commons')
        site = pywikibot.Site('test', 'wikipedia')
        self.page_1 = pywikibot.Page(site, 'Foo1')
        self.page_2 = pywikibot.Page(site, 'Foo2')
        self.page_3 = pywikibot.Page(site, 'Foo3')

    def test_format_source_field_single(self):
        sources = Counter({self.page_1: 5})
        expected = u'[[wikipedia:test:Foo1|Foo1]]'
        self.assertEquals(
            update_database.format_source_field(sources, self.commons),
            expected
        )

    def test_format_source_field_max(self):
        sources = Counter({self.page_1: 1, self.page_2: 3, self.page_3: 2})
        expected = (
            u'\n* [[wikipedia:test:Foo2|Foo2]] (3)'
            u'\n* [[wikipedia:test:Foo3|Foo3]] (2)'
            u'\n* [[wikipedia:test:Foo1|Foo1]] (1)'
        )
        self.assertEquals(
            update_database.format_source_field(
                sources, self.commons, sample_size=3),
            expected
        )

    def test_format_source_field_remaining(self):
        sources = Counter({self.page_1: 1, self.page_2: 3, self.page_3: 2})
        expected = (
            u'\n* [[wikipedia:test:Foo2|Foo2]] (3)'
            u'\n* [[wikipedia:test:Foo3|Foo3]] (2)'
            u"\n* ''and 1 more page(s)''"
        )
        self.assertEquals(
            update_database.format_source_field(
                sources, self.commons, sample_size=2),
            expected
        )
