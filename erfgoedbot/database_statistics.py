#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
Update the statistics of the monuments database at c:Commons:Monuments_database/Statistics

FIXME: Too much code duplication. Should probably just have one list of the
possible fields for the functions to work on.
"""
from collections import OrderedDict

import pywikibot

import erfgoedbot.common as common
import erfgoedbot.monuments_config as mconfig
from erfgoedbot.database_connection import (
    close_database_connection,
    connect_to_monuments_database
)
from erfgoedbot.statistics_table import StatisticsTable

_logger = "database_statistics"


def getCount(query, cursor):
    '''
    Return the result of the query
    '''
    cursor.execute(query)

    count, = cursor.fetchone()
    return count


def outputStatistics(statistics):
    """Output the statistics in wikitext on Commons."""
    title_column = OrderedDict([
        ('country', None),
        ('lang', '[[:en:List of ISO 639-1 codes|lang]]'),
        ('all', 'total'),
        ('name', None),
        ('address', None),
        ('municipality', None),
        ('coordinates', None),
        ('image', None),
        ('commonscat', None),
        ('article', None),
        ('wikidata', None),
        ('adm0', '[[:en:ISO 3166-1 alpha-2#Officially assigned code elements|adm0]]'),
        ('adm1', '[[:en:ISO 3166-2#Current codes|adm1]]'),
        ('adm2', None),
        ('adm3', None),
        ('adm4', None),
        ('source', 'source pages')
    ])
    numeric = [x for x in list(title_column.keys()) if x not in ('country', 'lang')]

    table = StatisticsTable(title_column, numeric, None)
    totals = dict.fromkeys(numeric, 0)
    country_format = (
        '[//tools.wmflabs.org/heritage/api/api.php?'
        'action=statistics&stcountry={country}&format=html&limit=0 {country}]')
    adm1_format = (
        '[//tools.wmflabs.org/heritage/api/api.php?'
        'action=adminlevels&format=json&admtree={adm0iso} {adm1}] '
        '<small>({adm1_p}%)</small>'
    )

    summation_row = (  # @todo: make use of common.table_bottom_row()
        '|- class="sortbottom"\n'
        '| || || {all} '
        '|| {name} <small>({name_p}%)</small> '
        '|| {address} <small>({address_p}%)</small> '
        '|| {municipality} <small>({municipality_p}%)</small> '
        '|| {coordinates} <small>({coordinates_p}%)</small> '
        '|| {image} <small>({image_p}%)</small> '
        '|| {commonscat} <small>({commonscat_p}%)</small> '
        '|| {article} <small>({article_p}%)</small> '
        '|| {wikidata} <small>({wikidata_p}%)</small> '
        '|| {adm0} <small>({adm0_p}%)</small> '
        '|| {adm1} <small>({adm1_p}%)</small> '
        '|| {adm2} <small>({adm2_p}%)</small> '
        '|| {adm3} <small>({adm3_p}%)</small> '
        '|| {adm4} <small>({adm4_p}%)</small> '
        '|| {source} '
    )

    empty_row = (
        '|-\n'
        '|| {country} || {lang}'
        '|| colspan="15" | Datasource [//tools.wmflabs.org/heritage/monuments_config/{country}_{lang}.json ({country}, {lang})] is configured, but no monuments are in the database.\n'
    )

    for country in sorted(statistics.keys()):
        for language in sorted(statistics.get(country).keys()):
            data = statistics[country][language]

            if not data:
                table.add_wikitext_row(empty_row.format(country=country, lang=language))
                continue

            display_data = {
                'country': country_format.format(**data),
                'lang': data.get('lang'),
                'all': data.get('all'),
                'source': data.get('source'),
                'adm1': adm1_format.format(
                    adm1_p=compute_percentage(
                        data.get('adm1'), data.get('all')),
                    **data)
            }
            for key in list(title_column.keys()):
                if key not in display_data:
                    display_data[key] = format_percentage(
                        data.get(key), data.get('all'))
            table.add_row(display_data, data)

    # construct total percentages
    totals = table.get_sum()
    for col in numeric:
        totals['{}_p'.format(col)] = compute_percentage(
            totals[col], totals['all'])

    table.add_wikitext_row(summation_row.format(**totals))
    output = table.to_wikitext(add_summation=False, inline=True)

    site = pywikibot.Site('commons', 'commons')
    page = pywikibot.Page(site, 'Commons:Monuments database/Statistics')
    comment = 'Updating monument database statistics'
    pywikibot.debug(output, _logger)
    common.save_to_wiki_or_local(page, comment, output)


def get_summary_statistics(country, language, conn, cursor):
    '''
    Do a bunch of queries to gather the statistics.
    '''
    queries = {}
    result = {}

    fields = [
        ('name', 'name'),
        ('address', 'address'),
        ('municipality', 'municipality'),
        ('coordinates', ('lat', 'lon')),
        ('image', 'image'),
        ('commonscat', 'commonscat'),
        ('article', 'monument_article'),
        ('wikidata', 'wd_item'),
        ('adm0', 'adm0'),
        ('adm1', 'adm1'),
        ('adm2', 'adm2'),
        ('adm3', 'adm3'),
        ('adm4', 'adm4'),
    ]

    for (label, database_field) in fields:
        queries[label] = build_summary_query(database_field)

    queries['all'] = (
        "SELECT COUNT(*) "
        "FROM monuments_all "
        "WHERE country='%s' AND lang='%s'")
    queries['adm0iso'] = (
        "SELECT adm0 "
        "FROM monuments_all "
        "WHERE country='%s' AND lang='%s' AND NOT (adm0='' OR adm0 IS NULL) "
        "LIMIT 1")
    queries['source'] = (
        "SELECT COUNT(DISTINCT(source)) "
        "FROM monuments_all "
        "WHERE country='%s' AND lang='%s'")

    result['country'] = country
    result['lang'] = language

    for (stat, query) in list(queries.items()):
        result[stat] = getCount(query % (country, language), cursor)

    return result


def build_summary_query(field_name):
    base_query = (
        "SELECT COUNT(*) "
        "FROM monuments_all "
        "WHERE country='%s' AND lang='%s' AND ")
    query = """NOT ({0}='' OR {0} IS NULL)"""
    if isinstance(field_name, tuple):
        return base_query + ' AND '.join([query.format(x) for x in field_name])
    else:
        return base_query + query.format(field_name)


def compute_percentage(value, total):
    return round(1.0 * value / max(total, 1) * 100, 2)


def format_percentage(value, total):
    percentage = compute_percentage(value, total)
    return '{0} <small>({1}%)</small>'.format(value, percentage)


def getLanguages(country, conn, cursor):
    '''
    Get the languages for a certain country code.
    '''
    result = []
    query = (
        "SELECT DISTINCT(lang) "
        "FROM monuments_all "
        "WHERE country=%s")

    # print query % (country,)
    cursor.execute(query, (country,))

    while True:
        try:
            (language,) = cursor.fetchone()
            result.append(language)
        except TypeError:
            break

    return result


def getCountries(conn, cursor):
    '''
    Get the list of country codes.
    '''
    result = []
    query = (
        "SELECT DISTINCT(country) "
        "FROM monuments_all")
    cursor.execute(query)

    while True:
        try:
            (country,) = cursor.fetchone()
            result.append(country)
        except TypeError:
            break

    return result


def main():
    """The main loop."""
    conn = None
    cursor = None
    skip_wd = False
    (conn, cursor) = connect_to_monuments_database()

    for arg in pywikibot.handle_args():
        option, sep, value = arg.partition(':')
        if option == '-skip_wd':
            skip_wd = True
        else:
            raise Exception(
                'Bad parameters. Expected "-skip_wd" or pywikibot args. '
                'Found "{}"'.format(option))

    statistics = {}

    for (countrycode, lang), countryconfig in mconfig.filtered_countries(
            skip_wd=skip_wd, skip_wlpa=True):
        if countrycode not in statistics:
            statistics[countrycode] = {}
        if lang not in statistics[countrycode]:
            statistics[countrycode][lang] = {}

    for country in getCountries(conn, cursor):
        for language in getLanguages(country, conn, cursor):
            statistics[country][language] = get_summary_statistics(
                country, language, conn, cursor)

    outputStatistics(statistics)
    close_database_connection(conn, cursor)


if __name__ == "__main__":
    main()
