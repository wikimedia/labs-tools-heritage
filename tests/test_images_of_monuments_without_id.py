#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Unit tests for images_of_monuments_without_id."""
import unittest

import mock

from erfgoedbot import images_of_monuments_without_id
from report_base_test import TestCreateReportBase


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
        self.comment = u'Images without an id'

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

        # autospec does not support assert_not_called
        patcher = mock.patch(
            'erfgoedbot.images_of_monuments_without_id.addCommonsTemplate')
        self.mock_add_commons_template = patcher.start()
        self.mock_add_commons_template.return_value = False
        self.addCleanup(patcher.stop)

    def bundled_asserts_outputted(self, result, expected_text):
        self.assertIsNone(result)
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
        self.mock_save_to_wiki_or_local.assert_called_once_with(
            self.mock_page.return_value, self.comment, expected_text,
            minorEdit=False)

    def bundled_asserts_skipped(self, result):
        self.assertFalse(result)
        self.mock_get_monuments_with_photo.assert_not_called()
        self.mock_get_monuments_with_template.assert_not_called()
        self.mock_get_monuments_without_template.assert_not_called()
        self.mock_site.assert_not_called()
        self.mock_page.assert_not_called()
        self.mock_add_commons_template.assert_not_called()
        self.mock_save_to_wiki_or_local.assert_not_called()

    def test_processCountry_skip_on_no_commons_template(self):
        self.countryconfig.pop('commonsTemplate')
        result = images_of_monuments_without_id.processCountry(
            self.countryconfig, self.add_template,
            'conn', 'cursor', 'conn2', 'cursor2')
        self.bundled_asserts_skipped(result)

    def test_processCountry_skip_on_no_commons_tracker_category(self):
        self.countryconfig.pop('commonsTrackerCategory')
        result = images_of_monuments_without_id.processCountry(
            self.countryconfig, self.add_template,
            'conn', 'cursor', 'conn2', 'cursor2')
        self.bundled_asserts_skipped(result)

    def test_processCountry_skip_on_no_allowed_output(self):
        self.countryconfig.pop('imagesWithoutIdPage')
        self.add_template = False
        result = images_of_monuments_without_id.processCountry(
            self.countryconfig, self.add_template,
            'conn', 'cursor', 'conn2', 'cursor2')
        self.bundled_asserts_skipped(result)

    def test_processCountry_output_empty(self):
        expected_text = (
            u'<gallery>\n'
            u'\n'
            u'</gallery>'
        )
        result = images_of_monuments_without_id.processCountry(
            self.countryconfig, self.add_template,
            'conn', 'cursor', 'conn2', 'cursor2')

        self.bundled_asserts_outputted(result, expected_text)
        self.mock_add_commons_template.assert_not_called()

    def test_processCountry_output_without_template(self):
        self.mock_get_monuments_without_template.return_value = ['Bar.jpg']
        expected_text = (
            u'<gallery>\n'
            u'File:Bar.jpg\n'
            u'</gallery>'
        )
        result = images_of_monuments_without_id.processCountry(
            self.countryconfig, self.add_template,
            'conn', 'cursor', 'conn2', 'cursor2')

        self.bundled_asserts_outputted(result, expected_text)
        self.mock_add_commons_template.assert_not_called()

    def test_processCountry_output_with_photo(self):
        self.mock_get_monuments_with_photo.return_value = {'Foobar.jpg': 123}
        expected_text = (
            u'<gallery>\n'
            u'File:Foobar.jpg|<nowiki>{{A template|123}}</nowiki>\n'
            u'</gallery>'
        )
        result = images_of_monuments_without_id.processCountry(
            self.countryconfig, self.add_template,
            'conn', 'cursor', 'conn2', 'cursor2')

        self.bundled_asserts_outputted(result, expected_text)
        self.mock_add_commons_template.assert_called_once_with(
            'Foobar.jpg', 'A template', 123)

    def test_processCountry_output_with_photo_without_template_no_overlap(self):
        self.mock_get_monuments_with_photo.return_value = {
            'Foobar.jpg': 123}
        self.mock_get_monuments_without_template.return_value = ['Bar.jpg']
        self.mock_get_monuments_with_template.return_value = ['Foo.jpg']
        expected_text = (
            u'<gallery>\n'
            u'File:Bar.jpg\n'
            u'File:Foobar.jpg|<nowiki>{{A template|123}}</nowiki>\n'
            u'</gallery>'
        )
        result = images_of_monuments_without_id.processCountry(
            self.countryconfig, self.add_template,
            'conn', 'cursor', 'conn2', 'cursor2')

        self.bundled_asserts_outputted(result, expected_text)
        self.mock_add_commons_template.assert_called_once_with(
            'Foobar.jpg', 'A template', 123)

    def test_processCountry_output_no_duplication(self):
        self.mock_get_monuments_with_photo.return_value = {'Bar.jpg': 456}
        self.mock_get_monuments_without_template.return_value = ['Bar.jpg']
        expected_text = (
            u'<gallery>\n'
            u'File:Bar.jpg|<nowiki>{{A template|456}}</nowiki>\n'
            u'</gallery>'
        )
        result = images_of_monuments_without_id.processCountry(
            self.countryconfig, self.add_template,
            'conn', 'cursor', 'conn2', 'cursor2')

        self.bundled_asserts_outputted(result, expected_text)
        self.mock_add_commons_template.assert_called_once_with(
            'Bar.jpg', 'A template', 456)

    def test_processCountry_no_output_without_target_page(self):
        self.countryconfig.pop('imagesWithoutIdPage')
        self.mock_get_monuments_with_photo.return_value = {
            'Foobar.jpg': 123}
        self.mock_get_monuments_without_template.return_value = ['Bar.jpg']
        self.mock_get_monuments_with_template.return_value = ['Foo.jpg']
        result = images_of_monuments_without_id.processCountry(
            self.countryconfig, self.add_template,
            'conn', 'cursor', 'conn2', 'cursor2')

        self.assertIsNone(result)
        self.mock_add_commons_template.assert_called_once_with(
            'Foobar.jpg', 'A template', 123)
        self.mock_get_monuments_with_photo.assert_called_once()
        self.mock_get_monuments_with_template.assert_called_once()
        self.mock_get_monuments_without_template.assert_called_once()
        self.mock_site.assert_not_called()
        self.mock_page.assert_not_called()
        self.mock_save_to_wiki_or_local.assert_not_called()

    def test_processCountry_output_with_template(self):
        self.mock_get_monuments_with_photo.return_value = {'Foo.jpg': 789}
        self.mock_get_monuments_with_template.return_value = ['Foo.jpg']
        expected_text = (
            u'<gallery>\n'
            u'\n'
            u'</gallery>'
        )
        result = images_of_monuments_without_id.processCountry(
            self.countryconfig, self.add_template,
            'conn', 'cursor', 'conn2', 'cursor2')

        self.bundled_asserts_outputted(result, expected_text)
        self.mock_add_commons_template.assert_not_called()

    def test_processCountry_output_template_added(self):
        self.mock_get_monuments_with_photo.return_value = {
            'Foobar.jpg': 123,
            'Bar.jpg': 456}
        self.mock_get_monuments_without_template.return_value = ['Bar.jpg']
        self.mock_add_commons_template.return_value = True
        expected_text = (
            u'<gallery>\n'
            u'\n'
            u'</gallery>'
        )
        result = images_of_monuments_without_id.processCountry(
            self.countryconfig, self.add_template,
            'conn', 'cursor', 'conn2', 'cursor2')

        self.bundled_asserts_outputted(result, expected_text)
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
        expected_text = (
            u'<gallery>\n'
            u'File:Bar.jpg|<nowiki>{{A template|456}}</nowiki>\n'
            u'File:Foobar.jpg|<nowiki>{{A template|123}}</nowiki>\n'
            u'</gallery>'
        )

        result = images_of_monuments_without_id.processCountry(
            self.countryconfig, self.add_template,
            'conn', 'cursor', 'conn2', 'cursor2')
        self.bundled_asserts_outputted(result, expected_text)
        self.mock_add_commons_template.assert_not_called()


