#!/usr/bin/python
# -*- coding: utf-8  -*-
'''

Bot to add {{Object location dec}} to monuments. Location is based on information from the monuments database.

'''
import pywikibot

import erfgoedbot.common as common
import erfgoedbot.monuments_config as mconfig
from erfgoedbot.database_connection import (
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
    site = pywikibot.getSite('commons', 'commons')
    query = (
        "SELECT page_title, cl_sortkey_prefix "
        "FROM page "
        "JOIN templatelinks ON page_id=tl_from "
        "JOIN categorylinks ON page_id=cl_from "
        "JOIN linktarget ON tl_target_id=lt_id "
        "WHERE page_namespace=6 AND page_is_redirect=0 "
        "AND lt_namespace=10 AND lt_title=%s "
        "AND cl_to=%s AND NOT EXISTS({sub}) "
        "LIMIT 10000")
    subquery = (
        "SELECT * "
        "FROM categorylinks AS loccat "
        "WHERE page_id=loccat.cl_from "
        "AND loccat.cl_to='Media_with_locations'"
    )
    commonsTemplate = countryconfig.get('commonsTemplate').replace(' ', '_')
    commonsTrackerCategory = countryconfig.get(
        'commonsTrackerCategory').replace(' ', '_')

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
            if not isinstance(pageName, str):
                pageName = str(pageName, encoding='utf-8')
            page = pywikibot.Page(site, 'File:' + pageName)
            try:
                if not isinstance(sortkey, str):
                    monumentId = str(sortkey, encoding='utf-8', errors='replace')
                else:
                    monumentId = sortkey
                # Just want the first line
                mLines = monumentId.splitlines()
                monumentId = mLines[0]
                # Remove leading and trailing spaces
                monumentId = monumentId.strip()
                # Remove leading zero's. FIXME: This should be replaced with
                # underscores
                monumentId = monumentId.lstrip('0')
                # Remove leading underscors.
                monumentId = monumentId.lstrip('_')
                yield (page, monumentId)
            except ValueError:
                pywikibot.output('Got value error for %s' % (monumentId,))


def locateImage(page, monumentId, countryconfig, conn, cursor):
    pywikibot.output('Working on: %s with id %s' % (page.title(), monumentId))

    # First check if the identifier returns something useful
    coordinates = getCoordinates(
        monumentId, countryconfig.get('country'), countryconfig.get('lang'),
        conn, cursor)
    if not coordinates:
        pywikibot.output(
            'File contains an unknown identifier: %s' % monumentId)
        return False

    (lat, lon, source) = coordinates

    # Ok. We know we have coordinates. Now check to be sure to see if there's
    # not already a template on the page.
    templates = page.templates()

    if ('Location' in templates or
            'Location dec' in templates or
            'Object location' in templates or
            'Object location dec' in templates):
        pywikibot.output(
            'Location template already found at: %s' % page.title())
        return False

    locationTemplate = '{{Object location dec|%s|%s|region:%s_type:landmark_scale:1500}}<!-- Location from %s -->' % (
        lat, lon, countryconfig.get('country').upper(), source)

    return locationTemplate


def getCoordinates(monumentId, countrycode, lang, conn, cursor):
    '''
    Get coordinates from the erfgoed database
    '''
    query = (
        "SELECT lat, lon, source "
        "FROM monuments_all "
        "WHERE id=%s "
        "AND country=%s "
        "AND lang=%s "
        "AND NOT lat=0 AND NOT lon=0 "
        "AND NOT lat='' AND NOT lon='' "
        "AND NOT lat IS NULL AND NOT lon IS NULL "
        "LIMIT 1")

    cursor.execute(query, (monumentId, countrycode, lang,))

    try:
        row = cursor.fetchone()
        return row
    except TypeError:
        return False


def addLocation(page, locationTemplate):
    try:
        oldtext = page.get()
    except pywikibot.exceptions.NoPageError:
        # For some reason we sometimes get a NoPageError Exception
        pywikibot.output('No text found at %s. Skipping' % (page.title(),))
        return False

    comment = 'Adding object location based on monument identifier'

    newtext = putAfterTemplate(
        oldtext, 'Information', locationTemplate, loose=True)
    pywikibot.showDiff(oldtext, newtext)
    common.save_to_wiki_or_local(page, comment, newtext)


def putAfterTemplate(oldtext, template, toadd, loose=True):
    '''
    Try to put text after template.
    If the template is not found return False if loose is set to False
    If loose is set to True: Remove interwiki's, categories, add template, restore categories, restore interwiki's.

    Based on cc-by-sa-3.0 code by Dschwen
    '''
    newtext = ''

    templatePosition = oldtext.find('{{%s' % (template,))

    if templatePosition >= 0:
        previousChar = ''
        currentChar = ''
        templatePosition += 2
        curly = 1
        square = 0

        while templatePosition < len(oldtext):
            currentChar = oldtext[templatePosition]

            if currentChar == '[' and previousChar == '[':
                square += 1
                previousChar = ''
            if currentChar == ']' and previousChar == ']':
                square -= 1
                previousChar = ''
            if currentChar == '{' and previousChar == '{':
                curly += 1
                previousChar = ''
            if currentChar == '}' and previousChar == '}':
                curly -= 1
                previousChar = ''

            previousChar = currentChar
            templatePosition += 1

            if curly == 0 and square <= 0:
                # Found end of template
                break
        newtext = oldtext[:templatePosition] + \
            '\n' + toadd + oldtext[templatePosition:]

    else:
        if loose:
            newtext = oldtext
            cats = pywikibot.getCategoryLinks(newtext)
            ll = pywikibot.getLanguageLinks(newtext)
            newtext = pywikibot.removeLanguageLinks(newtext)
            newtext = pywikibot.removeCategoryLinks(newtext)
            newtext += '\n' + toadd
            newtext = pywikibot.replaceCategoryLinks(newtext, cats)
            newtext = pywikibot.replaceLanguageLinks(newtext, ll)

    return newtext


def main():
    countrycode = ''
    lang = ''
    skip_wd = False

    # Connect database, we need that
    (conn, cursor) = connect_to_monuments_database()
    (conn2, cursor2) = connect_to_commons_database()

    for arg in pywikibot.handle_args():
        option, sep, value = arg.partition(':')
        if option == '-countrycode':
            countrycode = value
        elif option == '-langcode':
            lang = value
        elif option == '-skip_wd':
            skip_wd = True
        else:
            raise Exception(
                'Bad parameters. Expected "-countrycode", "-langcode", '
                '"-skip_wd" or pywikibot args. '
                'Found "{}"'.format(option))

    pywikibot.setSite(pywikibot.getSite('commons', 'commons'))

    if countrycode and lang:
        if not mconfig.countries.get((countrycode, lang)):
            pywikibot.output(
                'I have no config for countrycode "%s" in language "%s"' % (countrycode, lang))
            return False
        pywikibot.output(
            'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
        locateCountry(mconfig.countries.get((countrycode, lang)),
                      conn, cursor, conn2, cursor2)
    elif countrycode or lang:
        raise Exception('The "countrycode" and "langcode" arguments must '
                        'be used together.')
    else:
        for (countrycode, lang), countryconfig in mconfig.filtered_countries(
                skip_wd=skip_wd):
            if not countryconfig.get('autoGeocode'):
                pywikibot.output(
                    '"%s" in language "%s" is not supported in auto geocode mode (yet).' % (countrycode, lang))
            else:
                pywikibot.output(
                    'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
                try:
                    locateCountry(countryconfig, conn, cursor, conn2, cursor2)
                except Exception as e:
                    pywikibot.error(
                        'Unknown error occurred when processing country '
                        '{0} in lang {1}\n{2}'.format(countrycode, lang, str(e)))
                    continue

    close_database_connection(conn, cursor)


if __name__ == "__main__":
    pywikibot.log('Start of %s' % __file__)
    try:
        main()
    finally:
        pywikibot.stopme()
