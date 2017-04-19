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
        self.assertEquals(result, (2, 2))

    @mock.patch('erfgoedbot.populate_image_table.normalize_identifier', autospec=True)
    @mock.patch('erfgoedbot.populate_image_table.updateImage', autospec=True)
    def test_processSource_with_one_okay_picture_out_of_two(self, mock_updateImage, mock_normalize_identifier):
        """Trying to normalize the identifier of the first image throws a CannotNormalizeException,
        and the second succeeds. The processing does carry over to the second image.
        """
        self.mock_get_monuments.return_value = (
            (' 00000044\nEXAMPLE - 01.JPG', 'Example_-_01.jpg'),
            (' 00000044\nEXAMPLE - 02.JPG', 'Example_-_02.jpg')
        )
        mock_normalize_identifier.side_effect = [populate_image_table.CannotNormalizeException, u'44']
        result = populate_image_table.processSource('aa', self.country_config, None,
                                                    self.mock_cursor_1, None, self.mock_cursor_2)
        self.assertItemsEqual(mock_updateImage.mock_calls, [
            mock.call('aa', u'44', u'Example_-_02.jpg', False, None, self.mock_cursor_1)
        ])
        self.assertEquals(result, (2, 1))

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
        self.assertEquals(result, (1, 1))


class TestNormalizeIdentifier(unittest.TestCase):

    def test_normalize_identifier_none_raise_exception(self):
        with self.assertRaises(populate_image_table.CannotNormalizeException):
            populate_image_table.normalize_identifier(None)

    def test_normalize_identifier_alphanumeric(self):
        result = populate_image_table.normalize_identifier("PA123")
        self.assertEquals(result, u'PA123')

    def test_normalize_identifier_numbers(self):
        result = populate_image_table.normalize_identifier("12345")
        self.assertEquals(result, u'12345')

    def test_normalize_identifier_strips_spaces(self):
        result = populate_image_table.normalize_identifier(" 12345  ")
        self.assertEquals(result, u'12345')

    def test_normalize_identifier_with_slashes(self):
        result = populate_image_table.normalize_identifier("1.1/1")
        self.assertEquals(result, u'1.1/1')

    def test_normalize_identifier_with_dashes(self):
        result = populate_image_table.normalize_identifier("ASPA-101")
        self.assertEquals(result, u'ASPA-101')

    def test_normalize_identifier_strips_leading_zeroes(self):
        result = populate_image_table.normalize_identifier("0010")
        self.assertEquals(result, u'10')

    def test_normalize_identifier_strips_leading_underscores(self):
        result = populate_image_table.normalize_identifier("__123__45_")
        self.assertEquals(result, u'123__45_')

    def test_normalize_identifier_with_leading_zeroes_and_dashes(self):
        result = populate_image_table.normalize_identifier("00-147")
        self.assertEquals(result, u'-147')

    def test_normalize_identifier_with_unicode(self):
        result = populate_image_table.normalize_identifier("110Д000001-2")
        self.assertEquals(result, u'110Д000001-2')

    def test_normalize_identifier_does_not_convert_to_uppercase(self):
        result = populate_image_table.normalize_identifier("ab123")
        self.assertEquals(result, u'ab123')
