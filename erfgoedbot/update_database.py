#!/usr/bin/python
# -*- coding: utf-8  -*-
'''
Update the monuments database either from a text file or from some wiki page(s)

Usage:
# loop through all countries
python update_database.py

# work on specific country-lang
python update_database.py -countrycode:XX -langcode:YY

'''
import os
import warnings
import datetime
import urlparse
import time
from collections import Counter

from requests.exceptions import Timeout

import pywikibot
import pywikibot.data.sparql
from pywikibot import pagegenerators

import monuments_config as mconfig
import common as common
from converters import (
    extractWikilink,
    extract_elements_from_template_param,
    remove_commons_category_prefix,
    CH1903Converter,
    int_to_european_digits
)
from checkers import (
    checkLat,
    checkLon,
    check_wikidata,
    check_integer,
    check_lat_with_lon
)
from database_connection import (
    close_database_connection,
    connect_to_monuments_database
)

_logger = "update_database"


class NoPrimkeyException(Exception):
    pass


def run_check(check, fieldValue, monumentKey, countryconfig, sourcePage):
    """Run a named check."""
    if check == 'checkLat':
        return checkLat(fieldValue, monumentKey, countryconfig, sourcePage)
    elif check == 'checkLon':
        return checkLon(fieldValue, monumentKey, countryconfig, sourcePage)
    elif check == 'checkWD':
        return check_wikidata(fieldValue, monumentKey, sourcePage)
    elif check == 'checkInt':
        return check_integer(fieldValue, monumentKey, sourcePage)
    else:
        raise pywikibot.Error('Un-defined check in config for %s: %s'
                              % (countryconfig.get('table'), check))


def convertField(field, contents, countryconfig):
    """Convert a field."""
    if field.get('conv') == 'extractWikilink':
        return extractWikilink(contents.get(field.get('source')))
    elif field.get('conv') == 'remove_commons_category_prefix':
        return remove_commons_category_prefix(
            contents.get(field.get('source')))
    elif field.get('conv') == 'generateRegistrantUrl' and \
            countryconfig.get('registrantUrlBase'):
        return countryconfig.get('registrantUrlBase') % (
            contents.get(field.get('source')),)
    elif field.get('conv') == 'to_default_numeral':
        return int_to_european_digits(
            contents.get(field.get('source')))
    elif field.get('conv') == 'CH1903ToLat':
        (lat, lon) = CH1903Converter(
            contents.get('CH1903_X'), contents.get('CH1903_Y'))
        return lat
    elif field.get('conv') == 'CH1903ToLon':
        (lat, lon) = CH1903Converter(
            contents.get('CH1903_X'), contents.get('CH1903_Y'))
        return lon
    elif field.get('conv') == 'generateRegistrantUrl-sv-ship' and \
            countryconfig.get('registrantUrlBase'):
        idurl = contents.get(field.get('source')).replace(' ', '')
        if not idurl.startswith('wiki'):
            return countryconfig.get('registrantUrlBase') % idurl
        else:
            return u''
    elif field.get('conv') == 'es-ct-fop':
        pano = contents.get(field.get('source'))
        if pano == u'dp':
            return u'pd'
        elif pano == u'sí':
            return u'FoP'
        elif pano == u'no':
            return u'noFoP'
        else:
            return u''
    elif field.get('conv') == 'generateRegistrantUrl-wlpa-es-ct' and \
            countryconfig.get('registrantUrlBase'):
        idurlP = contents.get(field.get('source')).split('/')
        if len(idurlP) == 2 and idurlP[0] == u'bcn':
            return countryconfig.get('registrantUrlBase') % (idurlP[1],)
        else:
            return contents.get(field.get('source'))
    elif field.get('conv') == 'il-fop':
        fop = contents.get(field.get('source'))
        if fop == u'PD':
            return u'pd'
        elif fop == u'YES':
            return u'FoP'
        elif fop == u'NO':
            return u'noFoP'
        else:
            return u''
    elif field.get('conv') == 'fi-fop':
        dyear = contents.get(field.get('source'))
        cyear = datetime.datetime.now().year
        try:
            dyear = int(dyear)
            if (dyear + 70) < cyear:
                return u'pd'
            else:
                return u'noFoP'
        except ValueError:
            return u'noFoP'
    else:
        raise pywikibot.Error(
            'Un-defined converter in config for %s: %s' % (
                countryconfig.get('table'), field.get('conv')))


