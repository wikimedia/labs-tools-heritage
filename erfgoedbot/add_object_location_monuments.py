#!/usr/bin/python
# -*- coding: utf-8  -*-
'''

Bot to add {{Object location dec}} to monuments. Location is based on information from the monuments database.

'''
import pywikibot

import common as common
import monuments_config as mconfig
from database_connection import (
    close_database_connection,
    connect_to_commons_database,
    connect_to_monuments_database
)


def locateCountry(countryconfig, conn, cursor, conn2, cursor2):
    '''
    Locate images in a single country.
    '''
    if not countryconfig.get('commonsTemplate') or not countryconfig.get('commonsTrackerCategory'):
        # Not possible for this country. Silently return
        return False

    for (page, monumentId) in getMonumentsWithoutLocation(countryconfig, conn2, cursor2):
        locationTemplate = locateImage(
            page, monumentId, countryconfig, conn, cursor)
        if locationTemplate:
            addLocation(page, locationTemplate)


def getMonumentsWithoutLocation(countryconfig, conn2, cursor2):
    site = pywikibot.getSite(u'commons', u'commons')
    query = (
        u"SELECT page_title, cl_sortkey_prefix "
        u"FROM page "
        u"JOIN templatelinks ON page_id=tl_from "
        u"JOIN categorylinks ON page_id=cl_from "
        u"WHERE page_namespace=6 AND page_is_redirect=0 "
        u"AND tl_namespace=10 AND tl_title=%s "
        u"AND cl_to=%s AND NOT EXISTS({sub}) "
        u"LIMIT 10000")
    subquery = (
        u"SELECT * "
        u"FROM categorylinks AS loccat "
        u"WHERE page_id=loccat.cl_from "
        u"AND loccat.cl_to='Media_with_locations'"
    )
    commonsTemplate = countryconfig.get('commonsTemplate').replace(u' ', u'_')
    commonsTrackerCategory = countryconfig.get(
        'commonsTrackerCategory').replace(u' ', u'_')

    cursor2.execute(
        query.format(sub=subquery), (
            commonsTemplate.encode('utf-8'),
            commonsTrackerCategory.encode('utf-8')))

    while True:
        try:
            pageName, sortkey = cursor2.fetchone()
        except TypeError:
            # Nothing left
            break
        if pageName and sortkey:
            page = pywikibot.Page(site, 'File:' + unicode(pageName, 'utf-8'))
            try:
                monumentId = unicode(sortkey, 'utf-8', errors='replace')
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
                yield (page, monumentId)
            except ValueError:
                pywikibot.output(u'Got value error for %s' % (monumentId,))


def locateImage(page, monumentId, countryconfig, conn, cursor):
    pywikibot.output(u'Working on: %s with id %s' % (page.title(), monumentId))

    # First check if the identifier returns something useful
    coordinates = getCoordinates(
        monumentId, countryconfig.get('country'), countryconfig.get('lang'),
        conn, cursor)
    if not coordinates:
        pywikibot.output(
            u'File contains an unknown identifier: %s' % monumentId)
        return False

    (lat, lon, source) = coordinates

    # Ok. We know we have coordinates. Now check to be sure to see if there's
    # not already a template on the page.
    templates = page.templates()

    if (u'Location' in templates or
            u'Location dec' in templates or
            u'Object location' in templates or
            u'Object location dec' in templates):
        pywikibot.output(
            u'Location template already found at: %s' % page.title())
        return False

    locationTemplate = u'{{Object location dec|%s|%s|region:%s_type:landmark_scale:1500}}<!-- Location from %s -->' % (
        lat, lon, countryconfig.get('country').upper(), source)

    return locationTemplate


