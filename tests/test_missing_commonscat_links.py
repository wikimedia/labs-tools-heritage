#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Unit tests for missing_commonscat_links."""
import unittest
import unittest.mock as mock
from collections import OrderedDict

import custom_assertions  # noqa F401
from erfgoedbot import missing_commonscat_links
from report_base_test import TestCreateReportBase, TestCreateReportTableBase


class TestGetInterwikisMissingCommonscatPage(unittest.TestCase):

    """Test the getInterwikisMissingCommonscatPage method."""

    def setUp(self):
        patcher = mock.patch('erfgoedbot.missing_commonscat_links.mconfig')
        self.mock_mconfig = patcher.start()
        self.mock_mconfig.countries = {
            ('se', 'sv'): {'missingCommonscatPage': 'foobar'}
        }
        self.addCleanup(patcher.stop)

    def test_get_interwikis_missing_commonscat_page_hit(self):
        expected = '[[sv:foobar]]\n'
        result = missing_commonscat_links.getInterwikisMissingCommonscatPage(
            'se', 'fr')
        self.assertEqual(result, expected)

    def test_get_interwikis_missing_commonscat_page_no_hit(self):
        expected = ''
        result = missing_commonscat_links.getInterwikisMissingCommonscatPage(
            'fr', 'fr')
        self.assertEqual(result, expected)

    def test_get_interwikis_missing_commonscat_page_same_lang(self):
        expected = ''
        result = missing_commonscat_links.getInterwikisMissingCommonscatPage(
            'se', 'sv')
        self.assertEqual(result, expected)

    def test_get_interwikis_missing_commonscat_page_no_commonscat(self):
        self.mock_mconfig.countries = {('se', 'sv'): {'foo': 'bar'}}
        expected = ''
        result = missing_commonscat_links.getInterwikisMissingCommonscatPage(
            'se', 'fr')
        self.assertEqual(result, expected)


