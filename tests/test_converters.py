# -*- coding: utf-8  -*-
"""Unit tests for converters."""

import unittest
from erfgoedbot.converters import (
    ucfirst,
    extractWikilink,
    extract_elements_from_template_param,
    remove_commons_category_prefix,
    sanitize_wikitext_string,
    CH1903Converter,
    int_to_european_digits
)


class TestUcFirst(unittest.TestCase):

    """Test the ucfirst method."""

    def test_ucfirst_on_empty_string_returns_empty_string(self):
        self.assertEquals(ucfirst(''), '')

    def test_ucfirst_capitalizes_string(self):
        self.assertEquals(ucfirst('abcd'), 'Abcd')

    def test_ucfirst_on_already_capitalized_string_is_constant(self):
        self.assertEquals(ucfirst('Abcd'), 'Abcd')

    def test_ucfirst_keeps_capitalized_bits(self):
        self.assertEquals(ucfirst('abcD'), 'AbcD')


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


class TestExtractElementsFromTemplateParam(unittest.TestCase):

    """Test the extract_elements_from_template_param method."""

    def test_extract_elements_from_template_param_empty_string(self):
        self.assertEquals(extract_elements_from_template_param(''), ('', ''))

    def test_extract_elements_from_template_param(self):
        input_value = 'id=identifiant'
        expected = (u'id', u'identifiant')
        self.assertEquals(extract_elements_from_template_param(input_value), expected)

    def test_extract_elements_from_template_param_with_spaces(self):
        input_value = 'id = identifiant'
        expected = (u'id', u'identifiant')
        self.assertEquals(extract_elements_from_template_param(input_value), expected)


class TestSanitizeWikitextString(unittest.TestCase):

    """Test the sanitize_wikitext_string method."""

    def test_sanitize_wikitext_string_empty_string(self):
        self.assertEquals(sanitize_wikitext_string(''), '')

    def test_sanitize_wikitext_string_no_features(self):
        input_value = 'My monument name'
        expected = u'My monument name'
        self.assertEquals(sanitize_wikitext_string(input_value), expected)

    def test_sanitize_wikitext_string_with_reference_at_the_end(self):
        input_value = 'My monument name<ref>Serious reference</ref>'
        expected = u'My monument name'
        self.assertEquals(sanitize_wikitext_string(input_value), expected)

    def test_sanitize_wikitext_string_with_reused_reference_at_the_end(self):
        input_value = 'My monument name<ref name="refA"/>'
        expected = u'My monument name'
        self.assertEquals(sanitize_wikitext_string(input_value), expected)

    def test_sanitize_wikitext_string_with_comment_at_the_end(self):
        input_value = u'2.51058<!--coordenades de patmapa ajustades automàticament-->'
        self.assertEquals(sanitize_wikitext_string(input_value), '2.51058')
        self.assertEquals(sanitize_wikitext_string(u'Aaa Ccc <!-- B -->'), u'Aaa Ccc')

    def test_sanitize_wikitext_string_with_comment_in_the_middle(self):
        expected = u'Aaa Ccc'
        self.assertEquals(sanitize_wikitext_string(u'Aaa <!-- B -->Ccc'), expected)
        self.assertEquals(sanitize_wikitext_string(u'Aaa <!-- B b b --> Ccc'), expected)
        self.assertEquals(sanitize_wikitext_string(u'Aaa<!-- B b b --> Ccc'), expected)


class TestIntToEuropeanDigits(unittest.TestCase):

    """Test the int_to_european_digits method."""

    def test_int_to_european_digits_empty_string(self):
        self.assertEquals(int_to_european_digits(''), '')

    def test_int_to_european_digits_random_string(self):
        in_data = u'random string'
        self.assertEquals(int_to_european_digits(in_data), '')

    def test_int_to_european_digits_number_in(self):
        in_data = 1234567890
        self.assertEquals(int_to_european_digits(in_data),
                          '1234567890')

    def test_int_to_european_digits_european_in(self):
        in_data = u'1234567890'
        self.assertEquals(int_to_european_digits(in_data),
                          '1234567890')

    def test_int_to_european_digits_farsi_in(self):
        in_data = u'۱۲۳۴۵۶۷۸۹۰'
        self.assertEquals(int_to_european_digits(in_data),
                          '1234567890')

    def test_int_to_european_digits_arabic_in(self):
        in_data = u'١٢٣٤٥٦٧٨٩٠'
        self.assertEquals(int_to_european_digits(in_data),
                          '1234567890')
