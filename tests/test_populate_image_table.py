#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Unit tests for populate_image_table."""
import unittest
from collections import OrderedDict

import mock

import pywikibot

from erfgoedbot import populate_image_table
from report_base_test import TestCreateReportTableBase


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
        self.mock_cursor_commons = mock.Mock()
        self.mock_cursor_monuments = mock.Mock()
        patcher = mock.patch('erfgoedbot.populate_image_table.getMonumentPhotos')
        self.mock_get_monuments = patcher.start()

        patcher_2 = mock.patch('erfgoedbot.populate_image_table.connect_to_commons_database')
        mock_connect_to_commons_database = patcher_2.start()
        mock_connect_to_commons_database.return_value = (None, self.mock_cursor_commons)

        patcher_3 = mock.patch('erfgoedbot.populate_image_table.connect_to_monuments_database')
        mock_connect_to_monuments_database = patcher_3.start()
        mock_connect_to_monuments_database.return_value = (None, self.mock_cursor_monuments)

        patcher_4 = mock.patch('erfgoedbot.populate_image_table.close_database_connection')
        mock_close_database_connection = patcher_4.start()

        self.addCleanup(patcher.stop)
        self.addCleanup(patcher_2.stop)
        self.addCleanup(patcher_3.stop)
        self.addCleanup(patcher_4.stop)

    @mock.patch('erfgoedbot.populate_image_table.has_geolocation', autospec=True)
    @mock.patch('erfgoedbot.populate_image_table.updateImage', autospec=True)
    def test_processSource_with_two_okay_pictures(self, mock_updateImage, mock_has_geolocation):
        mock_has_geolocation.return_value = True
        self.mock_get_monuments.return_value = (
            (' 00000044\nEXAMPLE - 01.JPG', 'Example_-_01.jpg'),
            (' 00000044\nEXAMPLE - 02.JPG', 'Example_-_02.jpg')
        )
        result = populate_image_table.processSource('aa', self.country_config)
        self.assertItemsEqual(mock_updateImage.mock_calls, [
            mock.call('aa', u'44', u'Example_-_01.jpg', True, None, self.mock_cursor_monuments),
            mock.call('aa', u'44', u'Example_-_02.jpg', True, None, self.mock_cursor_monuments)])
        self.assertEquals(result, (2, 2))

    @mock.patch('erfgoedbot.populate_image_table.has_geolocation', autospec=True)
    @mock.patch('erfgoedbot.populate_image_table.normalize_identifier', autospec=True)
    @mock.patch('erfgoedbot.populate_image_table.updateImage', autospec=True)
    def test_processSource_with_one_okay_picture_out_of_two(self, mock_updateImage, mock_normalize_identifier, mock_has_geolocation):
        """Trying to normalize the identifier of the first image throws a CannotNormalizeException,
        and the second succeeds. The processing does carry over to the second image.
        """
        mock_has_geolocation.return_value = False
        self.mock_get_monuments.return_value = (
            (' 00000044\nEXAMPLE - 01.JPG', 'Example_-_01.jpg'),
            (' 00000044\nEXAMPLE - 02.JPG', 'Example_-_02.jpg')
        )
        mock_normalize_identifier.side_effect = [populate_image_table.CannotNormalizeException, u'44']
        result = populate_image_table.processSource('aa', self.country_config)
        self.assertItemsEqual(mock_updateImage.mock_calls, [
            mock.call('aa', u'44', u'Example_-_02.jpg', False, None, self.mock_cursor_monuments)
        ])
        self.assertEquals(result, (2, 1))

    @mock.patch('erfgoedbot.populate_image_table.has_geolocation', autospec=True)
    @mock.patch('erfgoedbot.populate_image_table.updateImage', autospec=True)
    def test_processSource_with_one_unicode_title(self, mock_updateImage, mock_has_geolocation):
        mock_has_geolocation.return_value = True
        self.mock_get_monuments.return_value = (
            (' 00000044\nEXAMPLE - 01.JPG', '71_Cathédrale_Saint-Sauveur.JPG'),
        )
        result = populate_image_table.processSource('aa', self.country_config)
        self.assertItemsEqual(mock_updateImage.mock_calls, [
            mock.call('aa', u'44', u'71_Cath\xe9drale_Saint-Sauveur.JPG',
                      True, None, self.mock_cursor_monuments)])
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


class TestMakeStatistics(TestCreateReportTableBase):

    """Test the makeStatistics method."""

    def setUp(self):
        self.class_name = 'erfgoedbot.populate_image_table'
        super(TestMakeStatistics, self).setUp()

        self.comment = (
            u'Updating indexed image statistics. '
            u'Total indexed images: {0}')
        commons = pywikibot.Site('commons', 'commons')
        self.page = pywikibot.Page(
            commons, u'Commons:Monuments database/Indexed images/Statistics')

    def bundled_asserts(self, expected_rows,
                        expected_total_images_sum,
                        expected_tracked_images_sum):
        """The full battery of asserts to do for each test."""
        expected_text = self.prefix + expected_rows + self.postfix
        self.mock_save_to_wiki_or_local.assert_called_once_with(
            self.page,
            self.comment.format(expected_tracked_images_sum),
            expected_text
        )
        self.mock_table_header_row.assert_called_once()
        self.mock_table_bottom_row.assert_called_once_with(
            5, {
                1: expected_total_images_sum,
                2: expected_tracked_images_sum})

    def test_output_statistics_single(self):
        statistics = {
            'foo': {
                'commonsTemplate': 'foo_temp',
                'commonsTrackerCategory': 'foo_cat',
                'totalImages': 10,
                'tracked_images': 5
            }
        }

        expected_rows = (
            u'|-\n'
            u'| foo \n'
            u'| 10 \n'
            u'| 5 \n'
            u'| {{tl|foo_temp}} \n'
            u'| [[:Category:foo_cat|foo_cat]] \n')
        expected_total_images_sum = 10
        expected_tracked_images_sum = 5

        populate_image_table.makeStatistics(statistics)
        self.bundled_asserts(
            expected_rows,
            expected_total_images_sum,
            expected_tracked_images_sum)

    def test_output_statistics_multiple(self):
        # provide in oposite order to ensure sorting kicks in
        statistics = OrderedDict([
            ('foo', {
                'commonsTemplate': 'foo_temp',
                'commonsTrackerCategory': 'foo_cat',
                'totalImages': 10,
                'tracked_images': 5
            }),
            ('bar', {
                'commonsTemplate': 'bar_temp',
                'commonsTrackerCategory': 'bar_cat',
                'totalImages': 100,
                'tracked_images': 50
            })
        ])

        expected_rows = (
            u'|-\n'
            u'| bar \n'
            u'| 100 \n'
            u'| 50 \n'
            u'| {{tl|bar_temp}} \n'
            u'| [[:Category:bar_cat|bar_cat]] \n'
            u'|-\n'
            u'| foo \n'
            u'| 10 \n'
            u'| 5 \n'
            u'| {{tl|foo_temp}} \n'
            u'| [[:Category:foo_cat|foo_cat]] \n')
        expected_total_images_sum = 110
        expected_tracked_images_sum = 55

        populate_image_table.makeStatistics(statistics)
        self.bundled_asserts(
            expected_rows,
            expected_total_images_sum,
            expected_tracked_images_sum)