class TestMakeStatistics(TestCreateReportTableBase):

    """Test the makeStatistics method."""

    def setUp(self):
        self.class_name = 'erfgoedbot.missing_commonscat_links'
        super(TestMakeStatistics, self).setUp()

        patcher = mock.patch(
            'erfgoedbot.missing_commonscat_links.common.get_template_link')
        self.mock_get_template_link = patcher.start()
        self.mock_get_template_link.return_value = '<row_template_link>'
        self.addCleanup(patcher.stop)

        self.commons = self.mock_site.return_value
        self.mock_report_page = mock.MagicMock()
        self.mock_report_page.title.return_value = '<report_page>'

        self.comment = (
            'Updating missing commonscat links statistics. '
            'Total missing links: {total_cats}')
        self.pagename = 'Commons:Monuments database/Missing commonscat links/Statistics'

    def bundled_asserts(self, expected_rows, expected_total_cats):
        """The full battery of asserts to do for each test."""
        expected_text = self.prefix + expected_rows + self.postfix

        self.mock_site.assert_called_once_with('commons', 'commons')
        self.mock_page.assert_called_once_with(
            self.mock_site.return_value, self.pagename)
        self.mock_save_to_wiki_or_local.assert_called_once_with(
            self.mock_page.return_value,
            self.comment.format(total_cats=expected_total_cats),
            expected_text
        )
        self.mock_table_header_row.assert_called_once()
        self.mock_table_bottom_row.assert_called_once_with(
            6, {2: expected_total_cats})

    def test_make_statistics_single_complete(self):
        statistics = [{
            'config': {
                'country': 'foo',
                'lang': 'en',
                'rowTemplate': 'row template',
                'commonsTemplate': 'commons template'},
            'report_page': self.mock_report_page,
            'total_cats': 123
        }]

        expected_rows = (
            '|-\n'
            '| foo \n'
            '| en \n'
            '| 123 \n'
            '| <report_page> \n'
            '| <row_template_link> \n'
            '| {{tl|commons template}} \n')
        expected_total_cats = 123

        missing_commonscat_links.makeStatistics(statistics)
        self.mock_get_template_link.assert_called_once_with(
            'en', 'wikipedia', 'row template', self.commons)
        self.bundled_asserts(expected_rows, expected_total_cats)

    def test_make_statistics_single_basic(self):
        statistics = [{
            'config': {
                'country': 'foo',
                'lang': 'en',
                'rowTemplate': 'row template'},
            'total_cats': 123
        }]

        expected_rows = (
            '|-\n'
            '| foo \n'
            '| en \n'
            '| 123 \n'
            '| --- \n'
            '| <row_template_link> \n'
            '| --- \n')
        expected_total_cats = 123

        missing_commonscat_links.makeStatistics(statistics)
        self.mock_get_template_link.assert_called_once_with(
            'en', 'wikipedia', 'row template', self.commons)
        self.bundled_asserts(expected_rows, expected_total_cats)

    def test_make_statistics_single_sparql_basic(self):
        statistics = [{
            'config': {
                'country': 'foo',
                'lang': 'en',
                'type': 'sparql'},
            'cmt': 'skipped: cannot handle sparql'
        }]

        expected_rows = (
            '|-\n'
            '| foo \n'
            '| en \n'
            '| skipped: cannot handle sparql \n'
            '| --- \n'
            '| --- \n'
            '| --- \n')
        expected_total_cats = 0

        missing_commonscat_links.makeStatistics(statistics)
        self.mock_get_template_link.assert_not_called()
        self.bundled_asserts(expected_rows, expected_total_cats)

    def test_make_statistics_basic_skipped(self):
        statistics = [{
            'config': {
                'country': 'foo',
                'lang': 'en',
                'rowTemplate': 'a template'},
            'cmt': 'skipped: no missingCommonscatPage'
        }]

        expected_rows = (
            '|-\n'
            '| foo \n'
            '| en \n'
            '| skipped: no missingCommonscatPage \n'
            '| --- \n'
            '| <row_template_link> \n'
            '| --- \n')
        expected_total_cats = 0

        missing_commonscat_links.makeStatistics(statistics)
        self.mock_get_template_link.assert_called_once_with(
            'en', 'wikipedia', 'a template', self.commons)
        self.bundled_asserts(expected_rows, expected_total_cats)

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
                'total_cats': 2
            },
            {
                'config': {
                    'country': 'bar',
                    'lang': 'fr',
                    'rowTemplate': 'a template',
                    'project': 'wikisource'},
                'report_page': report_page_2,
                'total_cats': 3
            }
        ]

        expected_rows = (
            '|-\n'
            '| bar \n'
            '| fr \n'
            '| 3 \n'
            '| <report_page:Barfoo> \n'
            '| <row_template_link> \n'
            '| --- \n'
            '|-\n'
            '| foo \n'
            '| en \n'
            '| 2 \n'
            '| <report_page:Foobar> \n'
            '| <row_template_link> \n'
            '| {{tl|commons template}} \n')
        expected_total_cats = 5

        missing_commonscat_links.makeStatistics(statistics)
        self.mock_get_template_link.assert_has_calls([
            mock.call('en', 'wikipedia', 'row template', self.commons),
            mock.call('fr', 'wikisource', 'a template', self.commons),
        ])
        self.bundled_asserts(expected_rows, expected_total_cats)

    def test_make_statistics_multiple_mixed(self):
        statistics = [
            {
                'config': {
                    'country': 'foo',
                    'lang': 'en',
                    'rowTemplate': 'row template',
                    'commonsTemplate': 'commons template'},
                'report_page': self.mock_report_page,
                'total_cats': 2
            },
            {
                'config': {
                    'country': 'bar',
                    'lang': 'fr',
                    'rowTemplate': 'a template'},
                'cmt': 'skipped: no missingCommonscatPage'
            }
        ]

        expected_rows = (
            '|-\n'
            '| bar \n'
            '| fr \n'
            '| skipped: no missingCommonscatPage \n'
            '| --- \n'
            '| <row_template_link> \n'
            '| --- \n'
            '|-\n'
            '| foo \n'
            '| en \n'
            '| 2 \n'
            '| <report_page> \n'
            '| <row_template_link> \n'
            '| {{tl|commons template}} \n')
        expected_total_cats = 2

        missing_commonscat_links.makeStatistics(statistics)
        self.mock_get_template_link.assert_has_calls([
            mock.call('en', 'wikipedia', 'row template', self.commons),
            mock.call('fr', 'wikipedia', 'a template', self.commons),
        ])
        self.bundled_asserts(expected_rows, expected_total_cats)