def unknownFieldsStatistics(countryconfig, unknownFields):
    """
    Outputs a list of any unknown fields as a wikitext table.

    The table contains the name and frequency of the field and a sample of
    source pages where this field was encountered.
    """
    site = pywikibot.Site(u'commons', u'commons')
    page = pywikibot.Page(
        site, u'Commons:Monuments database/Unknown fields/{0}'.format(
            countryconfig.get('table')))
    summary = u'Updating the list of unknown fields'

    text = u'{| class="wikitable sortable"\n'
    text += u'! Field !! Count !! Sources\n'
    for key, counter in unknownFields.items():
        text += u'|-\n'
        text += u'| {0} || {1} || {2}\n'.format(
            key, sum(counter.values()), format_source_field(counter, site))

    text += u'|}\n'
    text += u'[[Category:Commons:Monuments database/Unknown fields]]'

    common.save_to_wiki_or_local(page, summary, text)


def format_source_field(sources, site, sample_size=4):
    """
    Format a list of source pages to fit in the statistics field.

    @param sources: set of pywikibot.Page objects
    @param site: the site to which the output should be written (commons)
    @param sample_size: the number of source pages to output
    """
    source_text = ''
    if len(sources) == 1:
        source_page = sources.keys()[0]
        source_text = source_page.title(
            asLink=True, withNamespace=False, insite=site)
    else:
        source_slice = sources.most_common(sample_size)
        remaining = len(sources) - len(source_slice)
        for (source_page, source_count) in source_slice:
            source_text += u'\n* {0} ({1})'.format(
                source_page.title(
                    asLink=True, withNamespace=False, insite=site),
                source_count
            )
        if remaining:
            source_text += u"\n* ''and {0} more page(s)''".format(remaining)

    return source_text


def updateMonument(contents, source, countryconfig, conn, cursor, sourcePage):
    """Update a single monument in the source database."""
    fieldnames = []
    fieldvalues = []

    # Source is the first field
    fieldnames.append(u'source')
    fieldvalues.append(source)

    monumentKey = u''
    if contents.get(countryconfig.get('primkey')):
        monumentKey = contents.get(countryconfig.get('primkey'))

    for field in countryconfig.get('fields'):
        if field.get('dest') and len(contents.get(field.get('source'))):
            fieldnames.append(field.get('dest'))

            # Do some conversions here
            fieldValue = u''  # Should this be None?
            if field.get('conv'):
                fieldValue = convertField(field, contents, countryconfig)
            else:
                fieldValue = contents.get(field.get('source'))

            if field.get('check'):
                # check data
                if not run_check(field.get('check'), fieldValue, monumentKey,
                                 countryconfig, sourcePage):
                    fieldValue = u''  # throw away input if check fails
            fieldvalues.append(fieldValue)

    if countryconfig.get('countryBbox'):
        check_lat_with_lon(fieldnames, monumentKey, sourcePage)

    query = u"""REPLACE INTO `%s`(""" % (countryconfig.get('table'),)

    delimiter = u''
    for fieldname in fieldnames:
        query += delimiter + u"""`%s`""" % (fieldname,)
        delimiter = u', '

    query += u""") VALUES ("""

    delimiter = u''
    for fieldvalue in fieldvalues:
        query += delimiter + u"""%s"""
        delimiter = u', '

    query += u""")"""

    # print query % tuple(fieldvalues)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        cursor.execute(query, fieldvalues)

        # FIXME : Disable for now because print throws UnicodeEncodeErrors
        # if len(w) == 1:
        #  print w[-1].message, " when running ", query % tuple(fieldvalues)

    # print contents
    # print u'updating!'
    # time.sleep(5)


def processHeader(params, countryconfig):
    """
    Get the defaults for the row templates.

    Return all fields that seem to be valid. Ignore other fields.
    """
    contents = {}
    validFields = []

    for field in countryconfig.get('fields'):
        validFields.append(field.get(u'source'))

    for param in params:
        (field, value) = extract_elements_from_template_param(param)

        # Check first that field is not empty
        if field.strip():
            # Is it in the fields list?
            if field in validFields:
                contents[field] = value

    return contents


def process_monument_wikidata(params, countryconfig, conn, cursor):
    """Process a single instance of a wikidata sparql result."""
    if params['itemLabel']:
        params['name'] = params['itemLabel'].value

    if params['image']:
        params['image'] = urlparse.unquote(params['image'].value).split('/')[-1]

    if params['adminLabel']:
        params['admin'] = params['adminLabel'].value

    if params['monument_article']:
        params['monument_article'], _site = common.get_page_from_url(params['monument_article'].value)

    params['source'] = params['item'].value
    params['wd_item'] = params['item'].getID()

    if params['coordinate']:
        params['lat'], params['lon'] = params['coordinate'].value[len('Point('):-1].split(' ')

    del params['coordinate']
    del params['adminLabel']
    del params['itemLabel']
    del params['item']

    kill_list = []
    for key, value in params.items():
        if not value:
            kill_list.append(key)
    for key in kill_list:
        del params[key]

    query = u"""REPLACE INTO `%s`(""" % (countryconfig.get('table'),)

    first_query = u''
    second_query = u''
    delimiter = u''
    value_list = []
    for key, value in params.items():
        first_query += delimiter + u"""`%s`""" % (key,)
        second_query += delimiter + u"""%s"""
        value_list.append(value)
        delimiter = u', '

    query += first_query + u""") VALUES ("""

    query += second_query + u""")"""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        cursor.execute(query, value_list)


