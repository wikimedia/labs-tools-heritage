#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Support library of commonly shared functions."""
from __future__ import unicode_literals

import os
import re
from builtins import open

import pywikibot
from pywikibot.exceptions import OtherPageSaveError, PageSaveRelatedError


def get_source_link(source, harvest_type=None, label=None):
    """
    Format the source as an appropriate wiki link.

    Requires the target page to be on the same wiki unless it is a sparql
    harvest. Links to Wikidata are always prefixed.

    @param source: the source value from the SQL table
    @param harvest_type: the type of harvest from which the source was
        extracted. E.g. "sparql"
    @param label: Optional label to use for the link
    """
    try:
        page_title, (project, lang) = get_source_page(source, harvest_type)
    except ValueError:
        raise
    if project == 'wikidata':
        page_title = ':d:{0}'.format(page_title)

    if label:
        return '[[{0}|{1}]]'.format(page_title, label)
    return '[[{0}]]'.format(page_title)


def get_page_from_url(url):
    """
    Retrieve the wikipage and site from a page or entity url.
    """
    supported_sites = ['wikipedia', 'wikivoyage', 'wikidata', 'wikimedia']
    pattern = '\/\/(.+?)\.({0})\.org\/(wiki|entity)\/(.+?)$'.format(
        '|'.join(supported_sites))
    m = re.search(pattern, url)
    site = (m.group(2), m.group(1))
    page_name = m.group(4)
    return (page_name, site)


def get_source_page(source, harvest_type=None):
    """
    Retrieve the wikipage and site from the source field.

    Note that the returned site tuple may not be a valid pywikibot site. E.g.
    commons is ('wikimedia', 'commons') rather than ('commons', 'commons').

    @param source: the source value from the SQL table
    @param harvest_type: the type of harvest from which the source was
        extracted, e.g. "sparql".
    """
    site = None
    page_name = None
    if harvest_type == 'sparql':
        try:
            return get_page_from_url(source)
        except AttributeError:
            raise ValueError(
                'Could not find source list ({0})'.format(source))
    else:
        supported_sites = ['wikipedia', 'wikivoyage', 'wikidata', 'wikimedia']
        pattern = '\/\/(.+?)\.({0})\.org\/w\/index\.php\?title=(.+?)&'.format(
            '|'.join(supported_sites))
        m = re.search(pattern, source)
        try:
            site = (m.group(2), m.group(1))
            page_name = m.group(3)
        except AttributeError:
            raise ValueError(
                'Could not find source list ({0})'.format(source))

    return (page_name, site)


def save_to_wiki_or_local(page, summary, content, minorEdit=True):
    """
    Save the content to the page on a given site or store it locally.

    Whether the pages are outputted locally (and where to) is controlled by the
    HERITAGE_LOCAL_WRITE_PATH environment variable.

    @param page: the pywikibot.Page to which the content should be written
    @param content: the content to store
    @param summary: the edit summary to save the content with
    @param minorEdit: if the edit should be marked as minor (defaults to True)
    """
    if not isinstance(page, pywikibot.Page):
        pywikibot.warning(
            'Could not save page {0} because it is not a Page '
            'instance.'.format(page))

    local_path = os.environ.get('HERITAGE_LOCAL_WRITE_PATH')

    if not local_path:
        try:
            page.put(newtext=content, summary=summary, minorEdit=minorEdit)
        except (OtherPageSaveError, PageSaveRelatedError):
            pywikibot.warning(
                'Could not save page {0} ({1})'.format(page, summary))
    else:
        filename = os.path.join(local_path, page_to_filename(page))
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('#summary: {0}\n---------------\n'.format(summary))
            f.write(unicode(content))


def page_to_filename(page):
    """
    Create a standardised filename for a page.

    The name takes the form [site][namespace]pagename.wiki where '/', ':' and
    " " has been replaced by '_'. Namespace 0 is given as just '_'.

    @param page: the pywikibot.Page for which to generate a filename.
    """
    site_str = str(page.site)
    namespace_str = page.namespace().custom_prefix().rstrip(':') or '_'
    pagename_str = page.title(as_filename=True, with_ns=False)
    filename = '[{site}][{ns}]{page}.wiki'.format(
        site=site_str, ns=namespace_str, page=pagename_str)
    return filename.replace(' ', '_').replace(':', '_')


