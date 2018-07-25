#!/usr/bin/python
# -*- coding: utf-8  -*-
'''
Update the statistics of the monuments database at https://commons.wikimedia.org/wiki/Commons:Monuments_database/Statistics
FIXME: Too much code duplication. Should probably just have one list of the possible fields for the functions to work on.

'''
import pywikibot

import common as common
from database_connection import (
    close_database_connection,
    connect_to_monuments_database
)


def getCount(query, cursor):
    '''
    Return the result of the query
    '''
    cursor.execute(query)

    count, = cursor.fetchone()
    return count


def outputStatistics(statistics):
    '''
    Output the statistics in wikitext on Commons
    '''

    output = u'{| class="wikitable sortable"\n'
    output += \
        u'! country !! [[:en:List of ISO 639-1 codes|lang]] !! data-sort-type="number"|total !! data-sort-type="number"|name !! data-sort-type="number"|address !! data-sort-type="number"|municipality !!data-sort-type="number"| coordinates !! data-sort-type="number"|image !! data-sort-type="number"|commonscat !! data-sort-type="number"|article !! data-sort-type="number"|wikidata !! data-sort-type="number"|[[:en:ISO 3166-1 alpha-2#Officially assigned code elements|adm0]] !! data-sort-type="number"|[[:en:ISO 3166-2#Current codes|adm1]] !! data-sort-type="number"|adm2 !! data-sort-type="number"|adm3 !!data-sort-type="number"| adm4 !! data-sort-type="number"|source pages\n'

    totals = {}

    totals['all'] = 0
    totals['name'] = 0
    totals['address'] = 0
    totals['municipality'] = 0
    totals['coordinates'] = 0
    totals['image'] = 0
    totals['commonscat'] = 0
    totals['article'] = 0
    totals['wikidata'] = 0

    totals['adm0'] = 0
    totals['adm1'] = 0
    totals['adm2'] = 0
    totals['adm3'] = 0
    totals['adm4'] = 0

    totals['source'] = 0

    for country in sorted(statistics.keys()):
        for language in sorted(statistics.get(country).keys()):
            # print country
            # print language
            # print statistics[country][language]

            output += u'|-\n'
            output += \
                u'| [//tools.wmflabs.org/heritage/api/api.php?action=statistics&stcountry=%(country)s&format=html&limit=0 %(country)s] ' % statistics[
                    country][language]
            output += \
                u'|| %(lang)s || %(all)s ' % statistics[country][language]
            output += \
                u'|| %(name)s <small>(%(namePercentage)s%%)</small>' % statistics[
                    country][language]
            output += \
                u'|| %(address)s <small>(%(addressPercentage)s%%)</small>' % statistics[
                    country][language]
            output += \
                u'|| %(municipality)s <small>(%(municipalityPercentage)s%%)</small>' % statistics[
                    country][language]
            output += \
                u'|| %(coordinates)s <small>(%(coordinatesPercentage)s%%)</small>' % statistics[
                    country][language]
            output += \
                u'|| %(image)s <small>(%(imagePercentage)s%%)</small>' % statistics[
                    country][language]
            output += \
                u'|| %(commonscat)s <small>(%(commonscatPercentage)s%%)</small>' % statistics[
                    country][language]
            output += \
                u'|| %(article)s <small>(%(articlePercentage)s%%)</small>' % statistics[
                    country][language]
            output += \
                u'|| %(wikidata)s <small>(%(wikidataPercentage)s%%)</small>' % statistics[
                    country][language]

            output += \
                u'|| %(adm0)s <small>(%(adm0Percentage)s%%)</small>' % statistics[
                    country][language]
            output += \
                u'|| [//tools.wmflabs.org/heritage/api/api.php?action=adminlevels&format=json&admtree=%(adm0iso)s %(adm1)s] <small>(%(adm1Percentage)s%%)</small>' % statistics[
                    country][language]
            output += \
                u'|| %(adm2)s <small>(%(adm2Percentage)s%%)</small>' % statistics[
                    country][language]
            output += \
                u'|| %(adm3)s <small>(%(adm3Percentage)s%%)</small>' % statistics[
                    country][language]
            output += \
                u'|| %(adm4)s <small>(%(adm4Percentage)s%%)</small>' % statistics[
                    country][language]

            output += \
                u'|| %(source)s\n' % statistics[country][language]

            totals['all'] += \
                statistics[country][language]['all']
            totals['name'] += \
                statistics[country][language]['name']
            totals['address'] += \
                statistics[country][language]['address']
            totals['municipality'] += \
                statistics[country][language]['municipality']
            totals['coordinates'] += \
                statistics[country][language]['coordinates']
            totals['image'] += \
                statistics[country][language]['image']
            totals['commonscat'] += \
                statistics[country][language]['commonscat']
            totals['article'] += \
                statistics[country][language]['article']
            totals['wikidata'] += \
                statistics[country][language]['wikidata']

            totals['adm0'] += \
                statistics[country][language]['adm0']
            totals['adm1'] += \
                statistics[country][language]['adm1']
            totals['adm2'] += \
                statistics[country][language]['adm2']
            totals['adm3'] += \
                statistics[country][language]['adm3']
            totals['adm4'] += \
                statistics[country][language]['adm4']

            totals['source'] += \
                statistics[country][language]['source']

    totals['namePercentage'] = round(
        1.0 * totals['name'] / totals['all'] * 100, 2)
    totals['addressPercentage'] = round(
        1.0 * totals['address'] / totals['all'] * 100, 2)
    totals['municipalityPercentage'] = round(
        1.0 * totals['municipality'] / totals['all'] * 100, 2)
    totals['coordinatesPercentage'] = round(
        1.0 * totals['coordinates'] / totals['all'] * 100, 2)
    totals['imagePercentage'] = round(
        1.0 * totals['image'] / totals['all'] * 100, 2)
    totals['commonscatPercentage'] = round(
        1.0 * totals['commonscat'] / totals['all'] * 100, 2)
    totals['articlePercentage'] = round(
        1.0 * totals['article'] / totals['all'] * 100, 2)
    totals['wikidataPercentage'] = round(
        1.0 * totals['wikidata'] / totals['all'] * 100, 2)

    totals['adm0Percentage'] = round(
        1.0 * totals['adm0'] / totals['all'] * 100, 2)
    totals['adm1Percentage'] = round(
        1.0 * totals['adm1'] / totals['all'] * 100, 2)
    totals['adm2Percentage'] = round(
        1.0 * totals['adm2'] / totals['all'] * 100, 2)
    totals['adm3Percentage'] = round(
        1.0 * totals['adm3'] / totals['all'] * 100, 2)
    totals['adm4Percentage'] = round(
        1.0 * totals['adm4'] / totals['all'] * 100, 2)

    output += u'|- class="sortbottom"\n'
    output += u'| '
    output += u'|| || %(all)s' % totals
    output += \
        u'|| %(name)s <small>(%(namePercentage)s%%)</small>' % totals
    output += \
        u'|| %(address)s <small>(%(addressPercentage)s%%)</small>' % totals
    output += \
        u'|| %(municipality)s <small>(%(municipalityPercentage)s%%)</small>' % totals
    output += \
        u'|| %(coordinates)s <small>(%(coordinatesPercentage)s%%)</small>' % totals
    output += \
        u'|| %(image)s <small>(%(imagePercentage)s%%)</small>' % totals
    output += \
        u'|| %(commonscat)s <small>(%(commonscatPercentage)s%%)</small>' % totals
    output += \
        u'|| %(article)s <small>(%(articlePercentage)s%%)</small>' % totals
    output += \
        u'|| %(wikidata)s <small>(%(wikidataPercentage)s%%)</small>' % totals

    output += \
        u'|| %(adm0)s <small>(%(adm0Percentage)s%%)</small>' % totals
    output += \
        u'|| %(adm1)s <small>(%(adm1Percentage)s%%)</small>' % totals
    output += \
        u'|| %(adm2)s <small>(%(adm2Percentage)s%%)</small>' % totals
    output += \
        u'|| %(adm3)s <small>(%(adm3Percentage)s%%)</small>' % totals
    output += \
        u'|| %(adm4)s <small>(%(adm4Percentage)s%%)</small>' % totals

    output += u'|| %(source)s\n' % totals

    output += u'|}\n'

    site = pywikibot.Site('commons', 'commons')
    page = pywikibot.Page(site, u'Commons:Monuments database/Statistics')
    comment = u'Updating monument database statistics'
    common.save_to_wiki_or_local(page, comment, output)


