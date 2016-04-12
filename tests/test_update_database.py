"""Unit tests for update_database."""

import mock
import unittest

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
            mock_updateMonument.assert_called_with(expected_contents, 'DummySource', self.country_config, None, self.mock_cursor, self.mock_page)
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
        self.mock_cursor.execute.assert_called_with(expected_query, expected_query_params)


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

    def test_lookupSourceField_on_unknown_field_resturn_none(self):
        result = update_database.lookupSourceField("unknown", self.country_config)
        self.assertEqual(result, None)

    def test_lookupSourceField_on_known_field_resturn_dest(self):
        result = update_database.lookupSourceField(u'name', self.country_config)
        self.assertEqual(result, 'name')


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
            mock_processHeader.assert_called_with(['a', 'b'], self.country_config)

    def test_processPage_calls_processMonument(self):
        self.country_config['rowTemplate'] = 'MockTemplate'
        with mock.patch('erfgoedbot.update_database.processMonument', autospec=True) as mock_processMonument:
            update_database.processPage(self.mock_page, self.source, self.country_config, None, None)
            mock_processMonument.assert_called_with(
                ['a', 'b'],
                self.source,
                self.country_config,
                None, None, self.mock_page, {}, unknownFields={}
            )
