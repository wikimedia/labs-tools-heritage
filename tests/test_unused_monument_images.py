#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Unit tests for unused_monument_images."""

# from pywikibot.site import APISite
# from pywikibot.exceptions import NoPage
import unittest
from collections import OrderedDict

import mock

from erfgoedbot import unused_monument_images
from report_base_test import TestCreateReportBase, TestCreateReportTableBase


class TestGroupUnusedImagesBySource(unittest.TestCase):

    """Test the group_unused_images_by_source method."""

    def setUp(self):
        self.photos = {
            '123-filename': 'filename.jpg',
            '456-filename3': 'filename3.jpg',
        }
        self.without_photo = {
            '123': 'source_url_1',
            '789': 'source_url_2',
        }
        self.countryconfig = {}

        def return_input(*args):
            # return the part before "-" of the first arg
            return args[0].partition('-')[0]

        patcher = mock.patch(
            'erfgoedbot.common.get_id_from_sort_key')
        self.mock_get_id_from_sort_key = patcher.start()
        self.mock_get_id_from_sort_key.side_effect = return_input
        self.addCleanup(patcher.stop)

    def test_group_unused_images_by_source_basic(self):
        expected = {'source_url_1': {'123': ['filename.jpg']}}
        result = unused_monument_images.group_unused_images_by_source(
            self.photos, self.without_photo, self.countryconfig)

        self.assertEquals(result, expected)
        self.mock_get_id_from_sort_key.assert_has_calls([
            mock.call('123-filename', self.without_photo),
            mock.call('456-filename3', self.without_photo)],
            any_order=True
        )

    def test_group_unused_images_by_source_sparql(self):
        self.countryconfig = {'type': 'sparql'}

        expected = {'source_url_1': {'123': ['filename.jpg']}}
        result = unused_monument_images.group_unused_images_by_source(
            self.photos, self.without_photo, self.countryconfig)

        self.assertEquals(result, expected)
        self.mock_get_id_from_sort_key.assert_has_calls([
            mock.call('123-filename', self.without_photo),
            mock.call('456-filename3', self.without_photo)],
            any_order=True
        )

    def test_group_unused_images_by_source_group_ids(self):
        self.photos['123-filename2'] = 'filename2.jpg'

        expected = {
            'source_url_1': {
                '123': ['filename.jpg', 'filename2.jpg']
            }
        }
        result = unused_monument_images.group_unused_images_by_source(
            self.photos, self.without_photo, self.countryconfig)

        self.assertEquals(result, expected)
        self.mock_get_id_from_sort_key.assert_has_calls([
            mock.call('123-filename', self.without_photo),
            mock.call('123-filename2', self.without_photo),
            mock.call('456-filename3', self.without_photo)],
            any_order=True
        )

    def test_group_unused_images_by_source_group_sources(self):
        self.without_photo['456'] = 'source_url_1'

        expected = {
            'source_url_1': {
                '123': ['filename.jpg'],
                '456': ['filename3.jpg']
            }
        }
        result = unused_monument_images.group_unused_images_by_source(
            self.photos, self.without_photo, self.countryconfig)

        self.assertEquals(result, expected)
        self.mock_get_id_from_sort_key.assert_has_calls([
            mock.call('123-filename', self.without_photo),
            mock.call('456-filename3', self.without_photo)],
            any_order=True
        )


