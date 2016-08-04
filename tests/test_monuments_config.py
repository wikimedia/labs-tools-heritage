# -*- coding: utf-8  -*-
"""Validation for monuments_config."""

import unittest
from custom_assertions import CustomAssertions
from erfgoedbot import monuments_config as config


class TestMonumentsConfigValidation(unittest.TestCase, CustomAssertions):

    """Test that monuments_config is valid."""

    def setUp(self):
        self.longMessage = True
        self.label = ''

    def set_label(self, key):
        """Set self label based on the country key."""
        self.label = u'%s_(%s)' % key

    def test_monuments_config_valid_base_variables(self):
        """Ensure the base variables are present and of the right type."""
        self.assertIsInstance(config.db_server, str)
        self.assertIsInstance(config.db, str)
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
        required = [
            'project', 'lang', 'headerTemplate', 'rowTemplate', 'namespaces',
            'table', 'truncate', 'primkey', 'fields'
        ]
        optional = [
            'countryBbox', 'missingCommonscatPage', 'imagesWithoutIdPage',
            'registrantUrlBase', 'commonsCategoryBase', 'unusedImagesPage',
            'commonsTrackerCategory', 'commonsTemplate', 'autoGeocode']
        tmp = ['footerTemplate', ]  # Not used but present in existing config
        for key, data in config.countries.iteritems():
            self.set_label(key)
            self.assertIsInstance(data, dict, msg=self.label)
            self.assert_all_in(required, data.keys(), msg=self.label)
            self.assert_all_in(data.keys(), required + optional + tmp,
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
            'commonsTemplate': (str, unicode, bool)
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
            for n in data['namespaces']:
                self.assertIsInstance(n, int, msg=self.label)

    def test_monuments_config_valid_primkey_values(self):
        """Ensure that primkey values are valid field dest entries."""
        # TODO: should ensure primkey entries are present in field
        for key, data in config.countries.iteritems():
            self.set_label(key)

            # some primkeys are tuples
            tuple_primkey = data['primkey']
            if not isinstance(data['primkey'], tuple):
                tuple_primkey = (data['primkey'], )

            # find all dest values
            found_dest = []
            for field in data['fields']:
                found_dest.append(field['dest'])

            self.assert_all_in(tuple_primkey, found_dest, msg=self.label)

    def test_monuments_config_valid_country_fields(self):
        """Ensure the country field entry are all formatted correctly."""
        required = ['source', 'dest']
        optional = ['type', 'check', 'conv', 'default', 'auto_increment']
        for key, data in config.countries.iteritems():
            self.set_label(key)
            for field in data['fields']:
                self.assertIsInstance(field, dict, msg=self.label)
                self.assert_all_in(required, field.keys(), msg=self.label)
                self.assert_all_in(field.keys(), required + optional,
                                   msg=self.label)

    def test_monuments_config_country_field_dests_ascii(self):
        """Ensure the country field dest entries are all ascii."""
        for key, data in config.countries.iteritems():
            self.set_label(key)
            for field in data['fields']:
                self.assert_is_ascii(field.get('dest'), msg=self.label)

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
            for field in data['fields']:
                if field.get('conv'):
                    self.assertIn(field.get('conv'), recognized,
                                  msg=self.label)

    def test_monuments_config_generateRegistrantUrl_converter(self):
        """Ensure correct usage of generateRegistrantUrl converter.

        Ensure that a config with a generateRegistrantUrl
        has a valid registrantUrlBase.
        """
        for key, data in config.countries.iteritems():
            self.set_label(key)
            for field in data['fields']:
                if field.get('conv') == 'generateRegistrantUrl':
                    registrantUrlBase = data.get('registrantUrlBase')
                    msg = "No valid registrantUrlBase for %s" % (self.label)
                    self.assertTrue(registrantUrlBase, msg=msg)
                    self.assertIn('%s', registrantUrlBase, msg=msg)

    def test_monuments_config_known_checkers(self):
        """Ensure the only known checkers are used in field entries."""
        recognized = ['checkLon', 'checkLat', 'checkWD', 'checkInt']
        for key, data in config.countries.iteritems():
            self.set_label(key)
            for field in data['fields']:
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
