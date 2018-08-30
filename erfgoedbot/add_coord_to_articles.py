#!/usr/bin/python
# -*- coding: utf-8  -*-
'''

get coordinates from the Monuments database and
    add coordinate template to articles in Wikipedia

@author Kentaur

Usage:
# loop through all countries
python add_coord_to_articles.py

# work on specific country-lang
python add_coord_to_articles.py -countrycode:XX -langcode:YY

'''
import re

import pywikibot

import common as common
import monuments_config as mconfig
from database_connection import (
    close_database_connection,
    connect_to_commons_database,
    connect_to_monuments_database
)

# coordinate templates for different language wikipedias
wikiData = {
    ('et'): {
        'coordTemplate': 'Coordinate',
        # coordTemplateSyntax % (lat, lon, countrycode.upper() )
        'coordTemplateSyntax': u'{{Coordinate|NS=%f|EW=%f|type=landmark|region=%s}}'
    },
    ('fr'): {
        'coordTemplate': 'coord',
        # {{coord|52.51626|13.3777|type:landmark_region:DE|format=dms|display=title}}
        'coordTemplateSyntax': u'{{coord|%f|%f|type:landmark_region=%s|format=dms|display=title}}'
    }
}


# "constants"

# wikipedia article namespace
WP_ARTICLE_NS = 0
# wikipedia category namespace
WP_CATEGORY_NS = 14
# output debug messages
DEBUG = True


# classes

class Monument:
    # Constructor with default arguments
    def __init__(self, id=None):
        self.id = id
        self.name = u''
        self.country = u''
        self.wikilang = u''
        self.article = u''
        self.lat = None
        self.lon = None
        self.source = u''


# functions


def processCountry(countryconfig, coordconfig, connMon, cursorMon):
    '''
    Work on a single country.
    '''
    if (not coordconfig or not coordconfig.get('coordTemplate')):
        # No template found, just skip.
        pywikibot.output(
            u'Language: {0} has no coordTemplate set!'.format(
                countryconfig.get('lang')))
        return False

    (connWiki, cursorWiki) = connect_to_commons_database(
        countryconfig.get('lang'))

    withCoordinates = getMonumentsWithCoordinates(
        countryconfig.get('country'), countryconfig.get('lang'), cursorMon)

    articleNames = []
    duplicateArticles = []
    monumentsWithArticle = []

    for aMonument in withCoordinates:
        article_name = u''
        result = re.match("\[\[(.+?)\|.+?\]\]", aMonument.name)
        if (result and result.group(1)):
            article_name = result.group(1)

        result = re.match("\[\[([^\|]+?)\]\]", aMonument.name)
        if (result and result.group(1)):
            article_name = result.group(1)

        if (article_name):
            if article_name not in duplicateArticles:
                if article_name in articleNames:
                    duplicateArticles.append(article_name)
                    articleNames.remove(article_name)
                    for sMon in monumentsWithArticle:
                        if (sMon.article == article_name):
                            monumentsWithArticle.remove(sMon)
                            break
                else:
                    articleNames.append(article_name)
                    aMonument.article = article_name
                    monumentsWithArticle.append(aMonument)

    if len(duplicateArticles):
        pywikibot.output(u'Multiple references to following articles: %s in monument lists! Skipped those.' % duplicateArticles[:])

    for aMonument in monumentsWithArticle:
        PageNs = WP_ARTICLE_NS
        followRedirect = True
        (retStatus, pageId, redirNs, redirTitle) = getPageId(aMonument.article, connWiki, cursorWiki, PageNs, followRedirect)
        if (retStatus == 'FOLLOWED_REDIR' and redirNs == WP_ARTICLE_NS):
            aMonument.article = redirTitle
        if (pageId):
            if not hasCoordinates(pageId, countryconfig.get('lang'), cursorWiki):
                addCoords(countryconfig, aMonument, coordconfig)


def getMonumentsWithCoordinates(countrycode, lang, cursor):
    '''
    Get monuments with coordinates from monuments database for a certain country/language combination.
    '''
    result = []
    query = (
        u"SELECT id, name, lat, lon, source "
        u"FROM monuments_all "
        u"WHERE lat<>0 AND lon<>0 AND country=%s AND lang=%s")
    cursor.execute(query, (countrycode, lang))

    # result = cursor.fetchall ()
    while True:
        try:
            row = cursor.fetchone()
            aMon = Monument()
            aMon.country = countrycode
            aMon.wikilang = lang
            (aMon.id, aMon.name, aMon.lat, aMon.lon, aMon.source) = row
            result.append(aMon)
        except TypeError:
            break

    return result


def hasCoordinates(pageId, lang, cursor):
    '''
    check if Article has Article coords in WP coords DB
    '''

    if (pageId and lang):
        coordTable = 'u_dispenser_p.coord_' + lang + 'wiki'

        # check if primary coordinate i.e. article coordinate exists for pageId
        query = (
            u"SELECT gc_from "
            u"FROM %s "
            u"WHERE (gc_from = %d AND gc_primary = 1) "
            u"LIMIT 1")
        # FIXME escape & sanitize coordTable and pageId
        cursor.execute(query, (coordTable, int(pageId)))

        if (cursor.rowcount > 0):
            return True
        else:
            return False
    else:
        return False


