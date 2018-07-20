"""Unit tests for common."""
import os
import tempfile
import unittest
from collections import OrderedDict

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


class TestGetIdFromSortKey(unittest.TestCase):

    """Test the get_id_from_sort_key method."""

    def setUp(self):
        self.known_ids = ['123', '1230', '01230_', 'F00BAR']

    def test_get_id_from_sort_key_exact(self):
        sort_key = '123'
        expected = '123'
        result = common.get_id_from_sort_key(sort_key, self.known_ids)
        self.assertEquals(result, expected)

    def test_get_id_from_sort_key_exact_with_dict(self):
        known_ids = {
            '123': 'source_url',
            '1230': 'source_url',
            '01230_': 'source_url',
            'F00BAR': 'source_url'
        }
        sort_key = '123'
        expected = '123'
        result = common.get_id_from_sort_key(sort_key, known_ids)
        self.assertEquals(result, expected)

    def test_get_id_from_sort_key_multi_line(self):
        sort_key = '123\nfoo'
        expected = '123'
        result = common.get_id_from_sort_key(sort_key, self.known_ids)
        self.assertEquals(result, expected)

    def test_get_id_from_sort_key_trim(self):
        sort_key = ' \t123\t '
        expected = '123'
        result = common.get_id_from_sort_key(sort_key, self.known_ids)
        self.assertEquals(result, expected)

    def test_get_id_from_sort_key_padded(self):
        sort_key = '000001230'
        expected = '1230'
        result = common.get_id_from_sort_key(sort_key, self.known_ids)
        self.assertEquals(result, expected)

    def test_get_id_from_sort_key_underscored(self):
        sort_key = '_01230_'
        expected = '01230_'
        result = common.get_id_from_sort_key(sort_key, self.known_ids)
        self.assertEquals(result, expected)

    def test_get_id_from_sort_key_upper(self):
        sort_key = 'F00bar'
        expected = 'F00BAR'
        result = common.get_id_from_sort_key(sort_key, self.known_ids)
        self.assertEquals(result, expected)

    def test_get_id_from_sort_key_no_match(self):
        sort_key = ' 000_foo \nbar'
        expected = None
        result = common.get_id_from_sort_key(sort_key, self.known_ids)
        self.assertEquals(result, expected)


class TestTableHeaderRow(unittest.TestCase):

    """Test the table_header_row method."""

    def test_table_header_row_wo_numeric(self):
        columns = OrderedDict([('a', False), ('b', False), ('c', False)])
        expected = (
            u'{| class="wikitable sortable"\n'
            u'! a\n'
            u'! b\n'
            u'! c\n')
        result = common.table_header_row(columns)
        self.assertEquals(result, expected)

    def test_table_header_row_w_numeric(self):
        columns = OrderedDict([('a', False), ('b', True), ('c', False)])
        expected = (
            u'{| class="wikitable sortable"\n'
            u'! a\n'
            u'! data-sort-type="number"| b\n'
            u'! c\n')
        result = common.table_header_row(columns)
        self.assertEquals(result, expected)


class TestTableBottomRow(unittest.TestCase):

    """Test the table_bottom_row method."""

    def test_table_bottom_row_no_value(self):
        expected = (
            u'|- class="sortbottom"\n'
            u'|style="background-color: #ccc;"|\n'
            u'|style="background-color: #ccc;"|\n'
            u'|}\n')
        result = common.table_bottom_row(2)
        self.assertEquals(result, expected)

    def test_table_bottom_row_basic(self):
        values = {2: 123}
        expected = (
            u'|- class="sortbottom"\n'
            u'|style="background-color: #ccc;"|\n'
            u'|style="background-color: #ccc;"|\n'
            u"| '''123'''\n"
            u'|style="background-color: #ccc;"|\n'
            u'|style="background-color: #ccc;"|\n'
            u'|style="background-color: #ccc;"|\n'
            u'|}\n')
        result = common.table_bottom_row(6, values)
        self.assertEquals(result, expected)
