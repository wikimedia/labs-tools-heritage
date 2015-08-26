#!/usr/bin/python
# -*- coding: utf-8  -*-
'''
Update the monuments database either from a text file or from some wiki page(s)

Usage:
# loop through all countries
python update_database.py

# work on specific country-lang
python update_database.py -countrycode:XX -lang:YY

'''
import sys
import time
import warnings
import datetime
import monuments_config as mconfig
import pywikibot
import MySQLdb
from pywikibot import config
import re
from pywikibot import pagegenerators


def connectDatabase():
    '''
    Connect to the mysql database, if it fails, go down in flames
    '''
    conn = MySQLdb.connect(host=mconfig.db_server, db=mconfig.db, user=config.db_username,
                           passwd=config.db_password, use_unicode=True, charset='utf8')
    cursor = conn.cursor()
    return (conn, cursor)


def CH1903Converter(x, y):
    if not(x.strip() and y.strip()):
        # x or y is empty
        return (0, 0)
    x = float(x)
    y = float(y)

    lat = 16.9023892
    lat = lat + 3.238272 * (y - 200) / 1000
    lat = lat + 0.270978 * (x - 600) / 1000 * (x - 600) / 1000
    lat = lat + 0.002528 * (y - 200) / 1000 * (y - 200) / 1000
    lat = lat + 0.044700 * \
        (x - 600) / 1000 * (x - 600) / 1000 * (y - 200) / 1000
    lat = lat + 0.014000 * \
        (y - 200) / 1000 * (y - 200) / 1000 * (y - 200) / 1000
    lat = lat / 0.36  # Round 6

    lon = 2.6779094
    lon = lon + 4.728982 * (x - 600) / 1000
    lon = lon + 0.791484 * (x - 600) / 1000 * (y - 200) / 1000
    lon = lon + 0.130600 * \
        (x - 600) / 1000 * (y - 200) / 1000 * (y - 200) / 1000
    lon = lon - 0.043600 * \
        (x - 600) / 1000 * (x - 600) / 1000 * (x - 600) / 1000
    lon = lon / 0.36  # Round 6

    return (lat, lon)


def ucfirst(text):
    if (text):
        return text[0].upper() + text[1:]
    else:
        return ''


def extractWikilink(text):
    articleName = u''
    result = re.search("\[\[(.+?)(\||\]\])", text)
    if (result and result.group(1)):
        articleName = result.group(1)
        articleName = articleName.replace(u' ', u'_')
        articleName = ucfirst(articleName)

    return articleName


def reportDataError(errorMsg, wikiPage, exceptWord, comment=''):

    if not comment:
        comment = errorMsg

    pywikibot.output(errorMsg)
    talkPage = wikiPage.toggleTalkPage()
    try:
        content = talkPage.get()
    except (pywikibot.NoPage, pywikibot.IsRedirectPage):
        content = u''
    if exceptWord and exceptWord not in content:
        content += "\n\n" + errorMsg + " --~~~~" + "\n\n"
        talkPage.put(content, comment)
        return True

    return False


def checkLat(lat, monumentKey, countryconfig, sourcePage):
    if len(lat):
        try:
            lat = float(lat)
        except ValueError:
            errorMsg = u"Invalid latitude value: %s for monument %s" % (
                lat, monumentKey)
            reportDataError(errorMsg, sourcePage, monumentKey)
            return False
        countryBbox = ''
        if (countryconfig.get('countryBbox')):
            countryBbox = countryconfig.get('countryBbox')

        if (lat > 90 or lat < -90):
            errorMsg = u"Latitude for monument %s out of range: %s" % (
                monumentKey, lat)
            reportDataError(errorMsg, sourcePage, monumentKey)
            return False
        elif (countryBbox):
            maxsplit = 3
            (left, bottom, right, top) = countryBbox.split(",", maxsplit)
            bottom = float(bottom)
            top = float(top)
            minLat = min(bottom, top)
            maxLat = max(bottom, top)
            if (lat > maxLat or lat < minLat):
                errorMsg = u"Latitude for monument %s out of country area: %s" % (
                    monumentKey, lat)
                reportDataError(errorMsg, sourcePage, monumentKey)
                return False
            else:
                return True
        else:
            return True


