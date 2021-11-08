#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Unit tests for images_of_monuments_without_id."""
import unittest
import unittest.mock as mock

import custom_assertions  # noqa F401
from erfgoedbot import images_of_monuments_without_id
from report_base_test import TestCreateReportBase, TestCreateReportTableBase


class TestProcessCountry(TestCreateReportBase):

    """Test the processCountry method."""

    def setUp(self):
        self.class_name = 'erfgoedbot.images_of_monuments_without_id'
        super(TestProcessCountry, self).setUp()
        self.countryconfig = {
            'country': 'foo',
            'lang': 'bar',
            'commonsTemplate': 'A template',
            'commonsTrackerCategory': 'A category',
            'imagesWithoutIdPage': 'A report page',
            'project': 'wikisource'
        }
        self.add_template = True
        self.comment = 'Images without an id'

        patcher = mock.patch(
            'erfgoedbot.images_of_monuments_without_id.getMonumentsWithPhoto')
        self.mock_get_monuments_with_photo = patcher.start()
        self.mock_get_monuments_with_photo.return_value = {}
        self.addCleanup(patcher.stop)

        patcher = mock.patch(
            'erfgoedbot.images_of_monuments_without_id.getMonumentsWithTemplate')
        self.mock_get_monuments_with_template = patcher.start()
        self.mock_get_monuments_with_template.return_value = []
        self.addCleanup(patcher.stop)

        patcher = mock.patch(
            'erfgoedbot.images_of_monuments_without_id.getMonumentsWithoutTemplate')
        self.mock_get_monuments_without_template = patcher.start()
        self.mock_get_monuments_without_template.return_value = []
        self.addCleanup(patcher.stop)

        patcher = mock.patch(
            'erfgoedbot.images_of_monuments_without_id.addCommonsTemplate')
        self.mock_add_commons_template = patcher.start()
        self.mock_add_commons_template.return_value = False
        self.addCleanup(patcher.stop)

        patcher = mock.patch(
            'erfgoedbot.images_of_monuments_without_id.output_country_report')
        self.mock_output_country_report = patcher.start()
        self.addCleanup(patcher.stop)

    def bundled_asserts_outputted(self, result, expected_rows, expected_total):
        expected = {
            'report_page': self.mock_page.return_value,
            'config': self.countryconfig,
            'totals': expected_total
        }
        self.assertEqual(result, expected)
        self.mock_get_monuments_with_photo.assert_called_once_with(
            'foo', 'bar', 'conn', 'cursor')
        self.mock_get_monuments_with_template.assert_called_once_with(
            self.countryconfig,
            'conn2', 'cursor2')
        self.mock_get_monuments_without_template.assert_called_once_with(
            self.countryconfig,
            'conn2', 'cursor2')
        self.mock_site.assert_called_once_with('bar', 'wikisource')
        self.mock_page.assert_called_once_with(
            self.mock_site.return_value, 'A report page')
        self.mock_output_country_report.assert_called_once_with(
            expected_rows, self.mock_page.return_value)

    def bundled_asserts_skipped(self, result, expected_cmt):
        expected = {
            'config': self.countryconfig,
            'cmt': expected_cmt
        }
        self.assertEqual(result, expected)
        self.mock_get_monuments_with_photo.assert_not_called()
        self.mock_get_monuments_with_template.assert_not_called()
        self.mock_get_monuments_without_template.assert_not_called()
        self.mock_site.assert_not_called()
        self.mock_page.assert_not_called()
        self.mock_add_commons_template.assert_not_called()
        self.mock_output_country_report.assert_not_called()

    def test_processCountry_skip_on_no_commons_template(self):
        self.countryconfig.pop('commonsTemplate')
        expected_cmt = 'skipped: no commonsTemplate or commonsTrackerCategory'
        result = images_of_monuments_without_id.processCountry(
            self.countryconfig, self.add_template,
            'conn', 'cursor', 'conn2', 'cursor2')
        self.bundled_asserts_skipped(result, expected_cmt)

    def test_processCountry_skip_on_no_commons_tracker_category(self):
        self.countryconfig.pop('commonsTrackerCategory')
        expected_cmt = 'skipped: no commonsTemplate or commonsTrackerCategory'
        result = images_of_monuments_without_id.processCountry(
            self.countryconfig, self.add_template,
            'conn', 'cursor', 'conn2', 'cursor2')
        self.bundled_asserts_skipped(result, expected_cmt)

    def test_processCountry_skip_on_no_allowed_output(self):
        self.countryconfig.pop('imagesWithoutIdPage')
        self.add_template = False
        expected_cmt = 'skipped: no imagesWithoutIdPage or template addition'
        result = images_of_monuments_without_id.processCountry(
            self.countryconfig, self.add_template,
            'conn', 'cursor', 'conn2', 'cursor2')
        self.bundled_asserts_skipped(result, expected_cmt)

    def test_processCountry_output_empty(self):
        expected_rows = []
        expected_total = {
            'added': 0,
            'with_id': 0,
            'without_id': 0
        }
        result = images_of_monuments_without_id.processCountry(
            self.countryconfig, self.add_template,
            'conn', 'cursor', 'conn2', 'cursor2')

        self.bundled_asserts_outputted(result, expected_rows, expected_total)
        self.mock_add_commons_template.assert_not_called()

    def test_processCountry_output_without_template(self):
        self.mock_get_monuments_without_template.return_value = ['Bar.jpg']
        expected_rows = [
            ('Bar.jpg', )
        ]
        expected_total = {
            'added': 0,
            'with_id': 0,
            'without_id': 1
        }
        result = images_of_monuments_without_id.processCountry(
            self.countryconfig, self.add_template,
            'conn', 'cursor', 'conn2', 'cursor2')

        self.bundled_asserts_outputted(result, expected_rows, expected_total)
        self.mock_add_commons_template.assert_not_called()

    def test_processCountry_output_with_photo(self):
        self.mock_get_monuments_with_photo.return_value = {'Foobar.jpg': 123}
        expected_rows = [
            ('Foobar.jpg', 123, 'A template')
        ]
        expected_total = {
            'added': 0,
            'with_id': 1,
            'without_id': 0
        }
        result = images_of_monuments_without_id.processCountry(
            self.countryconfig, self.add_template,
            'conn', 'cursor', 'conn2', 'cursor2')

        self.bundled_asserts_outputted(result, expected_rows, expected_total)
        self.mock_add_commons_template.assert_called_once_with(
            'Foobar.jpg', 'A template', 123)

    def test_processCountry_output_with_photo_without_template_no_overlap(
            self):
        self.mock_get_monuments_with_photo.return_value = {
            'Foobar.jpg': 123}
        self.mock_get_monuments_without_template.return_value = ['Bar.jpg']
        self.mock_get_monuments_with_template.return_value = ['Foo.jpg']
        expected_rows = [
            ('Bar.jpg', ),
            ('Foobar.jpg', 123, 'A template')
        ]
        expected_total = {
            'added': 0,
            'with_id': 1,
            'without_id': 1
        }
        result = images_of_monuments_without_id.processCountry(
            self.countryconfig, self.add_template,
            'conn', 'cursor', 'conn2', 'cursor2')

        self.bundled_asserts_outputted(result, expected_rows, expected_total)
        self.mock_add_commons_template.assert_called_once_with(
            'Foobar.jpg', 'A template', 123)

    def test_processCountry_output_no_duplication(self):
        self.mock_get_monuments_with_photo.return_value = {'Bar.jpg': 456}
        self.mock_get_monuments_without_template.return_value = ['Bar.jpg']
        expected_rows = [
            ('Bar.jpg', 456, 'A template')
        ]
        expected_total = {
            'added': 0,
            'with_id': 1,
            'without_id': 0
        }
        result = images_of_monuments_without_id.processCountry(
            self.countryconfig, self.add_template,
            'conn', 'cursor', 'conn2', 'cursor2')

        self.bundled_asserts_outputted(result, expected_rows, expected_total)
        self.mock_add_commons_template.assert_called_once_with(
            'Bar.jpg', 'A template', 456)

    def test_processCountry_no_output_without_target_page(self):
        self.countryconfig.pop('imagesWithoutIdPage')
        self.mock_get_monuments_with_photo.return_value = {
            'Foobar.jpg': 123}
        self.mock_get_monuments_without_template.return_value = ['Bar.jpg']
        self.mock_get_monuments_with_template.return_value = ['Foo.jpg']
        expected = expected = {
            'report_page': None,
            'config': self.countryconfig,
            'totals': {
                'added': 0,
                'with_id': 1,
                'without_id': 1
            }
        }
        result = images_of_monuments_without_id.processCountry(
            self.countryconfig, self.add_template,
            'conn', 'cursor', 'conn2', 'cursor2')

        self.assertEqual(result, expected)
        self.mock_add_commons_template.assert_called_once_with(
            'Foobar.jpg', 'A template', 123)
        self.mock_get_monuments_with_photo.assert_called_once()
        self.mock_get_monuments_with_template.assert_called_once()
        self.mock_get_monuments_without_template.assert_called_once()
        self.mock_site.assert_not_called()
        self.mock_page.assert_not_called()
        self.mock_output_country_report.assert_not_called()

    def test_processCountry_output_with_template(self):
        self.mock_get_monuments_with_photo.return_value = {'Foo.jpg': 789}
        self.mock_get_monuments_with_template.return_value = ['Foo.jpg']
        expected_rows = []
        expected_total = {
            'added': 0,
            'with_id': 0,
            'without_id': 0
        }
        result = images_of_monuments_without_id.processCountry(
            self.countryconfig, self.add_template,
            'conn', 'cursor', 'conn2', 'cursor2')

        self.bundled_asserts_outputted(result, expected_rows, expected_total)
        self.mock_add_commons_template.assert_not_called()

    def test_processCountry_output_template_added(self):
        self.mock_get_monuments_with_photo.return_value = {
            'Foobar.jpg': 123,
            'Bar.jpg': 456}
        self.mock_get_monuments_without_template.return_value = ['Bar.jpg']
        self.mock_add_commons_template.return_value = True
        expected_rows = []
        expected_total = {
            'added': 2,
            'with_id': 0,
            'without_id': 0
        }
        result = images_of_monuments_without_id.processCountry(
            self.countryconfig, self.add_template,
            'conn', 'cursor', 'conn2', 'cursor2')

        self.bundled_asserts_outputted(result, expected_rows, expected_total)
        self.mock_add_commons_template.assert_has_calls([
            mock.call('Bar.jpg', 'A template', 456),
            mock.call('Foobar.jpg', 'A template', 123)])

    def test_processCountry_output_do_not_add_template(self):
        self.add_template = False
        self.mock_get_monuments_with_photo.return_value = {
            'Foobar.jpg': 123,
            'Bar.jpg': 456}
        self.mock_get_monuments_without_template.return_value = ['Bar.jpg']
        self.mock_add_commons_template.return_value = True
        expected_rows = [
            ('Bar.jpg', 456, 'A template'),
            ('Foobar.jpg', 123, 'A template')
        ]
        expected_total = {
            'added': 0,
            'with_id': 2,
            'without_id': 0
        }

        result = images_of_monuments_without_id.processCountry(
            self.countryconfig, self.add_template,
            'conn', 'cursor', 'conn2', 'cursor2')
        self.bundled_asserts_outputted(result, expected_rows, expected_total)
        self.mock_add_commons_template.assert_not_called()