class TestOutputCountryReport(TestCreateReportBase):

    """Test the output_country_report method."""

    def setUp(self):
        self.class_name = 'erfgoedbot.missing_commonscat_links'
        super(TestOutputCountryReport, self).setUp()
        self.mock_report_page = self.mock_page.return_value

        self.prefix = 'prefix'
        patcher = mock.patch(
            'erfgoedbot.missing_commonscat_links.common.instruction_header')
        self.mock_instruction_header = patcher.start()
        self.mock_instruction_header.return_value = self.prefix
        self.addCleanup(patcher.stop)

        patcher = mock.patch(
            'erfgoedbot.missing_commonscat_links.common.done_message')
        self.mock_done_message = patcher.start()
        self.addCleanup(patcher.stop)

        self.field_name = 'cf'

        self.missing_cats = OrderedDict()
        self.missing_cats['source_link_1'] = [
            ('Cat_11', 'id_1'),
            ('Cat_12', 'id_2')
        ]
        self.missing_cats['source_link_2'] = [
            ('Cat_21', 'id_3')
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
            expected_output
        )
        self.mock_instruction_header.assert_called_once()

    def test_output_country_report_complete(self):
        expected_cmt = 'Commonscat links to be made in monument lists: 3'
        expected_output = (
            '=== source_link_1 ===\n'
            '* <nowiki>|</nowiki> cf = [[:c:Category:Cat_11|Cat 11]] - id_1\n'
            '* <nowiki>|</nowiki> cf = [[:c:Category:Cat_12|Cat 12]] - id_2\n'
            '=== source_link_2 ===\n'
            '* <nowiki>|</nowiki> cf = [[:c:Category:Cat_21|Cat 21]] - id_3\n'
        )
        expected_totals = {
            'cats': 3,
            'pages': 2
        }

        result = missing_commonscat_links.output_country_report(
            self.missing_cats, self.field_name, self.mock_report_page)
        self.bundled_asserts(
            result,
            expected_cmt,
            expected_totals,
            expected_output)

    def test_output_country_report_max_cats(self):
        max_cats = 2

        expected_cmt = (
            'Commonscat links to be made in monument lists: 2 (list maximum '
            'reached), total of missing commonscat links: 3')
        expected_output = (
            '=== source_link_1 ===\n'
            '* <nowiki>|</nowiki> cf = [[:c:Category:Cat_11|Cat 11]] - id_1\n'
            '* <nowiki>|</nowiki> cf = [[:c:Category:Cat_12|Cat 12]] - id_2\n'
            '<!-- Maximum number of categories reached: 2, '
            'total of missing commonscat links: 3 -->\n')
        expected_totals = {
            'cats': 3,
            'pages': 2
        }

        result = missing_commonscat_links.output_country_report(
            self.missing_cats, self.field_name, self.mock_report_page,
            max_cats=max_cats)
        self.bundled_asserts(
            result,
            expected_cmt,
            expected_totals,
            expected_output)

    def test_output_country_report_max_images_all_candidates(self):
        max_cats = 1

        expected_cmt = (
            'Commonscat links to be made in monument lists: 1 (list maximum '
            'reached), total of missing commonscat links: 3')
        expected_output = (
            '=== source_link_1 ===\n'
            '* <nowiki>|</nowiki> cf = [[:c:Category:Cat_11|Cat 11]] - id_1\n'
            '* <nowiki>|</nowiki> cf = [[:c:Category:Cat_12|Cat 12]] - id_2\n'
            '<!-- Maximum number of categories reached: 1, '
            'total of missing commonscat links: 3 -->\n')
        expected_totals = {
            'cats': 3,
            'pages': 2
        }

        result = missing_commonscat_links.output_country_report(
            self.missing_cats, self.field_name, self.mock_report_page,
            max_cats=max_cats)
        self.bundled_asserts(
            result,
            expected_cmt,
            expected_totals,
            expected_output)

    def test_output_country_report_no_images(self):
        self.missing_cats = {}

        expected_cmt = 'Commonscat links to be made in monument lists: 0'
        expected_output = self.mock_done_message.return_value
        expected_totals = {
            'cats': 0,
            'pages': 0
        }

        result = missing_commonscat_links.output_country_report(
            self.missing_cats, self.field_name, self.mock_report_page)
        self.mock_done_message.assert_called_once()
        self.bundled_asserts(
            result,
            expected_cmt,
            expected_totals,
            expected_output)

    def test_output_country_report_with_iw_links(self):
        max_cats = 2

        expected_cmt = (
            'Commonscat links to be made in monument lists: 2 (list maximum '
            'reached), total of missing commonscat links: 3')
        expected_output = (
            '=== source_link_1 ===\n'
            '* <nowiki>|</nowiki> cf = [[:c:Category:Cat_11|Cat 11]] - id_1\n'
            '* <nowiki>|</nowiki> cf = [[:c:Category:Cat_12|Cat 12]] - id_2\n'
            '<!-- Maximum number of categories reached: 2, '
            'total of missing commonscat links: 3 -->\n'
            'iw_links text')
        expected_totals = {
            'cats': 3,
            'pages': 2
        }

        result = missing_commonscat_links.output_country_report(
            self.missing_cats, self.field_name, self.mock_report_page,
            max_cats=max_cats, iw_links='iw_links text')
        self.bundled_asserts(
            result,
            expected_cmt,
            expected_totals,
            expected_output)


