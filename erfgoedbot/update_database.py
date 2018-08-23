#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
Update the monuments database from a text file, some wiki page(s) or sparql.

Usage:
# loop through all countries
python update_database.py

# work on specific country-lang
python update_database.py -countrycode:XX -langcode:YY
"""
from __future__ import unicode_literals

import datetime
import os
import time
import urlparse
import warnings
from collections import Counter, OrderedDict

from requests.exceptions import ConnectionError, Timeout

import pywikibot
import pywikibot.data.sparql
from pywikibot import pagegenerators

import common as common
import monuments_config as mconfig
from checkers import (
    check_integer,
    check_lat_with_lon,
    check_wikidata,
    checkLat,
    checkLon
)
from converters import (
    CH1903Converter,
    extract_elements_from_template_param,
    extractWikilink,
    int_to_european_digits,
    remove_commons_category_prefix
)
from database_connection import (
    close_database_connection,
    connect_to_monuments_database
)

_logger = 'update_database'


class NoPrimkeyException(Exception):
    pass


def run_check(check, field_value, monument_key, countryconfig, source_page):
    """Run a named check."""
    if check == 'checkLat':
        return checkLat(field_value, monument_key, countryconfig, source_page)
    elif check == 'checkLon':
        return checkLon(field_value, monument_key, countryconfig, source_page)
    elif check == 'checkWD':
        return check_wikidata(field_value, monument_key, source_page)
    elif check == 'checkInt':
        return check_integer(field_value, monument_key, source_page)
    else:
        raise pywikibot.Error('Un-defined check in config for {0}: {1}'.format(
            countryconfig.get('table'), check))


def convert_field(field, contents, countryconfig):
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
            return ''
    elif field.get('conv') == 'es-ct-fop':
        pano = contents.get(field.get('source'))
        if pano == 'dp':
            return 'pd'
        elif pano == 'sí':
            return 'FoP'
        elif pano == 'no':
            return 'noFoP'
        else:
            return ''
    elif field.get('conv') == 'generateRegistrantUrl-wlpa-es-ct' and \
            countryconfig.get('registrantUrlBase'):
        idurl_p = contents.get(field.get('source')).split('/')
        if len(idurl_p) == 2 and idurl_p[0] == 'bcn':
            return countryconfig.get('registrantUrlBase') % (idurl_p[1],)
        else:
            return contents.get(field.get('source'))
    elif field.get('conv') == 'il-fop':
        fop = contents.get(field.get('source'))
        if fop == 'PD':
            return 'pd'
        elif fop == 'YES':
            return 'FoP'
        elif fop == 'NO':
            return 'noFoP'
        else:
            return ''
    elif field.get('conv') == 'fi-fop':
        dyear = contents.get(field.get('source'))
        cyear = datetime.datetime.now().year
        try:
            dyear = int(dyear)
            if (dyear + 70) < cyear:
                return 'pd'
            else:
                return 'noFoP'
        except ValueError:
            return 'noFoP'
    else:
        raise pywikibot.Error(
            'Un-defined converter in config for {1}: {2}'.format(
                countryconfig.get('table'), field.get('conv')))


def unknown_fields_statistics(countryconfig, unknown_fields):
    """
    Outputs a list of any unknown fields as a wikitext table.

    The table contains the name and frequency of the field and a sample of
    source pages where this field was encountered.

    @param countryconfig: the configurations for the dataset being processed.
    @param unknown_fields: dict of discovered fields with each value being a
        Counter for how frequently the field is encountered per page.
    @return: dict summarising the usages
    """
    site = pywikibot.Site('commons', 'commons')
    page = pywikibot.Page(
        site, 'Commons:Monuments database/Unknown fields/{0}'.format(
            countryconfig.get('table')))
    summary = 'Updating the list of unknown fields with {0} entries'

    # People can add a /header template with more info
    text = common.instruction_header(
        ':c:Commons:Monuments_database/Unknown fields')

    total_usages = 0
    pages_with_fields = set()

    if not unknown_fields:
        text += '\nThere are no unknown fields left. Great work!\n'
    else:
        column_names = ('Field', 'Count', 'Sources')
        numeric_columns = ('Count', )
        columns = OrderedDict(
            [(col, col in numeric_columns) for col in column_names])
        text += common.table_header_row(columns)
        for key, counter in unknown_fields.iteritems():
            total_usages += sum(counter.values())
            pages_with_fields.update(counter.keys())
            text += '|-\n'
            text += '| {0} || {1} || {2}\n'.format(
                key, sum(counter.values()), format_source_field(counter, site))
        text += '|}\n'

    text += '[[Category:Commons:Monuments database/Unknown fields]]'

    common.save_to_wiki_or_local(
        page, summary.format(len(unknown_fields)), text)

    return {
        'report_page': page,
        'config': countryconfig,
        'total_fields': len(unknown_fields),
        'total_pages': len(pages_with_fields),
        'total_usages': total_usages
    }


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
            as_link=True, with_ns=False, insite=site)
    else:
        source_slice = sources.most_common(sample_size)
        remaining = len(sources) - len(source_slice)
        for (source_page, source_count) in source_slice:
            source_text += '\n* {0} ({1})'.format(
                source_page.title(
                    as_link=True, with_ns=False, insite=site),
                source_count
            )
        if remaining:
            source_text += "\n* ''and {0} more page(s)''".format(remaining)

    return source_text


def update_monument(contents, source, countryconfig, conn, cursor,
                    source_page):
    """Update a single monument in the source database."""
    fieldnames = []
    fieldvalues = []

    # Source is the first field
    fieldnames.append('source')
    fieldvalues.append(source)

    monument_key = ''
    if contents.get(countryconfig.get('primkey')):
        monument_key = contents.get(countryconfig.get('primkey'))

    for field in countryconfig.get('fields'):
        if field.get('dest') and len(contents.get(field.get('source'))):
            fieldnames.append(field.get('dest'))

            # Do some conversions here
            field_value = ''  # Should this be None?
            if field.get('conv'):
                field_value = convert_field(field, contents, countryconfig)
            else:
                field_value = contents.get(field.get('source'))

            if field.get('check'):
                # check data
                if not run_check(field.get('check'), field_value, monument_key,
                                 countryconfig, source_page):
                    field_value = ''  # throw away input if check fails
            fieldvalues.append(field_value)

    if countryconfig.get('countryBbox'):
        check_lat_with_lon(fieldnames, monument_key, source_page)

    query = "REPLACE INTO `{0}` (`{1}`) VALUES ({2})".format(
        countryconfig.get('table'),
        '`, `'.join(fieldnames),
        ('%s, ' * len(fieldnames)).rstrip(', '))

    # print query % tuple(fieldvalues)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        cursor.execute(query, fieldvalues)

        # FIXME : Disable for now because print throws UnicodeEncodeErrors
        # if len(w) == 1:
        #  print w[-1].message, ' when running ', query % tuple(fieldvalues)

    # print contents
    # print 'updating!'
    # time.sleep(5)


def process_header(params, countryconfig):
    """
    Get the defaults for the row templates.

    Return all fields that seem to be valid. Ignore other fields.
    """
    contents = {}
    valid_fields = []

    for field in countryconfig.get('fields'):
        valid_fields.append(field.get('source'))

    for param in params:
        (field, value) = extract_elements_from_template_param(param)

        # Check first that field is not empty
        if field.strip():
            # Is it in the fields list?
            if field in valid_fields:
                contents[field] = value

    return contents


def monument_wikidata_generator(query_result, params):
    """Generator of monument database data from sparql query results."""
    for result_item in query_result:
        yield process_monument_wikidata(result_item, params)


def process_monument_wikidata(result, param_order):
    """Process a single instance of a wikidata sparql result."""
    # convert pywikibot.data.sparql.Literal to string
    literals = ('itemLabel', 'id', 'commonscat', 'address')
    for key in literals:
        if result[key]:
            result[key] = result[key].value

    if result['image']:
        result['image'] = urlparse.unquote(
            result['image'].value).split('/')[-1]

    if result['adminLabel']:
        result['admin'] = result['adminLabel'].value

    if result['monument_article']:
        result['monument_article'], _site = common.get_page_from_url(
            result['monument_article'].value)

    result['source'] = result['item'].value
    result['wd_item'] = result['item'].getID()

    if result['coordinate']:
        result['lat'], result['lon'] = result['coordinate'].value[
            len('Point('):-1].split(' ')

    # remove params that may not be NULL
    non_null_params = set(param_order) - set(('lat', 'lon'))
    for key in non_null_params:
        if key in result and not result[key]:
            del result[key]

    return tuple([result.get(key, '') for key in param_order])


def process_monument(params, source, countryconfig, conn, cursor, source_page,
                     header_defaults, unknown_fields):
    """Process a single instance of a monument row template."""
    title = source_page.title(True)

    # Get all the fields
    contents = {}
    # Add the source of information (permalink)
    contents['source'] = source
    for field in countryconfig.get('fields'):
        if field.get('source') in header_defaults:
            contents[field.get('source')] = header_defaults.get(
                field.get('source'))
        else:
            contents[field.get('source')] = ''

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
                    'Found unknown field on page {0} : ({1}: {2})'.format(
                        title, field, value),
                    _logger)
                if field not in unknown_fields:
                    unknown_fields[field] = Counter()
                unknown_fields[field][source_page] += 1
                # time.sleep(5)

    # If we truncate we don't have to check for primkey (it's a made up one)
    if countryconfig.get('truncate'):
        update_monument(
            contents, source, countryconfig, conn, cursor, source_page)
    # Check if the primkey is a tuple and if all parts are present
    elif isinstance(countryconfig.get('primkey'), tuple):
        all_keys = True
        for partkey in countryconfig.get('primkey'):
            if not contents.get(lookup_source_field(partkey, countryconfig)):
                all_keys = False
        if all_keys:
            update_monument(
                contents, source, countryconfig, conn, cursor, source_page)
    # Check if the primkey is filled. This only works for a single primkey,
    # not a tuple
    elif contents.get(lookup_source_field(countryconfig.get('primkey'),
                                          countryconfig)):
        update_monument(
            contents, source, countryconfig, conn, cursor, source_page)
    else:
        raise NoPrimkeyException


def lookup_source_field(destination, countryconfig):
    """Lookup the source field of a destination."""
    for field in countryconfig.get('fields'):
        if field.get('dest') == destination:
            return field.get('source')


def process_page(page, source, countryconfig, conn, cursor,
                 unknown_fields=None):
    """
    Process text containing one or more instances of the monument row template.

    Also makes a record of any unexpected fields.
    """
    if not unknown_fields:
        unknown_fields = {}

    templates = page.templatesWithParams()
    header_defaults = {}
    primkey_exceptions = 0

    for (template, params) in templates:
        template_name = template.title(with_ns=False)
        if template_name == countryconfig.get('headerTemplate'):
            header_defaults = process_header(params, countryconfig)
        if template_name == countryconfig.get('rowTemplate'):
            # print template
            # print params
            try:
                process_monument(
                    params, source, countryconfig, conn, cursor, page,
                    header_defaults, unknown_fields)
            except NoPrimkeyException:
                primkey_exceptions += 1
            # time.sleep(5)
        elif template_name == 'Commonscat' and len(params) >= 1:
            query = (
                """REPLACE INTO commonscat (site, title, commonscat) """
                """VALUES (%s, %s, %s)""")
            cursor.execute(
                query,
                (countryconfig.get('lang'), page.title(True), params[0]))

    # output missing primkey warning
    if primkey_exceptions > 0:
        pywikibot.warning('{0:d} primkey(s) missing on {1} ({2})'.format(
            primkey_exceptions, page.title(True), countryconfig.get('table')))

    return unknown_fields


def process_country(countryconfig, conn, cursor, full_update, days_back):
    """Process all the monuments of one country."""
    if countryconfig.get('type') == 'sparql':
        process_country_wikidata(countryconfig, conn, cursor)
    else:
        return process_country_list(
            countryconfig, conn, cursor, full_update, days_back)


def process_country_list(countryconfig, conn, cursor, full_update, days_back):
    """Process all the monuments of one country using row templates."""
    site = pywikibot.Site(countryconfig.get('lang'),
                          countryconfig.get('project'))
    row_template = pywikibot.Page(
        site, '{0}:{1}'.format(site.namespace(10),
                               countryconfig.get('rowTemplate')))

    trans_gen = pagegenerators.ReferringPageGenerator(
        row_template, onlyTemplateInclusion=True)
    filtered_gen = pagegenerators.NamespaceFilterPageGenerator(
        trans_gen, countryconfig.get('namespaces'), site=site)

    if countryconfig.get('truncate') or full_update:
        # Some countries are always truncated, otherwise only do it when
        # requested.
        query = """TRUNCATE table `{0}`""".format(countryconfig.get('table'))
        cursor.execute(query)
        generator = pagegenerators.PreloadingGenerator(filtered_gen)
        # FIXME : Truncate the table
    else:
        # Preloading first because the whole page needs to be fetched to get
        # the time
        pregenerator = pagegenerators.PreloadingGenerator(filtered_gen)
        begintime = datetime.datetime.utcnow() + \
            datetime.timedelta(days=0 - days_back)
        generator = pagegenerators.EdittimeFilterPageGenerator(
            pregenerator, begintime=begintime)

    unknown_fields = {}

    for page in generator:
        if page.exists() and not page.isRedirectPage():
            # Do some checking
            unknown_fields = process_page(
                page, page.permalink(percent_encoded=False), countryconfig,
                conn, cursor, unknown_fields=unknown_fields)

    return unknown_fields_statistics(countryconfig, unknown_fields)


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

    sq = pywikibot.data.sparql.SparqlQuery()
    try:
        query_result = sq.select(sparql_query, full_data=True)
    except (Timeout, ConnectionError):
        # timeout on https may end up being interpreted as a ConnectionError
        pywikibot.output('Sparql endpoint being slow, giving it a moment...')
        time.sleep(10)
        query_result = sq.select(sparql_query, full_data=True)

    pywikibot.output('Sparql query successful with {0} results'.format(
        len(query_result)))

    # todo: check and log duplicate ids manually
    params = ['monument_article', 'name', 'source', 'admin', 'image', 'lon',
              'wd_item', 'lat', 'address', 'commonscat', 'id']

    query = "REPLACE INTO `{0}` (`{1}`) VALUES ({2})".format(
        countryconfig.get('table'),
        '`, `'.join(params),
        ('%s, ' * len(params)).rstrip(', '))

    batch_size = 100
    for result_chunk in [query_result[i:i + batch_size]
                         for i in xrange(0, len(query_result), batch_size)]:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            cursor.executemany(
                query,
                monument_wikidata_generator(result_chunk, params))
        conn.commit()

    pywikibot.output('Finished processing {0} results'.format(
        min(len(query_result), i + batch_size)))


def make_statistics(statistics):
    """Output the overall results for unknown fields as a nice wikitable."""
    site = pywikibot.Site('commons', 'commons')
    page = pywikibot.Page(
        site, 'Commons:Monuments database/Unknown fields/Statistics')

    column_names = ('country', 'lang', 'Total fields', 'Total usage of fields',
                    'Total pages containing fields', 'Report page',
                    'Row template', 'Header template')
    columns = OrderedDict(
        [(col, col.startswith('Total ')) for col in column_names])
    text = common.table_header_row(columns)

    text_row = (
        '|-\n'
        '| {code} \n'
        '| {lang} \n'
        '| {total_fields} \n'
        '| {total_usages} \n'
        '| {total_pages} \n'
        '| {report_page} \n'
        '| {row_template} \n'
        '| {header_template} \n')

    total_fields_sum = 0
    total_usages_sum = 0
    total_pages_sum = 0
    for row in statistics:
        if not row:
            # sparql harvests don't generate statistics
            continue
        countryconfig = row.get('config')
        total_fields = row.get('total_fields')
        total_usages = row.get('total_usages')
        total_pages = row.get('total_pages')

        total_fields_sum += total_fields
        total_usages_sum += total_usages
        total_pages_sum += total_pages

        list_site = pywikibot.Site(
            countryconfig.get('lang'),
            countryconfig.get('project', 'wikipedia'))
        row_template_page = pywikibot.Page(
            list_site,
            'Template:{0}'.format(countryconfig.get('rowTemplate')))
        header_template_page = pywikibot.Page(
            list_site,
            'Template:{0}'.format(countryconfig.get('headerTemplate')))

        row_template = row_template_page.title(
            as_link=True, with_ns=False, insite=site)
        header_template = header_template_page.title(
            as_link=True, with_ns=False, insite=site)
        report_page = row.get('report_page').title(
            as_link=True, with_ns=False, insite=site)

        text += text_row.format(
            code=countryconfig.get('country'),
            lang=countryconfig.get('lang'),
            total_fields=total_fields,
            total_usages=total_usages,
            total_pages=total_pages,
            report_page=report_page,
            row_template=row_template,
            header_template=header_template)

    text += common.table_bottom_row(8, {
        2: total_fields_sum,
        3: total_usages_sum,
        4: total_pages_sum})

    comment = (
        'Updating unknown fields statistics. Total of {total_fields} '
        'unknown fields used {total_usages} times on {total_pages} different '
        'pages.'.format(total_fields=total_fields_sum,
                        total_usages=total_usages_sum,
                        total_pages=total_pages_sum))
    pywikibot.debug(text, _logger)
    common.save_to_wiki_or_local(page, comment, text)


def main():
    """The main loop."""
    # First find out what to work on

    countrycode = ''
    lang = ''
    full_update = True
    skip_wd = False
    days_back = 2  # Default 2 days. Runs every night so can miss one night.
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
            days_back = int(value)
        elif option == '-fullupdate':  # does nothing since already default
            full_update = True
        elif option == '-skip_wd':
            skip_wd = True
        else:
            raise Exception(
                'Bad parameters. Expected "-countrycode", "-langcode", '
                '"-daysback", "-fullupdate", "-skip_wd" or pywikibot args. '
                'Found "{}"'.format(option))

    if countrycode and lang:
        if not mconfig.countries.get((countrycode, lang)):
            pywikibot.warning(
                'I have no config for countrycode "{0}" '
                'in language "{1}"'.format(
                    countrycode, lang))
            return False

        pywikibot.log(
            'Working on countrycode "{0}" in language "{1}"'.format(
                countrycode, lang))
        try:
            countryconfig = mconfig.countries.get((countrycode, lang))
            process_country(countryconfig, conn, cursor, full_update,
                            days_back)
        except Exception, e:
            pywikibot.error(
                'Unknown error occurred when processing country '
                '{0} in lang {1}\n{2}'.format(countrycode, lang, str(e)))
    elif countrycode or lang:
        raise Exception('The "countrycode" and "langcode" arguments must '
                        'be used together.')
    else:
        statistics = []
        for (countrycode, lang), countryconfig in mconfig.countries.iteritems():
            if (countryconfig.get('skip') or
                    (skip_wd and (countryconfig.get('type') == 'sparql'))):
                continue
            pywikibot.log(
                'Working on countrycode "{0}" in language "{1}"'.format(
                    countrycode, lang))
            try:
                statistics.append(
                    process_country(countryconfig, conn, cursor, full_update,
                                    days_back))
            except Exception, e:
                pywikibot.error(
                    'Unknown error occurred when processing country '
                    '{0} in lang {1}\n{2}'.format(countrycode, lang, str(e)))
                continue
        make_statistics(statistics)

    close_database_connection(conn, cursor)


if __name__ == "__main__":
    main()
