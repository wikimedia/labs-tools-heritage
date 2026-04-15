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


import datetime
import os
import time
import urllib.parse
import warnings
from collections import Counter, OrderedDict

from requests.exceptions import ConnectionError, Timeout

import pywikibot
import pywikibot.data.sparql
from pywikibot import pagegenerators

import erfgoedbot.common as common
import erfgoedbot.monuments_config as mconfig
from erfgoedbot.checkers import (
    check_integer,
    check_lat_with_lon,
    check_wikidata,
    checkLat,
    checkLon
)
from erfgoedbot.converters import (
    CH1903Converter,
    extract_elements_from_template_param,
    extractWikilink,
    int_to_european_digits,
    remove_commons_category_prefix
)
from erfgoedbot.database_connection import (
    close_database_connection,
    connect_to_monuments_database
)
from erfgoedbot.statistics_table import StatisticsTable

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
        raise pywikibot.exceptions.Error('Un-defined check in config for {0}: {1}'.format(
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
        raise pywikibot.exceptions.Error(
            'Un-defined converter in config for {1}: {2}'.format(
                countryconfig.get('table'), field.get('conv')))


def _per_country_report(countryconfig, data, report_type,
                        title_column, row_builder,
                        total_entries=0, total_pages=0):
    """
    Shared skeleton for per-country report pages.

    Builds a wikitext table from *data*, saves it to a Commons subpage,
    and returns a dict with unified keys.

    @param countryconfig: the configurations for the dataset being processed.
    @param data: the data dict/Counter to iterate over.
    @param report_type: report name used in page title and category
        (e.g. 'Unknown fields').
    @param title_column: list of column names for the StatisticsTable.
    @param row_builder: callable(key, value, site) returning a row dict.
    @param total_entries: pre-computed entry count.
    @param total_pages: pre-computed page count.
    @return: dict with keys report_page, config, total_entries, total_pages,
        total_occurrences.
    """
    done_label = report_type[0].lower() + report_type[1:]
    site = pywikibot.Site('commons', 'commons')
    page = pywikibot.Page(
        site, 'Commons:Monuments database/{0}/{1}'.format(
            report_type, countryconfig.get('table')))
    summary = 'Updating the list of {0} with {{0}} entries'.format(
        done_label)

    central_page = ':c:Commons:Monuments_database/{0}'.format(report_type)
    text = common.instruction_header(central_page)

    total_occurrences = 0

    if not data:
        text += common.done_message(central_page, done_label)
    else:
        table = StatisticsTable(
            title_column, ['Count'], (title_column[0],))
        for key, value in data.items():
            table.add_row(row_builder(key, value, site))
        total_occurrences = table.get_sum('Count')
        text += table.to_wikitext(add_summation=False, inline=True)

    text += '[[Category:Commons:Monuments database/{0}]]'.format(report_type)

    common.save_to_wiki_or_local(
        page, summary.format(len(data)), text)

    return {
        'report_page': page,
        'config': countryconfig,
        'total_entries': total_entries or 0,
        'total_pages': total_pages or 0,
        'total_occurrences': total_occurrences
    }


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
    pages_with_fields = set()
    for counter in unknown_fields.values():
        pages_with_fields.update(list(counter.keys()))

    def row_builder(key, counter, site):
        return {
            'Field': key,
            'Count': sum(counter.values()),
            'Sources': format_source_field(counter, site)
        }

    return _per_country_report(
        countryconfig, unknown_fields,
        report_type='Unknown fields',
        title_column=['Field', 'Count', 'Sources'],
        row_builder=row_builder,
        total_entries=len(unknown_fields),
        total_pages=len(pages_with_fields)
    )


def format_source_field(sources, site, sample_size=4):
    """
    Format a list of source pages to fit in the statistics field.

    @param sources: set of pywikibot.Page objects
    @param site: the site to which the output should be written (commons)
    @param sample_size: the number of source pages to output
    """
    source_text = ''
    if len(sources) == 1:
        source_page = list(sources.keys())[0]
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


def duplicate_ids_statistics(countryconfig, duplicate_ids):
    """
    Outputs a list of any duplicate monument IDs as a wikitext table.

    The table contains the monument ID, frequency and a sample of
    source pages where the duplicate was encountered.

    @param countryconfig: the configurations for the dataset being processed.
    @param duplicate_ids: dict of monument IDs with each value being a
        Counter for how frequently the ID is encountered per page.
    @return: dict summarising the duplicate ID occurrences
    """
    pages_with_duplicates = set()
    for counter in duplicate_ids.values():
        pages_with_duplicates.update(list(counter.keys()))

    def row_builder(monument_id, counter, site):
        return {
            'Monument ID': monument_id,
            'Count': sum(counter.values()),
            'Sources': format_source_field(counter, site)
        }

    return _per_country_report(
        countryconfig, duplicate_ids,
        report_type='Duplicate IDs',
        title_column=['Monument ID', 'Count', 'Sources'],
        row_builder=row_builder,
        total_entries=len(duplicate_ids),
        total_pages=len(pages_with_duplicates)
    )


def missing_ids_statistics(countryconfig, missing_ids):
    """
    Outputs a list of pages with missing monument IDs as a wikitext table.

    The table contains the source page and the count of monuments with
    missing IDs on that page.

    @param countryconfig: the configurations for the dataset being processed.
    @param missing_ids: Counter of pages with missing IDs and their counts.
    @return: dict summarising the missing ID occurrences
    """
    def row_builder(source_page, count, site):
        return {
            'Source page': source_page.title(
                as_link=True, with_ns=False, insite=site),
            'Count': count
        }

    return _per_country_report(
        countryconfig, missing_ids,
        report_type='Missing IDs',
        title_column=['Source page', 'Count'],
        row_builder=row_builder,
        total_pages=len(missing_ids)
    )


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
            field_value = None
            if field.get('conv'):
                field_value = convert_field(field, contents, countryconfig)
            else:
                field_value = contents.get(field.get('source'))

            if field.get('check'):
                # check data
                if not run_check(field.get('check'), field_value, monument_key,
                                 countryconfig, source_page):
                    field_value = None  # throw away input if check fails
            fieldvalues.append(field_value)

            if field.get('dest') == countryconfig.get('primkey') and not field_value:
                pywikibot.warning("The primkey for monument %s on page %s turned out to resolve empty, skipping the monument" % (monument_key, source))
                return

    if countryconfig.get('countryBbox'):
        check_lat_with_lon(fieldnames, monument_key, source_page)

    query = "REPLACE INTO `{0}` (`{1}`) VALUES ({2})".format(
        countryconfig.get('table'),
        '`, `'.join(fieldnames),
        ('%s, ' * len(fieldnames)).rstrip(', '))

    # print query % tuple(fieldvalues)
    try:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            cursor.execute(query, fieldvalues)
    except Exception as e:
        pywikibot.error("Error when inserting monument from {}: {}".format(source_page, e))
        print(query % tuple(fieldvalues))

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
    literals = ('id', 'commonscat', 'address')
    for key in literals:
        if result[key]:
            result[key] = result[key].value

    if result['image']:
        result['image'] = urllib.parse.unquote(
            result['image'].value).split('/')[-1]

    if result['itemLabel']:
        result['name'] = result['itemLabel'].value

    if result['adminLabel']:
        result['admin'] = result['adminLabel'].value

    if result['monument_article']:
        result['monument_article'], _site = common.get_page_from_url(
            result['monument_article'].value)

    result['source'] = result['item'].value
    result['wd_item'] = result['item'].getID()

    if result['coordinate']:
        # ignore any unknown_value/some_value
        if 'Point(' in result['coordinate'].value:
            result['lon'], result['lat'] = result['coordinate'].value[
                len('Point('):-1].split(' ')

    # remove params that may not be NULL
    non_null_params = set(param_order) - set(('lat', 'lon'))
    for key in non_null_params:
        if key in result and not result[key]:
            del result[key]

    return tuple([result.get(key, '') for key in param_order])


def process_monument(params, source, countryconfig, conn, cursor, source_page,
                     header_defaults, harvest_state):
    """Process a single instance of a monument row template."""
    unknown_fields = harvest_state['unknown_fields']
    title = source_page.title()

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
            monument_id = get_monument_id(contents, countryconfig)
            if monument_id is not None:
                track_duplicate_ids(monument_id, source_page, harvest_state)
            update_monument(
                contents, source, countryconfig, conn, cursor, source_page)
        else:
            raise NoPrimkeyException
    # Check if the primkey is filled. This only works for a single primkey,
    # not a tuple
    elif contents.get(lookup_source_field(countryconfig.get('primkey'),
                                          countryconfig)):
        monument_id = get_monument_id(contents, countryconfig)
        if monument_id is not None:
            track_duplicate_ids(monument_id, source_page, harvest_state)
        update_monument(
            contents, source, countryconfig, conn, cursor, source_page)
    else:
        raise NoPrimkeyException


def lookup_source_field(destination, countryconfig):
    """Lookup the source field of a destination."""
    for field in countryconfig.get('fields'):
        if field.get('dest') == destination:
            return field.get('source')


def get_monument_id(contents, countryconfig):
    """Extract the monument ID value from contents.

    For tuple primkeys, the parts are joined with '-', per how this is done
    in the database. Note that this might differ from how they are presented
    on-wiki. Returns None if the source field cannot be resolved.
    """
    primkey = countryconfig.get('primkey')
    if isinstance(primkey, tuple):
        parts = []
        for partkey in primkey:
            source_field = lookup_source_field(partkey, countryconfig)
            if source_field is None:
                pywikibot.warning(
                    'primkey part %s has no matching source field '
                    'in config for %s'
                    % (partkey, countryconfig.get('table')))
                return None
            parts.append(contents.get(source_field, ''))
        return '-'.join(parts)
    else:
        source_field = lookup_source_field(primkey, countryconfig)
        if source_field is None:
            pywikibot.warning(
                'primkey %s has no matching source field in config for %s'
                % (primkey, countryconfig.get('table')))
            return None
        return contents.get(source_field, '')


def track_duplicate_ids(monument_id, source_page, harvest_state):
    """Track seen monument IDs and detect duplicates.

    On the first occurrence of an ID, it is recorded in seen_ids.
    On the second occurrence, a Counter is created in duplicate_ids
    and the original page (from seen_ids) is retroactively counted,
    so the Counter reflects all pages where the ID appeared.
    Subsequent occurrences simply increment the Counter.

    @param monument_id: the monument ID string to track.
    @param source_page: the pywikibot.Page where the ID was found.
    @param harvest_state: dict containing 'seen_ids' and 'duplicate_ids'.
    """
    if not monument_id:
        return
    seen_ids = harvest_state['seen_ids']
    duplicate_ids = harvest_state['duplicate_ids']
    if monument_id not in seen_ids:
        seen_ids[monument_id] = source_page
    elif monument_id not in duplicate_ids:
        duplicate_ids[monument_id] = Counter()
        duplicate_ids[monument_id][seen_ids[monument_id]] += 1
        duplicate_ids[monument_id][source_page] += 1
    else:
        duplicate_ids[monument_id][source_page] += 1


def _new_harvest_state():
    """Create a new harvest state dict with all required keys.

    @return: dict with keys 'unknown_fields' (dict of str to Counter),
        'seen_ids' (dict of str to Page), 'duplicate_ids' (dict of str
        to Counter), 'missing_ids' (Counter of Page to int).
    """
    return {'unknown_fields': {}, 'seen_ids': {}, 'duplicate_ids': {}, 'missing_ids': Counter()}


def process_page(page, source, countryconfig, conn, cursor,
                 harvest_state=None):
    """
    Process text containing one or more instances of the monument row template.

    Also tracks any unexpected fields, duplicate monument IDs, and missing IDs.
    """
    if harvest_state is None:
        harvest_state = _new_harvest_state()

    templates = page.templatesWithParams()
    header_defaults = {}

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
                    header_defaults, harvest_state)
            except NoPrimkeyException:
                harvest_state['missing_ids'][page] += 1
            # time.sleep(5)
        elif template_name == 'Commonscat' and len(params) >= 1:
            query = (
                """REPLACE INTO commonscat (site, title, commonscat) """
                """VALUES (%s, %s, %s)""")
            cursor.execute(
                query,
                (countryconfig.get('lang'), page.title(underscore=True), params[0]))

    return harvest_state


def process_country(countryconfig, conn, cursor, full_update, days_back, progress):
    """Process all the monuments of one country."""
    if countryconfig.get('type') == 'sparql':
        process_country_wikidata(countryconfig, conn, cursor)
    else:
        return process_country_list(
            countryconfig, conn, cursor, full_update, days_back, progress)


def process_country_list(countryconfig, conn, cursor, full_update, days_back, progress):
    """Process all the monuments of one country using row templates."""
    site = pywikibot.Site(countryconfig.get('lang'),
                          countryconfig.get('project'))
    row_template = pywikibot.Page(
        site, '{0}:{1}'.format(site.namespace(10),
                               countryconfig.get('rowTemplate')))

    trans_gen = row_template.getReferences(only_template_inclusion=True)
    filtered_gen = pagegenerators.NamespaceFilterPageGenerator(
        trans_gen, countryconfig.get('namespaces'), site=site)

    if countryconfig.get('truncate') or full_update:
        # Some countries are always truncated, otherwise only do it when
        # requested.
        query = """TRUNCATE table `{0}`""".format(countryconfig.get('table'))
        cursor.execute(query)
        generator = pagegenerators.PreloadingGenerator(filtered_gen, quiet=True)
        # FIXME : Truncate the table
    else:
        # Preloading first because the whole page needs to be fetched to get
        # the time
        pregenerator = pagegenerators.PreloadingGenerator(filtered_gen, quiet=True)
        begintime = datetime.datetime.utcnow() + \
            datetime.timedelta(days=0 - days_back)
        generator = pagegenerators.EdittimeFilterPageGenerator(
            pregenerator, begintime=begintime)

    harvest_state = _new_harvest_state()

    for page in generator:
        if page.exists() and not page.isRedirectPage():
            # Do some checking
            if progress:
                print(page.title())
            harvest_state = process_page(
                page, page.permalink(percent_encoded=False), countryconfig,
                conn, cursor, harvest_state=harvest_state)

    return {
        'unknown_fields': unknown_fields_statistics(
            countryconfig, harvest_state['unknown_fields']),
        'duplicate_ids': duplicate_ids_statistics(
            countryconfig, harvest_state['duplicate_ids']),
        'missing_ids': missing_ids_statistics(
            countryconfig, harvest_state['missing_ids']),
    }


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
    i = 0
    for result_chunk in [query_result[i:i + batch_size]
                         for i in range(0, len(query_result), batch_size)]:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            cursor.executemany(
                query,
                monument_wikidata_generator(result_chunk, params))
        conn.commit()

    pywikibot.output('Finished processing {0} results'.format(
        min(len(query_result), i + batch_size)))


def _make_aggregate_statistics(statistics, page_name, title_column,
                               row_builder, comment_template):
    """Output the overall results as a nice wikitable.

    @param statistics: list of per-country result dicts (or None for skipped
        countries). Each dict must contain a 'config' key.
    @param page_name: the Commons wiki page to write the table to.
    @param title_column: OrderedDict mapping column keys to display names.
    @param row_builder: callable(row, countryconfig, site) returning a dict
        of column key to value for a single table row.
    @param comment_template: format string for the edit summary, whose named
        placeholders must match the keys returned by StatisticsTable.get_sum().
    """
    site = pywikibot.Site('commons', 'commons')
    page = pywikibot.Page(site, page_name)

    table = StatisticsTable(
        title_column,
        [col for col in title_column if col.startswith('total')])
    for row in statistics:
        if row is None:
            # sparql harvests don't generate statistics
            continue
        countryconfig = row.get('config')
        row_data = row_builder(row, countryconfig, site)
        table.add_row(row_data)

    text = table.to_wikitext()
    comment = comment_template.format(**table.get_sum())
    pywikibot.debug(text, _logger)
    common.save_to_wiki_or_local(page, comment, text)


def make_unknown_fields_statistics(statistics):
    """Output the overall results for unknown fields as a nice wikitable."""
    title_column = OrderedDict([
        ('code', 'country'),
        ('lang', None),
        ('total_entries', 'Total fields'),
        ('total_occurrences', 'Total usage of fields'),
        ('total_pages', 'Total pages containing fields'),
        ('report_page', 'Report page'),
        ('row_template', 'Row template'),
        ('header_template', 'Header template')
    ])

    def row_builder(row, countryconfig, site):
        row_template = common.get_template_link(
            countryconfig.get('lang'),
            countryconfig.get('project', 'wikipedia'),
            countryconfig.get('rowTemplate'),
            site)
        header_template = common.get_template_link(
            countryconfig.get('lang'),
            countryconfig.get('project', 'wikipedia'),
            countryconfig.get('headerTemplate'),
            site)
        report_page = row.get('report_page').title(
            as_link=True, with_ns=False, insite=site)
        return {
            'code': countryconfig.get('country'),
            'lang': countryconfig.get('lang'),
            'total_entries': row.get('total_entries'),
            'total_occurrences': row.get('total_occurrences'),
            'total_pages': row.get('total_pages'),
            'report_page': report_page,
            'row_template': row_template,
            'header_template': header_template
        }

    _make_aggregate_statistics(
        statistics,
        'Commons:Monuments database/Unknown fields/Statistics',
        title_column,
        row_builder,
        'Updating unknown fields statistics. Total of {total_entries} '
        'unknown fields used {total_occurrences} times on {total_pages} '
        'different pages.')


def make_duplicate_id_statistics(statistics):
    """Output the overall results for duplicate IDs as a nice wikitable."""
    title_column = OrderedDict([
        ('code', 'country'),
        ('lang', None),
        ('total_entries', 'Total duplicate IDs'),
        ('total_occurrences', 'Total occurrences'),
        ('total_pages', 'Total pages with duplicates'),
        ('report_page', 'Report page'),
        ('row_template', 'Row template'),
    ])

    def row_builder(row, countryconfig, site):
        row_template = common.get_template_link(
            countryconfig.get('lang'),
            countryconfig.get('project', 'wikipedia'),
            countryconfig.get('rowTemplate'),
            site)
        report_page = row.get('report_page').title(
            as_link=True, with_ns=False, insite=site)
        return {
            'code': countryconfig.get('country'),
            'lang': countryconfig.get('lang'),
            'total_entries': row.get('total_entries'),
            'total_occurrences': row.get('total_occurrences'),
            'total_pages': row.get('total_pages'),
            'report_page': report_page,
            'row_template': row_template,
        }

    _make_aggregate_statistics(
        statistics,
        'Commons:Monuments database/Duplicate IDs/Statistics',
        title_column,
        row_builder,
        'Updating duplicate ID statistics. Total of {total_entries} '
        'duplicate IDs with {total_occurrences} occurrences on '
        '{total_pages} different pages.')


def make_missing_id_statistics(statistics):
    """Output the overall results for missing IDs as a nice wikitable."""
    title_column = OrderedDict([
        ('code', 'country'),
        ('lang', None),
        ('total_pages', 'Total pages with missing IDs'),
        ('total_occurrences', 'Total occurrences'),
        ('report_page', 'Report page'),
        ('row_template', 'Row template'),
    ])

    def row_builder(row, countryconfig, site):
        row_template = common.get_template_link(
            countryconfig.get('lang'),
            countryconfig.get('project', 'wikipedia'),
            countryconfig.get('rowTemplate'),
            site)
        report_page = row.get('report_page').title(
            as_link=True, with_ns=False, insite=site)
        return {
            'code': countryconfig.get('country'),
            'lang': countryconfig.get('lang'),
            'total_pages': row.get('total_pages'),
            'total_occurrences': row.get('total_occurrences'),
            'report_page': report_page,
            'row_template': row_template,
        }

    _make_aggregate_statistics(
        statistics,
        'Commons:Monuments database/Missing IDs/Statistics',
        title_column,
        row_builder,
        'Updating missing ID statistics. Total of {total_occurrences} '
        'missing IDs on {total_pages} different pages.')


def main():
    """The main loop."""
    # First find out what to work on

    countrycode = ''
    lang = ''
    full_update = True
    skip_wd = False
    progress = False
    days_back = 2  # Default 2 days. Runs every night so can miss one night.
    conn = None
    cursor = None

    for arg in pywikibot.handle_args():
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
        elif option == '-progress':
            progress = True
        else:
            raise Exception(
                'Bad parameters. Expected "-countrycode", "-langcode", '
                '"-daysback", "-fullupdate", "-skip_wd", "-progress" or pywikibot args. '
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
            (conn, cursor) = connect_to_monuments_database()
            process_country(countryconfig, conn, cursor, full_update,
                            days_back, progress)
            close_database_connection(conn, cursor)
        except Exception as e:
            pywikibot.error(
                'Unknown error occurred when processing country '
                '{0} in lang {1}\n{2}'.format(countrycode, lang, str(e)))
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
            try:
                (conn, cursor) = connect_to_monuments_database()
                statistics.append(
                    process_country(countryconfig, conn, cursor, full_update,
                                    days_back, progress))
                close_database_connection(conn, cursor)
            except Exception as e:
                pywikibot.error(
                    'Unknown error occurred when processing country '
                    '{0} in lang {1}\n{2}'.format(countrycode, lang, str(e)))
                continue
        unknown_fields_stats = [
            row.get('unknown_fields') if row else None
            for row in statistics
        ]
        duplicate_ids_stats = [
            row.get('duplicate_ids') if row else None
            for row in statistics
        ]
        missing_ids_stats = [
            row.get('missing_ids') if row else None
            for row in statistics
        ]
        make_unknown_fields_statistics(unknown_fields_stats)
        make_duplicate_id_statistics(duplicate_ids_stats)
        make_missing_id_statistics(missing_ids_stats)


if __name__ == "__main__":
    pywikibot.log('Start of %s' % __file__)
    main()