def processMonument(params, source, countryconfig, conn, cursor, sourcePage,
                    headerDefaults, unknownFields):
    """Process a single instance of a monument row template."""
    title = sourcePage.title(True)

    # Get all the fields
    contents = {}
    # Add the source of information (permalink)
    contents['source'] = source
    for field in countryconfig.get('fields'):
        if field.get(u'source') in headerDefaults:
            contents[field.get(u'source')] = headerDefaults.get(
                field.get(u'source'))
        else:
            contents[field.get(u'source')] = u''

    contents['title'] = title

    for param in params:
        (field, value) = extract_elements_from_template_param(param)

        # Check first that field is not empty
        if field.strip():
            # Is it in the fields list?
            if field in contents:
                # Load it with Big fucking escape hack. Stupid mysql lib
                # Do this somewhere else.replace("'", "\\'")
                contents[field] = value
            else:
                # FIXME: Include more information where it went wrong
                pywikibot.debug(
                    u'Found unknown field on page %s : (%s: %s)' % (
                        title, field, value),
                    _logger)
                if field not in unknownFields:
                    unknownFields[field] = Counter()
                unknownFields[field][sourcePage] += 1
                # time.sleep(5)

    # If we truncate we don't have to check for primkey (it's a made up one)
    if countryconfig.get('truncate'):
        updateMonument(
            contents, source, countryconfig, conn, cursor, sourcePage)
    # Check if the primkey is a tuple and if all parts are present
    elif isinstance(countryconfig.get('primkey'), tuple):
        allKeys = True
        for partkey in countryconfig.get('primkey'):
            if not contents.get(lookupSourceField(partkey, countryconfig)):
                allKeys = False
        if allKeys:
            updateMonument(
                contents, source, countryconfig, conn, cursor, sourcePage)
    # Check if the primkey is filled. This only works for a single primkey,
    # not a tuple
    elif contents.get(lookupSourceField(countryconfig.get('primkey'), countryconfig)):
        updateMonument(
            contents, source, countryconfig, conn, cursor, sourcePage)
    else:
        raise NoPrimkeyException


def lookupSourceField(destination, countryconfig):
    """Lookup the source field of a destination."""
    for field in countryconfig.get('fields'):
        if field.get('dest') == destination:
            return field.get('source')


def processPage(page, source, countryconfig, conn, cursor, unknownFields=None):
    """
    Process a text containing one or multiple instances of the monument row template.
    """
    if not unknownFields:
        unknownFields = {}

    templates = page.templatesWithParams()
    headerDefaults = {}
    primkey_exceptions = 0

    for (template, params) in templates:
        template_name = template.title(withNamespace=False)
        if template_name == countryconfig.get('headerTemplate'):
            headerDefaults = processHeader(params, countryconfig)
        if template_name == countryconfig.get('rowTemplate'):
            # print template
            # print params
            try:
                processMonument(
                    params, source, countryconfig, conn, cursor, page,
                    headerDefaults, unknownFields)
            except NoPrimkeyException:
                primkey_exceptions += 1
            # time.sleep(5)
        elif template_name == u'Commonscat' and len(params) >= 1:
            query = u"""REPLACE INTO commonscat (site, title, commonscat) VALUES (%s, %s, %s)"""
            cursor.execute(
                query, (countryconfig.get('lang'), page.title(True), params[0]))

    # output missing primkey warning
    if primkey_exceptions > 0:
        pywikibot.warning(u"%d primkey(s) missing on %s (%s)" % (
            primkey_exceptions, page.title(True), countryconfig.get('table')))

    return unknownFields


def processCountry(countryconfig, conn, cursor, fullUpdate, daysBack):
    """Process all the monuments of one country."""
    if countryconfig.get('type') == 'sparql':
        process_country_wikidata(countryconfig, conn, cursor)
    else:
        process_country_list(countryconfig, conn, cursor, fullUpdate, daysBack)


