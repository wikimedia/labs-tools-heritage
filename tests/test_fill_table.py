# -*- coding: utf-8  -*-
"""Validation for fill_table_monuments_all.sql with monuments_config.py."""

import unittest
import re
from custom_assertions import CustomAssertions
from erfgoedbot import monuments_config as config


def isolate_dataset_entries(text):
    """Parse sql to identify replacement groups."""
    data = {}
    results = re.findall('REPLACE INTO\n  `monuments_all_tmp`(.*?)'
                         'SELECT(.*?)'
                         'FROM `(.*?)`',
                         text, re.DOTALL | re.MULTILINE)

    for result in results:
        to_replace = result[0].strip('\n ()`').split('`, `')
        replaced, sources = isolate_dataset_data(result[1])
        data[result[2]] = {'to_replace': to_replace,
                           'replaced': replaced,
                           'sources': sources}

    return data


def isolate_dataset_data(text):
    """Identify replaced fields and source fields, if any."""
    replaced = set()
    sources = set()
    entries = text.strip().split('\n')
    for entry in entries:
        entry = entry.split(' AS ')
        replaced |= set(re.findall('`(.*?)`', entry[1]))
        sources |= set(re.findall('`(.*?)`', entry[0]))
    return list(replaced), list(sources)


class TestSQLTestParser(unittest.TestCase):

    """Test the sql parser utilised in later tests."""

    def test_isolate_dataset_entries(self):
        """Test isolate_dataset_entries used in later tests."""
        indata = """
SomeText
REPLACE INTO
  `monuments_all_tmp` (
    `tr_1`, `tr_2`, `tr_3`
  ) SELECT
    `s_1` AS `r_1`,
    'something' AS `r_2`,
    '' AS `r_3`,
    NULL AS `r_4`,
    ROUND(`s_2` * @granularity) AS `r_5`,
    `s_3` AS `r_6`, /* Comment 1 */
    `s_4` AS `r_7` -- Comment 2
    CONCATENATE(`s_5`, `s_6`) AS `r_7`
    FROM `monuments_some_(table)`;
SomeText
            """
        expected_table = 'monuments_some_(table)'
        expected_to_replace = ['tr_1', 'tr_2', 'tr_3']
        expected_replaced = ['r_1', 'r_2', 'r_3', 'r_4', 'r_5', 'r_6', 'r_7']
        expected_sources = ['s_1', 's_2', 's_3', 's_4', 's_5', 's_6']
        data = isolate_dataset_entries(indata)
        self.assertItemsEqual(data.keys(), [expected_table, ])
        self.assertItemsEqual(data[expected_table]['to_replace'],
                              expected_to_replace)
        self.assertItemsEqual(data[expected_table]['replaced'],
                              expected_replaced)
        self.assertItemsEqual(data[expected_table]['sources'],
                              expected_sources)


class FillTableMonumentsValidation(unittest.TestCase, CustomAssertions):

    """Validate fill_table_monuments_all.sql."""

    def setUp(self):
        with open('erfgoedbot/sql/fill_table_monuments_all.sql', 'r') as f:
            self.text = f.read()
        self.data = isolate_dataset_entries(self.text)

    def test_fill_table_monuments_all_replaced(self):
        """Ensure all variables stated to be replaced are in fact replaced."""
        self.longMessage = True
        for table, dataset in self.data.iteritems():
            self.assertItemsEqual(
                dataset['to_replace'], dataset['replaced'], msg=table)

    def test_fill_table_monuments_all_required_replacements(self):
        """Ensure the required variables are replaced, at least."""
        required = [
            'source', 'changed', 'lat_int', 'lon_int',
            'country', 'lang', 'id', 'adm0']
        for table, dataset in self.data.iteritems():
            msg = '%s in fill_table_monuments_all ' % table
            msg += 'missing required variable(s): %s'
            self.assert_all_in(required, dataset['replaced'], msg=msg)


class TestFillTableMonumentsOntoMonumentsConfig(unittest.TestCase,
                                                CustomAssertions):

    """Compatibility of fill_table_monuments_all.sql with monuments_config."""

    def setUp(self):
        with open('erfgoedbot/sql/fill_table_monuments_all.sql', 'r') as f:
            self.text = f.read()
        self.data = isolate_dataset_entries(self.text)
        self.process_config_tables()

    def process_config_tables(self):
        """Identify tables in monuments_config."""
        self.config_tables = []
        self.config_lookup = {}
        for key, data in config.countries.iteritems():
            table = data['table']
            if table.startswith('monuments'):  # i.e. not wlpa
                self.config_tables.append(table)
                self.config_lookup[table] = key

    def get_config_field_dests(self, table):
        """Return field destinations for a given table in monuments_config."""
        key = self.config_lookup[table]
        dest = []
        for field in config.countries[key]['fields']:
            dest.append(field['dest'])
        return dest

    def test_fill_table_monuments_all_tables_present(self):
        """Ensure all needed tables are present in monuments_config."""
        msg = '%s in fill_table_monuments_all not present in monuments_config'
        self.assert_all_in(self.data.keys(), self.config_tables, msg=msg)

    def test_fill_table_monuments_all_config_tables_used(self):
        """Ensure that all monuments_config tables are used."""
        msg = '%s in monuments_config not used in fill_table_monuments_all'
        self.assert_all_in(self.config_tables, self.data.keys(), msg=msg)

    def test_fill_table_monuments_all_source_in_config(self):
        """Ensure all sources are present in the corresponding config entry."""
        for table, dataset in self.data.iteritems():
            msg = '%s in fill_table_monuments_all ' % table
            msg += 'expects missing field(s): %s'
            dest = self.get_config_field_dests(table)
            dest += ['source', 'changed']  # implicitly defined
            self.assert_all_in(dataset['sources'], dest, msg=msg)
