#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Unit tests for update_database."""

import unittest
import unittest.mock as mock
from collections import Counter, OrderedDict

import pywikibot

import custom_assertions  # noqa F401
from erfgoedbot import update_database
from report_base_test import TestCreateReportBase, TestCreateReportTableBase


class TestUpdateDatabaseBase(unittest.TestCase):

    def setUp(self):
        self.country_config = {
            'primkey': 'id',
            'table': 'dummy_table',
            'fields': [
                {
                    'source': 'id',
                    'dest': 'id',
                },
                {
                    'source': 'name',
                    'dest': 'name',
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
        harvest_state = update_database._new_harvest_state()
        with self.assertRaises(update_database.NoPrimkeyException):
            update_database.process_monument(
                params, self.source, self.country_config, None, None,
                self.mock_page, self.header_defaults, harvest_state)
        self.assertEqual(harvest_state['unknown_fields'], {})

    def test_process_monument_with_one_unknown_param_correctly_returns_unknown_fields(self):
        params = [
            'id=1234',
            'name=A Monument Name',
            'some_unknown_field=An unknown field value'
        ]
        harvest_state = update_database._new_harvest_state()
        expected_unknown = Counter({self.mock_page: 1})
        with self.assertRaises(update_database.NoPrimkeyException):
            update_database.process_monument(
                params, self.source, self.country_config, None, None,
                self.mock_page, self.header_defaults, harvest_state)
        self.assertEqual(
            harvest_state['unknown_fields'],
            {'some_unknown_field': expected_unknown}
        )


class TestProcessMonumentWithPrimkey(TestUpdateDatabaseBase):

    def test_process_monument_with_empty_primkey_value(self):
        params = ['id=', 'name=A Monument Name']
        header_defaults = {}
        harvest_state = update_database._new_harvest_state()

        with self.assertRaises(update_database.NoPrimkeyException):
            update_database.process_monument(
                params, self.source, self.country_config, None,
                self.mock_cursor, self.mock_page, header_defaults,
                harvest_state)
        self.assertEqual(harvest_state['unknown_fields'], {})

    def test_process_monument_calls_update_monument_and_returns_unknown_fields(self):
        params = [
            'id=1234',
            'name=A Monument Name',
            'some_unknown_field=An unknown field value'
        ]
        header_defaults = {}
        harvest_state = update_database._new_harvest_state()

        expected_contents = {
            'title': 'MockPageTitle',
            'id': '1234',
            'name': 'A Monument Name',
            'source': 'DummySource'
        }
        expected_unknown = Counter({self.mock_page: 1})

        with mock.patch('erfgoedbot.update_database.update_monument', autospec=True) as mock_update_monument:
            update_database.process_monument(
                params, self.source, self.country_config, None,
                self.mock_cursor, self.mock_page, header_defaults,
                harvest_state)
            mock_update_monument.assert_called_once_with(
                expected_contents, 'DummySource', self.country_config, None,
                self.mock_cursor, self.mock_page)
        self.assertEqual(
            harvest_state['unknown_fields'],
            {'some_unknown_field': expected_unknown}
        )
        self.assertEqual(
            harvest_state['seen_ids'], {'1234': self.mock_page})
        self.assertEqual(harvest_state['duplicate_ids'], {})

    def test_process_monument_tuple_primkey_tracks_composite_id(self):
        self.country_config['primkey'] = ('id', 'name')
        params = ['id=62096', 'name=CLT-0001']
        header_defaults = {}
        harvest_state = update_database._new_harvest_state()

        with mock.patch('erfgoedbot.update_database.update_monument', autospec=True):
            update_database.process_monument(
                params, self.source, self.country_config, None,
                self.mock_cursor, self.mock_page, header_defaults,
                harvest_state)
        self.assertEqual(
            harvest_state['seen_ids'],
            {'62096-CLT-0001': self.mock_page})
        self.assertEqual(harvest_state['duplicate_ids'], {})

    def test_process_monument_duplicate_id_detected(self):
        params = ['id=1234', 'name=A Monument Name']
        header_defaults = {}
        harvest_state = update_database._new_harvest_state()

        with mock.patch('erfgoedbot.update_database.update_monument', autospec=True):
            update_database.process_monument(
                params, self.source, self.country_config, None,
                self.mock_cursor, self.mock_page, header_defaults,
                harvest_state)
            update_database.process_monument(
                params, self.source, self.country_config, None,
                self.mock_cursor, self.mock_page, header_defaults,
                harvest_state)
        self.assertEqual(
            harvest_state['duplicate_ids'],
            {'1234': Counter({self.mock_page: 2})})


class TestProcessMonumentTuplePrimkey(TestUpdateDatabaseBase):

    def setUp(self):
        super(TestProcessMonumentTuplePrimkey, self).setUp()
        self.country_config['primkey'] = ('id', 'name')
        self.header_defaults = {}

    def test_process_monument_tuple_primkey_missing_part_raises(self):
        params = ['id=1234', 'name=']
        harvest_state = update_database._new_harvest_state()

        with self.assertRaises(update_database.NoPrimkeyException):
            update_database.process_monument(
                params, self.source, self.country_config, None,
                self.mock_cursor, self.mock_page, self.header_defaults,
                harvest_state)


class TestUpdateMonument(TestUpdateDatabaseBase):

    def test_update_monument_executes_database_replace(self):
        source = 'DummySource'
        contents = {
            'title': 'MockPageTitle',
            'id': '1234',
            'name': 'A Monument Name',
            'source': source
        }
        update_database.update_monument(contents, source, self.country_config, None, self.mock_cursor, self.mock_page)
        expected_query = 'REPLACE INTO `dummy_table` (`source`, `id`, `name`) VALUES (%s, %s, %s)'
        expected_query_params = ['DummySource', '1234', 'A Monument Name']
        self.mock_cursor.execute.assert_called_once_with(expected_query, expected_query_params)


class TestProcessHeader(TestUpdateDatabaseBase):

    def test_process_header_parses_correct_fields_and_skips_unknowns(self):
        params = ['id=1234', 'name=A Monument Name', 'some_unknown_field=An unknown field value']
        result = update_database.process_header(params, self.country_config)
        expected_contents = {
            'id': '1234',
            'name': 'A Monument Name',
        }
        self.assertEqual(result, expected_contents)


class TestLookupSourceField(TestUpdateDatabaseBase):

    def setUp(self):
        super(TestLookupSourceField, self).setUp()
        self.country_config['fields'].append(
            {
                'source': 'source-name',
                'dest': 'dest-name',
            }
        )

    def test_lookup_source_field_on_unknown_field_return_none(self):
        result = update_database.lookup_source_field("unknown", self.country_config)
        self.assertEqual(result, None)

    def test_lookup_source_field_on_known_field_return_source(self):
        result = update_database.lookup_source_field('dest-name', self.country_config)
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
                None, None, self.mock_page, {},
                harvest_state=update_database._new_harvest_state()
            )

    def test_process_page_Commonscat(self):
        self.mock_template.title.return_value = "Commonscat"
        self.country_config['lang'] = 'ge'
        update_database.process_page(self.mock_page, self.source, self.country_config, None, self.mock_cursor)
        expected_query = "REPLACE INTO commonscat (site, title, commonscat) VALUES (%s, %s, %s)"
        expected_query_params = ('ge', 'MockPageTitle', 'a')
        self.mock_cursor.execute.assert_called_once_with(expected_query, expected_query_params)

    def test_process_page_tracks_missing_ids_on_NoPrimkeyException(self):
        self.country_config['rowTemplate'] = 'MockTemplate'
        # two templates to ensure count works
        self.mock_page.templatesWithParams.return_value = [
            (self.mock_template, ['a', 'b']),
            (self.mock_template, ['a', 'b'])
        ]

        with mock.patch('erfgoedbot.update_database.process_monument',
                        autospec=True,
                        side_effect=update_database.NoPrimkeyException):
            result = update_database.process_page(
                self.mock_page, self.source, self.country_config, None, None)
            self.assertEqual(
                result['missing_ids'][self.mock_page], 2)

    def test_process_page_shared_harvest_state_across_pages(self):
        """Harvest state accumulates duplicates and missing IDs across pages."""
        self.country_config['rowTemplate'] = 'MockTemplate'

        page_a = mock.create_autospec(update_database.pywikibot.Page)
        page_a.title.return_value = 'PageA'
        page_a.templatesWithParams.return_value = [
            (self.mock_template, ['id=1234', 'name=Mon'])
        ]

        page_b = mock.create_autospec(update_database.pywikibot.Page)
        page_b.title.return_value = 'PageB'
        page_b.templatesWithParams.return_value = [
            (self.mock_template, ['id=1234', 'name=Mon']),
            (self.mock_template, ['id=5678', 'name=Other'])
        ]

        page_c = mock.create_autospec(update_database.pywikibot.Page)
        page_c.title.return_value = 'PageC'
        page_c.templatesWithParams.return_value = [
            (self.mock_template, ['id=', 'name=NoId'])
        ]

        harvest_state = update_database._new_harvest_state()
        with mock.patch('erfgoedbot.update_database.update_monument',
                        autospec=True):
            update_database.process_page(
                page_a, 'src_a', self.country_config, None, None,
                harvest_state=harvest_state)
            update_database.process_page(
                page_b, 'src_b', self.country_config, None, None,
                harvest_state=harvest_state)
            update_database.process_page(
                page_c, 'src_c', self.country_config, None, None,
                harvest_state=harvest_state)

        # id=1234 seen on page_a and page_b -> duplicate
        self.assertIn('1234', harvest_state['duplicate_ids'])
        self.assertEqual(
            harvest_state['duplicate_ids']['1234'][page_a], 1)
        self.assertEqual(
            harvest_state['duplicate_ids']['1234'][page_b], 1)
        # id=5678 seen only once -> not a duplicate
        self.assertNotIn('5678', harvest_state['duplicate_ids'])
        self.assertIn('5678', harvest_state['seen_ids'])
        # page_c has empty id -> missing
        self.assertEqual(harvest_state['missing_ids'][page_c], 1)


class TestCountryBboxRequireLatLon(TestUpdateDatabaseBase):

    def setUp(self):
        super(TestCountryBboxRequireLatLon, self).setUp()
        self.country_config['countryBbox'] = '8.5,10.5,28.0,60.0'
        self.monument_key = 'some-key'
        self.contents = {
            'title': 'MockPageTitle',
            'id': self.monument_key,
            'name': 'A Monument Name',
            'source': self.source
        }

    def test_countryBbox_calls_check(self):
        expected_fieldnames = ['source', 'id', 'name']
        with mock.patch('erfgoedbot.update_database.check_lat_with_lon', autospec=True) as mock_check_lat_with_lon:
            update_database.update_monument(self.contents, self.source, self.country_config, None, self.mock_cursor, self.mock_page)
            mock_check_lat_with_lon.assert_called_once_with(expected_fieldnames, self.monument_key, self.mock_page)

    def test_countryBbox_calls_check_with_lon(self):
        self.country_config['fields'].append(
            {
                'source': 'lon',
                'dest': 'lon',
            }
        )
        self.contents['lon'] = '123'
        expected_fieldnames = ['source', 'id', 'name', 'lon']
        with mock.patch('erfgoedbot.update_database.check_lat_with_lon', autospec=True) as mock_check_lat_with_lon:
            update_database.update_monument(self.contents, self.source, self.country_config, None, self.mock_cursor, self.mock_page)
            mock_check_lat_with_lon.assert_called_once_with(expected_fieldnames, self.monument_key, self.mock_page)


class TestTriggerConversion(TestUpdateDatabaseBase):

    def test_call_convert_field(self):
        new_field = {
            'source': 'source-name',
            'dest': 'dest-name',
            'conv': 'some-converter',
        }
        self.country_config['fields'].append(new_field)
        source = 'DummySource'
        contents = {
            'title': 'MockPageTitle',
            'id': '1234',
            'name': 'A Monument Name',
            'source-name': 'Some value',
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
            'id': self.monument_key,
            'name': 'A Monument Name',
            'source': self.source
        }

    def test_trigger_checkLat(self):
        self.country_config['fields'].append(
            {
                'source': 'lat',
                'dest': 'lat',
                'check': 'checkLat',
            }
        )
        lat = '13.37'
        self.contents['lat'] = lat

        with mock.patch('erfgoedbot.update_database.checkLat', autospec=True) as mock_checkLat:
            update_database.update_monument(self.contents, self.source, self.country_config, None, self.mock_cursor, self.mock_page)
            mock_checkLat.assert_called_once_with(lat, self.monument_key, self.country_config, self.mock_page)

    def test_trigger_checkLon(self):
        self.country_config['fields'].append(
            {
                'source': 'lon',
                'dest': 'lon',
                'check': 'checkLon',
            }
        )
        lon = '-13.37'
        self.contents['lon'] = lon

        with mock.patch('erfgoedbot.update_database.checkLon', autospec=True) as mock_checkLon:
            update_database.update_monument(self.contents, self.source, self.country_config, None, self.mock_cursor, self.mock_page)
            mock_checkLon.assert_called_once_with(lon, self.monument_key, self.country_config, self.mock_page)

    def test_trigger_checkWD(self):
        self.country_config['fields'].append(
            {
                'source': 'wd_item',
                'dest': 'wd_item',
                'check': 'checkWD',
            }
        )
        wd_item = 'Q123'
        self.contents['wd_item'] = wd_item

        with mock.patch('erfgoedbot.update_database.check_wikidata', autospec=True) as mock_check_wikidata:
            update_database.update_monument(self.contents, self.source, self.country_config, None, self.mock_cursor, self.mock_page)
            mock_check_wikidata.assert_called_once_with(wd_item, self.monument_key, self.mock_page)

    def test_trigger_unknown_check(self):
        self.country_config['fields'].append(
            {
                'source': 'source-field',
                'dest': 'dest-field',
                'check': 'unknown',
            }
        )
        val = 'something'
        self.contents['source-field'] = val

        with self.assertRaises(pywikibot.exceptions.Error) as cm:
            update_database.update_monument(
                self.contents, self.source, self.country_config, None,
                self.mock_cursor, self.mock_page)
            self.assertEqual(
                cm.exception,
                'Un-defined check in config for dummy_table: unknown')

    def test_trigger_problematic_check(self):
        # It is a known bug that any function can be triggered using a check
        self.country_config['fields'].append(
            {
                'source': 'source-field',
                'dest': 'dest-field',
                'check': 'connectDatabase',
            }
        )
        val = 'something'
        self.contents['source-field'] = val

        with self.assertRaises(pywikibot.exceptions.Error) as cm:
            update_database.update_monument(
                self.contents, self.source, self.country_config, None,
                self.mock_cursor, self.mock_page)
            self.assertEqual(
                cm.exception,
                'Un-defined check in config for dummy_table: connectDatabase')


class TestFormatSourceField(unittest.TestCase):

    def setUp(self):
        self.commons = pywikibot.Site('commons', 'commons')
        site = pywikibot.Site('test', 'wikipedia')
        self.page_1 = pywikibot.Page(site, 'Foo1')
        self.page_2 = pywikibot.Page(site, 'Foo2')
        self.page_3 = pywikibot.Page(site, 'Foo3')

    def test_format_source_field_single(self):
        sources = Counter({self.page_1: 5})
        expected = '[[wikipedia:test:Foo1|Foo1]]'
        self.assertEqual(
            update_database.format_source_field(sources, self.commons),
            expected
        )

    def test_format_source_field_max(self):
        sources = Counter({self.page_1: 1, self.page_2: 3, self.page_3: 2})
        expected = (
            '\n* [[wikipedia:test:Foo2|Foo2]] (3)'
            '\n* [[wikipedia:test:Foo3|Foo3]] (2)'
            '\n* [[wikipedia:test:Foo1|Foo1]] (1)'
        )
        self.assertEqual(
            update_database.format_source_field(
                sources, self.commons, sample_size=3),
            expected
        )

    def test_format_source_field_remaining(self):
        sources = Counter({self.page_1: 1, self.page_2: 3, self.page_3: 2})
        expected = (
            '\n* [[wikipedia:test:Foo2|Foo2]] (3)'
            '\n* [[wikipedia:test:Foo3|Foo3]] (2)'
            "\n* ''and 1 more page(s)''"
        )
        self.assertEqual(
            update_database.format_source_field(
                sources, self.commons, sample_size=2),
            expected
        )


class TestMakeAggregateStatistics(TestCreateReportTableBase):

    """Test the _make_aggregate_statistics helper."""

    def setUp(self):
        self.class_name = 'erfgoedbot.update_database'
        super(TestMakeAggregateStatistics, self).setUp()

        self.commons = self.mock_site.return_value
        self.pagename = 'Commons:Test/Statistics'
        self.title_column = OrderedDict([
            ('code', 'country'),
            ('lang', None),
            ('total_items', 'Total items'),
        ])
        self.comment_template = 'Updated. Total: {total_items} items.'

    def simple_row_builder(self, row, countryconfig, site):
        return {
            'code': countryconfig.get('country'),
            'lang': countryconfig.get('lang'),
            'total_items': row.get('total_items'),
        }

    def bundled_asserts(self, expected_rows, expected_total_items):
        """The full battery of asserts to do for each test."""
        expected_text = self.prefix + expected_rows + self.postfix.format(
            total_items=expected_total_items)

        self.mock_site.assert_called_once_with('commons', 'commons')
        self.mock_page.assert_called_once_with(
            self.mock_site.return_value, self.pagename)
        self.mock_save_to_wiki_or_local.assert_called_once_with(
            self.mock_page.return_value,
            self.comment_template.format(
                total_items=expected_total_items),
            expected_text
        )
        self.mock_table_header_row.assert_called_once()
        self.mock_table_bottom_row.assert_called_once_with(3, {
            2: expected_total_items})

    def test__make_aggregate_statistics_single_row(self):
        statistics = [{
            'config': {'lang': 'en', 'country': 'foo'},
            'total_items': 42,
        }]

        expected_rows = (
            '|-\n'
            '| foo \n'
            '| en \n'
            '| 42 \n')

        update_database._make_aggregate_statistics(
            statistics, self.pagename, self.title_column,
            self.simple_row_builder, self.comment_template)
        self.bundled_asserts(expected_rows, 42)

    def test__make_aggregate_statistics_skips_none_entries(self):
        statistics = [None]

        update_database._make_aggregate_statistics(
            statistics, self.pagename, self.title_column,
            self.simple_row_builder, self.comment_template)
        self.bundled_asserts('', 0)

    def test__make_aggregate_statistics_multiple_rows(self):
        statistics = [
            {
                'config': {'lang': 'en', 'country': 'foo'},
                'total_items': 10,
            },
            {
                'config': {'lang': 'fr', 'country': 'bar'},
                'total_items': 20,
            }]

        expected_rows = (
            '|-\n'
            '| bar \n'
            '| fr \n'
            '| 20 \n'
            '|-\n'
            '| foo \n'
            '| en \n'
            '| 10 \n')

        update_database._make_aggregate_statistics(
            statistics, self.pagename, self.title_column,
            self.simple_row_builder, self.comment_template)
        self.bundled_asserts(expected_rows, 30)

    def test__make_aggregate_statistics_multiple_rows_with_none(self):
        statistics = [
            None,
            {
                'config': {'lang': 'en', 'country': 'foo'},
                'total_items': 42,
            },
            None]

        expected_rows = (
            '|-\n'
            '| foo \n'
            '| en \n'
            '| 42 \n')

        update_database._make_aggregate_statistics(
            statistics, self.pagename, self.title_column,
            self.simple_row_builder, self.comment_template)
        self.bundled_asserts(expected_rows, 42)


class TestPerCountryReport(TestCreateReportBase):

    """Test the _per_country_report helper."""

    def setUp(self):
        self.class_name = 'erfgoedbot.update_database'
        super(TestPerCountryReport, self).setUp()

        self.instruction_prefix = 'instruction_prefix'
        patcher = mock.patch(
            'erfgoedbot.update_database.common.instruction_header')
        self.mock_instruction_header = patcher.start()
        self.mock_instruction_header.return_value = self.instruction_prefix
        self.addCleanup(patcher.stop)

        self.done_message = 'done_message'
        patcher = mock.patch(
            'erfgoedbot.update_database.common.done_message')
        self.mock_done_message = patcher.start()
        self.mock_done_message.return_value = self.done_message
        self.addCleanup(patcher.stop)

        self.table_prefix = 'table_prefix'
        patcher = mock.patch(
            'erfgoedbot.update_database.common.table_header_row')
        self.mock_table_header_row = patcher.start()
        self.mock_table_header_row.return_value = self.table_prefix
        self.addCleanup(patcher.stop)

        self.countryconfig = {
            'table': 'table_name',
            'foo': 'bar'
        }
        self.commons = self.mock_site.return_value
        self.mock_report_page = self.mock_page.return_value

    def test_per_country_report_with_data(self):
        data = OrderedDict([('item_a', 3), ('item_b', 7)])

        def row_builder(key, value, site):
            return {'Item': key, 'Count': value}

        result = update_database._per_country_report(
            self.countryconfig, data,
            report_type='Test Report',
            title_column=['Item', 'Count'],
            row_builder=row_builder,
            total_entries=2,
            total_pages=5)

        self.mock_instruction_header.assert_called_once_with(
            ':c:Commons:Monuments_database/Test Report')
        self.mock_done_message.assert_not_called()

        expected_table = self.table_prefix + (
            '|-\n'
            '| item_a || 3 \n'
            '|-\n'
            '| item_b || 7 \n'
            '|}\n')
        expected_postfix = '[[Category:Commons:Monuments database/Test Report]]'
        expected_text = self.instruction_prefix + expected_table + expected_postfix

        self.mock_page.assert_called_once_with(
            self.commons,
            'Commons:Monuments database/Test Report/table_name')
        self.mock_save_to_wiki_or_local.assert_called_once_with(
            self.mock_report_page,
            'Updating the list of test Report with 2 entries',
            expected_text)

        self.assertEqual(result, {
            'report_page': self.mock_report_page,
            'config': self.countryconfig,
            'total_entries': 2,
            'total_pages': 5,
            'total_occurrences': 10
        })

    def test_per_country_report_empty(self):
        def row_builder(key, value, site):
            return {'Item': key, 'Count': value}

        result = update_database._per_country_report(
            self.countryconfig, {},
            report_type='Test Report',
            title_column=['Item', 'Count'],
            row_builder=row_builder,
            total_entries=0,
            total_pages=0)

        self.mock_done_message.assert_called_once_with(
            ':c:Commons:Monuments_database/Test Report', 'test Report')

        self.assertEqual(result, {
            'report_page': self.mock_report_page,
            'config': self.countryconfig,
            'total_entries': 0,
            'total_pages': 0,
            'total_occurrences': 0
        })

    def test_per_country_report_total_entries_defaults_to_zero(self):
        def row_builder(key, value, site):
            return {'Item': key, 'Count': value}

        result = update_database._per_country_report(
            self.countryconfig, {},
            report_type='Test report',
            title_column=['Item', 'Count'],
            row_builder=row_builder)

        self.assertEqual(result['total_entries'], 0)
        self.assertEqual(result['total_pages'], 0)
        self.assertEqual(result['total_occurrences'], 0)


class TestMakeUnknownFieldsStatistics(TestCreateReportTableBase):

    """Test the make_unknown_fields_statistics method."""

    def setUp(self):
        self.class_name = 'erfgoedbot.update_database'
        super(TestMakeUnknownFieldsStatistics, self).setUp()

        patcher = mock.patch(
            'erfgoedbot.update_database.common.get_template_link')
        self.mock_get_template_link = patcher.start()
        self.mock_get_template_link.return_value = '<template_link>'
        self.addCleanup(patcher.stop)

        self.commons = self.mock_site.return_value
        self.mock_report_page = mock.MagicMock()
        self.mock_report_page.title.return_value = '<report_page>'

        self.comment = (
            'Updating unknown fields statistics. Total of {total_entries} '
            'unknown fields used {total_occurrences} times on {total_pages} '
            'different pages.')
        self.pagename = 'Commons:Monuments database/Unknown fields/Statistics'

    def bundled_asserts(self, expected_rows,
                        expected_total_entries,
                        expected_total_occurrences,
                        expected_total_pages):
        """The full battery of asserts to do for each test."""
        expected_text = self.prefix + expected_rows + self.postfix.format(
            total_entries=expected_total_entries,
            total_occurrences=expected_total_occurrences,
            total_pages=expected_total_pages)

        self.mock_site.assert_called_once_with('commons', 'commons')
        self.mock_page.assert_called_once_with(
            self.mock_site.return_value, self.pagename)
        self.mock_save_to_wiki_or_local.assert_called_once_with(
            self.mock_page.return_value,
            self.comment.format(
                total_entries=expected_total_entries,
                total_occurrences=expected_total_occurrences,
                total_pages=expected_total_pages),
            expected_text
        )
        self.mock_table_header_row.assert_called_once()
        self.mock_table_bottom_row.assert_called_once_with(8, {
            2: expected_total_entries,
            3: expected_total_occurrences,
            4: expected_total_pages})

    def test_make_unknown_fields_statistics_single_basic(self):
        statistics = [{
            'config': {
                'lang': 'en',
                'country': 'foo',
                'rowTemplate': 'row template',
                'headerTemplate': 'head template'},
            'report_page': self.mock_report_page,
            'total_entries': 123,
            'total_occurrences': 456,
            'total_pages': 789
        }]

        expected_rows = (
            '|-\n'
            '| foo \n'
            '| en \n'
            '| 123 \n'
            '| 456 \n'
            '| 789 \n'
            '| <report_page> \n'
            '| <template_link> \n'
            '| <template_link> \n')
        expected_total_entries = 123
        expected_total_occurrences = 456
        expected_total_pages = 789

        update_database.make_unknown_fields_statistics(statistics)
        self.mock_get_template_link.assert_has_calls([
            mock.call('en', 'wikipedia', 'row template', self.commons),
            mock.call('en', 'wikipedia', 'head template', self.commons),
        ])
        self.bundled_asserts(expected_rows,
                             expected_total_entries,
                             expected_total_occurrences,
                             expected_total_pages)

    def test_make_unknown_fields_statistics_single_empty(self):
        statistics = [None, ]

        expected_rows = ''
        expected_total_entries = 0
        expected_total_occurrences = 0
        expected_total_pages = 0

        update_database.make_unknown_fields_statistics(statistics)
        self.bundled_asserts(expected_rows,
                             expected_total_entries,
                             expected_total_occurrences,
                             expected_total_pages)

    def test_make_unknown_fields_statistics_multiple_basic(self):
        report_page_1 = mock.MagicMock()
        report_page_1.title.return_value = '<report_page:Foobar>'
        report_page_2 = mock.MagicMock()
        report_page_2.title.return_value = '<report_page:Barfoo>'
        statistics = [
            {
                'config': {
                    'lang': 'en',
                    'country': 'foo',
                    'rowTemplate': 'row template',
                    'headerTemplate': 'head template'},
                'report_page': report_page_1,
                'total_entries': 123,
                'total_occurrences': 456,
                'total_pages': 789
            },
            {
                'config': {
                    'lang': 'fr',
                    'country': 'bar',
                    'rowTemplate': 'row2 template',
                    'headerTemplate': 'head2 template',
                    'project': 'wikisource'},
                'report_page': report_page_2,
                'total_entries': 321,
                'total_occurrences': 654,
                'total_pages': 987
            }]

        expected_rows = (
            '|-\n'
            '| bar \n'
            '| fr \n'
            '| 321 \n'
            '| 654 \n'
            '| 987 \n'
            '| <report_page:Barfoo> \n'
            '| <template_link> \n'
            '| <template_link> \n'
            '|-\n'
            '| foo \n'
            '| en \n'
            '| 123 \n'
            '| 456 \n'
            '| 789 \n'
            '| <report_page:Foobar> \n'
            '| <template_link> \n'
            '| <template_link> \n')
        expected_total_entries = 444
        expected_total_occurrences = 1110
        expected_total_pages = 1776

        update_database.make_unknown_fields_statistics(statistics)
        self.mock_get_template_link.assert_has_calls([
            mock.call('en', 'wikipedia', 'row template', self.commons),
            mock.call('en', 'wikipedia', 'head template', self.commons),
            mock.call('fr', 'wikisource', 'row2 template', self.commons),
            mock.call('fr', 'wikisource', 'head2 template', self.commons),
        ])
        self.bundled_asserts(expected_rows,
                             expected_total_entries,
                             expected_total_occurrences,
                             expected_total_pages)


class TestUnknownFieldsStatistics(TestCreateReportBase):

    """Test the unknown_fields_statistics method."""

    def setUp(self):
        self.class_name = 'erfgoedbot.update_database'
        super(TestUnknownFieldsStatistics, self).setUp()

        patcher = mock.patch(
            'erfgoedbot.update_database.format_source_field')
        self.mock_format_source_field = patcher.start()
        self.mock_format_source_field.return_value = 'formatted_entry'
        self.addCleanup(patcher.stop)

        self.instruction_prefix = 'instruction_prefix'
        patcher = mock.patch(
            'erfgoedbot.update_database.common.instruction_header')
        self.mock_instruction_header = patcher.start()
        self.mock_instruction_header.return_value = self.instruction_prefix
        self.addCleanup(patcher.stop)

        self.done_message = 'done_message'
        patcher = mock.patch(
            'erfgoedbot.update_database.common.done_message')
        self.mock_done_message = patcher.start()
        self.mock_done_message.return_value = self.done_message
        self.addCleanup(patcher.stop)

        self.table_prefix = 'table_prefix'
        patcher = mock.patch(
            'erfgoedbot.update_database.common.table_header_row')
        self.mock_table_header_row = patcher.start()
        self.mock_table_header_row.return_value = self.table_prefix
        self.addCleanup(patcher.stop)

        self.postfix = (
            '[[Category:Commons:Monuments database/Unknown fields]]')

        self.comment = 'Updating the list of unknown fields with {0} entries'
        self.countryconfig = {
            'table': 'table_name',
            'foo': 'bar'
        }
        self.pagename = 'Commons:Monuments database/Unknown fields/table_name'
        self.commons = self.mock_site.return_value
        self.mock_report_page = self.mock_page.return_value

        self.unknown_fields = OrderedDict()
        self.counter_1 = Counter({'page_11': 1, 'page_12': 5})
        self.unknown_fields['unknown_field_1'] = self.counter_1
        self.counter_2 = Counter({'page_21': 3})
        self.unknown_fields['unknown_field_2'] = self.counter_2

    def bundled_asserts(self, result,
                        expected_table,
                        expected_return,
                        expected_cmt):
        """The full battery of asserts to do for each test."""
        expected_output = (self.instruction_prefix + expected_table +
                           self.postfix)
        self.assertEqual(result, expected_return)
        self.mock_site.assert_called_once_with('commons', 'commons')
        self.mock_page.assert_called_once_with(
            self.mock_site.return_value, self.pagename)
        self.mock_save_to_wiki_or_local.assert_called_once_with(
            self.mock_report_page,
            expected_cmt,
            expected_output
        )
        self.mock_instruction_header.assert_called_once()

    def test_unknown_fields_statistics_complete(self):
        expected_cmt = self.comment.format(2)
        expected_table = self.table_prefix + (
            '|-\n'
            '| unknown_field_1 || 6 || formatted_entry \n'
            '|-\n'
            '| unknown_field_2 || 3 || formatted_entry \n'
            '|}\n')
        expected_return = {
            'report_page': self.mock_report_page,
            'config': self.countryconfig,
            'total_entries': 2,
            'total_pages': 3,
            'total_occurrences': 9
        }

        result = update_database.unknown_fields_statistics(
            self.countryconfig, self.unknown_fields)
        self.mock_format_source_field.assert_has_calls([
            mock.call(self.counter_1, self.commons),
            mock.call(self.counter_2, self.commons)],
        )
        self.bundled_asserts(result, expected_table, expected_return,
                             expected_cmt)

    def test_unknown_fields_statistics_no_unknown(self):
        expected_cmt = self.comment.format(0)
        expected_table = self.done_message
        expected_return = {
            'report_page': self.mock_report_page,
            'config': self.countryconfig,
            'total_entries': 0,
            'total_pages': 0,
            'total_occurrences': 0
        }

        result = update_database.unknown_fields_statistics(
            self.countryconfig, {})
        self.mock_format_source_field.assert_not_called()
        self.mock_done_message.assert_called_once()
        self.bundled_asserts(result, expected_table, expected_return,
                             expected_cmt)

    def test_unknown_fields_statistics_combine_pages(self):
        new_counter = Counter({'page_11': 3, 'page_21': 3, 'page_22': 3})
        self.unknown_fields['unknown_field_2'] = new_counter
        expected_cmt = self.comment.format(2)
        expected_table = self.table_prefix + (
            '|-\n'
            '| unknown_field_1 || 6 || formatted_entry \n'
            '|-\n'
            '| unknown_field_2 || 9 || formatted_entry \n'
            '|}\n')
        expected_return = {
            'report_page': self.mock_report_page,
            'config': self.countryconfig,
            'total_entries': 2,
            'total_pages': 4,
            'total_occurrences': 15
        }

        result = update_database.unknown_fields_statistics(
            self.countryconfig, self.unknown_fields)
        self.mock_format_source_field.assert_has_calls([
            mock.call(self.counter_1, self.commons),
            mock.call(new_counter, self.commons)],
        )
        self.bundled_asserts(result, expected_table, expected_return,
                             expected_cmt)


class TestProcessCountry(unittest.TestCase):

    """Test the process_country method."""

    def setUp(self):
        patcher = mock.patch(
            'erfgoedbot.update_database.process_country_wikidata')
        self.mock_process_country_wikidata = patcher.start()
        self.addCleanup(patcher.stop)

        patcher = mock.patch(
            'erfgoedbot.update_database.process_country_list')
        self.mock_process_country_list = patcher.start()
        self.mock_process_country_list.return_value = {
            'unknown_fields': 'unknown_field_stats',
            'duplicate_ids': 'duplicate_id_stats',
            'missing_ids': 'missing_id_stats',
        }
        self.addCleanup(patcher.stop)

    def test_process_country_sparql(self):
        config = {'type': 'sparql'}

        result = update_database.process_country(
            config, 'conn', 'cursor', 'full_update', 'days_back')
        self.assertEqual(result, None)
        self.mock_process_country_wikidata.assert_called_once_with(
            config, 'conn', 'cursor')
        self.mock_process_country_list.assert_not_called()

    def test_process_country_list(self):
        config = {'type': 'list'}

        result = update_database.process_country(
            config, 'conn', 'cursor', 'full_update', 'days_back')
        self.assertEqual(result, {
            'unknown_fields': 'unknown_field_stats',
            'duplicate_ids': 'duplicate_id_stats',
            'missing_ids': 'missing_id_stats',
        })
        self.mock_process_country_wikidata.assert_not_called()
        self.mock_process_country_list.assert_called_once_with(
            config, 'conn', 'cursor', 'full_update', 'days_back')

    def test_process_country_default_to_list(self):
        config = {}

        result = update_database.process_country(
            config, 'conn', 'cursor', 'full_update', 'days_back')
        self.assertEqual(result, {
            'unknown_fields': 'unknown_field_stats',
            'duplicate_ids': 'duplicate_id_stats',
            'missing_ids': 'missing_id_stats',
        })
        self.mock_process_country_wikidata.assert_not_called()
        self.mock_process_country_list.assert_called_once_with(
            config, 'conn', 'cursor', 'full_update', 'days_back')


class TestGetMonumentId(TestUpdateDatabaseBase):

    def test_get_monument_id_single_primkey(self):
        contents = {'id': '12345', 'name': 'Test'}
        result = update_database.get_monument_id(
            contents, self.country_config)
        self.assertEqual(result, '12345')

    def test_get_monument_id_tuple_primkey(self):
        self.country_config['primkey'] = ('id', 'name')
        contents = {'id': '62096', 'name': 'CLT-0001'}
        result = update_database.get_monument_id(
            contents, self.country_config)
        self.assertEqual(result, '62096-CLT-0001')

    def test_get_monument_id_single_primkey_no_source_field(self):
        self.country_config['primkey'] = 'nonexistent'
        contents = {'id': '12345'}
        result = update_database.get_monument_id(
            contents, self.country_config)
        self.assertIsNone(result)

    def test_get_monument_id_tuple_primkey_no_source_field(self):
        self.country_config['primkey'] = ('id', 'nonexistent')
        contents = {'id': '62096'}
        result = update_database.get_monument_id(
            contents, self.country_config)
        self.assertIsNone(result)


class TestTrackDuplicateIds(unittest.TestCase):

    def setUp(self):
        self.harvest_state = update_database._new_harvest_state()
        self.page_a = mock.MagicMock()
        self.page_b = mock.MagicMock()

    def test_track_duplicate_ids_first_occurrence(self):
        update_database.track_duplicate_ids(
            '123', self.page_a, self.harvest_state)
        self.assertEqual(
            self.harvest_state['seen_ids'], {'123': self.page_a})
        self.assertEqual(self.harvest_state['duplicate_ids'], {})

    def test_track_duplicate_ids_second_occurrence_different_page(self):
        update_database.track_duplicate_ids(
            '123', self.page_a, self.harvest_state)
        update_database.track_duplicate_ids(
            '123', self.page_b, self.harvest_state)
        self.assertEqual(
            self.harvest_state['duplicate_ids'],
            {'123': Counter({self.page_a: 1, self.page_b: 1})}
        )

    def test_track_duplicate_ids_third_occurrence(self):
        update_database.track_duplicate_ids(
            '123', self.page_a, self.harvest_state)
        update_database.track_duplicate_ids(
            '123', self.page_b, self.harvest_state)
        update_database.track_duplicate_ids(
            '123', self.page_b, self.harvest_state)
        self.assertEqual(
            self.harvest_state['duplicate_ids'],
            {'123': Counter({self.page_b: 2, self.page_a: 1})}
        )

    def test_track_duplicate_ids_same_page_duplicate(self):
        update_database.track_duplicate_ids(
            '123', self.page_a, self.harvest_state)
        update_database.track_duplicate_ids(
            '123', self.page_a, self.harvest_state)
        self.assertEqual(
            self.harvest_state['duplicate_ids'],
            {'123': Counter({self.page_a: 2})}
        )

    def test_track_duplicate_ids_empty_id_is_skipped(self):
        update_database.track_duplicate_ids(
            '', self.page_a, self.harvest_state)
        self.assertEqual(self.harvest_state['seen_ids'], {})
        self.assertEqual(self.harvest_state['duplicate_ids'], {})

    def test_track_duplicate_ids_none_id_is_skipped(self):
        update_database.track_duplicate_ids(
            None, self.page_a, self.harvest_state)
        self.assertEqual(self.harvest_state['seen_ids'], {})
        self.assertEqual(self.harvest_state['duplicate_ids'], {})


class TestDuplicateIdsStatistics(TestCreateReportBase):

    """Test the duplicate_ids_statistics method."""

    def setUp(self):
        self.class_name = 'erfgoedbot.update_database'
        super(TestDuplicateIdsStatistics, self).setUp()

        patcher = mock.patch(
            'erfgoedbot.update_database.format_source_field')
        self.mock_format_source_field = patcher.start()
        self.mock_format_source_field.return_value = 'formatted_entry'
        self.addCleanup(patcher.stop)

        self.instruction_prefix = 'instruction_prefix'
        patcher = mock.patch(
            'erfgoedbot.update_database.common.instruction_header')
        self.mock_instruction_header = patcher.start()
        self.mock_instruction_header.return_value = self.instruction_prefix
        self.addCleanup(patcher.stop)

        self.done_message = 'done_message'
        patcher = mock.patch(
            'erfgoedbot.update_database.common.done_message')
        self.mock_done_message = patcher.start()
        self.mock_done_message.return_value = self.done_message
        self.addCleanup(patcher.stop)

        self.table_prefix = 'table_prefix'
        patcher = mock.patch(
            'erfgoedbot.update_database.common.table_header_row')
        self.mock_table_header_row = patcher.start()
        self.mock_table_header_row.return_value = self.table_prefix
        self.addCleanup(patcher.stop)

        self.postfix = (
            '[[Category:Commons:Monuments database/Duplicate IDs]]')

        self.comment = 'Updating the list of duplicate IDs with {0} entries'
        self.countryconfig = {
            'table': 'table_name',
            'foo': 'bar'
        }
        self.pagename = (
            'Commons:Monuments database/Duplicate IDs/table_name')
        self.commons = self.mock_site.return_value
        self.mock_report_page = self.mock_page.return_value

        self.duplicate_ids = OrderedDict()
        self.counter_1 = Counter({'page_11': 1, 'page_12': 5})
        self.duplicate_ids['id_1'] = self.counter_1
        self.counter_2 = Counter({'page_21': 3})
        self.duplicate_ids['id_2'] = self.counter_2

    def bundled_asserts(self, result,
                        expected_table,
                        expected_return,
                        expected_cmt):
        """The full battery of asserts to do for each test."""
        expected_output = (self.instruction_prefix + expected_table +
                           self.postfix)
        self.assertEqual(result, expected_return)
        self.mock_site.assert_called_once_with('commons', 'commons')
        self.mock_page.assert_called_once_with(
            self.mock_site.return_value, self.pagename)
        self.mock_save_to_wiki_or_local.assert_called_once_with(
            self.mock_report_page,
            expected_cmt,
            expected_output
        )
        self.mock_instruction_header.assert_called_once()

    def test_duplicate_ids_statistics_complete(self):
        expected_cmt = self.comment.format(2)
        expected_table = self.table_prefix + (
            '|-\n'
            '| id_1 || 6 || formatted_entry \n'
            '|-\n'
            '| id_2 || 3 || formatted_entry \n'
            '|}\n')
        expected_return = {
            'report_page': self.mock_report_page,
            'config': self.countryconfig,
            'total_entries': 2,
            'total_pages': 3,
            'total_occurrences': 9
        }

        result = update_database.duplicate_ids_statistics(
            self.countryconfig, self.duplicate_ids)
        self.mock_format_source_field.assert_has_calls([
            mock.call(self.counter_1, self.commons),
            mock.call(self.counter_2, self.commons)],
        )
        self.bundled_asserts(result, expected_table, expected_return,
                             expected_cmt)

    def test_duplicate_ids_statistics_no_duplicates(self):
        expected_cmt = self.comment.format(0)
        expected_table = self.done_message
        expected_return = {
            'report_page': self.mock_report_page,
            'config': self.countryconfig,
            'total_entries': 0,
            'total_pages': 0,
            'total_occurrences': 0
        }

        result = update_database.duplicate_ids_statistics(
            self.countryconfig, {})
        self.mock_format_source_field.assert_not_called()
        self.mock_done_message.assert_called_once()
        self.bundled_asserts(result, expected_table, expected_return,
                             expected_cmt)


class TestMakeDuplicateIdStatistics(TestCreateReportTableBase):

    """Test the make_duplicate_id_statistics method."""

    def setUp(self):
        self.class_name = 'erfgoedbot.update_database'
        super(TestMakeDuplicateIdStatistics, self).setUp()

        patcher = mock.patch(
            'erfgoedbot.update_database.common.get_template_link')
        self.mock_get_template_link = patcher.start()
        self.mock_get_template_link.return_value = '<template_link>'
        self.addCleanup(patcher.stop)

        self.commons = self.mock_site.return_value
        self.mock_report_page = mock.MagicMock()
        self.mock_report_page.title.return_value = '<report_page>'

        self.comment = (
            'Updating duplicate ID statistics. Total of {total_entries} '
            'duplicate IDs with {total_occurrences} occurrences on '
            '{total_pages} different pages.')
        self.pagename = (
            'Commons:Monuments database/Duplicate IDs/Statistics')

    def bundled_asserts(self, expected_rows,
                        expected_total_entries,
                        expected_total_occurrences,
                        expected_total_pages):
        """The full battery of asserts to do for each test."""
        expected_text = self.prefix + expected_rows + self.postfix

        self.mock_site.assert_called_once_with('commons', 'commons')
        self.mock_page.assert_called_once_with(
            self.mock_site.return_value, self.pagename)
        self.mock_save_to_wiki_or_local.assert_called_once_with(
            self.mock_page.return_value,
            self.comment.format(
                total_entries=expected_total_entries,
                total_occurrences=expected_total_occurrences,
                total_pages=expected_total_pages),
            expected_text
        )
        self.mock_table_header_row.assert_called_once()
        self.mock_table_bottom_row.assert_called_once_with(7, {
            2: expected_total_entries,
            3: expected_total_occurrences,
            4: expected_total_pages})

    def test_make_duplicate_id_statistics_single_basic(self):
        statistics = [{
            'config': {
                'lang': 'en',
                'country': 'foo',
                'rowTemplate': 'row template'},
            'report_page': self.mock_report_page,
            'total_entries': 10,
            'total_occurrences': 25,
            'total_pages': 5
        }]

        expected_rows = (
            '|-\n'
            '| foo \n'
            '| en \n'
            '| 10 \n'
            '| 25 \n'
            '| 5 \n'
            '| <report_page> \n'
            '| <template_link> \n')
        expected_total_entries = 10
        expected_total_occurrences = 25
        expected_total_pages = 5

        update_database.make_duplicate_id_statistics(statistics)
        self.mock_get_template_link.assert_called_once_with(
            'en', 'wikipedia', 'row template', self.commons)
        self.bundled_asserts(expected_rows,
                             expected_total_entries,
                             expected_total_occurrences,
                             expected_total_pages)

    def test_make_duplicate_id_statistics_single_empty(self):
        statistics = [None, ]

        expected_rows = ''
        expected_total_entries = 0
        expected_total_occurrences = 0
        expected_total_pages = 0

        update_database.make_duplicate_id_statistics(statistics)
        self.bundled_asserts(expected_rows,
                             expected_total_entries,
                             expected_total_occurrences,
                             expected_total_pages)

    def test_make_duplicate_id_statistics_multiple_basic(self):
        report_page_1 = mock.MagicMock()
        report_page_1.title.return_value = '<report_page:Foobar>'
        report_page_2 = mock.MagicMock()
        report_page_2.title.return_value = '<report_page:Barfoo>'
        statistics = [
            {
                'config': {
                    'lang': 'en',
                    'country': 'foo',
                    'rowTemplate': 'row template'},
                'report_page': report_page_1,
                'total_entries': 10,
                'total_occurrences': 25,
                'total_pages': 5
            },
            {
                'config': {
                    'lang': 'fr',
                    'country': 'bar',
                    'rowTemplate': 'row2 template',
                    'project': 'wikisource'},
                'report_page': report_page_2,
                'total_entries': 20,
                'total_occurrences': 50,
                'total_pages': 8
            }]

        expected_rows = (
            '|-\n'
            '| bar \n'
            '| fr \n'
            '| 20 \n'
            '| 50 \n'
            '| 8 \n'
            '| <report_page:Barfoo> \n'
            '| <template_link> \n'
            '|-\n'
            '| foo \n'
            '| en \n'
            '| 10 \n'
            '| 25 \n'
            '| 5 \n'
            '| <report_page:Foobar> \n'
            '| <template_link> \n')
        expected_total_ids = 30
        expected_total_occurrences = 75
        expected_total_pages = 13

        update_database.make_duplicate_id_statistics(statistics)
        self.mock_get_template_link.assert_has_calls([
            mock.call('en', 'wikipedia', 'row template', self.commons),
            mock.call('fr', 'wikisource', 'row2 template', self.commons),
        ])
        self.bundled_asserts(expected_rows,
                             expected_total_ids,
                             expected_total_occurrences,
                             expected_total_pages)


class TestMissingIdsStatistics(TestCreateReportBase):

    """Test the missing_ids_statistics method."""

    def setUp(self):
        self.class_name = 'erfgoedbot.update_database'
        super(TestMissingIdsStatistics, self).setUp()

        self.instruction_prefix = 'instruction_prefix'
        patcher = mock.patch(
            'erfgoedbot.update_database.common.instruction_header')
        self.mock_instruction_header = patcher.start()
        self.mock_instruction_header.return_value = self.instruction_prefix
        self.addCleanup(patcher.stop)

        self.done_message = 'done_message'
        patcher = mock.patch(
            'erfgoedbot.update_database.common.done_message')
        self.mock_done_message = patcher.start()
        self.mock_done_message.return_value = self.done_message
        self.addCleanup(patcher.stop)

        self.table_prefix = 'table_prefix'
        patcher = mock.patch(
            'erfgoedbot.update_database.common.table_header_row')
        self.mock_table_header_row = patcher.start()
        self.mock_table_header_row.return_value = self.table_prefix
        self.addCleanup(patcher.stop)

        self.postfix = (
            '[[Category:Commons:Monuments database/Missing IDs]]')

        self.comment = 'Updating the list of missing IDs with {0} entries'
        self.countryconfig = {
            'table': 'table_name',
            'foo': 'bar'
        }
        self.pagename = 'Commons:Monuments database/Missing IDs/table_name'
        self.commons = self.mock_site.return_value
        self.mock_report_page = self.mock_page.return_value

        self.page_a = mock.MagicMock()
        self.page_a.title.return_value = '<page_a>'
        self.page_b = mock.MagicMock()
        self.page_b.title.return_value = '<page_b>'

    def bundled_asserts(self, result,
                        expected_table,
                        expected_return,
                        expected_cmt):
        """The full battery of asserts to do for each test."""
        expected_output = (self.instruction_prefix + expected_table +
                           self.postfix)
        self.assertEqual(result, expected_return)
        self.mock_site.assert_called_once_with('commons', 'commons')
        self.mock_page.assert_called_once_with(
            self.mock_site.return_value, self.pagename)
        self.mock_save_to_wiki_or_local.assert_called_once_with(
            self.mock_report_page,
            expected_cmt,
            expected_output
        )
        self.mock_instruction_header.assert_called_once()

    def test_missing_ids_statistics_complete(self):
        missing_ids = Counter({self.page_a: 3, self.page_b: 1})
        expected_cmt = self.comment.format(2)
        expected_table = self.table_prefix + (
            '|-\n'
            '| <page_a> || 3 \n'
            '|-\n'
            '| <page_b> || 1 \n'
            '|}\n')
        expected_return = {
            'report_page': self.mock_report_page,
            'config': self.countryconfig,
            'total_entries': 0,
            'total_pages': 2,
            'total_occurrences': 4
        }

        result = update_database.missing_ids_statistics(
            self.countryconfig, missing_ids)
        self.bundled_asserts(result, expected_table, expected_return,
                             expected_cmt)

    def test_missing_ids_statistics_no_missing(self):
        expected_cmt = self.comment.format(0)
        expected_table = self.done_message
        expected_return = {
            'report_page': self.mock_report_page,
            'config': self.countryconfig,
            'total_entries': 0,
            'total_pages': 0,
            'total_occurrences': 0
        }

        result = update_database.missing_ids_statistics(
            self.countryconfig, Counter())
        self.mock_done_message.assert_called_once()
        self.bundled_asserts(result, expected_table, expected_return,
                             expected_cmt)


class TestMakeMissingIdStatistics(TestCreateReportTableBase):

    """Test the make_missing_id_statistics method."""

    def setUp(self):
        self.class_name = 'erfgoedbot.update_database'
        super(TestMakeMissingIdStatistics, self).setUp()

        patcher = mock.patch(
            'erfgoedbot.update_database.common.get_template_link')
        self.mock_get_template_link = patcher.start()
        self.mock_get_template_link.return_value = '<template_link>'
        self.addCleanup(patcher.stop)

        self.commons = self.mock_site.return_value
        self.mock_report_page = mock.MagicMock()
        self.mock_report_page.title.return_value = '<report_page>'

        self.comment = (
            'Updating missing ID statistics. Total of {total_occurrences} '
            'missing IDs on {total_pages} different pages.')
        self.pagename = (
            'Commons:Monuments database/Missing IDs/Statistics')

    def bundled_asserts(self, expected_rows,
                        expected_total_pages,
                        expected_total_occurrences):
        """The full battery of asserts to do for each test."""
        expected_text = self.prefix + expected_rows + self.postfix

        self.mock_site.assert_called_once_with('commons', 'commons')
        self.mock_page.assert_called_once_with(
            self.mock_site.return_value, self.pagename)
        self.mock_save_to_wiki_or_local.assert_called_once_with(
            self.mock_page.return_value,
            self.comment.format(
                total_pages=expected_total_pages,
                total_occurrences=expected_total_occurrences),
            expected_text
        )
        self.mock_table_header_row.assert_called_once()
        self.mock_table_bottom_row.assert_called_once_with(6, {
            2: expected_total_pages,
            3: expected_total_occurrences})

    def test_make_missing_id_statistics_single_basic(self):
        statistics = [{
            'config': {
                'lang': 'en',
                'country': 'foo',
                'rowTemplate': 'row template'},
            'report_page': self.mock_report_page,
            'total_pages': 5,
            'total_occurrences': 25,
        }]

        expected_rows = (
            '|-\n'
            '| foo \n'
            '| en \n'
            '| 5 \n'
            '| 25 \n'
            '| <report_page> \n'
            '| <template_link> \n')
        expected_total_pages = 5
        expected_total_occurrences = 25

        update_database.make_missing_id_statistics(statistics)
        self.mock_get_template_link.assert_called_once_with(
            'en', 'wikipedia', 'row template', self.commons)
        self.bundled_asserts(expected_rows,
                             expected_total_pages,
                             expected_total_occurrences)

    def test_make_missing_id_statistics_single_empty(self):
        statistics = [None, ]

        expected_rows = ''
        expected_total_pages = 0
        expected_total_occurrences = 0

        update_database.make_missing_id_statistics(statistics)
        self.bundled_asserts(expected_rows,
                             expected_total_pages,
                             expected_total_occurrences)
