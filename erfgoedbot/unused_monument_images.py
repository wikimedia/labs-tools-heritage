#!/usr/bin/python
# -*- coding: utf-8  -*-
'''

Make a gallery of unused photos so people can add them to monument lists

Usage:
# loop thtough all countries
python unused_monument_images.py
# work on specific country-lang
python unused_monument_images.py -countrycode:XX -lang:YY

'''
import monuments_config as mconfig
import pywikibot
from pywikibot import config
import re
import MySQLdb


def connectDatabase():
    '''
    Connect to the rijksmonumenten mysql database, if it fails, go down in flames
    '''
    conn = MySQLdb.connect(host=mconfig.db_server, db=mconfig.db, user=config.db_username,
                           passwd=config.db_password, use_unicode=True, charset='utf8')
    conn.ping(True)
    cursor = conn.cursor()
    return (conn, cursor)


def connectDatabase2():
    '''
    Connect to the commons mysql database, if it fails, go down in flames
    '''
    conn = MySQLdb.connect('commonswiki.labsdb', db='commonswiki_p',
                           user=config.db_username, passwd=config.db_password, use_unicode=True, charset='latin1')
    cursor = conn.cursor()
    return (conn, cursor)


def processCountry(countrycode, lang, countryconfig, conn, cursor, conn2, cursor2):
    '''
    Work on a single country.
    '''
    if not countryconfig.get('unusedImagesPage'):
        # unusedImagesPage not set, just skip silently.
        return False

    unusedImagesPage = countryconfig.get('unusedImagesPage')
    commonsTrackerCategory = countryconfig.get(
        'commonsTrackerCategory'). replace(u' ', u'_')

    withoutPhoto = getMonumentsWithoutPhoto(countrycode, lang, conn, cursor)
    photos = getMonumentPhotos(commonsTrackerCategory, conn2, cursor2)

    pywikibot.output(u'withoutPhoto %s elements' % (len(withoutPhoto),))
    pywikibot.output(u'photos %s elements' % (len(photos),))

    # People can add a /header template for with more info
    text = u'{{#ifexist:{{FULLPAGENAME}}/header | {{/header}} }}\n'
    text = text + u'<gallery>\n'
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
                m = re.search(
                    '^[^\?]+\?title\=(.+?)&', withoutPhoto.get(monumentId))
                try:
                    wikiSourceList = m.group(1)
                except AttributeError:
                    pywikibot.output(u'Could not find wikiSourceList for %s (%s)' % (monumentId, withoutPhoto.get(monumentId)))
                    continue
                imageName = photos.get(catSortKey)
                # pywikibot.output(u'Key %s returned a result' % (monumentId,))
                # pywikibot.output(wikiSourceList)
                # pywikibot.output(imageName)
                if totalImages <= maxImages:
                    text = text + \
                        u'File:%s|[[%s|%s]]\n' % (
                            unicode(imageName, 'utf-8'), wikiSourceList, monumentId)
                totalImages = totalImages + 1
        except ValueError:
            pywikibot.output(u'Got value error for %s' % (monumentId,))

    text = text + u'</gallery>'

    if totalImages >= maxImages:
        text = text + \
            u'<!-- Maximum number of images reached: %s, total of unused images: %s -->\n' % (
                maxImages, totalImages)
        comment = u'Images to be used in monument lists: %s (gallery maximum reached), total of unused images: %s' % (
            maxImages, totalImages)
    else:
        comment = u'Images to be used in monument lists: %s' % totalImages

    # text = text + getInterwikisUnusedImages(countrycode, lang)

    site = pywikibot.Site(lang, u'wikipedia')
    page = pywikibot.Page(site, unusedImagesPage)
    pywikibot.output(text)
    page.put(text, comment)

    return totalImages


def getInterwikisUnusedImages(countrycode, lang):
    result = u''
    for (countrycode2, lang2), countryconfig in mconfig.countries.iteritems():
        if countrycode == countrycode2 and lang != lang2:
            if countryconfig.get('unusedImagesPage'):
                result = result + \
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
    text = text + \
        u'! country !! lang !! data-sort-type="number"|total !! page !! row template !! Commons template\n'

    totalImages = 0
    for ((countrycode, lang), countryconfig) in sorted(mconfig.countries.items()):
        if countryconfig.get('unusedImagesPage') and countryconfig.get('commonsTemplate'):
            text = text + u'|-\n'
            text = text + u'| %s ' % countrycode
            text = text + u'|| %s ' % lang
            text = text + u'|| %s ' % totals.get((countrycode, lang))
            totalImages = totalImages + totals.get((countrycode, lang))
            text = text + u'|| [[:%s:%s|%s]] ' % (lang, countryconfig.get(
                'unusedImagesPage'), countryconfig.get('unusedImagesPage'))
            text = text + u'|| [[:%s:Template:%s|%s]] ' % (
                lang, countryconfig.get('rowTemplate'), countryconfig.get('rowTemplate'))
            text = text + \
                u'|| {{tl|%s}}\n' % countryconfig.get('commonsTemplate')
    text = text + u'|- class="sortbottom"\n'
    text = text + u'| || || %s \n' % totalImages
    text = text + u'|}\n'

    site = pywikibot.Site('commons', 'commons')
    page = pywikibot.Page(
        site, u'Commons:Monuments database/Unused images/Statistics')

    comment = u'Updating unused image statistics. Total unused images: %s' % totalImages
    pywikibot.output(text)
    page.put(newtext=text, comment=comment)


def main():
    countrycode = u''
    conn = None
    cursor = None
    # Connect database, we need that
    (conn, cursor) = connectDatabase()
    (conn2, cursor2) = connectDatabase2()

    for arg in pywikibot.handleArgs():
        if arg.startswith('-countrycode:'):
            countrycode = arg[len('-countrycode:'):]

    if countrycode:
        lang = pywikibot.Site().language()
        if not mconfig.countries.get((countrycode, lang)):
            pywikibot.output(
                u'I have no config for countrycode "%s" in language "%s"' % (countrycode, lang))
            return False
        pywikibot.output(
            u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
        processCountry(countrycode, lang, mconfig.countries.get(
            (countrycode, lang)), conn, cursor, conn2, cursor2)
    else:
        totals = {}
        for (countrycode, lang), countryconfig in mconfig.countries.iteritems():
            pywikibot.output(
                u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
            totals[(countrycode, lang)] = processCountry(
                countrycode, lang, countryconfig, conn, cursor, conn2, cursor2)
        makeStatistics(mconfig, totals)


if __name__ == "__main__":
    main()
