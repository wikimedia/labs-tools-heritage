#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Support library of commonly shared functions."""

import re


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


def get_source_page(source, harvest_type=None):
    """
    Retrieve the wikipage and site from the source field.

    Note that the returned site tuple may not be a valid pywikibot site. E.g.
    commons is ('wikimedia', 'commons') rather than ('commons', 'commons').

    @param source: the source value from the SQL table
    @harvest_type: the type of harvest from which the source was extracted.
        e.g. "sparql"
    """
    site = None
    page_name = None
    if harvest_type == 'sparql':
        site = ('wikidata', 'www')
        page_name = source.split('/')[-1]
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
                u'Could not find source list ({0})'.format(source))

    return (page_name, site)
