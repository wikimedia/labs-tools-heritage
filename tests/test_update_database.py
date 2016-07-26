"""Unit tests for update_database."""

import mock
import unittest
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

    def test_processMonument_with_empty_params_returns_empty_unknown_fields(self):
        params = {}
        header_defaults = {}
        result = update_database.processMonument(params, self.source, self.country_config, None, None, self.mock_page, header_defaults)
        self.assertEqual(result, {})

    def test_processMonument_with_one_unknown_param_correctly_returns_unknown_fields(self):
        params = [u'id=1234', u'name=A Monument Name', u'some_unknown_field=An unknown field value']
        header_defaults = {}
        result = update_database.processMonument(params, self.source, self.country_config, None, None, self.mock_page, header_defaults)
        self.assertEqual(result, {u'some_unknown_field': 1})


class TestProcessMonumentWithPrimkey(TestUpdateDatabaseBase):

    def test_processMonument_calls_updateMonument_and_returns_unknown_fields(self):
        params = [u'id=1234', u'name=A Monument Name', u'some_unknown_field=An unknown field value']
        header_defaults = {}

        expected_contents = {
            'title': 'MockPageTitle',
            u'id': u'1234',
            u'name': u'A Monument Name',
            'source': 'DummySource'
        }

        with mock.patch('erfgoedbot.update_database.updateMonument', autospec=True) as mock_updateMonument:
            result = update_database.processMonument(params, self.source, self.country_config, None, self.mock_cursor, self.mock_page, header_defaults)
            mock_updateMonument.assert_called_once_with(expected_contents, 'DummySource', self.country_config, None, self.mock_cursor, self.mock_page)
        self.assertEqual(result, {u'some_unknown_field': 1})


class TestUpdateMonument(TestUpdateDatabaseBase):

    def test_updateMonument_executes_database_replace(self):
        source = 'DummySource'
        contents = {
            'title': 'MockPageTitle',
            u'id': u'1234',
            u'name': u'A Monument Name',
            'source': source
        }
        update_database.updateMonument(contents, source, self.country_config, None, self.mock_cursor, self.mock_page)
        expected_query = u'REPLACE INTO `dummy_table`(`source`, `id`, `name`) VALUES (%s, %s, %s)'
        expected_query_params = ['DummySource', u'1234', u'A Monument Name']
        self.mock_cursor.execute.assert_called_once_with(expected_query, expected_query_params)


class TestProcessHeader(TestUpdateDatabaseBase):

    def test_process_header_parses_correct_fields_and_skips_unknowns(self):
        params = [u'id=1234', u'name=A Monument Name', u'some_unknown_field=An unknown field value']
        result = update_database.processHeader(params, self.country_config)
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

    def test_lookupSourceField_on_unknown_field_return_none(self):
        result = update_database.lookupSourceField("unknown", self.country_config)
        self.assertEqual(result, None)

    def test_lookupSourceField_on_known_field_return_source(self):
        result = update_database.lookupSourceField(u'dest-name', self.country_config)
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

    def test_processPage_calls_processHeader(self):
        self.country_config['headerTemplate'] = 'MockTemplate'
        with mock.patch('erfgoedbot.update_database.processHeader', autospec=True) as mock_processHeader:
            update_database.processPage(self.mock_page, self.source, self.country_config, None, None)
            mock_processHeader.assert_called_once_with(['a', 'b'], self.country_config)

    def test_processPage_calls_processMonument(self):
        self.country_config['rowTemplate'] = 'MockTemplate'
        with mock.patch('erfgoedbot.update_database.processMonument', autospec=True) as mock_processMonument:
            update_database.processPage(self.mock_page, self.source, self.country_config, None, None)
            mock_processMonument.assert_called_once_with(
                ['a', 'b'],
                self.source,
                self.country_config,
                None, None, self.mock_page, {}, unknownFields={}
            )


class TestCountryBboxRequireLatLon(TestUpdateDatabaseBase):

    def setUp(self):
        super(TestCountryBboxRequireLatLon, self).setUp()
        self.country_config['countryBbox'] = u'8.5,10.5,28.0,60.0'
        self.monumentKey = 'some-key'
        self.contents = {
            'title': 'MockPageTitle',
            u'id': self.monumentKey,
            u'name': u'A Monument Name',
            'source': self.source
        }

    def test_countryBbox_calls_check(self):
        expected_fieldnames = [u'source', u'id', u'name']
        with mock.patch('erfgoedbot.update_database.check_lat_with_lon', autospec=True) as mock_check_lat_with_lon:
            update_database.updateMonument(self.contents, self.source, self.country_config, None, self.mock_cursor, self.mock_page)
            mock_check_lat_with_lon.assert_called_once_with(expected_fieldnames, self.monumentKey, self.mock_page)

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
            update_database.updateMonument(self.contents, self.source, self.country_config, None, self.mock_cursor, self.mock_page)
            mock_check_lat_with_lon.assert_called_once_with(expected_fieldnames, self.monumentKey, self.mock_page)


class TestTriggerConversion(TestUpdateDatabaseBase):

    def test_call_convertField(self):
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

        with mock.patch('erfgoedbot.update_database.convertField', autospec=True) as mock_convertField:
            update_database.updateMonument(contents, source, self.country_config, None, self.mock_cursor, self.mock_page)
            mock_convertField.assert_called_once_with(new_field, contents, self.country_config)


class TestTriggerChecks(TestUpdateDatabaseBase):

    def setUp(self):
        super(TestTriggerChecks, self).setUp()
        self.monumentKey = 'some-key'
        self.contents = {
            'title': 'MockPageTitle',
            u'id': self.monumentKey,
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
            update_database.updateMonument(self.contents, self.source, self.country_config, None, self.mock_cursor, self.mock_page)
            mock_checkLat.assert_called_once_with(lat, self.monumentKey, self.country_config, self.mock_page)

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
            update_database.updateMonument(self.contents, self.source, self.country_config, None, self.mock_cursor, self.mock_page)
            mock_checkLon.assert_called_once_with(lon, self.monumentKey, self.country_config, self.mock_page)

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
            update_database.updateMonument(self.contents, self.source, self.country_config, None, self.mock_cursor, self.mock_page)
            mock_check_wikidata.assert_called_once_with(wd_item, self.monumentKey, self.mock_page)

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
            update_database.updateMonument(self.contents, self.source, self.country_config, None, self.mock_cursor, self.mock_page)
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
            update_database.updateMonument(self.contents, self.source, self.country_config, None, self.mock_cursor, self.mock_page)
            self.assertEqual(cm.exception, 'Un-defined check in config for dummy_table: connectDatabase')
