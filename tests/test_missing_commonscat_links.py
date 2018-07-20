#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Unit tests for missing_commonscat_links."""

import unittest

import mock

from erfgoedbot import missing_commonscat_links


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
