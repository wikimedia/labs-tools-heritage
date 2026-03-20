from unittest import TestCase

from erfgoedbot.add_coord_to_articles import extract_article_name


class TestExtractArticleName(TestCase):

    def test_piped_wikilink(self):
        self.assertEqual(
            extract_article_name('[[Article Title|Display text]]'),
            'Article Title')

    def test_plain_wikilink(self):
        self.assertEqual(
            extract_article_name('[[Article Title]]'),
            'Article Title')

    def test_no_wikilink(self):
        self.assertEqual(extract_article_name('Just plain text'), '')

    def test_empty_string(self):
        self.assertEqual(extract_article_name(''), '')

    def test_piped_wikilink_with_special_chars(self):
        self.assertEqual(
            extract_article_name('[[Château de Versailles|Versailles]]'),
            'Château de Versailles')

    def test_plain_wikilink_with_special_chars(self):
        self.assertEqual(
            extract_article_name('[[Château de Versailles]]'),
            'Château de Versailles')
