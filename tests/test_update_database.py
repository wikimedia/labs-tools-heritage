#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Unit tests for update_database."""

import unittest
from collections import Counter, OrderedDict

import mock

import pywikibot

from erfgoedbot import update_database


class TestCreateReportBase(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch(
            'erfgoedbot.update_database.common.save_to_wiki_or_local')
        self.mock_save_to_wiki_or_local = patcher.start()
        self.addCleanup(patcher.stop)

        # silence logger
        patcher = mock.patch(
            'erfgoedbot.update_database.pywikibot.debug')
        self.mock_debug = patcher.start()
        self.addCleanup(patcher.stop)


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
                'source': u'source-field',
                'dest': u'dest-field',
                'check': u'connectDatabase',
            }
        )
        val = 'something'
        self.contents[u'source-field'] = val

        with self.assertRaises(pywikibot.Error) as cm:
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


class TestMakeStatistics(TestCreateReportBase):

    """Test the make_statistics method."""

    def setUp(self):
        super(TestMakeStatistics, self).setUp()

        self.prefix = 'prefix'
        patcher = mock.patch(
            'erfgoedbot.update_database.common.table_header_row')
        self.mock_table_header_row = patcher.start()
        self.mock_table_header_row.return_value = self.prefix
        self.addCleanup(patcher.stop)

        self.postfix = 'postfix'
        patcher = mock.patch(
            'erfgoedbot.update_database.common.table_bottom_row')
        self.mock_table_bottom_row = patcher.start()
        self.mock_table_bottom_row.return_value = self.postfix
        self.addCleanup(patcher.stop)

        self.comment = (
            u'Updating unknown fields statistics. Total of {total_fields} '
            u'unknown fields used {total_usages} times on {total_pages} '
            u'different pages.')
        commons = pywikibot.Site('commons', 'commons')
        self.page = pywikibot.Page(
            commons, u'Commons:Monuments database/Unknown fields/Statistics')

    def bundled_asserts(self, expected_rows,
                        expected_total_fields,
                        expected_total_usages,
                        expected_total_pages):
        """The full battery of asserts to do for each test."""
        expected_text = self.prefix + expected_rows + self.postfix.format(
            total_fields=expected_total_fields,
            total_usages=expected_total_usages,
            total_pages=expected_total_pages)

        self.mock_save_to_wiki_or_local.assert_called_once_with(
            self.page,
            self.comment.format(
                total_fields=expected_total_fields,
                total_usages=expected_total_usages,
                total_pages=expected_total_pages),
            expected_text
        )
        self.mock_table_header_row.assert_called_once()
        self.mock_table_bottom_row.assert_called_once_with(8, {
            2: expected_total_fields,
            3: expected_total_usages,
            4: expected_total_pages})

    def test_make_statistics_single_basic(self):
        test_wiki = pywikibot.Site('test', 'wikipedia')
        report_page = pywikibot.Page(test_wiki, 'Foobar')
        statistics = [{
            'config': {
                'lang': 'en',
                'country': 'foo',
                'rowTemplate': 'row template',
                'headerTemplate': 'head template'},
            'report_page': report_page,
            'total_fields': 123,
            'total_usages': 456,
            'total_pages': 789
        }]

        expected_rows = (
            u'|-\n'
            u'| foo \n'
            u'| en \n'
            u'| 123 \n'
            u'| 456 \n'
            u'| 789 \n'
            u'| [[wikipedia:test:Foobar|Foobar]] \n'
            u'| [[wikipedia:en:Template:Row template|Row template]] \n'
            u'| [[wikipedia:en:Template:Head template|Head template]] \n')
        expected_total_fields = 123
        expected_total_usages = 456
        expected_total_pages = 789

        update_database.make_statistics(statistics)
        self.bundled_asserts(expected_rows,
                             expected_total_fields,
                             expected_total_usages,
                             expected_total_pages)

    def test_make_statistics_single_empty(self):
        statistics = [None, ]

        expected_rows = ''
        expected_total_fields = 0
        expected_total_usages = 0
        expected_total_pages = 0

        update_database.make_statistics(statistics)
        self.bundled_asserts(expected_rows,
                             expected_total_fields,
                             expected_total_usages,
                             expected_total_pages)

    def test_make_statistics_multiple_basic(self):
        test_wiki = pywikibot.Site('test', 'wikipedia')
        report_page_1 = pywikibot.Page(test_wiki, 'Foobar')
        report_page_2 = pywikibot.Page(test_wiki, 'Barfoo')
        statistics = [
            {
                'config': {
                    'lang': 'en',
                    'country': 'foo',
                    'rowTemplate': 'row template',
                    'headerTemplate': 'head template'},
                'report_page': report_page_1,
                'total_fields': 123,
                'total_usages': 456,
                'total_pages': 789
            },
            {
                'config': {
                    'lang': 'fr',
                    'country': 'bar',
                    'rowTemplate': 'row2 template',
                    'headerTemplate': 'head2 template'},
                'report_page': report_page_2,
                'total_fields': 321,
                'total_usages': 654,
                'total_pages': 987
            }]

        expected_rows = (
            u'|-\n'
            u'| foo \n'
            u'| en \n'
            u'| 123 \n'
            u'| 456 \n'
            u'| 789 \n'
            u'| [[wikipedia:test:Foobar|Foobar]] \n'
            u'| [[wikipedia:en:Template:Row template|Row template]] \n'
            u'| [[wikipedia:en:Template:Head template|Head template]] \n'
            u'|-\n'
            u'| bar \n'
            u'| fr \n'
            u'| 321 \n'
            u'| 654 \n'
            u'| 987 \n'
            u'| [[wikipedia:test:Barfoo|Barfoo]] \n'
            u'| [[wikipedia:fr:Modèle:Row2 template|Row2 template]] \n'
            u'| [[wikipedia:fr:Modèle:Head2 template|Head2 template]] \n')
        expected_total_fields = 444
        expected_total_usages = 1110
        expected_total_pages = 1776

        update_database.make_statistics(statistics)
        self.bundled_asserts(expected_rows,
                             expected_total_fields,
                             expected_total_usages,
                             expected_total_pages)

    def test_make_statistics_multiple_mixed(self):
        test_wiki = pywikibot.Site('test', 'wikipedia')
        report_page = pywikibot.Page(test_wiki, 'Foobar')
        statistics = [
            None,
            {
                'config': {
                    'lang': 'en',
                    'country': 'foo',
                    'rowTemplate': 'row template',
                    'headerTemplate': 'head template'},
                'report_page': report_page,
                'total_fields': 123,
                'total_usages': 456,
                'total_pages': 789
            },
            None]

        expected_rows = (
            u'|-\n'
            u'| foo \n'
            u'| en \n'
            u'| 123 \n'
            u'| 456 \n'
            u'| 789 \n'
            u'| [[wikipedia:test:Foobar|Foobar]] \n'
            u'| [[wikipedia:en:Template:Row template|Row template]] \n'
            u'| [[wikipedia:en:Template:Head template|Head template]] \n')
        expected_total_fields = 123
        expected_total_usages = 456
        expected_total_pages = 789

        update_database.make_statistics(statistics)
        self.bundled_asserts(expected_rows,
                             expected_total_fields,
                             expected_total_usages,
                             expected_total_pages)


