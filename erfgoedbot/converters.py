#!/usr/bin/python
# -*- coding: utf-8  -*-

"""Conversion methods"""

import re


def CH1903Converter(x, y):
    if not(x.strip() and y.strip()):
        # x or y is empty
        return (0, 0)
    x = float(x)
    y = float(y)

    lat = 16.9023892
    lat = lat + 3.238272 * (y - 200) / 1000
    lat = lat + 0.270978 * (x - 600) / 1000 * (x - 600) / 1000
    lat = lat + 0.002528 * (y - 200) / 1000 * (y - 200) / 1000
    lat = lat + 0.044700 * \
        (x - 600) / 1000 * (x - 600) / 1000 * (y - 200) / 1000
    lat = lat + 0.014000 * \
        (y - 200) / 1000 * (y - 200) / 1000 * (y - 200) / 1000
    lat = lat / 0.36  # Round 6

    lon = 2.6779094
    lon = lon + 4.728982 * (x - 600) / 1000
    lon = lon + 0.791484 * (x - 600) / 1000 * (y - 200) / 1000
    lon = lon + 0.130600 * \
        (x - 600) / 1000 * (y - 200) / 1000 * (y - 200) / 1000
    lon = lon - 0.043600 * \
        (x - 600) / 1000 * (x - 600) / 1000 * (x - 600) / 1000
    lon = lon / 0.36  # Round 6

    return (lat, lon)


def ucfirst(text):
    if (text):
        return text[0].upper() + text[1:]
    else:
        return ''


def extractWikilink(text):
    articleName = u''
    result = re.search("\[\[(.+?)(\||\]\])", text)
    if (result and result.group(1)):
        articleName = result.group(1)
        articleName = articleName.replace(u' ', u'_')
        articleName = ucfirst(articleName)

    return articleName


def remove_commons_category_prefix(text):
    result = ''
    regex = re.compile(r"""
     (Commons:)?        # Commons prefix
     (Category:)?       # Category prefix
     (?P<category>.*)   # The link target
    """, re.VERBOSE)
    match = re.search(regex, text)
    if match:
        result = match.group('category')
    return result
