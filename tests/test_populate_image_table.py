#!/usr/bin/python
# -*- coding: utf-8  -*-

"""Unit tests for populate_image_table."""

import mock
import unittest

from erfgoedbot import populate_image_table


class TestGetSources(unittest.TestCase):

    def setUp(self):
        country_config_1 = {
            "country": "aa",
            "lang": "xx",
            "commonsTemplate": "Template A",
            "commonsTrackerCategory": "Tracker category A",
        }
        country_config_2 = {
            "country": "bb",
            "lang": "yy",
            "commonsTemplate": "Template B",
            "commonsTrackerCategory": "Tracker category B",
        }
        country_config = {
            (u'aa', u'xx'): country_config_1,
            (u'bb', u'yy'): country_config_2
        }
        patcher = mock.patch('erfgoedbot.monuments_config.get_countries')
        self.mock_get_countries = patcher.start()
        self.mock_get_countries.return_value = country_config
        self.addCleanup(patcher.stop)

    def test_getSources(self):
        result = populate_image_table.getSources()
        expected = {
            u'aa': {
                'commonsTrackerCategory': 'Tracker category A',
                'commonsTemplate': 'Template A'
            },
            u'bb': {
                'commonsTrackerCategory': 'Tracker category B',
                'commonsTemplate': 'Template B'
            }
        }
        self.assertItemsEqual(result, expected)


class TestProcessSource(unittest.TestCase):

    def setUp(self):
        self.country_config = {
            "country": "aa",
            "lang": "xx",
            "commonsTemplate": "Template A",
            "commonsTrackerCategory": "Tracker category A",
        }
        self.mock_cursor_1 = mock.Mock()
        self.mock_cursor_2 = mock.Mock()
        patcher = mock.patch('erfgoedbot.populate_image_table.getMonumentPhotos')
        self.mock_get_monuments = patcher.start()

        self.addCleanup(patcher.stop)

    @mock.patch('erfgoedbot.populate_image_table.has_geolocation', autospec=True)
    @mock.patch('erfgoedbot.populate_image_table.updateImage', autospec=True)
    def test_processSource_with_two_okay_pictures(self, mock_updateImage, mock_has_geolocation):
        mock_has_geolocation.return_value = True
        self.mock_get_monuments.return_value = (
            (' 00000044\nEXAMPLE - 01.JPG', 'Example_-_01.jpg'),
            (' 00000044\nEXAMPLE - 02.JPG', 'Example_-_02.jpg')
        )
        result = populate_image_table.processSource('aa', self.country_config, None,
                                                    self.mock_cursor_1, None, self.mock_cursor_2)
        self.assertItemsEqual(mock_updateImage.mock_calls, [
            mock.call('aa', u'44', u'Example_-_01.jpg', True, None, self.mock_cursor_1),
            mock.call('aa', u'44', u'Example_-_02.jpg', True, None, self.mock_cursor_1)])
        self.assertEquals(result, 2)

    @mock.patch('erfgoedbot.populate_image_table.has_geolocation', autospec=True)
    @mock.patch('erfgoedbot.populate_image_table.updateImage', autospec=True)
    def test_processSource_with_one_unicode_title(self, mock_updateImage, mock_has_geolocation):
        mock_has_geolocation.return_value = True
        self.mock_get_monuments.return_value = (
            (' 00000044\nEXAMPLE - 01.JPG', '71_Cathédrale_Saint-Sauveur.JPG'),
        )
        result = populate_image_table.processSource('aa', self.country_config, None,
                                                    self.mock_cursor_1, None, self.mock_cursor_2)
        self.assertItemsEqual(mock_updateImage.mock_calls, [
            mock.call('aa', u'44', u'71_Cath\xe9drale_Saint-Sauveur.JPG',
                      True, None, self.mock_cursor_1)])
        self.assertEquals(result, 1)