class TestUnknownFieldsStatistics(TestCreateReportBase):

    """Test the unknown_fields_statistics method."""

    def setUp(self):
        super(TestUnknownFieldsStatistics, self).setUp()
        self.mock_report_page = mock.create_autospec(
            update_database.pywikibot.Page,
        )
        patcher = mock.patch(
            'erfgoedbot.update_database.pywikibot.Page')
        self.mock_pwb_page = patcher.start()
        self.mock_pwb_page.return_value = self.mock_report_page
        self.addCleanup(patcher.stop)

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
            u'[[Category:Commons:Monuments database/Unknown fields]]')

        self.comment = u'Updating the list of unknown fields with {0} entries'
        self.countryconfig = {
            'table': 'table_name',
            'foo': 'bar'
        }
        self.commons = pywikibot.Site('commons', 'commons')

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
        self.mock_pwb_page.assert_called_once_with(
            self.commons,
            u'Commons:Monuments database/Unknown fields/table_name'
        )
        self.mock_save_to_wiki_or_local.assert_called_once_with(
            self.mock_report_page,
            expected_cmt,
            expected_output
        )
        self.mock_instruction_header.assert_called_once()

    def test_unknown_fields_statistics_complete(self):
        expected_cmt = self.comment.format(2)
        expected_table = self.table_prefix + (
            u'|-\n'
            u'| unknown_field_1 || 6 || formatted_entry\n'
            u'|-\n'
            u'| unknown_field_2 || 3 || formatted_entry\n'
            u'|}\n')
        expected_return = {
            'report_page': self.mock_report_page,
            'config': self.countryconfig,
            'total_fields': 2,
            'total_pages': 3,
            'total_usages': 9
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
            'total_fields': 0,
            'total_pages': 0,
            'total_usages': 0
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
            u'|-\n'
            u'| unknown_field_1 || 6 || formatted_entry\n'
            u'|-\n'
            u'| unknown_field_2 || 9 || formatted_entry\n'
            u'|}\n')
        expected_return = {
            'report_page': self.mock_report_page,
            'config': self.countryconfig,
            'total_fields': 2,
            'total_pages': 4,
            'total_usages': 15
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
        self.mock_process_country_list.return_value = 'unknown_field_stats'
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
        self.assertEqual(result, 'unknown_field_stats')
        self.mock_process_country_wikidata.assert_not_called()
        self.mock_process_country_list.assert_called_once_with(
            config, 'conn', 'cursor', 'full_update', 'days_back')

    def test_process_country_default_to_list(self):
        config = {}

        result = update_database.process_country(
            config, 'conn', 'cursor', 'full_update', 'days_back')
        self.assertEqual(result, 'unknown_field_stats')
        self.mock_process_country_wikidata.assert_not_called()
        self.mock_process_country_list.assert_called_once_with(
            config, 'conn', 'cursor', 'full_update', 'days_back')
