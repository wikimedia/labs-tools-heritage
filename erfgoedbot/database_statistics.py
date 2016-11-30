#!/usr/bin/python
# -*- coding: utf-8  -*-
'''
Update the statistics of the monuments database at https://commons.wikimedia.org/wiki/Commons:Monuments_database/Statistics
FIXME: Too much code duplication. Should probably just have one list of the possible fields for the functions to work on.

'''
import pywikibot

from database_connection import connect_to_monuments_database


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
    page.put(newtext=output, comment=comment)


def getStatistics(country, language, conn, cursor):
    '''
    Do a bunch of queries to gather the statistics.
    '''
    queries = {}
    result = {}

    queries[
        'all'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s'"""
    queries[
        'name'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (name='' OR name IS NULL)"""
    queries[
        'address'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (address='' OR address IS NULL)"""
    queries[
        'municipality'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (municipality='' OR municipality IS NULL)"""
    queries[
        'coordinates'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (lat=0 OR lat IS NULL) AND NOT (lon=0 OR lon IS NULL)"""
    queries[
        'image'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (image='' OR image IS NULL)"""
    queries[
        'commonscat'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (commonscat='' OR commonscat IS NULL)"""
    queries[
        'article'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (monument_article='' OR monument_article IS NULL)"""
    queries[
        'wikidata'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (wd_item='' OR wd_item IS NULL)"""

    queries[
        'adm0iso'] = u"""SELECT adm0 FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (adm0='' OR adm0 IS NULL) LIMIT 1"""
    queries[
        'adm0'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (adm0='' OR adm0 IS NULL)"""
    queries[
        'adm1'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (adm1='' OR adm1 IS NULL)"""
    queries[
        'adm2'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (adm2='' OR adm2 IS NULL)"""
    queries[
        'adm3'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (adm3='' OR adm3 IS NULL)"""
    queries[
        'adm4'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (adm4='' OR adm4 IS NULL)"""

    queries[
        'source'] = u"""SELECT COUNT(DISTINCT(source)) FROM monuments_all WHERE country='%s' AND lang='%s'"""

    result['country'] = country
    result['lang'] = language

    for (stat, query) in queries.items():
        # print query % (country, language)
        result[stat] = getCount(query % (country, language), cursor)

    result['namePercentage'] = round(
        1.0 * result['name'] / result['all'] * 100, 2)
    result['addressPercentage'] = round(
        1.0 * result['address'] / result['all'] * 100, 2)
    result['municipalityPercentage'] = round(
        1.0 * result['municipality'] / result['all'] * 100, 2)
    result['coordinatesPercentage'] = round(
        1.0 * result['coordinates'] / result['all'] * 100, 2)
    result['imagePercentage'] = round(
        1.0 * result['image'] / result['all'] * 100, 2)
    result['commonscatPercentage'] = round(
        1.0 * result['commonscat'] / result['all'] * 100, 2)
    result['articlePercentage'] = round(
        1.0 * result['article'] / result['all'] * 100, 2)
    result['wikidataPercentage'] = round(
        1.0 * result['wikidata'] / result['all'] * 100, 2)

    result['adm0Percentage'] = round(
        1.0 * result['adm0'] / result['all'] * 100, 2)
    result['adm1Percentage'] = round(
        1.0 * result['adm1'] / result['all'] * 100, 2)
    result['adm2Percentage'] = round(
        1.0 * result['adm2'] / result['all'] * 100, 2)
    result['adm3Percentage'] = round(
        1.0 * result['adm3'] / result['all'] * 100, 2)
    result['adm4Percentage'] = round(
        1.0 * result['adm4'] / result['all'] * 100, 2)

    return result


def getLanguages(country, conn, cursor):
    '''
    Get the languages for a certain country code.
    '''
    result = []
    query = u"""SELECT DISTINCT(lang) FROM monuments_all WHERE country='%s'"""

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
    query = u"""SELECT DISTINCT(country) FROM monuments_all"""
    cursor.execute(query)

    while True:
        try:
            (country,) = cursor.fetchone()
            result.append(country)
        except TypeError:
            break

    return result


def main():
    '''
    The main loop
    '''

    conn = None
    cursor = None
    (conn, cursor) = connect_to_monuments_database()

    statistics = {}

    for country in getCountries(conn, cursor):
        statistics[country] = {}
        for language in getLanguages(country, conn, cursor):
            statistics[country][language] = getStatistics(
                country, language, conn, cursor)

    outputStatistics(statistics)


if __name__ == "__main__":
    main()
