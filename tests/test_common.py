"""Unit tests for common."""

import os
import tempfile
import unittest

import mock

import pywikibot

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


class TestGetPageFromUrl(unittest.TestCase):

    def test_get_page_from_url_entity(self):
        source = 'http://www.wikidata.org/entity/Q123'
        result = common.get_page_from_url(source)
        self.assertEquals(result, ('Q123', ('wikidata', 'www')))

    def test_get_page_from_url_page(self):
        source = 'http://www.wikidata.org/wiki/Q123'
        result = common.get_page_from_url(source)
        self.assertEquals(result, ('Q123', ('wikidata', 'www')))

    def test_get_page_from_url_wikipedia(self):
        source = 'http://en.wikipedia.org/entity/foo'
        result = common.get_page_from_url(source)
        self.assertEquals(result, ('foo', ('wikipedia', 'en')))


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


class TestPageToFilename(unittest.TestCase):

    def test_page_to_filename_commons(self):
        site = pywikibot.Site('commons', 'commons')
        page = pywikibot.Page(site, 'Foo')
        self.assertEquals(
            common.page_to_filename(page),
            '[commons_commons][_]Foo.wiki'
        )

    def test_page_to_filename_wikipedia(self):
        site = pywikibot.Site('en', 'wikipedia')
        page = pywikibot.Page(site, 'Foo')
        self.assertEquals(
            common.page_to_filename(page),
            '[wikipedia_en][_]Foo.wiki'
        )

    def test_page_to_filename_namespace(self):
        site = pywikibot.Site('commons', 'commons')
        page = pywikibot.Page(site, 'Template:Foo')
        self.assertEquals(
            common.page_to_filename(page),
            '[commons_commons][Template]Foo.wiki'
        )

    def test_page_to_filename_subpage(self):
        site = pywikibot.Site('commons', 'commons')
        page = pywikibot.Page(site, 'Foo/Bar')
        self.assertEquals(
            common.page_to_filename(page),
            '[commons_commons][_]Foo_Bar.wiki'
        )

    def test_page_to_filename_with_spaces(self):
        site = pywikibot.Site('commons', 'commons')
        page = pywikibot.Page(site, 'Foo bar')
        self.assertEquals(
            common.page_to_filename(page),
            '[commons_commons][_]Foo_bar.wiki'
        )


class TestSaveToWikiOrLocal(unittest.TestCase):

    def setUp(self):
        site = pywikibot.Site('test', 'wikipedia')
        self.page = pywikibot.Page(site, 'Foo')

        patcher = mock.patch('erfgoedbot.common.page_to_filename')
        self.mock_page_to_filename = patcher.start()
        self.mock_page_to_filename.return_value = 'filename'
        self.addCleanup(patcher.stop)

        # Create a temporary file
        self.test_outfile = tempfile.NamedTemporaryFile(delete=False)
        patcher = mock.patch('erfgoedbot.common.os.path.join')
        self.mock_join = patcher.start()
        self.mock_join.return_value = self.test_outfile.name
        self.addCleanup(patcher.stop)

        # Ensure tests don't write
        patcher = mock.patch('erfgoedbot.common.pywikibot.Page.put')
        self.mock_page_put = patcher.start()
        self.addCleanup(patcher.stop)

        # Mock environment variable
        patcher = mock.patch('erfgoedbot.common.os.environ.get')
        self.mock_environ_get = patcher.start()
        self.mock_environ_get.return_value = None
        self.addCleanup(patcher.stop)

    def tearDown(self):
        # Closes and removes the file
        os.remove(self.test_outfile.name)

    def test_save_to_wiki_or_local_write_to_wiki(self):
        summary = 'a summary'
        content = 'The content'
        common.save_to_wiki_or_local(self.page, summary, content)
        self.mock_environ_get.assert_called_once_with(
            'HERITAGE_LOCAL_WRITE_PATH')
        self.mock_page_put.assert_called_once_with(
            newtext=content, summary=summary, minorEdit=True)
        self.mock_page_to_filename.assert_not_called()
        self.mock_join.assert_not_called()
        self.assertEquals(self.test_outfile.read(), '')

    def test_save_to_wiki_or_local_write_locally(self):
        summary = 'a summary'
        content = u'The content'
        self.mock_environ_get.return_value = 'something'
        common.save_to_wiki_or_local(self.page, summary, content)
        self.mock_environ_get.assert_called_once_with(
            'HERITAGE_LOCAL_WRITE_PATH')
        self.mock_page_put.assert_not_called()
        self.mock_page_to_filename.assert_called_once_with(self.page)
        self.mock_join.assert_called_once_with('something', 'filename')
        self.assertEquals(
            self.test_outfile.read(),
            '#summary: a summary\n---------------\nThe content'
        )