def getStatistics(country, language, conn, cursor):
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
        queries[label] = build_query(database_field)

    queries['all'] = (
        u"SELECT COUNT(*) "
        u"FROM monuments_all "
        u"WHERE country='%s' AND lang='%s'")
    queries['adm0iso'] = (
        u"SELECT adm0 "
        u"FROM monuments_all "
        u"WHERE country='%s' AND lang='%s' AND NOT (adm0='' OR adm0 IS NULL) "
        u"LIMIT 1")
    queries['source'] = (
        u"SELECT COUNT(DISTINCT(source)) "
        u"FROM monuments_all "
        u"WHERE country='%s' AND lang='%s'")

    result['country'] = country
    result['lang'] = language

    for (stat, query) in queries.items():
        result[stat] = getCount(query % (country, language), cursor)

    for (field_label, _) in fields:
        result[field_label + 'Percentage'] = compute_percentage(result[field_label], result['all'])

    return result


def build_query(field_name):
    base_query = (
        u"SELECT COUNT(*) "
        u"FROM monuments_all "
        u"WHERE country='%s' AND lang='%s' AND ")
    query = u"""NOT ({0}='' OR {0} IS NULL)"""
    if isinstance(field_name, tuple):
        return base_query + ' AND '.join([query.format(x) for x in field_name])
    else:
        return base_query + query.format(field_name)


def compute_percentage(value, total):
    return round(1.0 * value / max(total, 1) * 100, 2)


def getLanguages(country, conn, cursor):
    '''
    Get the languages for a certain country code.
    '''
    result = []
    query = (
        u"SELECT DISTINCT(lang) "
        u"FROM monuments_all "
        u"WHERE country='%s'")

    # print query % (country,)
    cursor.execute(query % (country,))

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
        u"SELECT DISTINCT(country) "
        u"FROM monuments_all")
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
    (conn, cursor) = connect_to_monuments_database()

    for arg in pywikibot.handleArgs():
        option, sep, value = arg.partition(':')
        raise Exception(
            u'Bad parameters. Expected pywikibot args. '
            u'Found "{}"'.format(option))

    statistics = {}

    for country in getCountries(conn, cursor):
        statistics[country] = {}
        for language in getLanguages(country, conn, cursor):
            statistics[country][language] = getStatistics(
                country, language, conn, cursor)

    outputStatistics(statistics)
    close_database_connection(conn, cursor)


if __name__ == "__main__":
    main()