class TestFormatGalleryRow(unittest.TestCase):

    """Test the format_gallery_row method."""

    def test_format_gallery_row_image(self):
        image = 'Foo.jpg'
        self.assertEqual(
            'File:Foo.jpg',
            images_of_monuments_without_id.format_gallery_row(image)
        )

    def test_format_gallery_row_id(self):
        image = 'Foo.jpg'
        id = 123
        self.assertEqual(
            'File:Foo.jpg|123',
            images_of_monuments_without_id.format_gallery_row(image, id)
        )

    def test_format_gallery_row_template(self):
        image = 'Foo.jpg'
        id = 123
        template = 'Bar'
        self.assertEqual(
            'File:Foo.jpg|<nowiki>{{Bar|123}}</nowiki>',
            images_of_monuments_without_id.format_gallery_row(
                image, id, template)
        )


class TestAddCommonsTemplate(unittest.TestCase):

    """Test the addCommonsTemplate method."""

    def setUp(self):
        self.identifier = 123
        self.image = 'Foo.jpg'
        self.page_templates = ['Pre-existing Template']
        self.comment = 'Adding template {0} based on usage in list'

        # silence diff viewer
        patcher = mock.patch(
            'erfgoedbot.images_of_monuments_without_id.common.pywikibot.showDiff',
            autospec=True)
        self.mock_show_diff = patcher.start()
        self.addCleanup(patcher.stop)

        # autospec does not support assert_not_called
        patcher = mock.patch(
            'erfgoedbot.images_of_monuments_without_id.common.save_to_wiki_or_local')
        self.mock_save_to_wiki_or_local = patcher.start()
        self.addCleanup(patcher.stop)

        patcher = mock.patch(
            'erfgoedbot.images_of_monuments_without_id.pywikibot.Site',
            autospec=True)
        self.mock_site = patcher.start()
        self.addCleanup(patcher.stop)

        patcher = mock.patch(
            'erfgoedbot.images_of_monuments_without_id.pywikibot.FilePage',
            autospec=True)
        self.mock_page = patcher.start()
        self.image_page = self.mock_page.return_value
        self.addCleanup(patcher.stop)

        self.image_page.exists.return_value = True
        self.image_page.isRedirectPage.return_value = False
        self.image_page.templates.return_value = self.page_templates
        self.image_page.get.return_value = '<page contents>'

    def bundled_asserts_skipped(self, result):
        self.assertFalse(result)
        self.mock_site.assert_called_once_with('commons', 'commons')
        self.mock_page.assert_called_once_with(
            self.mock_site.return_value, self.image)
        self.mock_save_to_wiki_or_local.assert_not_called()

    def test_addCommonsTemplate_successfull(self):
        template = 'A new template'
        expected_text = '{{A new template|123}}\n<page contents>'
        result = images_of_monuments_without_id.addCommonsTemplate(
            self.image, template, self.identifier)

        self.assertTrue(result)
        self.mock_site.assert_called_once_with('commons', 'commons')
        self.mock_page.assert_called_once_with(
            self.mock_site.return_value, self.image)
        self.mock_save_to_wiki_or_local.assert_called_once_with(
            self.mock_page.return_value,
            self.comment.format(template),
            expected_text
        )

    def test_addCommonsTemplate_skip_on_non_exist(self):
        self.image_page.exists.return_value = False
        template = 'A new template'
        result = images_of_monuments_without_id.addCommonsTemplate(
            self.image, template, self.identifier)

        self.bundled_asserts_skipped(result)

    def test_addCommonsTemplate_skip_on_redirect(self):
        self.image_page.isRedirectPage.return_value = True
        template = 'A new template'
        result = images_of_monuments_without_id.addCommonsTemplate(
            self.image, template, self.identifier)

        self.bundled_asserts_skipped(result)

    def test_addCommonsTemplate_skip_on_existing_template(self):
        template = 'Pre-existing Template'
        result = images_of_monuments_without_id.addCommonsTemplate(
            self.image, template, self.identifier)

        self.bundled_asserts_skipped(result)


