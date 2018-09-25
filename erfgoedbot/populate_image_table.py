#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
Update the image table with all the images tracked by a template in
https://commons.wikimedia.org/wiki/Category:Cultural_heritage_monuments_with_known_IDs

The fields:
* country - same as country field in the monuments_all table
* id - same as the id field in the monuments_all table
* img_name - The filename at Commons

First the bots loops over the configuration and gets:
* countrycode
* commonsTemplate
* commonsTrackerCategory
Some countries are available in multiple languages. This is deduplicated

For each combination the bot will loop over the Commons database and insert the
information into the image table.


Make a gallery of unused photos so people can add them to monument lists

Usage:
# Do everything
python populate_image_table.py
# Do just a specific country
python populate_image_table.py -countrycode:xx
"""
import warnings

import pywikibot

import common as common
import monuments_config as mconfig
from database_connection import (
    close_database_connection,
    connect_to_commons_database,
    connect_to_monuments_database
)
from statistics_table import StatisticsTable

_logger = "populate_image_table"


class CannotNormalizeException(Exception):
    pass


def getSources(countrycode=u'', skip_wd=False):
    """Get a dictionary of sources to go harvest."""
    sources = {}
    for (icountrycode, lang), countryconfig in mconfig.filtered_countries(
            skip_wd=skip_wd):
        if not countrycode or (countrycode and countrycode == icountrycode):
            if icountrycode not in sources:
                if countryconfig.get('commonsTemplate') and countryconfig.get('commonsTrackerCategory'):
                    sources[icountrycode] = {
                        'commonsTemplate': countryconfig.get('commonsTemplate'),
                        'commonsTrackerCategory': countryconfig.get('commonsTrackerCategory'),
                    }
    return sources


def processSources(sources):
    """Loop over all sources and process them."""
    result = sources
    for countrycode, countryconfig in sources.iteritems():
        (totalImages, tracked_images) = processSource(countrycode, countryconfig)
        result[countrycode]['totalImages'] = totalImages
        result[countrycode]['tracked_images'] = tracked_images
    return result


def processSource(countrycode, countryconfig):
    """Work on a single source (country)."""
    pywikibot.log(u'Processing country "{0}"'.format(countrycode))

    commonsTemplate = countryconfig.get('commonsTemplate').replace(u' ', u'_')
    commonsTrackerCategory = countryconfig.get(
        'commonsTrackerCategory').replace(u' ', u'_')

    (conn2, cursor2) = connect_to_commons_database()
    photos = getMonumentPhotos(commonsTrackerCategory, conn2, cursor2)
    cursor2.close()

    pywikibot.log(
        u'For country "%s" I found %s photos tagged with "{{%s}}" in '
        u'[[Category:%s]]' % (countrycode, len(photos), commonsTemplate,
                              commonsTrackerCategory))

    tracked_photos = 0

    (conn, cursor) = connect_to_monuments_database()

    for catSortKey, page_title in photos:
        try:
            monumentId = normalize_identifier(catSortKey)
        except CannotNormalizeException:
            pywikibot.log(
                u'Could not normalize monument identifier {0} ({1})'.format(
                    catSortKey, page_title))
            # We could not normalize the monument identifier: not adding to the table
            continue

        try:
            name = unicode(page_title, 'utf-8')
        except UnicodeDecodeError:
            pywikibot.warning(
                u'Got unicode decode error with name {0} ({1})'.format(
                    name, monumentId))
            # This results in not tracking this file. That may not be the desired behaviour.
            continue
        # UnicodeDecodeError is a subclass of ValueError and should catch most
        except ValueError:
            pywikibot.warning(
                u'Got value error with name {0} ({1})'.format(
                    name, monumentId))
            continue

        image_has_geolocation = has_geolocation(name)

        tracked_photos += 1
        updateImage(countrycode, monumentId, name, image_has_geolocation, conn, cursor)

    close_database_connection(conn, cursor)
    return (len(photos), tracked_photos)


def normalize_identifier(data):
    try:
        monumentId = unicode(data, 'utf-8')
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
        # All uppercase, same happens in other list
        # monumentId = monumentId.upper()
        return monumentId
    except (UnicodeDecodeError, TypeError, IndexError) as e:
        raise CannotNormalizeException(e)


def has_geolocation(page_title):
    site = pywikibot.Site(u'commons', u'commons')
    page = pywikibot.ImagePage(site, page_title)
    geoloc_cat = pywikibot.Category(site, "Category:Media with locations")
    return geoloc_cat in list(page.categories())


def getMonumentPhotos(commonsTrackerCategory, conn, cursor):
    """Return all monument photos in a given tracker category on Commons."""
    result = []

    query = (
        u"SELECT cl_sortkey_prefix, page_title "
        u"FROM page "
        u"JOIN categorylinks ON page_id=cl_from "
        u"WHERE page_namespace=6 AND page_is_redirect=0 AND cl_to=%s")

    cursor.execute(query, (commonsTrackerCategory,))

    result = cursor.fetchall()
    """
    while True:
        try:
            row = cursor.fetchone()
            #(image, id) = row
            result.append(row)
        print row
            #result[id] = image
        except TypeError:
            break
    """
    return result


def updateImage(countrycode, monumentId, name, has_geolocation, conn, cursor):
    """Update an entry for a single image."""
    query = (u"REPLACE INTO `image` "
             u"(`country`, `id`, `img_name`, `has_geolocation`) "
             u"VALUES (%s, %s, %s, %s)")
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        cursor.execute(query,
                       (countrycode, monumentId, name, has_geolocation,))


def makeStatistics(totals):
    """Make statistics on the number of indexed images and put on Commons."""
    site = pywikibot.Site('commons', 'commons')
    page = pywikibot.Page(
        site, u'Commons:Monuments database/Indexed images/Statistics')

    title_column = [
        'country', ('images', 'total'), 'tracked',
        ('template', 'tracker template'), ('cat', 'tracker category')
    ]
    table = StatisticsTable(title_column, ('images', 'tracked'))

    for (countrycode, countryresults) in sorted(totals.iteritems()):
        table.add_row({
            'country': countrycode,
            'images': countryresults.get('totalImages'),
            'tracked': countryresults.get('tracked_images'),
            'template': u'{{tl|%s}}' % countryresults.get('commonsTemplate'),
            'cat': u'[[:Category:{cat}|{cat}]]'.format(
                cat=countryresults.get('commonsTrackerCategory'))
        })

    text = table.to_wikitext()

    comment = (
        u'Updating indexed image statistics. '
        u'Total indexed images: {}'.format(table.get_sum('tracked')))
    pywikibot.debug(text, _logger)
    common.save_to_wiki_or_local(page, comment, text)


def main():
    countrycode = u''
    skip_wd = False

    for arg in pywikibot.handleArgs():
        option, sep, value = arg.partition(':')
        if option == '-countrycode':
            countrycode = value
        elif option == '-skip_wd':
            skip_wd = True
        else:
            raise Exception(
                u'Bad parameters. Expected "-countrycode", "-skip_wd" or '
                u'pywikibot args. Found "{}"'.format(option))

    if countrycode:
        sources = getSources(countrycode=countrycode)
        if not sources:
            pywikibot.warning(
                u'I have no config for countrycode "{0}"'.format(countrycode))
            return False
        else:
            totals = processSources(sources)

    else:
        pywikibot.log(u'Working on all countrycodes')
        sources = getSources(skip_wd=skip_wd)
        if not sources:
            pywikibot.warning(
                u'No sources found, something went completely wrong')
            return False
        else:
            pywikibot.log(
                u'Found {0} countries with monument tracker templates to work '
                u'on'.format(len(sources)))
            totals = processSources(sources)

            makeStatistics(totals)


if __name__ == "__main__":
    main()