def process_sort_key_query_result(cursor):
    """Invert and convert cursor of a query requesting title and sort key.

    This assumes a request to the categorylinks table where only two values are
    selected for and where cl_sortkey or cl_sortkey_prefix is the second one.

    As cl_sortkey and cl_sortkey_prefix may contain partial characters, any
    characters which cannot be decoded must be replaced.

    @param cursor: the pymysql.connect.cursor for the executed query
    @return: dict
    """
    result = {}
    while True:
        try:
            row = cursor.fetchone()
            (page_title, sort_key) = row
            sort_key = unicode(sort_key, 'utf-8', errors='replace')
            page_title = unicode(page_title, 'utf-8')
            result[sort_key] = page_title
        except TypeError:
            break

    return result


def get_id_from_sort_key(sort_key, known_ids):
    """
    Attempt to get a monument id from a category sort key.

    Candidate ids are compared to a list of known ids.

    @param sort_key: a category sort key or sort key prefix
    @param known_ids: a list of known ids, or a dict where the keys are known
        ids.
    @return: unicode|None
    """
    if sort_key == '':
        return None

    # ensure there are no remaining encoding issues
    if not isinstance(sort_key, unicode):
        sort_key = unicode(sort_key, 'utf-8', errors='replace')
    # Just want the first line
    monument_id = sort_key.splitlines()[0]
    # Remove leading and trailing spaces
    monument_id = monument_id.strip()

    # Now try some variants until we have a hit
    if monument_id in known_ids:
        return monument_id

    # Only remove leading zero's if we don't have a hit.
    monument_id = monument_id.lstrip(u'0')
    if monument_id in known_ids:
        return monument_id
    # Only remove leading underscores if we don't have a hit.
    monument_id = monument_id.lstrip(u'_')
    if monument_id in known_ids:
        return monument_id
    # Only all uppercase if we don't have a hit.
    monument_id = monument_id.upper()
    if monument_id in known_ids:
        return monument_id

    # Return None if no match has been found
    return None


def instruction_header(central_page, subpage='header'):
    """
    A wikitext header embedding a local subpage or linking to central one.

    @param central_page: the page name, including interwiki prefix
    @param subpage: the name of the subpage to embed, if it exists. Defaults
        to 'header'.
    """
    # percentage formatting to avoid having to escape all curly brackets
    data = {'central_page': central_page, 'subpage': subpage}
    return (
        u'{{#ifexist:{{FULLPAGENAME}}/%(subpage)s'
        u'|{{/%(subpage)s}}'
        u'|For information on how to use this report and how to localise '
        u'these instructions visit '
        u'[[%(central_page)s]]. }}\n' % data)


def table_header_row(columns):
    """
    A wikitext table header row.

    @param columns: OrderedDict of the desired columns in the format
        OrderedDict({name: is_numeric}). Where is_numeric indicates that the
        column shuld be sorted as numbers.
    """
    text = u'{| class="wikitable sortable"\n'
    for name, is_numeric in columns.iteritems():
        if is_numeric:
            text += u'! data-sort-type="number"| {0}\n'.format(name)
        else:
            text += u'! {0}\n'.format(name)
    return text


def table_bottom_row(num_columns, values=None):
    """
    A wikitext table bottom row, where empty values are grey and others bold.

    @param num_columns: the number of columns
    @param values: a dict with column numbers and their values. Numbering of
        columns starting from 0.
    """
    values = values or {}
    text = u'|- class="sortbottom"\n'
    for i in range(num_columns):
        if i in values.keys():
            text += u"| '''{}'''\n".format(values[i])
        else:
            text += u'|style="background-color: #ccc;"|\n'
    text += u'|}\n'
    return text
