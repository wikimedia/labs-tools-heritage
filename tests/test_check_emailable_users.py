#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Unit tests for check_emailable_users."""
import unittest

import mock
from freezegun import freeze_time

from erfgoedbot import check_emailable_users


class TestGetUsernamesFromDatabase(unittest.TestCase):

    def setUp(self):
        self.mock_cursor_commons = mock.Mock()
        self.mock_cursor_commons.fetchall.return_value = [('A',), ('B',)]
        patcher = mock.patch('erfgoedbot.check_emailable_users.connect_to_commons_database')
        mock_connect_to_commons_database = patcher.start()
        mock_connect_to_commons_database.return_value = (None, self.mock_cursor_commons)
        self.addCleanup(patcher.stop)
        self.expected_query = (
            u"SELECT"
            u" user.user_name as uploader"
            u" FROM (SELECT"
            u"   cl_to,"
            u"   cl_from"
            u"   FROM categorylinks"
            u"   WHERE cl_to = %s AND cl_type = 'file') cats"
            u" INNER JOIN page ON cl_from = page_id"
            u" INNER JOIN image ON page_title = img_name"
            u" LEFT JOIN actor ON actor.actor_id = image.img_actor"
            u" LEFT JOIN user ON user.user_id = actor.actor_user"
            u" WHERE img_timestamp BETWEEN %s AND %s"
            u" GROUP BY uploader"
        )

    @freeze_time("2018-09-14 03:21:34")
    def test_get_usernames_with_default_delta(self):
        result = check_emailable_users.get_usernames_from_database(None, self.mock_cursor_commons, "Some_category")
        expected_query_params = ('Some_category', '20180914012134', '20180914032134')
        self.mock_cursor_commons.execute.assert_called_once_with(self.expected_query, expected_query_params)
        self.mock_cursor_commons.fetchall.assert_called_once_with()
        self.assertEquals(result, ['A', 'B'])

    @freeze_time("2018-09-14 03:21:34")
    def test_get_usernames_with_custom_delta(self):
        result = check_emailable_users.get_usernames_from_database(None, self.mock_cursor_commons, "Some_category", delta_minutes=60)
        expected_query_params = ('Some_category', '20180914022134', '20180914032134')
        self.mock_cursor_commons.execute.assert_called_once_with(self.expected_query, expected_query_params)
        self.mock_cursor_commons.fetchall.assert_called_once_with()
        self.assertEquals(result, ['A', 'B'])
