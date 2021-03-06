# -*- coding: utf-8  -*-
"""Custom assertions for erfgoedbot unit tests."""
import sys


class CustomAssertions:

    """Introduce custom assertions."""

    def assert_all_in(self, first, second, msg=None):
        """Test that all first are in second, else append failing to msg."""
        error_msg = '[%%s] not found in %s' % second
        if msg:
            if not self.longMessage:
                # msg itself specifies where to append failing
                error_msg = msg
            else:
                error_msg = '%s: %s' % (msg, error_msg)
        try:
            self.assertLessEqual(set(first), set(second))
        except AssertionError:
            diff = set(first) - set(second)
            raise AssertionError(error_msg % ', '.join(diff))

    def assert_all_in_string(self, first, text, msg=None):
        """Test that all first are in text, else append failing to msg."""
        error_msg = '[%%s] not found in %s' % text
        if msg:
            if not self.longMessage:
                # msg itself specifies where to append failing
                error_msg = msg
            else:
                error_msg = '%s: %s' % (msg, error_msg)
        not_found = [s for s in first if s not in text]
        if not_found:
            raise AssertionError(error_msg % ', '.join(not_found))

    # From python 3.7 can just use .isascii()
    def assert_is_ascii(self, text, msg=None):
        """Assert that a string is ascii."""
        error_msg = '"%s" not ascii' % text
        if msg:
            error_msg = '%s : %s' % (error_msg, msg)
        if len(text) != len(text.encode()):
            raise AssertionError(error_msg)


# Backport of function existing in py >= 3.6
def assert_called_once(self):
    """assert that the mock was called only once.
    """
    if not self.call_count == 1:
        msg = ("Expected '%s' to have been called once. Called %s times.%s"
               % (self._mock_name or 'mock',
                  self.call_count,
                  self._calls_repr()))
        raise AssertionError(msg)


if sys.version_info[:3] < (3, 6, 0):
    from unittest.mock import NonCallableMock
    NonCallableMock.assert_called_once = assert_called_once