class TestOutputCountryReport(TestCreateReportBase):

    """Test the output_country_report method."""

    def setUp(self):
        self.class_name = 'erfgoedbot.images_of_monuments_without_id'
        super(TestOutputCountryReport, self).setUp()
        self.mock_report_page = self.mock_page.return_value

        self.rows = [
            ('foo.jpg', 123, 'Bar'),
            ('bar.jpg', 123),
            ('foobar.jpg', )
        ]

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

        # autospec does not support assert_not_called
        patcher = mock.patch(
            'erfgoedbot.images_of_monuments_without_id.format_gallery_row')
        self.mock_format_gallery_row = patcher.start()
        self.mock_format_gallery_row.return_value = '<formatted row>'
        self.addCleanup(patcher.stop)

    def bundled_asserts(self, expected_cmt, expected_output):
        """The full battery of asserts to do for each test."""
        expected_output = self.prefix + expected_output

        self.mock_save_to_wiki_or_local.assert_called_once_with(
            self.mock_report_page,
            expected_cmt,
            expected_output,
            minorEdit=False
        )
        self.mock_instruction_header.assert_called_once()

    def test_output_country_report_empty(self):
        expected_cmt = 'Images without an id: 0'
        expected_output = self.mock_done_message.return_value

        images_of_monuments_without_id.output_country_report(
            [], self.mock_report_page)
        self.mock_done_message.assert_called_once()
        self.bundled_asserts(
            expected_cmt,
            expected_output)
        self.mock_format_gallery_row.assert_not_called()

    def test_output_country_report_complete(self):
        expected_cmt = 'Images without an id: 3'
        expected_output = (
            '<gallery>\n'
            '<formatted row>\n'
            '<formatted row>\n'
            '<formatted row>\n'
            '</gallery>')

        images_of_monuments_without_id.output_country_report(
            self.rows, self.mock_report_page)
        self.bundled_asserts(
            expected_cmt,
            expected_output)
        self.mock_format_gallery_row.assert_has_calls([
            mock.call('foo.jpg', 123, 'Bar'),
            mock.call('bar.jpg', 123),
            mock.call('foobar.jpg', )
        ])
        self.mock_done_message.assert_not_called()

    def test_output_country_report_max_images(self):
        max_images = 2

        expected_cmt = (
            'Images without an id: 2 (gallery maximum reached), '
            'total of images without id: 3')
        expected_output = (
            '<gallery>\n'
            '<formatted row>\n'
            '<formatted row>\n'
            '</gallery>\n'
            '<!-- Maximum number of images reached: 2, '
            'total of images without id: 3 -->')

        images_of_monuments_without_id.output_country_report(
            self.rows, self.mock_report_page, max_images=max_images)
        self.bundled_asserts(
            expected_cmt,
            expected_output)
        self.mock_format_gallery_row.assert_has_calls([
            mock.call('foo.jpg', 123, 'Bar'),
            mock.call('bar.jpg', 123)
        ])
        self.mock_done_message.assert_not_called()