class TestGroupMissingCommonscatBySource(unittest.TestCase):

    """Test the group_missing_commonscat_by_source method."""

    def setUp(self):
        super(TestGroupMissingCommonscatBySource, self).setUp()
        patcher = mock.patch('erfgoedbot.missing_commonscat_links.mconfig')
        self.mock_mconfig = patcher.start()
        self.mock_mconfig.countries = {
            ('se', 'sv'): {'missingCommonscatPage': 'foobar'}
        }
        self.addCleanup(patcher.stop)

    def test_group_missing_commonscat_by_source_empty(self):
        result = missing_commonscat_links.group_missing_commonscat_by_source(
            {}, {}, self.mock_mconfig)
        self.assertEqual(result, {})

    def test_group_missing_commonscat_by_source(self):
        # group_missing_commonscat_by_source(commonscats, withoutCommonscat,
        #                                countryconfig)
        commons_cats = {
            'ID_1': 'Some Monument',
            'ID_2': 'Some Other Monument',
            'ID_3': 'Yet Another Monument',
        }
        without_commonscat = {
            'ID_1': '//de.wikipedia.org/w/index.php?title=Dummy_page_A&oldid=12345',
            'ID_2': '//de.wikipedia.org/w/index.php?title=Dummy_page_A&oldid=12345',
            'ID_3': '//de.wikipedia.org/w/index.php?title=Dummy_page_B&oldid=12345',
        }
        expected = {
            '[[Dummy_page_A]]': [
                ('Some Monument', 'ID_1'),
                ('Some Other Monument', 'ID_2'),
            ],
            '[[Dummy_page_B]]': [
                ('Yet Another Monument', 'ID_3'),
            ]
        }

        result = missing_commonscat_links.group_missing_commonscat_by_source(
            commons_cats, without_commonscat, self.mock_mconfig)
        self.assertEqual(result, expected)
