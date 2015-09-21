"""Unit tests for converters."""

import unittest
from erfgoedbot.converters import extractWikilink


class TestExtractWikilink(unittest.TestCase):

    """Test the extractWikilink method."""

    def test_extractWikilink_simple_link(self):
        article = "[[Article]]"
        self.assertEquals(extractWikilink(article), "Article")

    def test_extractWikilink_piped_link(self):
        article = "[[Article|article]]"
        self.assertEquals(extractWikilink(article), "Article")

    def test_extractWikilink_link_uncapitalized(self):
        article = "[[article]]"
        self.assertEquals(extractWikilink(article), "Article")