def getPageId(pageName, conn, cursor,
              pageNamespace=WP_ARTICLE_NS, followRedirect=False):
    '''
    get Wikipedia pagename pageId
    '''

    # underscores
    pageName = pageName.replace(u' ', u'_')
    retStatus = ''
    pageId = ''
    redirNs = ''
    redirTitle = u''

    # FIXME page_titles like 'Château_de_Bercy' won't work, but titles like 'Käru' do ??
    query = (
        u"SELECT page_id, page_is_redirect "
        u"FROM page "
        u"WHERE page_namespace = %s AND page_title = %s")
    cursor.execute(query, (pageNamespace, pageName))
    if DEBUG:
        print cursor._executed
        print u'rowcount: %d ' % cursor.rowcount

    if (cursor.rowcount > 0):
        row = cursor.fetchone()
        (pageId, IsRedirect) = row
        if (IsRedirect):
            if (followRedirect):
                (redirNs, redirTitle) = getRedirPageNsTitle(pageId, cursor)
                redirTitle = unicode(redirTitle, "utf-8")
                (dummy0, pageId, dummy1, dummy2) = getPageId(redirTitle, conn, cursor, redirNs)
                retStatus = 'FOLLOWED_REDIR'
            else:
                retStatus = 'REDIRECT'
        else:
            retStatus = 'OK'

    return (retStatus, pageId, redirNs, redirTitle)


def getRedirPageNsTitle(pageId, cursor):
    '''
    Get redirect page namespace and title.
    '''

    if (pageId):
        pageNs = ''
        pageTitle = u''

        query = (
            u"SELECT rd_namespace, rd_title "
            u"FROM redirect "
            u"WHERE rd_from = %s")
        cursor.execute(query, (pageId,))

        if (cursor.rowcount > 0):
            row = cursor.fetchone()
            (pageNs, pageTitle) = row

        return (pageNs, pageTitle)


def addCoords(countryconfig, monument, coordconfig):
    '''
    Add the coordinates to article.
    '''
    countrycode = countryconfig.get('country')
    lang = countryconfig.get('lang')
    if (countrycode and lang):
        coordTemplate = coordconfig.get('coordTemplate')
        coordTemplateSyntax = coordconfig.get('coordTemplateSyntax')
        site = pywikibot.getSite(lang, 'wikipedia')

        page = pywikibot.Page(site, monument.article)
        try:
            text = page.get()
        except pywikibot.NoPage:  # First except, prevent empty pages
            return False
        except pywikibot.IsRedirectPage:  # second except, prevent redirect
            pywikibot.output(u'%s is a redirect!' % monument.article)
            return False
        except pywikibot.Error:  # third exception, take the problem and print
            pywikibot.output(u"Some error, skipping..")
            return False

        if coordTemplate in page.templates():
            return False

        newtext = text
        replCount = 1
        coordText = coordTemplateSyntax % (monument.lat, monument.lon,
                                           countrycode.upper())
        localCatName = pywikibot.getSite().namespace(WP_CATEGORY_NS)
        catStart = r'\[\[(' + localCatName + '|Category):'
        catStartPlain = u'[[' + localCatName + ':'
        replacementText = u''
        replacementText = coordText + '\n\n' + catStartPlain

        # insert coordinate template before categories
        newtext = re.sub(catStart, replacementText, newtext, replCount, flags=re.IGNORECASE)

        if text != newtext:
            try:
                source_link = common.get_source_link(
                    monument.source,
                    countryconfig.get('type'))
            except ValueError:
                source_link = ''
            comment = u'Adding template %s based on %s, # %s' % (coordTemplate, source_link, monument.id)
            pywikibot.showDiff(text, newtext)
            modPage = pywikibot.input(u'Modify page: %s ([y]/n) ?' % (monument.article))
            if (modPage.lower == 'y' or modPage == ''):
                page.put(newtext, comment)
            return True
        else:
            return False
    else:
        return False


def main():
    countrycode = u''
    lang = u''
    skip_wd = False
    connMon = None
    cursorMon = None

    (connMon, cursorMon) = connect_to_monuments_database()

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
                u'"-skip_wd" or pywikibot args. Found "{}"'.format(option))

    if countrycode and lang:
        if not mconfig.countries.get((countrycode, lang)):
            pywikibot.output(u'I have no config for countrycode "%s" in language "%s"' % (countrycode, lang))
            return False
        pywikibot.output(u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
        processCountry(mconfig.countries.get((countrycode, lang)),
                       wikiData.get(lang), connMon, cursorMon)
    elif countrycode or lang:
        raise Exception(u'The "countrycode" and "langcode" arguments must '
                        u'be used together.')
    else:
        for (countrycode, lang), countryconfig in mconfig.filtered_countries(
                skip_wd=skip_wd):
            pywikibot.output(u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
            processCountry(
                countryconfig, wikiData.get(lang), connMon, cursorMon)

    close_database_connection(connMon, cursorMon)


if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
