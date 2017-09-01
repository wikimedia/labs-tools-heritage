#!/usr/bin/python
# -*- coding: utf-8  -*-
'''

Make a gallery of unused photos so people can add them to monument lists

Usage:
# loop thtough all countries
python unused_monument_images.py
# work on specific country-lang
python unused_monument_images.py -countrycode:XX -langcode:YY

'''
import pywikibot

import monuments_config as mconfig
import common as common
from database_connection import (
    close_database_connection,
    connect_to_monuments_database,
    connect_to_commons_database
)

_logger = "unused_images"


def processCountry(countrycode, lang, countryconfig, conn, cursor, conn2, cursor2):
    '''
    Work on a single country.
    '''
    if not countryconfig.get('unusedImagesPage'):
        # unusedImagesPage not set, just skip silently.
        return False

    unusedImagesPage = countryconfig.get('unusedImagesPage')
    project = countryconfig.get('project', u'wikipedia')
    commonsTrackerCategory = countryconfig.get(
        'commonsTrackerCategory').replace(u' ', u'_')

    withoutPhoto = getMonumentsWithoutPhoto(countrycode, lang, conn, cursor)
    photos = getMonumentPhotos(commonsTrackerCategory, conn2, cursor2)

    pywikibot.log(u'withoutPhoto %s elements' % (len(withoutPhoto),))
    pywikibot.log(u'photos %s elements' % (len(photos),))

    # People can add a /header template for with more info
    text = u'{{#ifexist:{{FULLPAGENAME}}/header | {{/header}} }}\n'
    text += u'<gallery>\n'
    totalImages = 0
    maxImages = 1000

    for catSortKey in sorted(photos.keys()):
        try:
            monumentId = unicode(catSortKey, 'utf-8')
            # Just want the first line
            mLines = monumentId.splitlines()
            monumentId = mLines[0]
            # Remove leading and trailing spaces
            monumentId = monumentId.strip()

            # No try some variants until we have a hit

            # Only remove leading zero's if we don't have a hit.
            if monumentId not in withoutPhoto:
                monumentId = monumentId.lstrip(u'0')
            # Only remove leading underscores if we don't have a hit.
            if monumentId not in withoutPhoto:
                monumentId = monumentId.lstrip(u'_')
            # Only all uppercase if we don't have a hit.
            if monumentId not in withoutPhoto:
                monumentId = monumentId.upper()

            if monumentId in withoutPhoto:
                try:
                    source_link = common.get_source_link(
                        withoutPhoto.get(monumentId),
                        countryconfig.get('type'),
                        monumentId)
                except ValueError:
                    pywikibot.warning(
                        u'Could not find wikiSourceList for %s (%s)' % (
                            monumentId, withoutPhoto.get(monumentId)))
                    continue
                imageName = photos.get(catSortKey)
                # pywikibot.output(u'Key %s returned a result' % (monumentId,))
                # pywikibot.output(imageName)
                if totalImages <= maxImages:
                    text += u'File:{0}|{1}\n'.format(
                        unicode(imageName, 'utf-8'), source_link)
                totalImages += 1
        except ValueError:
            pywikibot.warning(u'Got value error for %s' % (monumentId,))

    text += u'</gallery>'

    if totalImages >= maxImages:
        text += \
            u'<!-- Maximum number of images reached: %s, total of unused images: %s -->\n' % (
                maxImages, totalImages)
        comment = u'Images to be used in monument lists: %s (gallery maximum reached), total of unused images: %s' % (
            maxImages, totalImages)
    else:
        comment = u'Images to be used in monument lists: %s' % totalImages

    # text += getInterwikisUnusedImages(countrycode, lang)

    site = pywikibot.Site(lang, project)
    page = pywikibot.Page(site, unusedImagesPage)
    pywikibot.debug(text, _logger)
    page.put(text, comment, minorEdit=False)

    return totalImages


def getInterwikisUnusedImages(countrycode, lang):
    result = u''
    for (countrycode2, lang2), countryconfig in mconfig.countries.iteritems():
        if countrycode == countrycode2 and lang != lang2:
            if countryconfig.get('unusedImagesPage'):
                result += \
                    u'[[%s:%s]]\n' % (
                        lang2, countryconfig.get('unusedImagesPage'))

    return result


def getMonumentsWithoutPhoto(countrycode, lang, conn, cursor):
    result = {}

    query = u"""SELECT id, source FROM monuments_all WHERE image='' AND country=%s AND lang=%s"""

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


def getMonumentPhotos(commonsTrackerCategory, conn, cursor):
    result = {}

    query = u"""SELECT page_title, cl_sortkey FROM page JOIN categorylinks ON page_id=cl_from WHERE page_namespace=6 AND page_is_redirect=0 AND cl_to=%s"""

    cursor.execute(query, (commonsTrackerCategory,))

    while True:
        try:
            row = cursor.fetchone()
            (image, id) = row
            result[id] = image
        except TypeError:
            break

    return result


def makeStatistics(mconfig, totals):
    text = u'{| class="wikitable sortable"\n'
    text += \
        u'! country !! lang !! data-sort-type="number"|total !! page !! row template !! Commons template\n'

    totalImages = 0
    for ((countrycode, lang), countryconfig) in sorted(mconfig.countries.items()):
        if countryconfig.get('unusedImagesPage') and countryconfig.get('commonsTemplate'):
            text += u'|-\n'
            text += u'| %s ' % countrycode
            text += u'|| %s ' % lang
            text += u'|| %s ' % totals.get((countrycode, lang))
            totalImages += totals.get((countrycode, lang))
            text += u'|| [[:%s:%s|%s]] ' % (lang, countryconfig.get(
                'unusedImagesPage'), countryconfig.get('unusedImagesPage'))
            text += u'|| [[:%s:Template:%s|%s]] ' % (
                lang, countryconfig.get('rowTemplate'), countryconfig.get('rowTemplate'))
            text += \
                u'|| {{tl|%s}}\n' % countryconfig.get('commonsTemplate')
    text += u'|- class="sortbottom"\n'
    text += u'| || || %s \n' % totalImages
    text += u'|}\n'

    site = pywikibot.Site('commons', 'commons')
    page = pywikibot.Page(
        site, u'Commons:Monuments database/Unused images/Statistics')

    comment = u'Updating unused image statistics. Total unused images: %s' % totalImages
    pywikibot.debug(text, _logger)
    page.put(newtext=text, comment=comment)


def main():
    countrycode = u''
    lang = u''
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
        else:
            raise Exception(
                u'Bad parameters. Expected "-countrycode", "-langcode" or '
                u'pywikibot args. Found "{}"'.format(option))

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
            pywikibot.log(
                u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
            totals[(countrycode, lang)] = processCountry(
                countrycode, lang, countryconfig, conn, cursor, conn2, cursor2)
        makeStatistics(mconfig, totals)

    close_database_connection(conn, cursor)


if __name__ == "__main__":
    main()