def process_country_list(countryconfig, conn, cursor, fullUpdate, daysBack):
    """Process all the monuments of one country using row templates."""
    site = pywikibot.Site(countryconfig.get('lang'), countryconfig.get('project'))
    rowTemplate = pywikibot.Page(
        site, u'%s:%s' % (site.namespace(10), countryconfig.get('rowTemplate')))

    transGen = pagegenerators.ReferringPageGenerator(
        rowTemplate, onlyTemplateInclusion=True)
    filteredGen = pagegenerators.NamespaceFilterPageGenerator(
        transGen, countryconfig.get('namespaces'), site=site)

    if countryconfig.get('truncate') or fullUpdate:
        # Some countries are always truncated, otherwise only do it when
        # requested.
        query = u"""TRUNCATE table `%s`""" % (countryconfig.get('table'),)
        cursor.execute(query)
        generator = pagegenerators.PreloadingGenerator(filteredGen)
        # FIXME : Truncate the table
    else:
        # Preloading first because the whole page needs to be fetched to get
        # the time
        pregenerator = pagegenerators.PreloadingGenerator(filteredGen)
        begintime = datetime.datetime.utcnow() + \
            datetime.timedelta(days=0 - daysBack)
        generator = pagegenerators.EdittimeFilterPageGenerator(
            pregenerator, begintime=begintime)

    unknownFields = {}

    for page in generator:
        if page.exists() and not page.isRedirectPage():
            # Do some checking
            unknownFields = processPage(
                page, page.permalink(percent_encoded=False), countryconfig,
                conn, cursor, unknownFields=unknownFields)

    try:
        unknownFieldsStatistics(countryconfig, unknownFields)
    except pywikibot.exceptions.PageSaveRelatedError as e:
        pywikibot.warning(
            'Could not update field statistics. Details below:\n{}'.format(e))


def load_wikidata_template_sparql():
    """Fetch the SPARQL template for a wikidata config."""
    filename = 'wikidata_query.sparql'
    with open(os.path.join(get_template_dir(), filename), 'r') as f:
        sparql = f.read()
    return sparql


def get_template_dir():
    """Fetch the SQL template for a wikidata config."""
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'template')


def process_country_wikidata(countryconfig, conn, cursor):
    """Process all the monuments of one country using sparql."""
    sparql_select = countryconfig.get('sparql')
    sparql_template = load_wikidata_template_sparql()

    sparql_query = sparql_template % dict(
        select_statement=sparql_select,
        lang=countryconfig.get('lang'),
        project=countryconfig.get('project')
    )
    # print sparql_query
    sq = pywikibot.data.sparql.SparqlQuery()
    try:
        query_result = sq.select(sparql_query, full_data=True)
    except Timeout:
        pywikibot.output('Sparql endpoint being slow, giving it a moment...')
        time.sleep(10)
        query_result = sq.select(sparql_query, full_data=True)

    for resultitem in query_result:
        process_monument_wikidata(resultitem, countryconfig, conn, cursor)


def main():
    """The main loop."""
    # First find out what to work on

    countrycode = u''
    lang = u''
    fullUpdate = True
    skip_wd = False
    daysBack = 2  # Default 2 days. Runs every night so can miss one night.
    conn = None
    cursor = None
    (conn, cursor) = connect_to_monuments_database()

    for arg in pywikibot.handleArgs():
        option, sep, value = arg.partition(':')
        if option == '-countrycode':
            countrycode = value
        elif option == '-langcode':
            lang = value
        elif option == '-daysback':
            daysBack = int(value)
        elif option == u'-fullupdate':  # does nothing since already default
            fullUpdate = True
        elif option == u'-skip_wd':
            skip_wd = True
        else:
            raise Exception(
                u'Bad parameters. Expected "-countrycode", "-langcode", '
                u'"-daysback", "-fullupdate", "-skip_wd" or pywikibot args. '
                u'Found "{}"'.format(option))

    if countrycode and lang:
        if not mconfig.countries.get((countrycode, lang)):
            pywikibot.warning(
                u'I have no config for countrycode "%s" in language "%s"' % (
                    countrycode, lang))
            return False

        pywikibot.log(
            u'Working on countrycode "%s" in language "%s"' % (
                countrycode, lang))
        try:
            countryconfig = mconfig.countries.get((countrycode, lang))
            processCountry(countryconfig, conn, cursor, fullUpdate, daysBack)
        except Exception, e:
            pywikibot.error(
                u"Unknown error occurred when processing country "
                u"%s in lang %s\n%s" % (countrycode, lang, str(e)))
    elif countrycode or lang:
        raise Exception(u'The "countrycode" and "langcode" arguments must '
                        u'be used together.')
    else:
        for (countrycode, lang), countryconfig in mconfig.countries.iteritems():
            if (countryconfig.get('skip') or
                    (skip_wd and (countryconfig.get('type') == 'sparql'))):
                continue
            pywikibot.log(
                u'Working on countrycode "%s" in language "%s"' % (
                    countrycode, lang))
            try:
                processCountry(countryconfig, conn, cursor, fullUpdate,
                               daysBack)
            except Exception, e:
                pywikibot.error(
                    u"Unknown error occurred when processing country "
                    u"%s in lang %s\n%s" % (countrycode, lang, str(e)))
                continue

    close_database_connection(conn, cursor)


if __name__ == "__main__":
    main()
