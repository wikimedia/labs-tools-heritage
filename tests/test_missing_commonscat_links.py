#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Unit tests for missing_commonscat_links."""
import unittest
from collections import OrderedDict

import mock

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
        expected = u'[[sv:foobar]]\n'
        result = missing_commonscat_links.getInterwikisMissingCommonscatPage(
            'se', 'fr')
        self.assertEquals(result, expected)

    def test_get_interwikis_missing_commonscat_page_no_hit(self):
        expected = u''
        result = missing_commonscat_links.getInterwikisMissingCommonscatPage(
            'fr', 'fr')
        self.assertEquals(result, expected)

    def test_get_interwikis_missing_commonscat_page_same_lang(self):
        expected = u''
        result = missing_commonscat_links.getInterwikisMissingCommonscatPage(
            'se', 'sv')
        self.assertEquals(result, expected)

    def test_get_interwikis_missing_commonscat_page_no_commonscat(self):
        self.mock_mconfig.countries = {('se', 'sv'): {'foo': 'bar'}}
        expected = u''
        result = missing_commonscat_links.getInterwikisMissingCommonscatPage(
            'se', 'fr')
        self.assertEquals(result, expected)


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
            u'Updating missing commonscat links statistics. '
            u'Total missing links: {total_cats}')
        self.pagename = u'Commons:Monuments database/Missing commonscat links/Statistics'

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
            'code': 'foo',
            'lang': 'en',
            'config': {
                'rowTemplate': 'row template',
                'commonsTemplate': 'commons template'},
            'report_page': self.mock_report_page,
            'total_cats': 123
        }]

        expected_rows = (
            u'|-\n'
            u'| foo \n'
            u'| en \n'
            u'| 123 \n'
            u'| <report_page> \n'
            u'| <row_template_link> \n'
            u'| {{tl|commons template}} \n')
        expected_total_cats = 123

        missing_commonscat_links.makeStatistics(statistics)
        self.mock_get_template_link.assert_called_once_with(
            'en', 'wikipedia', 'row template', self.commons)
        self.bundled_asserts(expected_rows, expected_total_cats)

    def test_make_statistics_single_basic(self):
        statistics = [{
            'code': 'foo',
            'lang': 'en',
            'config': {'rowTemplate': 'row template'},
            'total_cats': 123
        }]

        expected_rows = (
            u'|-\n'
            u'| foo \n'
            u'| en \n'
            u'| 123 \n'
            u'| --- \n'
            u'| <row_template_link> \n'
            u'| --- \n')
        expected_total_cats = 123

        missing_commonscat_links.makeStatistics(statistics)
        self.mock_get_template_link.assert_called_once_with(
            'en', 'wikipedia', 'row template', self.commons)
        self.bundled_asserts(expected_rows, expected_total_cats)

    def test_make_statistics_single_sparql_basic(self):
        statistics = [{
            'code': 'foo',
            'lang': 'en',
            'config': {'type': 'sparql'},
            'cmt': 'skipped: cannot handle sparql'
        }]

        expected_rows = (
            u'|-\n'
            u'| foo \n'
            u'| en \n'
            u'| skipped: cannot handle sparql \n'
            u'| --- \n'
            u'| --- \n'
            u'| --- \n')
        expected_total_cats = 0

        missing_commonscat_links.makeStatistics(statistics)
        self.mock_get_template_link.assert_not_called()
        self.bundled_asserts(expected_rows, expected_total_cats)

    def test_make_statistics_basic_skipped(self):
        statistics = [{
            'code': 'foo',
            'lang': 'en',
            'config': {'rowTemplate': 'a template'},
            'cmt': 'skipped: no missingCommonscatPage'
        }]

        expected_rows = (
            u'|-\n'
            u'| foo \n'
            u'| en \n'
            u'| skipped: no missingCommonscatPage \n'
            u'| --- \n'
            u'| <row_template_link> \n'
            u'| --- \n')
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
                'code': 'foo',
                'lang': 'en',
                'config': {
                    'rowTemplate': 'row template',
                    'commonsTemplate': 'commons template',
                    'project': 'wikipedia'},
                'report_page': report_page_1,
                'total_cats': 2
            },
            {
                'code': 'bar',
                'lang': 'fr',
                'config': {
                    'rowTemplate': 'a template',
                    'project': 'wikisource'},
                'report_page': report_page_2,
                'total_cats': 3
            }
        ]

        expected_rows = (
            u'|-\n'
            u'| foo \n'
            u'| en \n'
            u'| 2 \n'
            u'| <report_page:Foobar> \n'
            u'| <row_template_link> \n'
            u'| {{tl|commons template}} \n'
            u'|-\n'
            u'| bar \n'
            u'| fr \n'
            u'| 3 \n'
            u'| <report_page:Barfoo> \n'
            u'| <row_template_link> \n'
            u'| --- \n')
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
                'code': 'foo',
                'lang': 'en',
                'config': {
                    'rowTemplate': 'row template',
                    'commonsTemplate': 'commons template'},
                'report_page': self.mock_report_page,
                'total_cats': 2
            },
            {
                'code': 'bar',
                'lang': 'fr',
                'config': {'rowTemplate': 'a template'},
                'cmt': 'skipped: no missingCommonscatPage'
            }
        ]

        expected_rows = (
            u'|-\n'
            u'| foo \n'
            u'| en \n'
            u'| 2 \n'
            u'| <report_page> \n'
            u'| <row_template_link> \n'
            u'| {{tl|commons template}} \n'
            u'|-\n'
            u'| bar \n'
            u'| fr \n'
            u'| skipped: no missingCommonscatPage \n'
            u'| --- \n'
            u'| <row_template_link> \n'
            u'| --- \n')
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
        expected_cmt = u'Commonscat links to be made in monument lists: 3'
        expected_output = (
            u'=== source_link_1 ===\n'
            u'* <nowiki>|</nowiki> cf = [[:c:Category:Cat_11|Cat 11]] - id_1\n'
            u'* <nowiki>|</nowiki> cf = [[:c:Category:Cat_12|Cat 12]] - id_2\n'
            u'=== source_link_2 ===\n'
            u'* <nowiki>|</nowiki> cf = [[:c:Category:Cat_21|Cat 21]] - id_3\n'
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
            u'Commonscat links to be made in monument lists: 2 (list maximum '
            u'reached), total of missing commonscat links: 3')
        expected_output = (
            u'=== source_link_1 ===\n'
            u'* <nowiki>|</nowiki> cf = [[:c:Category:Cat_11|Cat 11]] - id_1\n'
            u'* <nowiki>|</nowiki> cf = [[:c:Category:Cat_12|Cat 12]] - id_2\n'
            u'<!-- Maximum number of categories reached: 2, '
            u'total of missing commonscat links: 3 -->\n')
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
            u'Commonscat links to be made in monument lists: 1 (list maximum '
            u'reached), total of missing commonscat links: 3')
        expected_output = (
            u'=== source_link_1 ===\n'
            u'* <nowiki>|</nowiki> cf = [[:c:Category:Cat_11|Cat 11]] - id_1\n'
            u'* <nowiki>|</nowiki> cf = [[:c:Category:Cat_12|Cat 12]] - id_2\n'
            u'<!-- Maximum number of categories reached: 1, '
            u'total of missing commonscat links: 3 -->\n')
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

        expected_cmt = u'Commonscat links to be made in monument lists: 0'
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
            u'Commonscat links to be made in monument lists: 2 (list maximum '
            u'reached), total of missing commonscat links: 3')
        expected_output = (
            u'=== source_link_1 ===\n'
            u'* <nowiki>|</nowiki> cf = [[:c:Category:Cat_11|Cat 11]] - id_1\n'
            u'* <nowiki>|</nowiki> cf = [[:c:Category:Cat_12|Cat 12]] - id_2\n'
            u'<!-- Maximum number of categories reached: 2, '
            u'total of missing commonscat links: 3 -->\n'
            u'iw_links text')
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
            u'[[Dummy_page_A]]': [
                (u'Some Monument', u'ID_1'),
                (u'Some Other Monument', u'ID_2'),
            ],
            u'[[Dummy_page_B]]': [
                (u'Yet Another Monument', u'ID_3'),
            ]
        }

        result = missing_commonscat_links.group_missing_commonscat_by_source(
            commons_cats, without_commonscat, self.mock_mconfig)
        self.assertEqual(result, expected)
