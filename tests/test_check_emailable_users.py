#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Unit tests for check_emailable_users."""
import unittest
import unittest.mock as mock

from freezegun import freeze_time

import pywikibot

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
            "SELECT"
            " user.user_name as uploader"
            " FROM (SELECT"
            "   cl_from"
            "   FROM categorylinks"
            "   JOIN linktarget ON cl_target_id=lt_id"
            "   WHERE lt_namespace=14 AND lt_title=%s"
            "   AND cl_type='file') cats"
            " INNER JOIN page ON cl_from = page_id"
            " INNER JOIN file ON page_title = file_name"
            " INNER JOIN filerevision ON filerevision.fr_id = file.file_latest"
            " LEFT JOIN actor ON actor.actor_id = filerevision.fr_actor"
            " LEFT JOIN user ON user.user_id = actor.actor_user"
            " WHERE fr_timestamp BETWEEN %s AND %s"
            " GROUP BY uploader"
        )

    @freeze_time("2018-09-14 03:21:34")
    def test_get_usernames_with_default_delta(self):
        result = check_emailable_users.get_usernames_from_database(None, self.mock_cursor_commons, "Some_category")
        expected_query_params = ('Some_category', '20180914012134', '20180914032134')
        self.mock_cursor_commons.execute.assert_called_once_with(self.expected_query, expected_query_params)
        self.mock_cursor_commons.fetchall.assert_called_once_with()
        self.assertEqual(result, ['A', 'B'])

    @freeze_time("2018-09-14 03:21:34")
    def test_get_usernames_with_custom_delta(self):
        result = check_emailable_users.get_usernames_from_database(None, self.mock_cursor_commons, "Some_category", delta_minutes=60)
        expected_query_params = ('Some_category', '20180914022134', '20180914032134')
        self.mock_cursor_commons.execute.assert_called_once_with(self.expected_query, expected_query_params)
        self.mock_cursor_commons.fetchall.assert_called_once_with()
        self.assertEqual(result, ['A', 'B'])

    @freeze_time("2018-09-14 03:21:34")
    def test_get_usernames_with_no_result(self):
        self.mock_cursor_commons.fetchall.return_value = []
        result = check_emailable_users.get_usernames_from_database(None, self.mock_cursor_commons, "Some_category")
        expected_query_params = ('Some_category', '20180914012134', '20180914032134')
        self.mock_cursor_commons.execute.assert_called_once_with(self.expected_query, expected_query_params)
        self.mock_cursor_commons.fetchall.assert_called_once_with()
        self.assertEqual(result, [])


class TestNotifyUser(unittest.TestCase):
    """Test the notify_user function."""

    def setUp(self):
        self.mock_user = mock.create_autospec(pywikibot.User)
        self.mock_talk_page = mock.create_autospec(pywikibot.Page)
        self.mock_user.getUserTalkPage.return_value = self.mock_talk_page
        self.mock_user.site.username.return_value = 'TestBot'
        self.mock_talk_page.text = 'Existing talk page text'

    def test_happy_path_saves_notification(self):
        """User not yet notified — save is called."""
        self.mock_talk_page.revisions.return_value = [
            {'user': 'SomeOtherUser'}]
        check_emailable_users.notify_user(self.mock_user)
        self.mock_talk_page.save.assert_called_once_with(
            summary='Notifying WLM participant of missing e-mail address.',
            minor=False)

    def test_already_notified_skips_save(self):
        """Bot username in recent history — save is not called."""
        self.mock_talk_page.revisions.return_value = [
            {'user': 'TestBot'}]
        check_emailable_users.notify_user(self.mock_user)
        self.mock_talk_page.save.assert_not_called()

    def test_locked_page_is_caught(self):
        """LockedPageError is caught and does not propagate."""
        self.mock_talk_page.revisions.return_value = [
            {'user': 'SomeOtherUser'}]
        self.mock_talk_page.save.side_effect = (
            pywikibot.exceptions.LockedPageError(
                mock.create_autospec(pywikibot.Page)))
        # Should not raise
        check_emailable_users.notify_user(self.mock_user)