def checkLon(lon, monumentKey,  countryconfig, sourcePage):
    if len(lon):
        try:
            lon = float(lon)
        except ValueError:
            errorMsg = u"Invalid longitude value: %s for monument %s" % (
                lon, monumentKey)
            reportDataError(errorMsg, sourcePage, monumentKey)
            return False
        countryBbox = ''
        if (countryconfig.get('countryBbox')):
            countryBbox = countryconfig.get('countryBbox')

        if (lon > 180 or lon < -180):
            errorMsg = u"Longitude for monument %s out of range: %s" % (
                monumentKey, lon)
            reportDataError(errorMsg, sourcePage, monumentKey)
            return False
        elif (countryBbox):
            maxsplit = 3
            (left, bottom, right, top) = countryBbox.split(",", maxsplit)
            left = float(left)
            right = float(right)
            minLon = min(left, right)
            maxLon = max(left, right)
            if (lon > maxLon or lon < minLon):
                errorMsg = u"Longitude for monument %s out of country area: %s" % (
                    monumentKey, lon)
                reportDataError(errorMsg, sourcePage, monumentKey)
                return False
            else:
                return True
        else:
            return True


def convertField(field, contents, countryconfig):
    '''
    Convert a field
    '''

    if field.get('conv') == 'extractWikilink':
        return extractWikilink(contents.get(field.get('source')))
    elif field.get('conv') == 'generateRegistrantUrl' and countryconfig.get('registrantUrlBase'):
        return countryconfig.get('registrantUrlBase') % (contents.get(field.get('source')),)
    elif field.get('conv') == 'CH1903ToLat':
        (lat, lon) = CH1903Converter(
            contents.get('CH1903_X'), contents.get('CH1903_Y'))
        return lat
    elif field.get('conv') == 'CH1903ToLon':
        (lat, lon) = CH1903Converter(
            contents.get('CH1903_X'), contents.get('CH1903_Y'))
        return lon
    elif field.get('conv') == 'generateRegistrantUrl-sv-ship' and countryconfig.get('registrantUrlBase'):
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
    elif field.get('conv') == 'generateRegistrantUrl-wlpa-es-ct' and countryconfig.get('registrantUrlBase'):
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
            if (dyear+70) < cyear:
                return u'pd'
            else:
                return u'noFoP'
        except ValueError:
            return u'noFoP'
    return u''


def unknownFieldsStatistics(countryconfig, unknownFields):
    '''
    Produce some unknown field statistics to debug.
    This is still very raw data. Should be formatted and more information.
    '''
    site = site = pywikibot.Site(u'commons', u'commons')
    page = pywikibot.Page(
        site, u'Commons:Monuments database/Unknown fields/%s' % (countryconfig.get('table'),))

    text = u'{| class="wikitable sortable"\n'
    text = text + u'! Field !! Count\n'
    for key, value in unknownFields.items():
        text = text + u'|-\n'
        text = text + u'| %s || %s\n' % (key, value)

    text = text + u'|}'
    comment = u'Updating the list of unknown fields'
    page.put(text, comment)