class TestMakeStatistics(TestCreateReportTableBase):

    """Test the makeStatistics method."""

    def setUp(self):
        self.class_name = 'erfgoedbot.unused_monument_images'
        super(TestMakeStatistics, self).setUp()

        patcher = mock.patch(
            'erfgoedbot.unused_monument_images.common.get_template_link')
        self.mock_get_template_link = patcher.start()
        self.mock_get_template_link.return_value = '<row_template_link>'
        self.addCleanup(patcher.stop)

        self.commons = self.mock_site.return_value
        self.mock_report_page = mock.MagicMock()
        self.mock_report_page.title.return_value = '<report_page>'

        self.comment = (
            u'Updating unused image statistics. Total of {total_images} '
            u'unused images for {total_ids} different monuments.')
        self.pagename = u'Commons:Monuments database/Unused images/Statistics'

    def bundled_asserts(self, expected_rows,
                        expected_total_images,
                        expected_total_ids):
        """The full battery of asserts to do for each test."""
        expected_text = self.prefix + expected_rows + self.postfix

        self.mock_site.assert_called_once_with('commons', 'commons')
        self.mock_page.assert_called_once_with(
            self.mock_site.return_value, self.pagename)
        self.mock_save_to_wiki_or_local.assert_called_once_with(
            self.mock_page.return_value,
            self.comment.format(
                total_images=expected_total_images,
                total_ids=expected_total_ids),
            expected_text
        )
        self.mock_table_header_row.assert_called_once()
        self.mock_table_bottom_row.assert_called_once_with(
            7, {2: expected_total_images, 3: expected_total_ids})

    def test_make_statistics_single_complete(self):
        statistics = [{
            'config': {
                'country': 'foo',
                'lang': 'en',
                'rowTemplate': 'row template',
                'commonsTemplate': 'commons template'},
            'report_page': self.mock_report_page,
            'total_images': 321,
            'total_ids': 123
        }]

        expected_rows = (
            u'|-\n'
            u'| foo \n'
            u'| en \n'
            u'| 321 \n'
            u'| 123 \n'
            u'| <report_page> \n'
            u'| <row_template_link> \n'
            u'| {{tl|commons template}} \n')
        expected_total_images = 321
        expected_total_ids = 123

        unused_monument_images.makeStatistics(statistics)
        self.mock_get_template_link.assert_called_once_with(
            'en', 'wikipedia', 'row template', self.commons)
        self.bundled_asserts(
            expected_rows,
            expected_total_images,
            expected_total_ids)

    def test_make_statistics_single_basic(self):
        statistics = [{
            'config': {
                'country': 'foo',
                'lang': 'en',
                'rowTemplate': 'row template'},
            'total_images': 321,
            'total_ids': 123
        }]

        expected_rows = (
            u'|-\n'
            u'| foo \n'
            u'| en \n'
            u'| 321 \n'
            u'| 123 \n'
            u'| --- \n'
            u'| <row_template_link> \n'
            u'| --- \n')
        expected_total_images = 321
        expected_total_ids = 123

        unused_monument_images.makeStatistics(statistics)
        self.mock_get_template_link.assert_called_once_with(
            'en', 'wikipedia', 'row template', self.commons)
        self.bundled_asserts(
            expected_rows,
            expected_total_images,
            expected_total_ids)

    def test_make_statistics_single_sparql_basic(self):
        statistics = [{
            'config': {
                'country': 'foo',
                'lang': 'en',
                'type': 'sparql'},
            'total_images': 321,
            'total_ids': 123
        }]

        expected_rows = (
            u'|-\n'
            u'| foo \n'
            u'| en \n'
            u'| 321 \n'
            u'| 123 \n'
            u'| --- \n'
            u'| --- \n'
            u'| --- \n')
        expected_total_images = 321
        expected_total_ids = 123

        unused_monument_images.makeStatistics(statistics)
        self.mock_get_template_link.assert_not_called()
        self.bundled_asserts(
            expected_rows,
            expected_total_images,
            expected_total_ids)

    def test_make_statistics_basic_skipped(self):
        statistics = [{
            'config': {
                'country': 'foo',
                'lang': 'en',
                'rowTemplate': 'a template'},
            'cmt': 'skipped: no unusedImagesPage'
        }]

        expected_rows = (
            u'|-\n'
            u'| foo \n'
            u'| en \n'
            u'| skipped: no unusedImagesPage \n'
            u'| --- \n'
            u'| --- \n'
            u'| <row_template_link> \n'
            u'| --- \n')
        expected_total_images = 0
        expected_total_ids = 0

        unused_monument_images.makeStatistics(statistics)
        self.mock_get_template_link.assert_called_once_with(
            'en', 'wikipedia', 'a template', self.commons)
        self.bundled_asserts(
            expected_rows,
            expected_total_images,
            expected_total_ids)

    def test_make_statistics_multiple_complete(self):
        report_page_1 = mock.MagicMock()
        report_page_1.title.return_value = '<report_page:Foobar>'
        report_page_2 = mock.MagicMock()
        report_page_2.title.return_value = '<report_page:Barfoo>'
        statistics = [
            {
                'config': {
                    'country': 'foo',
                    'lang': 'en',
                    'rowTemplate': 'row template',
                    'commonsTemplate': 'commons template',
                    'project': 'wikipedia'},
                'report_page': report_page_1,
                'total_images': 3,
                'total_ids': 2
            },
            {
                'config': {
                    'country': 'bar',
                    'lang': 'fr',
                    'rowTemplate': 'a template',
                    'project': 'wikisource'},
                'report_page': report_page_2,
                'total_images': 7,
                'total_ids': 3
            }
        ]

        expected_rows = (
            u'|-\n'
            u'| foo \n'
            u'| en \n'
            u'| 3 \n'
            u'| 2 \n'
            u'| <report_page:Foobar> \n'
            u'| <row_template_link> \n'
            u'| {{tl|commons template}} \n'
            u'|-\n'
            u'| bar \n'
            u'| fr \n'
            u'| 7 \n'
            u'| 3 \n'
            u'| <report_page:Barfoo> \n'
            u'| <row_template_link> \n'
            u'| --- \n')
        expected_total_images = 10
        expected_total_ids = 5

        unused_monument_images.makeStatistics(statistics)
        self.mock_get_template_link.assert_has_calls([
            mock.call('en', 'wikipedia', 'row template', self.commons),
            mock.call('fr', 'wikisource', 'a template', self.commons),
        ])
        self.bundled_asserts(
            expected_rows,
            expected_total_images,
            expected_total_ids)

    def test_make_statistics_multiple_mixed(self):
        statistics = [
            {
                'config': {
                    'country': 'foo',
                    'lang': 'en',
                    'rowTemplate': 'row template',
                    'commonsTemplate': 'commons template'},
                'report_page': self.mock_report_page,
                'total_images': 3,
                'total_ids': 2
            },
            {
                'config': {
                    'country': 'bar',
                    'lang': 'fr',
                    'rowTemplate': 'a template'},
                'cmt': 'skipped: no unusedImagesPage'
            }
        ]

        expected_rows = (
            u'|-\n'
            u'| foo \n'
            u'| en \n'
            u'| 3 \n'
            u'| 2 \n'
            u'| <report_page> \n'
            u'| <row_template_link> \n'
            u'| {{tl|commons template}} \n'
            u'|-\n'
            u'| bar \n'
            u'| fr \n'
            u'| skipped: no unusedImagesPage \n'
            u'| --- \n'
            u'| --- \n'
            u'| <row_template_link> \n'
            u'| --- \n')
        expected_total_images = 3
        expected_total_ids = 2

        unused_monument_images.makeStatistics(statistics)
        self.mock_get_template_link.assert_has_calls([
            mock.call('en', 'wikipedia', 'row template', self.commons),
            mock.call('fr', 'wikipedia', 'a template', self.commons),
        ])
        self.bundled_asserts(
            expected_rows,
            expected_total_images,
            expected_total_ids)


