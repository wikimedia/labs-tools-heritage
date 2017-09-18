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
    pagename_str = page.title(as_filename=True, withNamespace=False)
    filename = '[{site}][{ns}]{page}.wiki'.format(
        site=site_str, ns=namespace_str, page=pagename_str)
    return filename.replace(' ', '_').replace(':', '_')