def updateMonument(contents, source, countryconfig, conn, cursor, sourcePage):
    '''
    '''

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
            fieldValue = u''
            if field.get('conv'):
                fieldValue = convertField(field, contents, countryconfig)
            else:
                fieldValue = contents.get(field.get('source'))

            if field.get('check'):
                # check data
                # run function with name field.get('check')
                globals()[field.get('check')](
                    fieldValue, monumentKey, countryconfig, sourcePage)
            fieldvalues.append(fieldValue)

    if countryconfig.get('countryBbox'):
        if 'lat' in fieldnames and 'lon' not in fieldnames:
            errorMsg = u"Longitude is not set for monument %s." % (
                monumentKey, )
            reportDataError(errorMsg, sourcePage, monumentKey)
        if 'lon' in fieldnames and 'lat' not in fieldnames:
            errorMsg = u"Latitude is not set for monument %s." % (
                monumentKey, )
            reportDataError(errorMsg, sourcePage, monumentKey)

    query = u"""REPLACE INTO `%s`(""" % (countryconfig.get('table'),)

    delimiter = u''
    for fieldname in fieldnames:
        query = query + delimiter + u"""`%s`""" % (fieldname,)
        delimiter = u', '

    query = query + u""") VALUES ("""

    delimiter = u''
    for fieldvalue in fieldvalues:
        query = query + delimiter + u"""%s"""
        delimiter = u', '

    query = query + u""")"""

    # query = u"""REPLACE INTO monumenten(objrijksnr, woonplaats, adres, objectnaam, type_obj, oorspr_functie, bouwjaar, architect, cbs_tekst, RD_x, RD_y, lat, lon, image, source)
    # VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""";
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
    '''
    Get the defaults for the row templates. Return all fields that seem to be valid. Ignore other fields.
    '''

    contents = {}
    validFields = []

    for field in countryconfig.get('fields'):
        validFields.append(field.get(u'source'))

    for param in params:
        # Split at =
        (field, sep, value) = param.partition(u'=')
        # Remove leading or trailing spaces
        field = field.strip()
        value = value.split("<ref")[0].strip()

        # Check first that field is not empty
        if field.strip():
            # Is it in the fields list?
            if field in validFields:
                contents[field] = value

    return contents


def processMonument(params, source, countryconfig, conn, cursor, sourcePage, headerDefaults, unknownFields=None):
    '''
    Process a single instance of a monument row template
    '''

    if not unknownFields:
        unknownFields = {}

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
        # Split at =
        (field, sep, value) = param.partition(u'=')
        # Remove leading or trailing spaces
        field = field.strip()
        value = value.split("<ref")[0].strip()

        # Check first that field is not empty
        if field.strip():
            # Is it in the fields list?
            if field in contents:
                # Load it with Big fucking escape hack. Stupid mysql lib
                # Do this somewhere else.replace("'", "\\'")
                contents[field] = value
            else:
                # FIXME: Include more information where it went wrong
                pywikibot.output(
                    u'Found unknown field: %s on page %s' % (field, title))
                pywikibot.output(u'Field: %s' % (field,))
                pywikibot.output(u'Value: %s' % (value,))
                if field in unknownFields:
                    unknownFields[field] = unknownFields.get(field) + 1
                else:
                    unknownFields[field] = 1
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
        print "No primkey available"
    return unknownFields


def lookupSourceField(destination, countryconfig):
    '''
    Lookup the source field of a destination.
    '''
    for field in countryconfig.get('fields'):
        if field.get('dest') == destination:
            return field.get('source')


def processText(text, source, countryconfig, conn, cursor, page=None, unknownFields=None):
    '''
    Process a text containing one or multiple instances of the monument row template
    '''
    if not unknownFields:
        unknownFields = {}

    if not page:
        site = site = pywikibot.Site(countryconfig.get('lang'), countryconfig.get('project'))
        page = pywikibot.Page(site, u'User:Multichill/Zandbak')
    templates = page.templatesWithParams()
    headerDefaults = {}

    for (template, params) in templates:
        template_name = template.title(withNamespace=False)
        if template_name == countryconfig.get('headerTemplate'):
            headerDefaults = processHeader(params, countryconfig)
        if template_name == countryconfig.get('rowTemplate'):
            # print template
            # print params
            unknownFields = processMonument(
                params, source, countryconfig, conn, cursor, page, headerDefaults, unknownFields=unknownFields)
            # time.sleep(5)
        elif template_name == u'Commonscat' and len(params) >= 1:
            query = u"""REPLACE INTO commonscat (site, title, commonscat) VALUES (%s, %s, %s)"""
            cursor.execute(
                query, (countryconfig.get('lang'), page.title(True), params[0]))

    return unknownFields


