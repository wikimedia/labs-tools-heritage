#!/usr/bin/python
# -*- coding: utf-8  -*-

"""Conversion methods"""

import re

from erfgoedbot.checkers import is_int


def CH1903Converter(x, y):
    if not(x.strip() and y.strip()):
        # x or y is empty
        return (0, 0)
    x = float(x)
    y = float(y)

    lat = 16.9023892
    lat += 3.238272 * (y - 200) / 1000
    lat += 0.270978 * (x - 600) / 1000 * (x - 600) / 1000
    lat += 0.002528 * (y - 200) / 1000 * (y - 200) / 1000
    lat += 0.044700 * \
        (x - 600) / 1000 * (x - 600) / 1000 * (y - 200) / 1000
    lat += 0.014000 * \
        (y - 200) / 1000 * (y - 200) / 1000 * (y - 200) / 1000
    lat = lat / 0.36  # Round 6

    lon = 2.6779094
    lon += 4.728982 * (x - 600) / 1000
    lon += 0.791484 * (x - 600) / 1000 * (y - 200) / 1000
    lon += 0.130600 * \
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
    articleName = ''
    # result = re.search("\[\[(.+?)(\||\]\])", text)
    regex = re.compile(r"""
      \[\[              # Opening brackets
      (?P<target>.+?)   # Link target
      (\||\]\])         # Either a pipe or closing brackets
    """, re.VERBOSE)
    match = re.search(regex, text)
    if match:
        articleName = match.group('target')
        articleName = articleName.replace(' ', '_')
        articleName = ucfirst(articleName)
    return articleName


def remove_commons_category_prefix(text):
    result = ''
    regex = re.compile(r"""
     ([Cc]ommons:)?     # Commons prefix
     (Category:)?       # Category prefix
     (?P<category>.*)   # The link target
    """, re.VERBOSE)
    match = re.search(regex, text)
    if match:
        result = match.group('category')
    return result


def remove_file_prefix(text, prefixes):
    """
    Remove a leading file namespace prefix from an image name.

    Some wikis have a convention of giving the image as a full page title,
    rather than as just a file name.

    Surrounding whitespace is always stripped, whether or not a prefix was
    found.

    @param text: the image name, with or without a prefix
    @param prefixes: all of the names of the file namespace on the source
        wiki, canonical, localized and aliases, since any of them may have
        been used. If empty no prefix is removed.
    @return: the image name without a file namespace prefix
    """
    text = text.strip()
    if not prefixes:
        # an empty alternation still matches, stripping a bare leading colon
        return text

    regex = re.compile(r'^:?[\s_]*({0})[\s_]*:[\s_]*'.format(
        '|'.join(re.escape(prefix) for prefix in prefixes)), re.IGNORECASE)
    return regex.sub('', text)


def extract_elements_from_template_param(template_param):

    """Extract and sanitize the contents of a parsed template param."""

    (field, _, value) = template_param.partition('=')
    # Remove leading or trailing spaces
    field = field.strip()
    return (field, sanitize_wikitext_string(value))


def sanitize_wikitext_string(value):

    """Remove undesirable wikitext features from a string."""

    value = value.split("<ref")[0].strip()
    value = re.sub(r"\s?<!--.*?-->\s?", ' ', value)
    return value.strip()


def int_to_european_digits(text):

    """
    Convert integer in recognized scripts to European digits.

    European Digits meaning 0123456789 (slight clarification per
    https://en.wikipedia.org/wiki/Arabic_numerals)

    Returns an empty string on fail and trims any leading zeros.
    """
    if is_int(text):
        return '%d' % int(text)
    return ''
