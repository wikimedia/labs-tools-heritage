#!/usr/bin/python
# -*- coding: utf-8  -*-
'''

Make a list of monuments where a category about the monument exists, but no link is in the list yet.

Usage:
# loop thtough all countries
python missing_commonscat_links.py
# work on specific country-lang
python missing_commonscat_links.py -countrycode:XX -langcode:YY

'''
import re

import pywikibot

import monuments_config as mconfig
import common as common
from database_connection import (
    close_database_connection,
    connect_to_monuments_database,
    connect_to_commons_database
)

_logger = "missing_commonscat"


def processCountry(countrycode, lang, countryconfig, conn, cursor, conn2,
                   cursor2):
    '''
    Work on a single country.
    '''
    if not countryconfig.get('missingCommonscatPage'):
        # missingCommonscatPage not set, just skip silently.
        return False

    if countryconfig.get('type') == 'sparql':
        # This script does not (yet) work for SPARQL sources, skip silently
        return False

    commonscatField = lookupSourceField(u'commonscat', countryconfig)
    if not commonscatField:
        # Field is missing. Something is seriously wrong, but we just skip it
        # silently
        return False

    missingCommonscatPage = countryconfig.get('missingCommonscatPage')
    commonsTrackerCategory = countryconfig.get(
        'commonsTrackerCategory'). replace(u' ', u'_')

    withoutCommonscat = getMonumentsWithoutCommonscat(
        countrycode, lang, conn, cursor)
    commonscats = getMonumentCommonscats(
        commonsTrackerCategory, conn2, cursor2)

    pywikibot.log(u'withoutCommonscat %s elements' % (len(withoutCommonscat),))
    pywikibot.log(u'commonscats %s elements' % (len(commonscats),))

    # People can add a /header template for with more info
    text = u'{{#ifexist:{{FULLPAGENAME}}/header | {{/header}} }}\n'
    # text += u'<gallery>\n'
    totalCategories = 0
    maxCategories = 1000

    for catSortKey in sorted(commonscats.keys()):
        try:
            monumentId = unicode(catSortKey, 'utf-8')
            # Just want the first line
            mLines = monumentId.splitlines()
            monumentId = mLines[0]
            # Remove leading and trailing spaces
            monumentId = monumentId.strip()
            # Remove leading zero's. FIXME: This should be replaced with
            # underscores
            monumentId = monumentId.lstrip(u'0')
            # Remove leading underscors.
            monumentId = monumentId.lstrip(u'_')
            # All uppercase, same happens in other list. FIXME: Remove this
            monumentId = monumentId.upper()
            if monumentId in withoutCommonscat:
                m = re.search(
                    '^[^\?]+\?title\=(.+?)&', withoutCommonscat.get(monumentId))
                wikiSourceList = m.group(1)
                categoryName = commonscats.get(catSortKey)
                # pywikibot.output(u'Key %s returned a result' % (monumentId,))
                # pywikibot.output(wikiSourceList)
                # pywikibot.output(imageName)
                if totalCategories <= maxCategories:
                    text += u'* <nowiki>|</nowiki> %s = [[:Commons:Category:%s|%s]] - %s @ [[%s]]\n' % (commonscatField, unicode(
                        categoryName, 'utf-8'), unicode(categoryName, 'utf-8').replace(u'_', u' '), monumentId, wikiSourceList)
                totalCategories += 1
        except ValueError:
            pywikibot.warning(u'Got value error for %s' % (monumentId,))

    # text += u'</gallery>'

    if totalCategories >= maxCategories:
        text += \
            u'<!-- Maximum number of categories reached: %s, total of missing commonscat links: %s -->\n' % (
                maxCategories, totalCategories)
        comment = u'Commonscat links to be made in monument lists: %s (list maximum reached),  total of missing commonscat links: %s' % (
            maxCategories, totalCategories)
    else:
        comment = u'Commonscat links to be made in monument lists: %s' % totalCategories

    text += getInterwikisMissingCommonscatPage(countrycode, lang)

    site = pywikibot.Site(lang, u'wikipedia')
    page = pywikibot.Page(site, missingCommonscatPage)
    pywikibot.debug(text, _logger)
    common.save_to_wiki_or_local(page, comment, text)

    return totalCategories


def lookupSourceField(destination, countryconfig):
    '''
    Lookup the source field of a destination.
    '''
    for field in countryconfig.get('fields'):
        if field.get('dest') == destination:
            return field.get('source')


