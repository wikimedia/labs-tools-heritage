#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
Find monuments where a commons category exists, but no link is in the list yet.

Usage:
# loop through all countries
python missing_commonscat_links.py
# work on specific country-lang
python missing_commonscat_links.py -countrycode:XX -langcode:YY
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

_logger = "missing_commonscat"


def processCountry(countrycode, lang, countryconfig, conn, cursor, conn2,
                   cursor2):
    """Work on a single country."""
    if not countryconfig.get('missingCommonscatPage'):
        # missingCommonscatPage not set, just skip silently.
        return {
            'code': countrycode,
            'lang': lang,
            'config': countryconfig,
            'cmt': 'skipped: no missingCommonscatPage'
        }
    if not countryconfig.get('commonsTrackerCategory'):
        # commonsTrackerCategory not set, just skip silently.
        return {
            'code': countrycode,
            'lang': lang,
            'config': countryconfig,
            'cmt': 'skipped: no commonsTrackerCategory'
        }

    if countryconfig.get('type') == 'sparql':
        # This script does not (yet) work for SPARQL sources, skip silently
        return {
            'code': countrycode,
            'lang': lang,
            'config': countryconfig,
            'cmt': 'skipped: cannot handle sparql'
        }

    commonscatField = lookupSourceField(u'commonscat', countryconfig)
    if not commonscatField:
        # Field is missing. Something is seriously wrong, but we just skip it
        # silently
        return {
            'code': countrycode,
            'lang': lang,
            'config': countryconfig,
            'cmt': 'skipped: no template field matched to commonscat!!'
        }

    missingCommonscatPage = countryconfig.get('missingCommonscatPage')
    commonsTrackerCategory = countryconfig.get(
        'commonsTrackerCategory'). replace(u' ', u'_')

    withoutCommonscat = getMonumentsWithoutCommonscat(
        countrycode, lang, conn, cursor)
    commonscats = getMonumentCommonscats(
        commonsTrackerCategory, conn2, cursor2)

    pywikibot.log(u'withoutCommonscat {num} elements'.format(
        num=len(withoutCommonscat)))
    pywikibot.log(u'commonscats {num} elements'.format(
        num=len(withoutCommonscat)))

    missing_commonscat = group_missing_commonscat_by_source(
        commonscats, withoutCommonscat, countryconfig)

    site = pywikibot.Site(lang, u'wikipedia')
    page = pywikibot.Page(site, missingCommonscatPage)
    iw_links = getInterwikisMissingCommonscatPage(countrycode, lang)
    totals = output_country_report(
        missing_commonscat, commonscatField, page, iw_links)

    return {
        'code': countrycode,
        'lang': lang,
        'report_page': page,
        'config': countryconfig,
        'total_cats': totals['cats'],
        'total_pages': totals['pages']
    }


def output_country_report(missing_commonscat, commonscat_field, report_page,
                          iw_links=None, max_cats=1000):
    """
    Format and output the missing commonscats data for a a single country.

    @param missing_commonscat: the output of group_missing_commonscat_by_source
    @param commonscat_field: the template field used for adding a commonscat
    @param report_page: pywikibot.Page to which the report should be written
    @param iw_links: any interwiki links to append to the page.
    @param max_cats: the max number of categories to report to a page. Defaults
        to 1000.  Note that actual number of images may be slightly higher in
        order to ensure all entries in a given list are presented.
    """
    # People can add a /header template for with more info
    text = common.instruction_header(
        ':c:Commons:Monuments_database/Missing_commonscat_links')
    total_pages = 0
    totalCategories = 0

    if not missing_commonscat:
        text += u'\nThere are no missing commonscat left. Great work!\n'
    else:
        for source_page, cats in missing_commonscat.iteritems():
            total_pages += 1
            if totalCategories < max_cats:
                text += u'=== {0} ===\n'.format(source_page)
                for (cat_name, monument_id) in cats:
                    text += (
                        u'* <nowiki>|</nowiki> {field} = '
                        u'[[:c:Category:{_name}|{name}]] - {id}\n'.format(
                            field=commonscat_field,
                            _name=cat_name,
                            name=cat_name.replace(u'_', u' '),
                            id=monument_id
                        )
                    )
                totalCategories += len(cats)
            else:
                totalCategories += len(cats)

    if totalCategories >= max_cats:
        text += (
            u'<!-- Maximum number of categories reached: {max}, '
            u'total of missing commonscat links: {total} -->\n'.format(
                max=max_cats, total=totalCategories))
        comment = (
            u'Commonscat links to be made in monument lists: '
            u'{max} (list maximum reached), '
            u'total of missing commonscat links: {total}'.format(
                max=max_cats, total=totalCategories))
    else:
        comment = u'Commonscat links to be made in monument lists: {0}'.format(
            totalCategories)

    if iw_links:
        text += iw_links

    pywikibot.debug(text, _logger)
    common.save_to_wiki_or_local(report_page, comment, text)

    return {
        'cats': totalCategories,
        'pages': total_pages
    }


