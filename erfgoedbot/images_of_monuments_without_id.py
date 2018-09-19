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
import pywikibot

import common as common
import monuments_config as mconfig
from database_connection import (
    close_database_connection,
    connect_to_commons_database,
    connect_to_monuments_database
)

_logger = "images_without_id"


def processCountry(countryconfig, add_template, conn, cursor, conn2, cursor2):
    """
    Work on a single dataset.
    """
    if (not countryconfig.get('commonsTemplate') or
            not countryconfig.get('commonsTrackerCategory')):
        # No template or tracker category found, just skip silently.
        return False
    if (not add_template and not countryconfig.get('imagesWithoutIdPage')):
        # no actions possible
        return False

    commonsTemplate = countryconfig.get('commonsTemplate')
    imagesWithoutIdPage = countryconfig.get('imagesWithoutIdPage')
    project = countryconfig.get('project') or u'wikipedia'

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
    ignoreList = [u'Monumentenschildje.jpg', u'Rijksmonument-Schildje-NL.jpg']

    gallery_rows = []

    # FIXME implement max_images per output_country_report
    for image in withoutTemplate:
        if image not in ignoreList:
            # An image is in the category and is in the list of used images
            if withPhoto.get(image):
                added = add_template and addCommonsTemplate(
                    image, commonsTemplate, withPhoto.get(image))
                if not added:
                    gallery_rows.append(
                        (image, withPhoto.get(image), commonsTemplate))
            # An image is in the category and is not in the list of used images
            else:
                gallery_rows.append((image, ))

    # An image is in the list of used images, but not in the category
    for image in withPhoto:
        # Skip images which already have the templates and the ones in without
        # templates to prevent duplicates
        if image not in ignoreList and \
                image not in withTemplate and \
                image not in withoutTemplate:
            added = add_template and addCommonsTemplate(
                image, commonsTemplate, withPhoto.get(image))
            if not added:
                gallery_rows.append(
                    (image, withPhoto.get(image), commonsTemplate))

    # imagesWithoutIdPage isn't set for every source, just skip it if it's not
    # set
    if imagesWithoutIdPage:
        site = pywikibot.Site(countryconfig.get('lang'), project)
        report_page = pywikibot.Page(site, imagesWithoutIdPage)

        output_country_report(gallery_rows, report_page)


def output_country_report(rows, report_page):
    """
    Output a gallery of images without id.

    @param rows: list of (image, id, template) or (image, ) tuples.
    @param report_page: pywikibot.Page where report will be outputted.
    """
    gallery_rows = [format_gallery_row(*row) for row in rows]
    text = u'<gallery>\n{}\n</gallery>'.format('\n'.join(gallery_rows))
    comment = u'Images without an id'

    pywikibot.debug(text, _logger)
    common.save_to_wiki_or_local(
        report_page, comment, text, minorEdit=False)


def format_gallery_row(image, id=None, template=None):
    """
    Output a wikitext formated row for a gallery.

    Outputs either just the filename or a caption consisting of an id or
    template wrapped id depending on how many args are provided.
    """
    text = u'File:%(image)s'
    if id and template:
        text += u'|<nowiki>{{%(template)s|%(id)s}}</nowiki>'
    elif id:
        text += u'|%(id)s'
    return text % {'image': image, 'id': id, 'template': template}


def getMonumentsWithPhoto(countrycode, lang, conn, cursor):
    """
    Get all images in the monuments database for a dataset.

    @return dict
    """
    result = {}
    query = (
        u"SELECT image, id "
        u"FROM monuments_all "
        u"WHERE NOT image='' AND country=%s AND lang=%s")
    cursor.execute(query, (countrycode, lang))

    while True:
        try:
            row = cursor.fetchone()
            (image, id) = row
            # Spaces are lowercase in the other database
            image = image.replace(u' ', u'_')
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
        'commonsCategoryBase').replace(u' ', u'_')
    commonsTemplate = countryconfig.get('commonsTemplate').replace(u' ', u'_')

    result = []
    query = (
        u"SELECT DISTINCT(page_title) "
        u"FROM page "
        u"JOIN categorylinks ON page_id=cl_from "
        u"WHERE page_namespace=6 AND page_is_redirect=0 "
        u"AND (cl_to='%s' OR cl_to LIKE '%s\_in\_%%') AND NOT EXISTS({sub}) "
        u"ORDER BY page_title ASC"
    )
    subquery = (
        u"SELECT * "
        u"FROM templatelinks "
        u"WHERE page_id=tl_from AND tl_namespace=10 AND tl_title='%s'")
    cursor.execute(
        query.format(sub=subquery) % (
            commonsCategoryBase, commonsCategoryBase, commonsTemplate))

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
        'commonsTrackerCategory').replace(u' ', u'_')

    result = []
    query = (
        u"SELECT DISTINCT(page_title) "
        u"FROM page "
        u"JOIN categorylinks ON page_id=cl_from "
        u"WHERE page_namespace=6 AND page_is_redirect=0 AND cl_to=%s "
        u"ORDER BY page_title ASC")
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
    newtext = u'{{%s|%s}}\n' % (commonsTemplate, identifier) + text

    comment = u'Adding template {0} based on usage in list'.format(
        commonsTemplate)

    pywikibot.showDiff(text, newtext)
    common.save_to_wiki_or_local(page, comment, newtext)
    return True


def main():
    countrycode = u''
    lang = u''
    skip_wd = False
    add_template = False
    conn = None
    cursor = None
    # Connect database, we need that
    (conn, cursor) = connect_to_monuments_database()
    (conn2, cursor2) = connect_to_commons_database()

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
                u'Bad parameters. Expected "-countrycode", "-langcode", '
                u'"-skip_wd", "-add_template" or pywikibot args. '
                u'Found "{}"'.format(option))

    if countrycode and lang:
        if not mconfig.countries.get((countrycode, lang)):
            pywikibot.warning(
                u'I have no config for countrycode "{0}" '
                u'in language "{1}"'.format(countrycode, lang))
            return False
        pywikibot.log(
            u'Working on countrycode "{0}" in language "{1}"'.format(
                countrycode, lang))
        processCountry(mconfig.countries.get((countrycode, lang)),
                       add_template, conn, cursor, conn2, cursor2)
    elif countrycode or lang:
        raise Exception(u'The "countrycode" and "langcode" arguments must '
                        u'be used together.')
    else:
        for (countrycode, lang), countryconfig in mconfig.countries.iteritems():
            if (countryconfig.get('skip') or
                    (skip_wd and (countryconfig.get('type') == 'sparql'))):
                continue
            pywikibot.log(
                u'Working on countrycode "{0}" in language "{1}"'.format(
                    countrycode, lang))
            processCountry(
                countryconfig, add_template, conn, cursor, conn2, cursor2)

    close_database_connection(conn, cursor)


if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
