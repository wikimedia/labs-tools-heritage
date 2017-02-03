"""Unit tests for update_database."""

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
