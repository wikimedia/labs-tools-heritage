#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Unit tests for monuments_config."""

import unittest
import unittest.mock as mock

from erfgoedbot import monuments_config


class TestFilteredCountries(unittest.TestCase):
    """Test the filtered_countries method."""

    def setUp(self):
        self.countries = {
            ('foo', 'bar'): {
                'country': 'foo',
                'lang': 'bar'},
            ('foo_rich', 'bar_rich'): {
                'country': 'foo_rich',
                'lang': 'bar_rich',
                'type': 'list',
                'table': 'monuments_foo_bar'},
            ('foo_skip', 'bar_skip'): {
                'country': 'foo_skip',
                'lang': 'bar_skip',
                'skip': True},
            ('foo_sparql', 'bar_sparql'): {
                'country': 'foo_sparql',
                'lang': 'bar_sparql',
                'type': 'sparql'},
            ('foo_wlpa', 'bar_wlpa'): {
                'country': 'foo_sparql',
                'lang': 'bar_sparql',
                'table': 'wlpa_foo_bar',
            }
        }

        patcher = mock.patch(
            'erfgoedbot.monuments_config.get_countries', autospec=True)
        self.mock_get_countries = patcher.start()
        self.mock_get_countries.return_value = self.countries
        self.addCleanup(patcher.stop)

    def test_filtered_countries_no_countries(self):
        self.mock_get_countries.return_value = {}
        countries = set()
        for (c, l), conf in monuments_config.filtered_countries():
            countries.add(c)
        self.assertEqual(countries, set())

    def test_filtered_countries_default(self):
        expected_countries = set(['foo', 'foo_sparql', 'foo_wlpa', 'foo_rich'])
        countries = set()
        for (c, l), conf in monuments_config.filtered_countries():
            countries.add(c)
        self.assertEqual(countries, expected_countries)

    def test_filtered_countries_skip_wd(self):
        expected_countries = set(['foo', 'foo_wlpa', 'foo_rich'])
        countries = set()
        for (c, l), conf in monuments_config.filtered_countries(skip_wd=True):
            countries.add(c)
        self.assertEqual(countries, expected_countries)

    def test_filtered_countries_skip_wlpa(self):
        expected_countries = set(['foo', 'foo_sparql', 'foo_rich'])
        countries = set()
        for (c, l), conf in monuments_config.filtered_countries(
                skip_wlpa=True):
            countries.add(c)
        self.assertEqual(countries, expected_countries)

    def test_filtered_countries_keep_skip(self):
        expected_countries = set(
            ['foo', 'foo_skip', 'foo_sparql', 'foo_wlpa', 'foo_rich'])
        countries = set()
        for (c, l), conf in monuments_config.filtered_countries(
                respect_skip=False):
            countries.add(c)
        self.assertEqual(countries, expected_countries)