def processCountry(countryconfig, conn, cursor, fullUpdate, daysBack):
    '''
    Process all the monuments of one country
    '''

    site = pywikibot.Site(countryconfig.get('lang'), countryconfig.get('project'))
    rowTemplate = pywikibot.Page(
        site, u'%s:%s' % (site.namespace(10), countryconfig.get('rowTemplate')))

    transGen = pagegenerators.ReferringPageGenerator(
        rowTemplate, onlyTemplateInclusion=True)
    filteredGen = pagegenerators.NamespaceFilterPageGenerator(
        transGen, countryconfig.get('namespaces'))

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
        begintime = datetime.datetime.utcnow(
        ) + datetime.timedelta(days=0-daysBack)
        generator = pagegenerators.EdittimeFilterPageGenerator(
            pregenerator, begintime=begintime)

    unknownFields = {}

    for page in generator:
        if page.exists() and not page.isRedirectPage():
            # Do some checking
            unknownFields = processText(page.get(), page.permalink(
            ), countryconfig, conn, cursor, page=page, unknownFields=unknownFields)

    unknownFieldsStatistics(countryconfig, unknownFields)


def processTextfile(textfile, countryconfig, conn, cursor):
    '''
    Process the contents of a text file containing one or more lines with the Tabelrij rijksmonument template
    '''
    file = open(textfile, 'r')
    for line in file:
        processText(
            line.decode('UTF-8').strip(), textfile, countryconfig, conn, cursor)


def main():
    '''
    The main loop
    '''
    # First find out what to work on

    countrycode = u''
    textfile = u''
    fullUpdate = True
    daysBack = 2  # Default 2 days. Runs every night so can miss one night.
    conn = None
    cursor = None
    (conn, cursor) = connectDatabase()

    for arg in pywikibot.handleArgs():
        if arg.startswith('-countrycode:'):
            countrycode = arg[len('-countrycode:'):]
        elif arg.startswith('-textfile:'):
            textfile = arg[len('-textfile:'):]
        elif arg.startswith('-daysback:'):
            daysBack = int(arg[len('-daysback:'):])
        elif arg == u'-fullupdate':
            fullUpdate = True
        else:
            raise Exception(
                "Bad parameters. Expected -countrycode, -textfile, -daysback, -fullupdate or  pywikipediabot args.")

    if countrycode:
        lang = pywikibot.Site().language()
        if not mconfig.countries.get((countrycode, lang)):
            pywikibot.output(
                u'I have no config for countrycode "%s" in language "%s"' % (countrycode, lang))
            return False
        pywikibot.output(
            u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
        if textfile:
            pywikibot.output(u'Going to work on textfile.')
            processTextfile(
                textfile, mconfig.countries.get((countrycode, lang)), conn, cursor)
        else:
            try:
                processCountry(
                    mconfig.countries.get((countrycode, lang)), conn, cursor, fullUpdate, daysBack)
            except Exception, e:
                pywikibot.output("Unknown error occurred when processing country %s in lang %s" % (countrycode, lang))
                pywikibot.output(str(e))
    else:
        for (countrycode, lang), countryconfig in mconfig.countries.iteritems():
            pywikibot.output(
                u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
            try:
                processCountry(countryconfig, conn, cursor, fullUpdate, daysBack)
            except Exception, e:
                pywikibot.output("Unknown error occurred when processing country %s in lang %s" % (countrycode, lang))
                pywikibot.output(str(e))
                continue
    '''


    generator = genFactory.getCombinedGenerator()
    if not generator:
        pywikibot.output(u'You have to specify what to work on. This can either be -textfile:<filename> to work on a local file or you can use one of the standard pagegenerators (in pagegenerators.py)')
    else:
        pregenerator = pagegenerators.PreloadingGenerator(generator)
        for page in pregenerator:
        if page.exists() and not page.isRedirectPage():
            # Do some checking
            processText(page.get(), page.permalink(), conn, cursor, page=page)
    '''

if __name__ == "__main__":
    main()
