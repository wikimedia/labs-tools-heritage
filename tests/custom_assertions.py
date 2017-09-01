# -*- coding: utf-8  -*-
"""Custom assertions for erfgoedbot unit tests."""


class CustomAssertions:

    """Introduce custom assertions."""

    def assert_all_in(self, first, second, msg=None):
        """Test that all first are in second, else append failing to msg."""
        error_msg = u'[%%s] not found in %s' % second
        if msg:
            if not self.longMessage:
                # msg itself specifies where to append failing
                error_msg = msg
            else:
                error_msg = u'%s: %s' % (msg, error_msg)
        try:
            self.assertLessEqual(set(first), set(second))
        except AssertionError:
            diff = set(first) - set(second)
            raise AssertionError(error_msg % ', '.join(diff))

    def assert_all_in_string(self, first, text, msg=None):
        """Test that all first are in text, else append failing to msg."""
        error_msg = u'[%%s] not found in %s' % text
        if msg:
            if not self.longMessage:
                # msg itself specifies where to append failing
                error_msg = msg
            else:
                error_msg = u'%s: %s' % (msg, error_msg)
        not_found = filter(lambda s: s not in text, first)
        if not_found:
            raise AssertionError(error_msg % ', '.join(not_found))

    def assert_is_ascii(self, text, msg=None):
        """Assert that a string is ascii."""
        error_msg = u'"%s" not ascii' % text
        if msg:
            error_msg = u'%s : %s' % (error_msg, msg)
        try:
            text.decode('ascii')
        except UnicodeEncodeError:
            raise AssertionError(error_msg)