class TestMakeStatistics(TestCreateReportTableBase):

    """Test the make_statistics method."""

    def setUp(self):
        self.class_name = 'erfgoedbot.images_of_monuments_without_id'
        super(TestMakeStatistics, self).setUp()

        self.commons = self.mock_site.return_value
        self.mock_report_page = mock.MagicMock()
        self.mock_report_page.title.return_value = '<report_page>'

        self.config = {
            'country': 'foo',
            'lang': 'en',
            'commonsTemplate': 'commons template'
        }

        self.comment = (
            'Updating images without id statistics. Total of {total_with_id} '
            'images with suggested ids and {total_without_id} without.')
        self.pagename = ('Commons:Monuments database/'
                         'Images without id/Statistics')

    def bundled_asserts(self, expected_rows,
                        expected_total_with_id,
                        expected_total_without_id):
        """The full battery of asserts to do for each test."""
        expected_text = self.prefix + expected_rows + self.postfix

        self.mock_site.assert_called_once_with('commons', 'commons')
        self.mock_page.assert_called_once_with(
            self.mock_site.return_value, self.pagename)
        self.mock_save_to_wiki_or_local.assert_called_once_with(
            self.mock_page.return_value,
            self.comment.format(
                total_with_id=expected_total_with_id,
                total_without_id=expected_total_without_id),
            expected_text
        )
        self.mock_table_header_row.assert_called_once()
        self.mock_table_bottom_row.assert_called_once_with(
            6, {2: expected_total_with_id, 3: expected_total_without_id})

    def test_make_statistics_single_complete(self):
        totals = {
            'added': 123,
            'with_id': 456,
            'without_id': 789
        }
        statistics = [{
            'config': self.config,
            'report_page': self.mock_report_page,
            'totals': totals
        }]

        expected_rows = (
            '|-\n'
            '| foo \n'
            '| en \n'
            '| 456 \n'
            '| 789 \n'
            '| <report_page> \n'
            '| {{tl|commons template}} \n')
        expected_total_with_id = 456
        expected_total_without_id = 789

        images_of_monuments_without_id.make_statistics(statistics)
        self.bundled_asserts(
            expected_rows,
            expected_total_with_id,
            expected_total_without_id)

    def test_make_statistics_single_sparql_basic(self):
        totals = {
            'added': 123,
            'with_id': 456,
            'without_id': 789
        }
        self.config['type'] = 'sparql'
        statistics = [{
            'config': self.config,
            'report_page': self.mock_report_page,
            'totals': totals
        }]

        expected_rows = (
            '|-\n'
            '| foo \n'
            '| en \n'
            '| 456 \n'
            '| 789 \n'
            '| <report_page> \n'
            '| {{tl|commons template}} \n')
        expected_total_with_id = 456
        expected_total_without_id = 789

        images_of_monuments_without_id.make_statistics(statistics)
        self.bundled_asserts(
            expected_rows,
            expected_total_with_id,
            expected_total_without_id)

    def test_make_statistics_basic_skipped(self):
        statistics = [{
            'config': self.config,
            'report_page': self.mock_report_page,
            'cmt': 'skipped: due to foo'
        }]

        expected_rows = (
            '|-\n'
            '| foo \n'
            '| en \n'
            '| skipped: due to foo \n'
            '| --- \n'
            '| <report_page> \n'
            '| {{tl|commons template}} \n')
        expected_total_with_id = 0
        expected_total_without_id = 0

        images_of_monuments_without_id.make_statistics(statistics)
        self.bundled_asserts(
            expected_rows,
            expected_total_with_id,
            expected_total_without_id)

    def test_make_statistics_skipped_no_report_or_template(self):
        self.config.pop('commonsTemplate')
        statistics = [{
            'config': self.config,
            'cmt': 'skipped: due to foo'
        }]

        expected_rows = (
            '|-\n'
            '| foo \n'
            '| en \n'
            '| skipped: due to foo \n'
            '| --- \n'
            '| --- \n'
            '| --- \n')
        expected_total_with_id = 0
        expected_total_without_id = 0

        images_of_monuments_without_id.make_statistics(statistics)
        self.bundled_asserts(
            expected_rows,
            expected_total_with_id,
            expected_total_without_id)

    def test_make_statistics_skipped_none_report(self):
        statistics = [{
            'config': self.config,
            'report_page': None,
            'cmt': 'skipped: due to foo'
        }]

        expected_rows = (
            '|-\n'
            '| foo \n'
            '| en \n'
            '| skipped: due to foo \n'
            '| --- \n'
            '| --- \n'
            '| {{tl|commons template}} \n')
        expected_total_with_id = 0
        expected_total_without_id = 0

        images_of_monuments_without_id.make_statistics(statistics)
        self.bundled_asserts(
            expected_rows,
            expected_total_with_id,
            expected_total_without_id)

    def test_make_statistics_multiple_complete(self):
        report_page_1 = mock.MagicMock()
        report_page_1.title.return_value = '<report_page:Foobar>'
        report_page_2 = mock.MagicMock()
        report_page_2.title.return_value = '<report_page:Barfoo>'
        config_2 = {
            'country': 'bar',
            'lang': 'fr',
            'commonsTemplate': 'another template'
        }
        statistics = [
            {
                'config': self.config,
                'report_page': report_page_1,
                'totals': {
                    'added': 1,
                    'with_id': 2,
                    'without_id': 3}
            },
            {
                'config': config_2,
                'report_page': report_page_2,
                'totals': {
                    'added': 4,
                    'with_id': 5,
                    'without_id': 6}
            }
        ]

        expected_rows = (
            '|-\n'
            '| foo \n'
            '| en \n'
            '| 2 \n'
            '| 3 \n'
            '| <report_page:Foobar> \n'
            '| {{tl|commons template}} \n'
            '|-\n'
            '| bar \n'
            '| fr \n'
            '| 5 \n'
            '| 6 \n'
            '| <report_page:Barfoo> \n'
            '| {{tl|another template}} \n')
        expected_total_with_id = 7
        expected_total_without_id = 9

        images_of_monuments_without_id.make_statistics(statistics)
        self.bundled_asserts(
            expected_rows,
            expected_total_with_id,
            expected_total_without_id)

    def test_make_statistics_multiple_mixed(self):
        config_2 = {
            'country': 'bar',
            'lang': 'fr',
        }
        statistics = [
            {
                'config': self.config,
                'report_page': self.mock_report_page,
                'totals': {
                    'added': 1,
                    'with_id': 2,
                    'without_id': 3}
            },
            {
                'config': config_2,
                'cmt': 'skipped: due to foo'
            }
        ]

        expected_rows = (
            '|-\n'
            '| foo \n'
            '| en \n'
            '| 2 \n'
            '| 3 \n'
            '| <report_page> \n'
            '| {{tl|commons template}} \n'
            '|-\n'
            '| bar \n'
            '| fr \n'
            '| skipped: due to foo \n'
            '| --- \n'
            '| --- \n'
            '| --- \n')
        expected_total_with_id = 2
        expected_total_without_id = 3

        images_of_monuments_without_id.make_statistics(statistics)
        self.bundled_asserts(
            expected_rows,
            expected_total_with_id,
            expected_total_without_id)