def group_missing_commonscat_by_source(commonscats, withoutCommonscat,
                                       countryconfig):
    """Identify all unused images and group them by source page and id."""
    missing_commonscat = {}

    for catSortKey in sorted(commonscats.keys()):
        try:
            monumentId = common.get_id_from_sort_key(
                catSortKey, withoutCommonscat)
        except ValueError:
            pywikibot.warning(u'Got value error for {0}'.format(catSortKey))
            continue

        if monumentId in withoutCommonscat:
            try:
                source_link = common.get_source_link(
                    withoutCommonscat.get(monumentId),
                    countryconfig.get('type'))
                if source_link not in missing_commonscat:
                    missing_commonscat[source_link] = []
            except ValueError:
                pywikibot.warning(
                    u'Could not find source page for {0} ({1})'.format(
                        monumentId, withoutCommonscat.get(monumentId)))
                continue

            missing_commonscat[source_link].append(
                (commonscats.get(catSortKey), monumentId))

    return missing_commonscat


def lookupSourceField(destination, countryconfig):
    """Lookup the source field of a destination."""
    for field in countryconfig.get('fields'):
        if field.get('dest') == destination:
            return field.get('source')


def getInterwikisMissingCommonscatPage(countrycode, lang):
    """Get interwiki link to missing_commonscat_page for the same country."""
    result = u''
    for (countrycode2, lang2), countryconfig in mconfig.countries.iteritems():
        if countrycode == countrycode2 and lang != lang2:
            if countryconfig.get('missingCommonscatPage'):
                result += u'[[{lang}:{page}]]\n'.format(
                    lang=lang2,
                    page=countryconfig.get('missingCommonscatPage'))

    return result


def getMonumentsWithoutCommonscat(countrycode, lang, conn, cursor):
    """
    Retrieve all monuments in the database without commonscat.

    @return dict of monuments without commonscat with id as key and source
        (list) as value.
    """
    result = {}

    query = (
        u"SELECT id, source "
        u"FROM monuments_all "
        u"WHERE (commonscat IS NULL or commonscat='') "
        u"AND country=%s AND lang=%s")

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
    """
    Retrieve all commons categories in the tracking category.

    @return dict of commons categories with category_sort_key as key and
        category name as value. category_sort_key contains the monument id.
    """
    query = (
        u"SELECT page_title, cl_sortkey_prefix "
        u"FROM page "
        u"JOIN categorylinks ON page_id=cl_from "
        u"WHERE page_namespace=14 AND page_is_redirect=0 AND cl_to=%s")

    cursor.execute(query, (commonsTrackerCategory,))

    return common.process_sort_key_query_result(cursor)


def makeStatistics(statistics):
    """Output the overall results of the bot as a nice wikitable."""
    site = pywikibot.Site('commons', 'commons')
    page = pywikibot.Page(
        site,
        u'Commons:Monuments database/Missing commonscat links/Statistics')

    column_names = ('country', 'lang', 'total', 'page', 'row template',
                    'Commons template')
    numeric_columns = ('total', )
    columns = OrderedDict(
        [(col, col in numeric_columns) for col in column_names])
    text = common.table_header_row(columns)

    text_row = (
        u'|-\n'
        u'| {code} \n'
        u'| {lang} \n'
        u'| {total_cats} \n'
        u'| {report_page} \n'
        u'| {row_template} \n'
        u'| {commons_template} \n')

    total_cats_sum = 0
    for row in statistics:
        countryconfig = row.get('config')
        total_cats_or_cmt = row.get('total_cats')
        row_template = u'---'
        commons_template = u'---'
        report_page = u'---'

        if row.get('total_cats') is not None:
            total_cats_sum += row.get('total_cats')
        else:
            total_cats_or_cmt = row.get('cmt')

        if countryconfig.get('type') != 'sparql':
            row_site = pywikibot.Site(
                row.get('lang'),
                countryconfig.get('project', u'wikipedia'))
            row_template_page = pywikibot.Page(
                row_site,
                u'Template:{0}'.format(countryconfig.get('rowTemplate')))
            row_template = row_template_page.title(
                as_link=True, with_ns=False, insite=site)

        if countryconfig.get('commonsTemplate'):
            commons_template = u'{{tl|%s}}' % (
                countryconfig.get('commonsTemplate'), )

        if row.get('report_page'):
            report_page = row.get('report_page').title(
                as_link=True, with_ns=False, insite=site)

        text += text_row.format(
            code=row.get('code'),
            lang=row.get('lang'),
            total_cats=total_cats_or_cmt,
            report_page=report_page,
            row_template=row_template,
            commons_template=commons_template)

    text += common.table_bottom_row(6, {2: total_cats_sum})

    comment = (
        u'Updating missing commonscat links statistics. '
        u'Total missing links: {total_cats}'.format(total_cats=total_cats_sum))
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
                u'I have no config for countrycode "{code}" in language '
                u'"{lang}"'.format(code=countrycode, lang=lang))
            return False
        pywikibot.log(
            u'Working on countrycode "{code}" in language "{lang}"'.format(
                code=countrycode, lang=lang))
        processCountry(countrycode, lang, mconfig.countries.get(
            (countrycode, lang)), conn, cursor, conn2, cursor2)
    elif countrycode or lang:
        raise Exception(u'The "countrycode" and "langcode" arguments must '
                        u'be used together.')
    else:
        statistics = []
        for (countrycode, lang), countryconfig in mconfig.countries.iteritems():
            if (countryconfig.get('skip') or
                    (skip_wd and (countryconfig.get('type') == 'sparql'))):
                continue
            pywikibot.log(
                u'Working on countrycode "{code}" in language "{lang}"'.format(
                    code=countrycode, lang=lang))
            statistics.append(
                processCountry(
                    countrycode, lang, countryconfig, conn, cursor, conn2,
                    cursor2))
        makeStatistics(statistics)

    close_database_connection(conn, cursor)


if __name__ == "__main__":
    main()