def getCoordinates(monumentId, countrycode, lang, conn, cursor):
    '''
    Get coordinates from the erfgoed database
    '''
    query = (
        u"SELECT lat, lon, source "
        u"FROM monuments_all "
        u"WHERE id=%s "
        u"AND country=%s "
        u"AND lang=%s "
        u"AND NOT lat=0 AND NOT lon=0 "
        u"AND NOT lat='' AND NOT lon='' "
        u"AND NOT lat IS NULL AND NOT lon IS NULL "
        u"LIMIT 1")

    cursor.execute(query, (monumentId, countrycode, lang,))

    try:
        row = cursor.fetchone()
        return row
    except TypeError:
        return False


def addLocation(page, locationTemplate):
    try:
        oldtext = page.get()
    except pywikibot.NoPage:
        # For some reason we sometimes get a NoPage Exception
        pywikibot.output(u'No text found at %s. Skipping' % (page.title(),))
        return False

    comment = u'Adding object location based on monument identifier'

    newtext = putAfterTemplate(
        oldtext, u'Information', locationTemplate, loose=True)
    pywikibot.showDiff(oldtext, newtext)
    common.save_to_wiki_or_local(page, comment, newtext)


def putAfterTemplate(oldtext, template, toadd, loose=True):
    '''
    Try to put text after template.
    If the template is not found return False if loose is set to False
    If loose is set to True: Remove interwiki's, categories, add template, restore categories, restore interwiki's.

    Based on cc-by-sa-3.0 code by Dschwen
    '''
    newtext = u''

    templatePosition = oldtext.find(u'{{%s' % (template,))

    if templatePosition >= 0:
        previousChar = u''
        currentChar = u''
        templatePosition += 2
        curly = 1
        square = 0

        while templatePosition < len(oldtext):
            currentChar = oldtext[templatePosition]

            if currentChar == u'[' and previousChar == u'[':
                square += 1
                previousChar = u''
            if currentChar == u']' and previousChar == u']':
                square -= 1
                previousChar = u''
            if currentChar == u'{' and previousChar == u'{':
                curly += 1
                previousChar = u''
            if currentChar == u'}' and previousChar == u'}':
                curly -= 1
                previousChar = u''

            previousChar = currentChar
            templatePosition += 1

            if curly == 0 and square <= 0:
                # Found end of template
                break
        newtext = oldtext[:templatePosition] + \
            u'\n' + toadd + oldtext[templatePosition:]

    else:
        if loose:
            newtext = oldtext
            cats = pywikibot.getCategoryLinks(newtext)
            ll = pywikibot.getLanguageLinks(newtext)
            newtext = pywikibot.removeLanguageLinks(newtext)
            newtext = pywikibot.removeCategoryLinks(newtext)
            newtext += u'\n' + toadd
            newtext = pywikibot.replaceCategoryLinks(newtext, cats)
            newtext = pywikibot.replaceLanguageLinks(newtext, ll)

    return newtext


def main():
    countrycode = u''
    lang = u''
    skip_wd = False

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

    pywikibot.setSite(pywikibot.getSite(u'commons', u'commons'))

    if countrycode and lang:
        if not mconfig.countries.get((countrycode, lang)):
            pywikibot.output(
                u'I have no config for countrycode "%s" in language "%s"' % (countrycode, lang))
            return False
        pywikibot.output(
            u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
        locateCountry(mconfig.countries.get((countrycode, lang)),
                      conn, cursor, conn2, cursor2)
    elif countrycode or lang:
        raise Exception(u'The "countrycode" and "langcode" arguments must '
                        u'be used together.')
    else:
        for (countrycode, lang), countryconfig in mconfig.countries.iteritems():
            if (countryconfig.get('skip') or
                    (skip_wd and (countryconfig.get('type') == 'sparql'))):
                continue
            if not countryconfig.get('autoGeocode'):
                pywikibot.output(
                    u'"%s" in language "%s" is not supported in auto geocode mode (yet).' % (countrycode, lang))
            else:
                pywikibot.output(
                    u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
                locateCountry(countryconfig, conn, cursor, conn2, cursor2)

    close_database_connection(conn, cursor)


if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
