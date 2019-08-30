#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
Make a gallery of unused photos so people can add them to monument lists.

Usage:
# loop through all countries
python unused_monument_images.py
# work on specific country-lang
python unused_monument_images.py -countrycode:XX -langcode:YY
"""
from collections import OrderedDict

import pywikibot

import common as common
import monuments_config as mconfig
from database_connection import (
    close_database_connection,
    connect_to_commons_database,
    connect_to_monuments_database
)
from statistics_table import StatisticsTable

_logger = "unused_images"


def group_unused_images_by_source(photos, withoutPhoto, countryconfig):
    """Identify all unused images and group them by source page and id."""
    unused_images = {}

    for catSortKey in sorted(photos.keys()):
        try:
            monumentId = common.get_id_from_sort_key(catSortKey, withoutPhoto)
        except ValueError:
            pywikibot.warning(u'Got value error for {0}'.format(catSortKey))
            continue

        if monumentId in withoutPhoto:
            source = withoutPhoto.get(monumentId)
            if source not in unused_images:
                unused_images[source] = {}
            imageName = photos.get(catSortKey)

            if monumentId not in unused_images[source]:
                unused_images[source][monumentId] = []

            unused_images[source][monumentId].append(imageName)

    return unused_images


def processCountry(countryconfig, conn, cursor, conn2, cursor2):
    """Work on a single country."""
    if not countryconfig.get('unusedImagesPage'):
        # unusedImagesPage not set, just skip silently.
        return {
            'config': countryconfig,
            'cmt': 'skipped: no unusedImagesPage'
        }
    if not countryconfig.get('commonsTrackerCategory'):
        # commonsTrackerCategory not set, just skip silently.
        return {
            'config': countryconfig,
            'cmt': 'skipped: no commonsTrackerCategory'
        }

    unusedImagesPage = countryconfig.get('unusedImagesPage')
    project = countryconfig.get('project', u'wikipedia')
    commonsTrackerCategory = countryconfig.get(
        'commonsTrackerCategory').replace(u' ', u'_')

    withoutPhoto = getMonumentsWithoutPhoto(
        countryconfig.get('country'), countryconfig.get('lang'), conn, cursor)
    photos = getMonumentPhotos(commonsTrackerCategory, conn2, cursor2)

    pywikibot.log(u'withoutPhoto {0} elements'.format(len(withoutPhoto)))
    pywikibot.log(u'photos {0} elements'.format(len(photos)))

    unused_images = group_unused_images_by_source(
        photos, withoutPhoto, countryconfig)

    site = pywikibot.Site(countryconfig.get('lang'), project)
    page = pywikibot.Page(site, unusedImagesPage)
    totals = output_country_report(
        unused_images, page, countryconfig.get('type') == 'sparql')

    return {
        'report_page': page,
        'config': countryconfig,
        'total_images': totals['images'],
        'total_pages': totals['pages'],
        'total_ids': totals['ids']
    }


def output_country_report(unused_images, report_page, is_sparql=False,
                          max_images=1000):
    """
    Format and output the unused images data for a a single country.

    @param unused_images: the output of group_unused_images
    @param report_page: pywikibot.Page to which the report should be written
    @param is_sparql: If this is a sparql dataset. Defaults to False.
    @param max_images: the max number of images to report to a page. Defaults
        to 1000. Note that actual number of images may be slightly higher in
        order to ensure all candidates for a given monument id are presented.
    """
    # People can add a /header template for with more info
    central_page = ':c:Commons:Monuments database/Unused images'
    text = common.instruction_header(central_page)
    total_pages = 0
    total_ids = 0
    totalImages = 0
    page_link = None

    if not unused_images:
        text += common.done_message(central_page, 'unused images')
    else:
        for source_page, value in unused_images.iteritems():
            total_pages += 1
            if totalImages < max_images:
                try:
                    if is_sparql:
                        page_link = common.get_source_link(
                            source_page, 'sparql',
                            # only one monument_id per sparql source_page
                            label=value.keys()[0])
                    else:
                        page_link = common.get_source_link(source_page)
                        text += u'=== {0} ===\n'.format(page_link)
                except ValueError:  # could not parse source
                    pywikibot.warning(
                        u'Could not find source page for {0} ({1})'.format(
                            value.keys()[0]), source_page)
                    continue

                text += u'<gallery>\n'
                for monument_id, candidates in value.iteritems():
                    total_ids += 1
                    if totalImages < max_images:
                        for candidate in candidates:
                            if is_sparql:
                                text += u'File:{0}|{1}\n'.format(
                                    candidate, page_link)
                            else:
                                text += u'File:{0}|{1}\n'.format(
                                    candidate, monument_id)
                    totalImages += len(candidates)
                text += u'</gallery>\n'
            else:
                for monument_id, candidates in value.iteritems():
                    total_ids += 1
                    totalImages += len(candidates)

    if totalImages >= max_images:
        text += (
            u'<!-- Maximum number of images reached: {0}, '
            u'total of unused images: {1} -->\n'.format(
                max_images, totalImages))
        comment = (
            u'Images to be used in monument lists: '
            u'{0} (gallery maximum reached), '
            u'total of unused images: {1}'.format(
                max_images, totalImages))
    else:
        comment = u'Images to be used in monument lists: {0}'.format(
            totalImages)

    pywikibot.debug(text, _logger)
    common.save_to_wiki_or_local(report_page, comment, text, minorEdit=False)

    return {
        'images': totalImages,
        'pages': total_pages,
        'ids': total_ids
    }


def getMonumentsWithoutPhoto(countrycode, lang, conn, cursor):
    """
    Get all unillustrated monuments.

    @return dict of unillustrated monuments with id as key and source (list)
        as value.
    """
    result = {}

    query = (
        u"""SELECT id, source """
        u"""FROM monuments_all """
        u"""WHERE image='' AND country=%s AND lang=%s""")

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
    """
    Get all monument images.

    @return dict of monument images with category_sort_key as key and filename
        as value. category_sort_key contains the monument id.
    """
    query = (
        u"SELECT page_title, cl_sortkey_prefix "
        u"FROM page "
        u"JOIN categorylinks ON page_id=cl_from "
        u"WHERE page_namespace=6 AND page_is_redirect=0 AND cl_to=%s")

    cursor.execute(query, (commonsTrackerCategory,))

    return common.process_sort_key_query_result(cursor)


def makeStatistics(statistics):
    """
    Output the overall results of the bot as a nice wikitable.

    Does not make use of total_pages which is reported by processCountry as
    this is equivalent to total_ids for sparql sources and hard to explain
    otherwise.
    """
    site = pywikibot.Site('commons', 'commons')
    page = pywikibot.Page(
        site, u'Commons:Monuments database/Unused images/Statistics')

    title_column = OrderedDict([
        ('code', 'country'),
        ('lang', None),
        ('total_images', 'Total unused image candidates'),
        ('total_ids', 'Total monuments with unused images'),
        ('Report page', None),
        ('Row template', None),
        ('Commons template', None)
    ])
    table = StatisticsTable(title_column, ('total_images', 'total_ids'))

    for row in statistics:
        countryconfig = row.get('config')
        total_images_or_cmt = row.get('total_images')
        total_ids = row.get('total_ids')
        row_template = None
        commons_template = None
        report_page = None

        if row.get('total_images') is None:
            total_images_or_cmt = row.get('cmt')
            total_ids = None

        if countryconfig.get('type') != 'sparql':
            row_template = common.get_template_link(
                countryconfig.get('lang'),
                countryconfig.get('project', u'wikipedia'),
                countryconfig.get('rowTemplate'),
                site)

        if countryconfig.get('commonsTemplate'):
            commons_template = u'{{tl|%s}}' % (
                countryconfig.get('commonsTemplate'), )

        if row.get('report_page'):
            report_page = row.get('report_page').title(
                as_link=True, with_ns=False, insite=site)

        table.add_row({
            'code': countryconfig.get('country'),
            'lang': countryconfig.get('lang'),
            'total_images': total_images_or_cmt,
            'total_ids': total_ids,
            'Report page': report_page,
            'Row template': row_template,
            'Commons template': commons_template})

    text = table.to_wikitext()

    comment = (
        u'Updating unused image statistics. Total of {total_images} '
        u'unused images for {total_ids} different monuments.'.format(
            **table.get_sum()))
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
        elif option == u'-skip_wd':
            skip_wd = True
        else:
            raise Exception(
                u'Bad parameters. Expected "-countrycode", "-langcode", '
                u'"-skip_wd" or pywikibot args. '
                u'Found "{}"'.format(option))

    if countrycode and lang:
        if not mconfig.countries.get((countrycode, lang)):
            pywikibot.warning(
                u'I have no config for countrycode "{code}" in '
                u'language "{lang}"'.format(code=countrycode, lang=lang))
            return False
        pywikibot.log(
            u'Working on countrycode "{code}" in language "{lang}"'.format(
                code=countrycode, lang=lang))
        processCountry(mconfig.countries.get((countrycode, lang)),
                       conn, cursor, conn2, cursor2)
    elif countrycode or lang:
        raise Exception(u'The "countrycode" and "langcode" arguments must '
                        u'be used together.')
    else:
        statistics = []
        for (countrycode, lang), countryconfig in mconfig.filtered_countries(
                skip_wd=skip_wd):
            pywikibot.log(
                u'Working on countrycode "{code}" in language "{lang}"'.format(
                    code=countrycode, lang=lang))
            try:
                statistics.append(processCountry(
                    countryconfig, conn, cursor, conn2, cursor2))
            except Exception as e:
                pywikibot.error(
                    u'Unknown error occurred when processing country '
                    u'{0} in lang {1}\n{2}'.format(countrycode, lang, str(e)))
                statistics.append({
                    'config': countryconfig,
                    'cmt': 'failed: unexpected error during processing'
                })
                continue
        makeStatistics(statistics)

    close_database_connection(conn, cursor)


if __name__ == "__main__":
    pywikibot.log(u'Start of %s' % __file__)
    main()
