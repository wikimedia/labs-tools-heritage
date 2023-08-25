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

import erfgoedbot.common as common
import erfgoedbot.monuments_config as mconfig
from erfgoedbot.database_connection import (
    close_database_connection,
    connect_to_commons_database,
    connect_to_monuments_database
)
from erfgoedbot.statistics_table import StatisticsTable

_logger = "missing_commonscat"


def processCountry(countryconfig, conn, cursor, conn2, cursor2):
    """Work on a single country."""
    if not countryconfig.get('missingCommonscatPage'):
        # missingCommonscatPage not set, just skip silently.
        return {
            'config': countryconfig,
            'cmt': 'skipped: no missingCommonscatPage'
        }
    if not countryconfig.get('commonsTrackerCategory'):
        # commonsTrackerCategory not set, just skip silently.
        return {
            'config': countryconfig,
            'cmt': 'skipped: no commonsTrackerCategory'
        }

    if countryconfig.get('type') == 'sparql':
        # This script does not (yet) work for SPARQL sources, skip silently
        return {
            'config': countryconfig,
            'cmt': 'skipped: cannot handle sparql'
        }

    commonscatField = lookupSourceField('commonscat', countryconfig)
    if not commonscatField:
        # Field is missing. Something is seriously wrong, but we just skip it
        # silently
        return {
            'config': countryconfig,
            'cmt': 'skipped: no template field matched to commonscat!!'
        }

    missingCommonscatPage = countryconfig.get('missingCommonscatPage')
    commonsTrackerCategory = countryconfig.get(
        'commonsTrackerCategory'). replace(' ', '_')

    withoutCommonscat = getMonumentsWithoutCommonscat(
        countryconfig.get('country'), countryconfig.get('lang'), conn, cursor)
    commonscats = getMonumentCommonscats(
        commonsTrackerCategory, conn2, cursor2)

    pywikibot.log('withoutCommonscat {num} elements'.format(
        num=len(withoutCommonscat)))
    pywikibot.log('commonscats {num} elements'.format(
        num=len(withoutCommonscat)))

    missing_commonscat = group_missing_commonscat_by_source(
        commonscats, withoutCommonscat, countryconfig)

    site = pywikibot.Site(
        countryconfig.get('lang'),
        countryconfig.get('project', 'wikipedia'))
    page = pywikibot.Page(site, missingCommonscatPage)
    iw_links = getInterwikisMissingCommonscatPage(
        countryconfig.get('country'), countryconfig.get('lang'))
    totals = output_country_report(
        missing_commonscat, commonscatField, page, iw_links)

    return {
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
    central_page = ':c:Commons:Monuments_database/Missing_commonscat_links'
    text = common.instruction_header(central_page)
    total_pages = 0
    totalCategories = 0

    if not missing_commonscat:
        text += common.done_message(central_page, 'missing commonscat')
    else:
        for source_page, cats in missing_commonscat.items():
            total_pages += 1
            if totalCategories < max_cats:
                text += '=== {0} ===\n'.format(source_page)
                for (cat_name, monument_id) in cats:
                    text += (
                        '* <nowiki>|</nowiki> {field} = '
                        '[[:c:Category:{_name}|{name}]] - {id}\n'.format(
                            field=commonscat_field,
                            _name=cat_name,
                            name=cat_name.replace('_', ' '),
                            id=monument_id
                        )
                    )
                totalCategories += len(cats)
            else:
                totalCategories += len(cats)

    if totalCategories >= max_cats:
        text += (
            '<!-- Maximum number of categories reached: {max}, '
            'total of missing commonscat links: {total} -->\n'.format(
                max=max_cats, total=totalCategories))
        comment = (
            'Commonscat links to be made in monument lists: '
            '{max} (list maximum reached), '
            'total of missing commonscat links: {total}'.format(
                max=max_cats, total=totalCategories))
    else:
        comment = 'Commonscat links to be made in monument lists: {0}'.format(
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
            pywikibot.warning('Got value error for {0}'.format(catSortKey))
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
                    'Could not find source page for {0} ({1})'.format(
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
    result = ''
    for (countrycode2, lang2), countryconfig in mconfig.countries.items():
        if countrycode == countrycode2 and lang != lang2:
            if countryconfig.get('missingCommonscatPage'):
                result += '[[{lang}:{page}]]\n'.format(
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
        "SELECT id, source "
        "FROM monuments_all "
        "WHERE (commonscat IS NULL or commonscat='') "
        "AND country=%s AND lang=%s")

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
        "SELECT page_title, cl_sortkey_prefix "
        "FROM page "
        "JOIN categorylinks ON page_id=cl_from "
        "WHERE page_namespace=14 AND page_is_redirect=0 AND cl_to=%s")

    cursor.execute(query, (commonsTrackerCategory,))

    return common.process_sort_key_query_result(cursor)


def makeStatistics(statistics):
    """Output the overall results of the bot as a nice wikitable."""
    site = pywikibot.Site('commons', 'commons')
    page = pywikibot.Page(
        site,
        'Commons:Monuments database/Missing commonscat links/Statistics')

    title_column = OrderedDict([
        ('code', 'country'),
        ('lang', None),
        ('total', None),
        ('report_page', 'page'),
        ('row template', None),
        ('Commons template', None)
    ])
    table = StatisticsTable(title_column, ('total', ))

    for row in statistics:
        countryconfig = row.get('config')
        total_cats_or_cmt = row.get('total_cats')
        row_template = None
        commons_template = None
        report_page = None

        if row.get('total_cats') is None:
            total_cats_or_cmt = row.get('cmt')

        if countryconfig.get('type') != 'sparql':
            row_template = common.get_template_link(
                countryconfig.get('lang'),
                countryconfig.get('project', 'wikipedia'),
                countryconfig.get('rowTemplate'),
                site)

        if countryconfig.get('commonsTemplate'):
            commons_template = '{{tl|%s}}' % (
                countryconfig.get('commonsTemplate'), )

        if row.get('report_page'):
            report_page = row.get('report_page').title(
                as_link=True, with_ns=False, insite=site)

        table.add_row({
            'code': countryconfig.get('country'),
            'lang': countryconfig.get('lang'),
            'total': total_cats_or_cmt,
            'report_page': report_page,
            'row template': row_template,
            'Commons template': commons_template})

    text = table.to_wikitext()

    comment = (
        'Updating missing commonscat links statistics. '
        'Total missing links: {total_cats}'.format(
            total_cats=table.get_sum('total')))
    pywikibot.debug(text, _logger)
    common.save_to_wiki_or_local(page, comment, text)


def main():
    countrycode = ''
    lang = ''
    skip_wd = False
    conn = None
    cursor = None
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

    if countrycode and lang:
        if not mconfig.countries.get((countrycode, lang)):
            pywikibot.warning(
                'I have no config for countrycode "{code}" in language '
                '"{lang}"'.format(code=countrycode, lang=lang))
            return False
        pywikibot.log(
            'Working on countrycode "{code}" in language "{lang}"'.format(
                code=countrycode, lang=lang))
        processCountry(mconfig.countries.get((countrycode, lang)),
                       conn, cursor, conn2, cursor2)
    elif countrycode or lang:
        raise Exception('The "countrycode" and "langcode" arguments must '
                        'be used together.')
    else:
        statistics = []
        for (countrycode, lang), countryconfig in mconfig.filtered_countries(
                skip_wd=skip_wd):
            pywikibot.log(
                'Working on countrycode "{code}" in language "{lang}"'.format(
                    code=countrycode, lang=lang))
            try:
                statistics.append(processCountry(
                    countryconfig, conn, cursor, conn2, cursor2))
            except Exception as e:
                pywikibot.error(
                    'Unknown error occurred when processing country '
                    '{0} in lang {1}\n{2}'.format(countrycode, lang, str(e)))
                statistics.append({
                    'config': countryconfig,
                    'cmt': 'failed: unexpected error during processing'
                })
                continue
        makeStatistics(statistics)

    close_database_connection(conn, cursor)


if __name__ == "__main__":
    pywikibot.log('Start of %s' % __file__)
    main()
