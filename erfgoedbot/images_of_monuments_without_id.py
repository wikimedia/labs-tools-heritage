#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
Process monument images on Commons without tracker templates.

Makes a gallery of images without an id, and the suitable id template to add to
the image page, based on the image usage in the lists or category membership.

If triggered with the '-add_templates parameter', attempts to add the id
template to the image page on Commons.

Assumes that all id templates are of the form {{template_name|id}}, for
templates where this does not hold added templates, and suggestions on gallery
pages will be incorrect/misleading.

Usage:
# loop through all countries
python images_of_monuments_without_id.py
# work on specific country-lang
python images_of_monuments_without_id.py -countrycode:XX -langcode:YY
"""
from collections import OrderedDict

import pywikibot

import erfgoedbot.common as common
import erfgoedbot.monuments_config as mconfig
from erfgoedbot.database_connection import (
    close_database_connection,
    connect_to_commons_database,
    connect_to_monuments_database
)
from erfgoedbot.statistics_table import StatisticsTable

_logger = "images_without_id"


def processCountry(countryconfig, add_template, conn, cursor, conn2, cursor2):
    """
    Work on a single dataset.
    """
    if (not countryconfig.get('commonsTemplate') or
            not countryconfig.get('commonsTrackerCategory')):
        # No template or tracker category found, just skip silently.
        return {
            'config': countryconfig,
            'cmt': 'skipped: no commonsTemplate or commonsTrackerCategory'
        }
    if (not add_template and not countryconfig.get('imagesWithoutIdPage')):
        # no actions possible
        return {
            'config': countryconfig,
            'cmt': 'skipped: no imagesWithoutIdPage or template addition'
        }

    commonsTemplate = countryconfig.get('commonsTemplate')
    imagesWithoutIdPage = countryconfig.get('imagesWithoutIdPage')
    project = countryconfig.get('project') or 'wikipedia'

    # All items in the list with a photo
    withPhoto = getMonumentsWithPhoto(
        countryconfig.get('country'), countryconfig.get('lang'), conn, cursor)

    # All items on Commons with the id template
    withTemplate = getMonumentsWithTemplate(countryconfig, conn2, cursor2)

    # All items on Commons in the monument tree without the id template
    withoutTemplate = getMonumentsWithoutTemplate(
        countryconfig, conn2, cursor2)

    # Get the image ignore list
    # FIXME: Make an actual function of this instead of a static list.
    ignoreList = ['Monumentenschildje.jpg', 'Rijksmonument-Schildje-NL.jpg']

    gallery_rows = []
    totals = {
        'added': 0,
        'with_id': 0,
        'without_id': 0
    }

    # FIXME implement max_images per output_country_report
    for image in withoutTemplate:
        if image not in ignoreList:
            # An image is in the category and is in the list of used images
            if withPhoto.get(image):
                added = add_template and addCommonsTemplate(
                    image, commonsTemplate, withPhoto.get(image))
                if added:
                    totals['added'] += 1
                else:
                    gallery_rows.append(
                        (image, withPhoto.get(image), commonsTemplate))
                    totals['with_id'] += 1
            # An image is in the category and is not in the list of used images
            else:
                gallery_rows.append((image, ))
                totals['without_id'] += 1

    # An image is in the list of used images, but not in the category
    for image in withPhoto:
        # Skip images which already have the templates and the ones in without
        # templates to prevent duplicates
        if (image not in ignoreList and
                image not in withTemplate and
                image not in withoutTemplate):
            added = add_template and addCommonsTemplate(
                image, commonsTemplate, withPhoto.get(image))
            if added:
                totals['added'] += 1
            else:
                gallery_rows.append(
                    (image, withPhoto.get(image), commonsTemplate))
                totals['with_id'] += 1

    # imagesWithoutIdPage isn't set for every source, skip it if it's not set
    report_page = None
    if imagesWithoutIdPage:
        site = pywikibot.Site(countryconfig.get('lang'), project)
        report_page = pywikibot.Page(site, imagesWithoutIdPage)

        output_country_report(gallery_rows, report_page)

    return {
        'report_page': report_page,
        'config': countryconfig,
        'totals': totals
    }


def output_country_report(rows, report_page, max_images=1000):
    """
    Output a gallery of images without id.

    @param rows: list of (image, id, template) or (image, ) tuples.
    @param report_page: pywikibot.Page where report will be outputted.
    @param max_images: the max number of images to report to a page. Defaults
        to 1000.
    """
    # FIXME create this page. Different name?
    central_page = ':c:Commons:Monuments database/Images without id'
    text = common.instruction_header(central_page)

    if rows:
        gallery_rows = [format_gallery_row(*row) for row in rows[:max_images]]
        text += '<gallery>\n{}\n</gallery>'.format('\n'.join(gallery_rows))
    else:
        text += common.done_message(central_page, 'images without id')

    if len(rows) > max_images:
        text += (
            '\n<!-- Maximum number of images reached: {0}, '
            'total of images without id: {1} -->'.format(
                max_images, len(rows)))
        comment = (
            'Images without an id: {0} (gallery maximum reached), '
            'total of images without id: {1}'.format(
                max_images, len(rows)))
    else:
        comment = 'Images without an id: {0}'.format(len(rows))

    pywikibot.debug(text, _logger)
    common.save_to_wiki_or_local(
        report_page, comment, text, minorEdit=False)


def format_gallery_row(image, id=None, template=None):
    """
    Output a wikitext formated row for a gallery.

    Outputs either just the filename or a caption consisting of an id or
    template wrapped id depending on how many args are provided.
    """
    text = 'File:%(image)s'
    if id and template:
        text += '|<nowiki>{{%(template)s|%(id)s}}</nowiki>'
    elif id:
        text += '|%(id)s'
    return text % {'image': image, 'id': id, 'template': template}


def getMonumentsWithPhoto(countrycode, lang, conn, cursor):
    """
    Get all images in the monuments database for a dataset.

    @return dict
    """
    result = {}
    query = (
        "SELECT image, id "
        "FROM monuments_all "
        "WHERE NOT image='' AND country=%s AND lang=%s")
    cursor.execute(query, (countrycode, lang))

    while True:
        try:
            row = cursor.fetchone()
            (image, id) = row
            # Spaces are lowercase in the other database
            image = image.replace(' ', '_')
            # First char always needs to be uppercase
            image = image[0].upper() + image[1:]
            result[image] = id
        except TypeError:
            break

    return result


def getMonumentsWithoutTemplate(countryconfig, conn, cursor):
    """
    Get all images in the relevant category tree without a tracker template.

    @return list
    """
    # FIXME add possibility of only running this on the base category only
    commonsCategoryBase = countryconfig.get(
        'commonsCategoryBase').replace(' ', '_')
    commonsTemplate = countryconfig.get('commonsTemplate').replace(' ', '_')

    result = []
    query = (
        "SELECT DISTINCT(page_title) "
        "FROM page "
        "JOIN categorylinks ON page_id=cl_from "
        "WHERE page_namespace=6 AND page_is_redirect=0 "
        "AND (cl_to=%s OR cl_to LIKE %s) AND NOT EXISTS({sub}) "
        "ORDER BY page_title ASC"
    )
    subquery = (
        "SELECT * "
        "FROM templatelinks "
        "WHERE page_id=tl_from AND tl_namespace=10 AND tl_title=%s")
    cursor.execute(
        query.format(sub=subquery), (
            commonsCategoryBase, '{}_in_%'.format(commonsCategoryBase),
            commonsTemplate))

    while True:
        try:
            row = cursor.fetchone()
            (image,) = row
            result.append(image.decode('utf-8'))
        except TypeError:
            break

    return result


def getMonumentsWithTemplate(countryconfig, conn, cursor):
    """Get all images which contain the tracker template."""

    commonsTrackerCategory = countryconfig.get(
        'commonsTrackerCategory').replace(' ', '_')

    result = []
    query = (
        "SELECT DISTINCT(page_title) "
        "FROM page "
        "JOIN categorylinks ON page_id=cl_from "
        "WHERE page_namespace=6 AND page_is_redirect=0 AND cl_to=%s "
        "ORDER BY page_title ASC")
    cursor.execute(query, (commonsTrackerCategory,))

    while True:
        try:
            row = cursor.fetchone()
            (image,) = row
            result.append(image.decode('utf-8'))
        except TypeError:
            break

    return result


def addCommonsTemplate(image, commonsTemplate, identifier):
    """
    Add the commonsTemplate with identifier to the image.

    Assumes that the template only takes one unnamed parameter, the id.
    """
    site = pywikibot.Site('commons', 'commons')
    page = pywikibot.ImagePage(site, image)
    if not page.exists() or page.isRedirectPage() or page.isEmpty():
        return False

    if commonsTemplate in page.templates():
        return False

    text = page.get()
    newtext = '{{%s|%s}}\n' % (commonsTemplate, identifier) + text

    comment = 'Adding template {0} based on usage in list'.format(
        commonsTemplate)

    pywikibot.showDiff(text, newtext)
    common.save_to_wiki_or_local(page, comment, newtext)
    return True


def make_statistics(statistics):
    """
    Output the overall results of the bot as a nice wikitable.

    @param statistics: list of per dataset statistic dicts where the allowed
        keys are: config, totals, report page and cmt.
    """
    site = pywikibot.Site('commons', 'commons')
    page = pywikibot.Page(
        site, 'Commons:Monuments database/Images without id/Statistics')

    title_column = OrderedDict([
        ('code', 'country'),
        ('lang', '[[:en:List of ISO 639-1 codes|lang]]'),
        ('total_with_id', 'Total monuments with suggested id'),
        ('total_without_id', 'Total monuments without suggested id'),
        # ('total_added', 'Total templates automatically added'),
        ('Report page', None),
        ('Commons template', None)
    ])
    numeric = [key for key in list(title_column.keys()) if key.startswith('total_')]
    table = StatisticsTable(title_column, numeric)

    for row in statistics:
        country_config = row.get('config')
        totals = row.get('totals', {})
        total_with_id_or_cmt = row.get('cmt')
        commons_template = None
        report_page = None

        if totals:
            total_with_id_or_cmt = totals.get('with_id')

        if country_config.get('commonsTemplate'):
            commons_template = '{{tl|%s}}' % (
                country_config.get('commonsTemplate'), )

        if row.get('report_page'):
            report_page = row.get('report_page').title(
                as_link=True, with_ns=False, insite=site)

        table.add_row({
            'code': country_config.get('country'),
            'lang': country_config.get('lang'),
            'total_with_id': total_with_id_or_cmt,
            'total_without_id': totals.get('without_id'),
            # 'total_added': totals.get('added'),
            'Report page': report_page,
            'Commons template': commons_template})

    text = table.to_wikitext()

    comment = (
        'Updating images without id statistics. Total of {total_with_id} '
        'images with suggested ids and {total_without_id} without.'.format(
            **table.get_sum()))
    pywikibot.debug(text, _logger)
    common.save_to_wiki_or_local(page, comment, text)


def main():
    countrycode = ''
    lang = ''
    skip_wd = False
    add_template = False
    conn = None
    cursor = None

    # FIXME add option to only run based on list usage, not category membership
    for arg in pywikibot.handleArgs():
        option, sep, value = arg.partition(':')
        if option == '-countrycode':
            countrycode = value
        elif option == '-langcode':
            lang = value
        elif option == '-skip_wd':
            skip_wd = True
        elif option == '-add_template':
            add_template = True
        else:
            raise Exception(
                'Bad parameters. Expected "-countrycode", "-langcode", '
                '"-skip_wd", "-add_template" or pywikibot args. '
                'Found "{}"'.format(option))

    if countrycode and lang:
        if not mconfig.countries.get((countrycode, lang)):
            pywikibot.warning(
                'I have no config for countrycode "{0}" '
                'in language "{1}"'.format(countrycode, lang))
            return False
        pywikibot.log(
            'Working on countrycode "{0}" in language "{1}"'.format(
                countrycode, lang))
        (conn, cursor) = connect_to_monuments_database()
        (conn2, cursor2) = connect_to_commons_database()
        processCountry(mconfig.countries.get((countrycode, lang)),
                       add_template, conn, cursor, conn2, cursor2)
        close_database_connection(conn, cursor)
    elif countrycode or lang:
        raise Exception('The "countrycode" and "langcode" arguments must '
                        'be used together.')
    else:
        statistics = []
        for (countrycode, lang), countryconfig in mconfig.filtered_countries(
                skip_wd=skip_wd):
            pywikibot.log(
                'Working on countrycode "{0}" in language "{1}"'.format(
                    countrycode, lang))
            (conn, cursor) = connect_to_monuments_database()
            (conn2, cursor2) = connect_to_commons_database()
            try:
                statistics.append(processCountry(
                    countryconfig, add_template, conn, cursor, conn2, cursor2))
            except Exception as e:
                pywikibot.error(
                    'Unknown error occurred when processing country '
                    '{0} in lang {1}\n{2}'.format(countrycode, lang, str(e)))
                statistics.append({
                    'config': countryconfig,
                    'cmt': 'failed: unexpected error during processing'
                })
                continue
            finally:
                close_database_connection(conn, cursor)
        make_statistics(statistics)


if __name__ == "__main__":
    pywikibot.log('Start of %s' % __file__)
    try:
        main()
    finally:
        pywikibot.stopme()