def getInterwikisMissingCommonscatPage(countrycode, lang):
    result = u''
    for (countrycode2, lang2), countryconfig in mconfig.countries.iteritems():
        if countrycode == countrycode2 and lang != lang2:
            if countryconfig.get('missingCommonscatPage'):
                result += \
                    u'[[%s:%s]]\n' % (
                        lang2, countryconfig.get('missingCommonscatPage'))

    return result


def getMonumentsWithoutCommonscat(countrycode, lang, conn, cursor):
    result = {}

    query = u"""SELECT id, source FROM monuments_all WHERE (commonscat IS NULL or commonscat='') AND country=%s AND lang=%s"""

    cursor.execute(query, (countrycode, lang))

    while True:
        try:
            row = cursor.fetchone()
            (id, source) = row
            # To uppercase, same happens in the other list
            result[id.upper()] = source
        except TypeError:
            break

    return result


def getMonumentCommonscats(commonsTrackerCategory, conn, cursor):
    result = {}

    query = u"""SELECT page_title, cl_sortkey FROM page JOIN categorylinks ON page_id=cl_from WHERE page_namespace=14 AND page_is_redirect=0 AND cl_to=%s"""

    cursor.execute(query, (commonsTrackerCategory,))

    while True:
        try:
            row = cursor.fetchone()
            (category, id) = row
            result[id] = category
        except TypeError:
            break

    return result


def makeStatistics(mconfig, totals):
    text = u'{| class="wikitable sortable"\n'
    text += \
        u'! country !! lang !! total !! page !! row template !! Commons template\n'

    totalCategories = 0
    for ((countrycode, lang), countryconfig) in sorted(mconfig.countries.items()):
        if countryconfig.get('skip'):
            continue
        if countryconfig.get('missingCommonscatPage') and countryconfig.get('commonsTemplate'):
            text += u'|-\n'
            text += u'| %s ' % countrycode
            text += u'|| %s ' % lang
            text += u'|| %s ' % totals.get((countrycode, lang))
            totalCategories += totals.get((countrycode, lang))
            text += u'|| [[:%s:%s|%s]] ' % (lang, countryconfig.get(
                'missingCommonscatPage'), countryconfig.get('missingCommonscatPage'))
            text += u'|| [[:%s:Template:%s|%s]] ' % (
                lang, countryconfig.get('rowTemplate'), countryconfig.get('rowTemplate'))
            text += \
                u'|| {{tl|%s}}\n' % countryconfig.get('commonsTemplate')
    text += u'|- class="sortbottom"\n'
    text += u'| || || %s \n' % totalCategories
    text += u'|}\n'

    site = pywikibot.Site('commons', 'commons')
    page = pywikibot.Page(
        site, u'Commons:Monuments database/Missing commonscat links/Statistics')

    comment = u'Updating missing commonscat links statistics. Total missing links: %s' % totalCategories
    pywikibot.debug(text, _logger)
    common.save_to_wiki_or_local(page, comment, text)


def main():
    countrycode = u''
    lang = u''
    skip_wd = False
    conn = None
    cursor = None
    # Connect database, we need that
    (conn, cursor) = connect_to_monuments_database()
    (conn2, cursor2) = connect_to_commons_database()

    for arg in pywikibot.handleArgs():
        option, sep, value = arg.partition(':')
        if option == '-countrycode':
            countrycode = value
        elif option == '-langcode':
            lang = value
        elif option == '-skip_wd':
            skip_wd = True
        else:
            raise Exception(
                u'Bad parameters. Expected "-countrycode", "-langcode", '
                u'"-skip_wd" or pywikibot args. '
                u'Found "{}"'.format(option))

    if countrycode and lang:
        if not mconfig.countries.get((countrycode, lang)):
            pywikibot.warning(
                u'I have no config for countrycode "%s" in language "%s"' % (countrycode, lang))
            return False
        pywikibot.log(
            u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
        processCountry(countrycode, lang, mconfig.countries.get(
            (countrycode, lang)), conn, cursor, conn2, cursor2)
    elif countrycode or lang:
        raise Exception(u'The "countrycode" and "langcode" arguments must '
                        u'be used together.')
    else:
        totals = {}
        for (countrycode, lang), countryconfig in mconfig.countries.iteritems():
            if (countryconfig.get('skip') or
                    (skip_wd and (countryconfig.get('type') == 'sparql'))):
                continue
            pywikibot.log(
                u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
            totals[(countrycode, lang)] = processCountry(
                countrycode, lang, countryconfig, conn, cursor, conn2, cursor2)
        makeStatistics(mconfig, totals)

    close_database_connection(conn, cursor)


if __name__ == "__main__":
    main()
