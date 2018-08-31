# -*- coding: utf-8  -*-
"""Base class for testing report outputting."""
from __future__ import unicode_literals

import unittest

import mock


class TestCreateReportBase(unittest.TestCase):

        def setUp(self):
            patcher = mock.patch(
                '{}.common.save_to_wiki_or_local'.format(self.class_name),
                autospec=True)
            self.mock_save_to_wiki_or_local = patcher.start()
            self.addCleanup(patcher.stop)

            # silence logger
            patcher = mock.patch(
                '{}.pywikibot.debug'.format(self.class_name),
                autospec=True)
            self.mock_debug = patcher.start()
            self.addCleanup(patcher.stop)

            patcher = mock.patch(
                '{}.pywikibot.Site'.format(self.class_name), autospec=True)
            self.mock_site = patcher.start()
            self.addCleanup(patcher.stop)

            patcher = mock.patch(
                '{}.pywikibot.Page'.format(self.class_name), autospec=True)
            self.mock_page = patcher.start()
            self.addCleanup(patcher.stop)


class TestCreateReportTableBase(TestCreateReportBase):

        def setUp(self):
            super(TestCreateReportTableBase, self).setUp()

            self.prefix = 'prefix'
            self.postfix = 'postfix'

            patcher = mock.patch(
                'erfgoedbot.missing_commonscat_links.common.table_header_row')
            self.mock_table_header_row = patcher.start()
            self.mock_table_header_row.return_value = self.prefix
            self.addCleanup(patcher.stop)

            patcher = mock.patch(
                'erfgoedbot.missing_commonscat_links.common.table_bottom_row')
            self.mock_table_bottom_row = patcher.start()
            self.mock_table_bottom_row.return_value = self.postfix
            self.addCleanup(patcher.stop)
