# -*- coding: utf-8  -*-
"""Validation for monuments_config."""

import unittest

from custom_assertions import CustomAssertions
from erfgoedbot import monuments_config as config


class ValidateMonumentsConfig(unittest.TestCase, CustomAssertions):

    """Test that all monuments_configs/*.json are valid."""

    def setUp(self):
        self.longMessage = True
        self.label = ''

    def set_label(self, key):
        """Set self label based on the country key."""
        self.label = u'%s_(%s)' % key

    def test_monuments_config_valid_base_variables(self):
        """Ensure the base variables are present and of the right type."""
        self.assertIsInstance(config.countries, dict)

    def test_monuments_config_valid_country_keys(self):
        """Ensure all country keys are country, lang tuples."""
        for key, data in config.countries.iteritems():
            self.set_label(key)
            self.assertIsInstance(key, tuple, msg=self.label)
            self.assertEqual(len(key), 2, msg=self.label)
            self.assertEqual(key[1], data['lang'], msg=self.label)

    def test_monuments_config_valid_country_entries(self):
        """Ensure all countries contain the required entries, only."""
        # TODO resolve tmp
        required_all = [
            'project', 'lang', 'table', 'country', 'description'
        ]
        required_base_sql = [
            'headerTemplate', 'rowTemplate', 'namespaces',
            'truncate', 'primkey', 'fields'
        ]
        required_base_sparql = [
            'sparql'
        ]

        required_sql = ['sql_lang', 'sql_country', 'sql_data']

        optional_base = [
            'countryBbox', 'missingCommonscatPage', 'imagesWithoutIdPage',
            'registrantUrlBase', 'commonsCategoryBase', 'unusedImagesPage',
            'commonsTrackerCategory', 'commonsTemplate', 'autoGeocode', 'type',
            'skip'
        ]
        optional_sql = ['sql_where', ]
        for key, data in config.countries.iteritems():
            self.set_label(key)
            if key[0].startswith('wlpa'):
                required = required_all + required_base_sql
                optional = optional_base
            else:
                required = required_all + required_sql
                if data.get('type') == 'sparql':
                    required += required_base_sparql
                else:
                    required += required_base_sql
                optional = optional_base + optional_sql
            self.assertIsInstance(data, dict, msg=self.label)
            self.assert_all_in(required, data.keys(), msg=self.label)
            self.assert_all_in(data.keys(), required + optional,
                               msg=self.label)

    def test_monuments_config_valid_country_entry_types(self):
        """Ensure the country entries are all of the right type."""
        # TODO: commonsTemplate=bool is a hack which can be replaced by using
        # either u'' or removing/commenting out the entry
        expected = {
            'truncate': bool,
            'autoGeocode': bool,
            'namespaces': list,
            'fields': list,
            'primkey': (str, unicode, tuple),
            'commonsTemplate': (str, unicode, bool),
            'sql_lang': (str, unicode),
            'sql_country': (str, unicode),
            'sql_data': dict,
            'sql_where': (str, unicode),
            'skip': bool
        }
        expected_default = (str, unicode)
        for key, data in config.countries.iteritems():
            self.set_label(key)
            for entry in data.keys():
                if entry in expected.keys():
                    self.assertIsInstance(data[entry], expected[entry],
                                          msg=u'%s: %s' % (self.label, entry))
                else:
                    self.assertIsInstance(data[entry], expected_default,
                                          msg=u'%s: %s' % (self.label, entry))

    def test_monuments_config_valid_namespaces_types(self):
        """Ensure that namespaces is a list of ints."""
        for key, data in config.countries.iteritems():
            self.set_label(key)
            for n in data.get('namespaces', []):
                self.assertIsInstance(n, int, msg=self.label)

    def test_monuments_config_valid_primkey_values(self):
        """Ensure that primkey values are valid field dest entries."""
        # TODO: should ensure primkey entries are present in field
        for key, data in config.countries.iteritems():
            self.set_label(key)

            if data.get('type') == 'sparql':
                continue

            # some primkeys are tuples
            tuple_primkey = data['primkey']
            if not isinstance(data['primkey'], tuple):
                tuple_primkey = (data['primkey'], )

            # find all dest values
            found_dest = []
            for field in data.get('fields', []):
                found_dest.append(field['dest'])

            self.assert_all_in(tuple_primkey, found_dest, msg=self.label)

    def test_monuments_config_valid_country_fields(self):
        """Ensure the country field entry are all formatted correctly."""
        required = ['source', 'dest']
        optional = ['type', 'check', 'conv', 'default', 'auto_increment']
        for key, data in config.countries.iteritems():
            self.set_label(key)
            for field in data.get('fields', []):
                self.assertIsInstance(field, dict, msg=self.label)
                self.assert_all_in(required, field.keys(), msg=self.label)
                self.assert_all_in(field.keys(), required + optional,
                                   msg=self.label)

    def test_monuments_config_country_field_dests_ascii(self):
        """Ensure the country field dest entries are all ascii."""
        for key, data in config.countries.iteritems():
            self.set_label(key)
            for field in data.get('fields', []):
                self.assert_is_ascii(field.get('dest'), msg=self.label)

    def test_monuments_config_country_field_lat_and_lon(self):
        """Ensure the country field dest entries contain lat-lon pair."""
        # if one is present both should be present
        for key, data in config.countries.iteritems():
            self.set_label(key)
            dests = [field.get('dest') for field in data.get('fields', [])]
            if 'lat' in dests:
                self.assertIn('lon', dests, msg=self.label)
            if 'lon' in dests:
                self.assertIn('lat', dests, msg=self.label)

    def test_monuments_config_known_converters(self):
        """Ensure the only known converters are used in field entries."""
        recognized = [
            'extractWikilink', 'generateRegistrantUrl', 'to_default_numeral',
            'CH1903ToLat', 'CH1903ToLon', 'remove_commons_category_prefix',
            'es-ct-fop', 'il-fop', 'fi-fop',
            'generateRegistrantUrl-wlpa-es-ct', 'generateRegistrantUrl-sv-ship'
        ]
        for key, data in config.countries.iteritems():
            self.set_label(key)
            for field in data.get('fields', []):
                if field.get('conv'):
                    self.assertIn(field.get('conv'), recognized,
                                  msg=self.label)

    def test_monuments_config_registrant_url_base_converter(self):
        """Ensure correct usage of generateRegistrantUrl converter.

        Ensure that a config with a generateRegistrantUrl
        has a valid registrantUrlBase.
        """
        for key, data in config.countries.iteritems():
            self.set_label(key)
            for field in data.get('fields', []):
                if field.get('conv') == 'generateRegistrantUrl':
                    registrant_url_base = data.get('registrantUrlBase')
                    msg = "No valid registrantUrlBase for %s" % (self.label)
                    self.assertTrue(registrant_url_base, msg=msg)
                    self.assertIn('%s', registrant_url_base, msg=msg)

    def test_monuments_config_known_checkers(self):
        """Ensure the only known checkers are used in field entries."""
        recognized = ['checkLon', 'checkLat', 'checkWD', 'checkInt']
        for key, data in config.countries.iteritems():
            self.set_label(key)
            for field in data.get('fields', []):
                if field.get('check'):
                    self.assertIn(field.get('check'), recognized,
                                  msg=self.label)

    def test_monuments_config_underscored_templates(self):
        """Ensure template param names do not contain namespace or underscore.

        The precence of a ':' is used as a signal for the namespace being
        included.
        """
        template_params = ['headerTemplate', 'rowTemplate', 'commonsTemplate']
        for key, data in config.countries.iteritems():
            self.set_label(key)
            for template in template_params:
                if data.get(template):
                    self.assertNotIn('_', data.get(template), msg=self.label)
                    self.assertNotIn(':', data.get(template), msg=self.label)

    def test_monuments_config_valid_sparql(self):
        """Ensure that the sparql query delivers ?item and ?id."""
        # TODO: should ensure primkey entries are present in field
        for key, data in config.countries.iteritems():
            if data.get('type') != 'sparql':
                continue

            self.set_label(key)
            required_selects = ['?item', '?id']
            self.assert_all_in_string(
                required_selects, data.get('sparql'), msg=self.label)
