"""Unit tests for converters."""

import unittest
from erfgoedbot.converters import (
    extractWikilink,
    remove_commons_category_prefix,
    CH1903Converter
)


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

    def test_extractWikilink_link_pipe_only(self):
        article = "[[Article|]]"
        self.assertEquals(extractWikilink(article), "Article")

    def test_extractWikilink_link_spaces_are_replaced_with_underscores(self):
        article = "[[Some article|]]"
        self.assertEquals(extractWikilink(article), "Some_article")

    def test_extractWikilink_link_no_link(self):
        article = "article"
        self.assertEquals(extractWikilink(article), "")


class TestRemoveCommonsCategoryPrefix(unittest.TestCase):

    """Test the remove_commons_category_prefix method."""

    def test_remove_commons_category_prefix_empty_should_return_empty(self):
        text = ''
        self.assertEquals(remove_commons_category_prefix(text), "")

    def test_remove_commons_category_prefix_lowercase_should_remove_double_prefix(self):
        text = 'commons:Category:Tropaeum Traiani'
        self.assertEquals(remove_commons_category_prefix(text), "Tropaeum Traiani")

    def test_remove_commons_category_prefix_uppercase_should_remove_double_prefix(self):
        text = 'Commons:Category:Tropaeum Traiani'
        self.assertEquals(remove_commons_category_prefix(text), "Tropaeum Traiani")

    def test_remove_commons_category_prefix_should_remove_single_prefix(self):
        text = 'Category:Tropaeum Traiani'
        self.assertEquals(remove_commons_category_prefix(text), "Tropaeum Traiani")

    def test_remove_commons_category_prefix_with_no_prefix_should_return(self):
        text = 'Tropaeum Traiani'
        self.assertEquals(remove_commons_category_prefix(text), "Tropaeum Traiani")


class TestCH1903Converter(unittest.TestCase):

    """Test the CH1903Converter method."""

    def test_CH1903Converter_empty(self):
        self.assertEquals(CH1903Converter('', ''), (0, 0))

    def test_CH1903Converter_dummy(self):
        expected = (45.42221774940194, -0.15036807152500034)
        self.assertEquals(CH1903Converter('1', '1'), expected)