class TestOutputCountryReport(TestCreateReportBase):

    """Test the output_country_report method."""

    def setUp(self):
        self.class_name = 'erfgoedbot.unused_monument_images'
        super(TestOutputCountryReport, self).setUp()
        self.mock_report_page = self.mock_page.return_value

        self.prefix = 'prefix'
        patcher = mock.patch(
            'erfgoedbot.unused_monument_images.common.instruction_header')
        self.mock_instruction_header = patcher.start()
        self.mock_instruction_header.return_value = self.prefix
        self.addCleanup(patcher.stop)

        patcher = mock.patch(
            'erfgoedbot.missing_commonscat_links.common.done_message')
        self.mock_done_message = patcher.start()
        self.addCleanup(patcher.stop)

        def return_input(*args, **kargs):
            # return the part before "-" of the first arg
            return args[0].replace('url', 'link')

        patcher = mock.patch(
            'erfgoedbot.unused_monument_images.common.get_source_link')
        self.mock_get_source_link = patcher.start()
        self.mock_get_source_link.side_effect = return_input
        self.addCleanup(patcher.stop)

        self.unused_images = OrderedDict()
        self.unused_images['source_url_1'] = OrderedDict()
        self.unused_images['source_url_1']['id_11'] = [
            'filename1_11.jpg',
            'filename1_12.jpg'
        ]
        self.unused_images['source_url_1']['id_12'] = [
            'filename1_21.jpg',
            'filename1_22.jpg'
        ]
        self.unused_images['source_url_2'] = OrderedDict()
        self.unused_images['source_url_2']['id_21'] = [
            'filename2.jpg'
        ]

    def bundled_asserts(self, result,
                        expected_cmt,
                        expected_totals,
                        expected_output):
        """The full battery of asserts to do for each test."""
        expected_output = self.prefix + expected_output

        self.assertEqual(result, expected_totals)
        self.mock_save_to_wiki_or_local.assert_called_once_with(
            self.mock_report_page,
            expected_cmt,
            expected_output,
            minorEdit=False
        )
        self.mock_instruction_header.assert_called_once()

    def test_output_country_report_complete(self):
        expected_cmt = u'Images to be used in monument lists: 5'
        expected_output = (
            u'=== source_link_1 ===\n'
            u'<gallery>\n'
            u'File:filename1_11.jpg|id_11\n'
            u'File:filename1_12.jpg|id_11\n'
            u'File:filename1_21.jpg|id_12\n'
            u'File:filename1_22.jpg|id_12\n'
            u'</gallery>\n'
            u'=== source_link_2 ===\n'
            u'<gallery>\n'
            u'File:filename2.jpg|id_21\n'
            u'</gallery>\n')
        expected_totals = {
            'images': 5,
            'pages': 2,
            'ids': 3
        }

        result = unused_monument_images.output_country_report(
            self.unused_images, self.mock_report_page)
        self.bundled_asserts(
            result,
            expected_cmt,
            expected_totals,
            expected_output)
        self.mock_get_source_link.assert_has_calls([
            mock.call('source_url_1'),
            mock.call('source_url_2')])

    def test_output_country_report_max_images(self):
        max_images = 2

        expected_cmt = (
            u'Images to be used in monument lists: 2 (gallery maximum '
            u'reached), total of unused images: 5')
        expected_output = (
            u'=== source_link_1 ===\n'
            u'<gallery>\n'
            u'File:filename1_11.jpg|id_11\n'
            u'File:filename1_12.jpg|id_11\n'
            u'</gallery>\n'
            u'<!-- Maximum number of images reached: 2, '
            u'total of unused images: 5 -->\n')
        expected_totals = {
            'images': 5,
            'pages': 2,
            'ids': 3
        }

        result = unused_monument_images.output_country_report(
            self.unused_images, self.mock_report_page, max_images=max_images)
        self.bundled_asserts(
            result,
            expected_cmt,
            expected_totals,
            expected_output)
        self.mock_get_source_link.assert_called_once_with('source_url_1')

    def test_output_country_report_max_images_all_candidates(self):
        max_images = 3

        expected_cmt = (
            u'Images to be used in monument lists: 3 (gallery maximum '
            u'reached), total of unused images: 5')
        expected_output = (
            u'=== source_link_1 ===\n'
            u'<gallery>\n'
            u'File:filename1_11.jpg|id_11\n'
            u'File:filename1_12.jpg|id_11\n'
            u'File:filename1_21.jpg|id_12\n'
            u'File:filename1_22.jpg|id_12\n'
            u'</gallery>\n'
            u'<!-- Maximum number of images reached: 3, '
            u'total of unused images: 5 -->\n')
        expected_totals = {
            'images': 5,
            'pages': 2,
            'ids': 3
        }

        result = unused_monument_images.output_country_report(
            self.unused_images, self.mock_report_page, max_images=max_images)
        self.bundled_asserts(
            result,
            expected_cmt,
            expected_totals,
            expected_output)
        self.mock_get_source_link.assert_called_once_with('source_url_1')

    def test_output_country_report_no_images(self):
        max_images = 3
        self.unused_images = {}

        expected_cmt = u'Images to be used in monument lists: 0'
        expected_output = self.mock_done_message.return_value
        expected_totals = {
            'images': 0,
            'pages': 0,
            'ids': 0
        }

        result = unused_monument_images.output_country_report(
            self.unused_images, self.mock_report_page, max_images=max_images)
        self.mock_done_message.assert_called_once()
        self.bundled_asserts(
            result,
            expected_cmt,
            expected_totals,
            expected_output)
        self.mock_get_source_link.assert_not_called()

    def test_output_country_report_sparql(self):
        del self.unused_images['source_url_1']['id_12']  # only one id per item
        expected_cmt = u'Images to be used in monument lists: 3'
        expected_output = (
            u'<gallery>\n'
            u'File:filename1_11.jpg|source_link_1\n'
            u'File:filename1_12.jpg|source_link_1\n'
            u'</gallery>\n'
            u'<gallery>\n'
            u'File:filename2.jpg|source_link_2\n'
            u'</gallery>\n')
        expected_totals = {
            'images': 3,
            'pages': 2,
            'ids': 2
        }

        result = unused_monument_images.output_country_report(
            self.unused_images, self.mock_report_page, is_sparql=True)
        self.bundled_asserts(
            result,
            expected_cmt,
            expected_totals,
            expected_output)
        self.mock_get_source_link.assert_has_calls([
            mock.call('source_url_1', 'sparql', label='id_11'),
            mock.call('source_url_2', 'sparql', label='id_21')])