class TestFormatGalleryRow(unittest.TestCase):

    """Test the format_gallery_row method."""

    def test_format_gallery_row_image(self):
        image = 'Foo.jpg'
        self.assertEqual(
            u'File:Foo.jpg',
            images_of_monuments_without_id.format_gallery_row(image)
        )

    def test_format_gallery_row_id(self):
        image = 'Foo.jpg'
        id = 123
        self.assertEqual(
            u'File:Foo.jpg|123',
            images_of_monuments_without_id.format_gallery_row(image, id)
        )

    def test_format_gallery_row_template(self):
        image = 'Foo.jpg'
        id = 123
        template = 'Bar'
        self.assertEqual(
            u'File:Foo.jpg|<nowiki>{{Bar|123}}</nowiki>',
            images_of_monuments_without_id.format_gallery_row(
                image, id, template)
        )


class TestAddCommonsTemplate(unittest.TestCase):

    """Test the addCommonsTemplate method."""

    def setUp(self):
        self.identifier = 123
        self.image = 'Foo.jpg'
        self.page_templates = ['Pre-existing Template']
        self.comment = u'Adding template {0} based on usage in list'

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
            'erfgoedbot.images_of_monuments_without_id.pywikibot.ImagePage',
            autospec=True)
        self.mock_page = patcher.start()
        self.image_page = self.mock_page.return_value
        self.addCleanup(patcher.stop)

        self.image_page.exists.return_value = True
        self.image_page.isRedirectPage.return_value = False
        self.image_page.isEmpty.return_value = False
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
        expected_text = u'{{A new template|123}}\n<page contents>'
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

    def test_addCommonsTemplate_skip_on_empty(self):
        self.image_page.isEmpty.return_value = True
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

        # autospec does not support assert_not_called
        patcher = mock.patch(
            'erfgoedbot.images_of_monuments_without_id.format_gallery_row')
        self.mock_format_gallery_row = patcher.start()
        self.mock_format_gallery_row.return_value = '<formatted row>'
        self.addCleanup(patcher.stop)

    def bundled_asserts(self, expected_cmt, expected_output):
        """The full battery of asserts to do for each test."""

        self.mock_save_to_wiki_or_local.assert_called_once_with(
            self.mock_report_page,
            expected_cmt,
            expected_output,
            minorEdit=False
        )

    def test_output_country_report_empty(self):
        expected_cmt = u'Images without an id'
        expected_output = (
            u'<gallery>\n'
            u'\n'
            u'</gallery>')

        images_of_monuments_without_id.output_country_report(
            [], self.mock_report_page)
        self.bundled_asserts(
            expected_cmt,
            expected_output)
        self.mock_format_gallery_row.assert_not_called()

    def test_output_country_report_complete(self):
        expected_cmt = u'Images without an id'
        expected_output = (
            u'<gallery>\n'
            u'<formatted row>\n'
            u'<formatted row>\n'
            u'<formatted row>\n'
            u'</gallery>')

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
