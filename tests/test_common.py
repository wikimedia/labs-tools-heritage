"""Unit tests for common."""

import unittest
import mock
from erfgoedbot import common


class TestGetSourcePage(unittest.TestCase):

    def test_getSourcePage_wikipedia(self):
        source = '//en.wikipedia.org/w/index.php?title=foo&oldid=123'
        result = common.get_source_page(source)
        self.assertEquals(result, ('foo', ('wikipedia', 'en')))

    def test_getSourcePage_wikipedia_urlencode(self):
        source = '//ka.wikipedia.org/w/index.php?title=%E1%83%95%E1%83%98%E1%83%99&oldid=3179801'
        result = common.get_source_page(source)
        self.assertEquals(
            result, ('%E1%83%95%E1%83%98%E1%83%99', ('wikipedia', 'ka')))

    def test_getSourcePage_wikivoyage(self):
        source = '//ru.wikivoyage.org/w/index.php?title=foo&oldid=123'
        result = common.get_source_page(source)
        self.assertEquals(result, ('foo', ('wikivoyage', 'ru')))

    def test_getSourcePage_sparql(self):
        source = 'http://www.wikidata.org/entity/Q123'
        result = common.get_source_page(source, 'sparql')
        self.assertEquals(result, ('Q123', ('wikidata', 'www')))


class TestGetSourceLink(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch('erfgoedbot.common.get_source_page')
        self.mock_get_source = patcher.start()
        self.addCleanup(patcher.stop)

    def test_getSourcePage_wikipedia(self):
        self.mock_get_source.return_value = ('foo', ('wikipedia', 'en'))
        result = common.get_source_link('a link')
        self.assertEquals(result, '[[foo]]')

    def test_getSourcePage_wikipedia_label(self):
        self.mock_get_source.return_value = ('foo', ('wikipedia', 'en'))
        result = common.get_source_link('a link', label='bar')
        self.assertEquals(result, '[[foo|bar]]')

    def test_getSourcePage_sparql(self):
        self.mock_get_source.return_value = ('Q123', ('wikidata', 'www'))
        result = common.get_source_link('a link', 'sparql')
        self.assertEquals(result, '[[:d:Q123]]')

    def test_getSourcePage_sparql_label(self):
        self.mock_get_source.return_value = ('Q123', ('wikidata', 'www'))
        result = common.get_source_link('a link', 'sparql', 'bar')
        self.assertEquals(result, '[[:d:Q123|bar]]')
