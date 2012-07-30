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
import sys, time, warnings, datetime
import monuments_config as mconfig
sys.path.append("/home/project/e/r/f/erfgoed/pywikipedia")
import wikipedia, MySQLdb, config, re, pagegenerators

def connectDatabase():
    '''
    Connect to the mysql database, if it fails, go down in flames
    '''
    conn = MySQLdb.connect(host=mconfig.db_server, db=mconfig.db, user = config.db_username, passwd = config.db_password, use_unicode=True, charset='utf8')
    cursor = conn.cursor()
    return (conn, cursor)

def CH1903Converter(x, y):
    if not(x.strip() and y.strip()):
	# x or y is empty
	return (0,0)
    x = float(x)
    y = float(y)

    lat = 16.9023892
    lat = lat + 3.238272 * ( y - 200 ) / 1000 
    lat = lat + 0.270978 * ( x - 600 ) / 1000 * ( x - 600 ) / 1000
    lat = lat + 0.002528 * ( y - 200 ) / 1000 * ( y - 200 ) / 1000
    lat = lat + 0.044700 * ( x - 600 ) / 1000 * ( x - 600 ) / 1000 * ( y - 200 ) / 1000
    lat = lat + 0.014000 * ( y - 200 ) / 1000 * ( y - 200 ) / 1000 * ( y - 200 ) / 1000
    lat = lat / 0.36 # Round 6

    lon = 2.6779094
    lon = lon + 4.728982 * ( x - 600 ) / 1000
    lon = lon + 0.791484 * ( x - 600 ) / 1000 * ( y - 200 ) / 1000
    lon = lon + 0.130600 * ( x - 600 ) / 1000 * ( y - 200 ) / 1000 * ( y - 200 ) / 1000
    lon = lon - 0.043600 * ( x - 600 ) / 1000 * ( x - 600 ) / 1000 * ( x - 600 ) / 1000
    lon = lon / 0.36 # Round 6
    
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

    wikipedia.output(errorMsg)
    talkPage = wikiPage.toggleTalkPage()
    try:
        content = talkPage.get() 
    except (wikipedia.NoPage, wikipedia.IsRedirectPage):
        content = u''
    if exceptWord and exceptWord not in content:
        content += "\n\n" + errorMsg + " --~~~~" + "\n\n"
        talkPage.put(content, comment)
        return True
    
    return False

def checkLat(lat, monumentKey, countryconfig, sourcePage):
    if len( lat ):
        try:
            lat = float(lat)
        except ValueError:
            errorMsg = u"Invalid latitude value: %s for monument %s" % (lat, monumentKey)
            reportDataError(errorMsg, sourcePage, monumentKey)
            return False
        countryBbox = ''
        if ( countryconfig.get('countryBbox') ):
            countryBbox = countryconfig.get('countryBbox')

        if ( lat > 90 or lat < -90 ) :
            errorMsg = u"Latitude for monument %s out of range: %s" % (monumentKey, lat )
            reportDataError(errorMsg, sourcePage, monumentKey)
            return False
        elif ( countryBbox ):
            maxsplit = 3
            ( left, bottom, right, top ) = countryBbox.split(",", maxsplit)
            bottom = float( bottom )
            top = float( top )
            minLat = min(bottom, top)
            maxLat = max(bottom, top)
            if (lat > maxLat or lat < minLat):
                errorMsg = u"Latitude for monument %s out of country area: %s" % (monumentKey, lat )
                reportDataError(errorMsg, sourcePage, monumentKey)
                return False
            else: 
                return True
        else:
            return True


def checkLon(lon, monumentKey,  countryconfig, sourcePage):
    if len( lon ):
        try:
            lon = float(lon)
        except ValueError:
            errorMsg = u"Invalid longitude value: %s for monument %s" % (lon, monumentKey)
            reportDataError(errorMsg, sourcePage, monumentKey)
            return False
        countryBbox = ''
        if ( countryconfig.get('countryBbox') ):
            countryBbox = countryconfig.get('countryBbox')
        
        if ( lon > 180 or lon < -180 ) :
            errorMsg = u"Longitude for monument %s out of range: %s" % (monumentKey, lon ) 
            reportDataError(errorMsg, sourcePage, monumentKey)
            return False
        elif ( countryBbox ):
            maxsplit = 3
            ( left, bottom, right, top ) = countryBbox.split(",", maxsplit)
            left = float( left )
            right = float( right )
            minLon = min(left, right)
            maxLon = max(left, right)
            if (lon > maxLon or lon < minLon):
                errorMsg = u"Longitude for monument %s out of country area: %s" % (monumentKey, lon )
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
        return extractWikilink( contents.get(field.get('source')) )
    elif field.get('conv') == 'generateRegistrantUrl' and countryconfig.get('registrantUrlBase'):
        return countryconfig.get('registrantUrlBase') % (contents.get(field.get('source')),)
    elif field.get('conv') == 'CH1903ToLat':
        (lat, lon) = CH1903Converter(contents.get('CH1903_X'), contents.get('CH1903_Y'))
        return lat
    elif field.get('conv') == 'CH1903ToLon':
        (lat, lon) = CH1903Converter(contents.get('CH1903_X'), contents.get('CH1903_Y'))
        return lon
        
    return u''

def updateMonument(contents, source, countryconfig, conn, cursor, sourcePage):
    '''
    '''

    fieldnames = []
    fieldvalues = []

    # Source is the first field
    fieldnames.append(u'source')
    fieldvalues.append(source)

    monumentKey = u''
    if contents.get(countryconfig.get('primkey')) :
        monumentKey = contents.get(countryconfig.get('primkey'))


    for field in countryconfig.get('fields'):
        if field.get('dest') and len( contents.get(field.get('source')) ):
            fieldnames.append(field.get('dest'))
            
            #Do some conversions here
            fieldValue = u''
            if field.get('conv'):
                fieldValue = convertField(field, contents, countryconfig) 
            else:
                fieldValue = contents.get(field.get('source'))
                
            if field.get('check'):
                # check data
                # run function with name field.get('check')
                globals()[field.get('check')](fieldValue, monumentKey, countryconfig, sourcePage)
            fieldvalues.append(fieldValue)


    if countryconfig.get('countryBbox'):
       if 'lat' in fieldnames and 'lon' not in fieldnames:
           errorMsg = u"Longitude is not set for monument %s." % (monumentKey, )
           reportDataError(errorMsg, sourcePage, monumentKey)
       if 'lon' in fieldnames and 'lat' not in fieldnames:
           errorMsg = u"Latitude is not set for monument %s." % (monumentKey, )
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


    #query = u"""REPLACE INTO monumenten(objrijksnr, woonplaats, adres, objectnaam, type_obj, oorspr_functie, bouwjaar, architect, cbs_tekst, RD_x, RD_y, lat, lon, image, source)
    #VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""";
    #print query % tuple(fieldvalues)
    with warnings.catch_warnings(record=True) as w:
      warnings.simplefilter("always")
      cursor.execute(query, fieldvalues)

      #FIXME : Disable for now because print throws UnicodeEncodeErrors
      #if len(w) == 1:
      #  print w[-1].message, " when running ", query % tuple(fieldvalues)
      
    #print contents
    #print u'updating!'
    #time.sleep(5)

def processHeader(params, countryconfig):
    '''
    Get the defaults for the row templates. Return all fields that seem to be valid. Ignore other fields.
    '''

    contents = {}
    validFields = []

    for field in countryconfig.get('fields'):
        validFields.append(field.get(u'source'))

    for param in params:
	#Split at =
	(field, sep, value) = param.partition(u'=')
	# Remove leading or trailing spaces
	field = field.strip()
	value = value.split("<ref")[0].strip()
	
	#Check first that field is not empty
	if field.strip():
            #Is it in the fields list?
            if field in validFields:
                contents[field] = value

    return contents


def processMonument(params, source, countryconfig, conn, cursor, sourcePage, headerDefaults):
    '''
    Process a single instance of a monument row template
    '''
    
    title = sourcePage.title(True)
    
    # Get all the fields
    contents = {}
    # Add the source of information (permalink)
    contents['source'] = source
    for field in countryconfig.get('fields'):
        if field.get(u'source') in headerDefaults:
            contents[field.get(u'source')] = headerDefaults.get(field.get(u'source'))
        else:
            contents[field.get(u'source')]=u''
    
    contents['title'] = title

    for param in params:
	#Split at =
	(field, sep, value) = param.partition(u'=')
	# Remove leading or trailing spaces
	field = field.strip()
	value = value.split("<ref")[0].strip()
	
	#Check first that field is not empty
	if field.strip():
            #Is it in the fields list?
            if field in contents:
                #Load it with Big fucking escape hack. Stupid mysql lib
                contents[field] = value # Do this somewhere else.replace("'", "\\'")
            else:
                #FIXME: Include more information where it went wrong
                wikipedia.output(u'Found unknown field: %s on page %s' % (field, title) )
		wikipedia.output(u'Field: %s' % (field,))
		wikipedia.output(u'Value: %s' % (value,))
                #time.sleep(5)

    # If we truncate we don't have to check for primkey (it's a made up one)
    if countryconfig.get('truncate'):
	updateMonument(contents, source, countryconfig, conn, cursor, sourcePage)
    # Check if the primkey is a tuple and if all parts are present
    elif isinstance(countryconfig.get('primkey'), tuple):
	allKeys=True
	for partkey in countryconfig.get('primkey'):
	    if not contents.get(lookupSourceField(partkey, countryconfig)):
		allKeys=False
	if allKeys:
	    updateMonument(contents, source, countryconfig, conn, cursor, sourcePage)
    # Check if the primkey is filled. This only works for a single primkey, not a tuple
    elif contents.get(lookupSourceField(countryconfig.get('primkey'), countryconfig)):
	updateMonument(contents, source, countryconfig, conn, cursor, sourcePage)
    else:
	print "No primkey available"

def lookupSourceField(destination, countryconfig):
    '''
    Lookup the source field of a destination.
    '''
    for field in countryconfig.get('fields'):
	if field.get('dest')==destination:
	    return field.get('source')

def processText(text, source, countryconfig, conn, cursor, page=None):
    '''
    Process a text containing one or multiple instances of the monument row template
    '''
    if not page:
	site = site = wikipedia.getSite(countryconfig.get('lang'), countryconfig.get('project'))
	page = wikipedia.Page(site, u'User:Multichill/Zandbak')
    templates = page.templatesWithParams(thistxt=text)
    headerDefaults = {}
    
    for (template, params) in templates:
        if template==countryconfig.get('headerTemplate'):
            headerDefaults = processHeader(params, countryconfig)
	if template==countryconfig.get('rowTemplate'):
	    #print template
	    #print params
	    processMonument(params, source, countryconfig, conn, cursor, page, headerDefaults)
	    #time.sleep(5)
	elif template == u'Commonscat' and len(params)>=1:
	    query = u"""REPLACE INTO commonscat (site, title, commonscat) VALUES (%s, %s, %s)"""
	    cursor.execute(query, (countryconfig.get('lang'), page.title(True), params[0]))
 

def processCountry(countryconfig, conn, cursor, fullUpdate, daysBack):
    '''
    Process all the monuments of one country
    '''

    site = wikipedia.getSite(countryconfig.get('lang'), countryconfig.get('project'))
    rowTemplate = wikipedia.Page(site, u'%s:%s' % (site.namespace(10), countryconfig.get('rowTemplate')))

    transGen = pagegenerators.ReferringPageGenerator(rowTemplate, onlyTemplateInclusion=True)
    filteredGen = pagegenerators.NamespaceFilterPageGenerator(transGen, countryconfig.get('namespaces'))

    if countryconfig.get('truncate') or fullUpdate:
	# Some countries are always truncated, otherwise only do it when requested.
	query = u"""TRUNCATE table `%s`""" % (countryconfig.get('table'),)
	cursor.execute(query)
    	generator = pagegenerators.PreloadingGenerator(filteredGen)
	#FIXME : Truncate the table
    else:
	# Preloading first because the whole page needs to be fetched to get the time
	pregenerator = pagegenerators.PreloadingGenerator(filteredGen)
	begintime = datetime.datetime.utcnow() + datetime.timedelta(days=0-daysBack)
	generator = pagegenerators.EdittimeFilterPageGenerator(pregenerator, begintime=begintime)

    for page in generator:
	if page.exists() and not page.isRedirectPage():
	    # Do some checking
	    processText(page.get(), page.permalink(), countryconfig, conn, cursor, page=page)


def processTextfile(textfile, countryconfig, conn, cursor):
    '''
    Process the contents of a text file containing one or more lines with the Tabelrij rijksmonument template
    '''
    file = open(textfile, 'r')
    for line in file:
	processText(line.decode('UTF-8').strip(), textfile, countryconfig, conn, cursor)

def main():
    '''
    The main loop
    '''
    # First find out what to work on

    countrycode = u''
    textfile = u''
    fullUpdate = True
    daysBack = 2 # Default 2 days. Runs every night so can miss one night.
    conn = None
    cursor = None
    (conn, cursor) = connectDatabase()

    for arg in wikipedia.handleArgs():
	if arg.startswith('-countrycode:'):
	    countrycode = arg [len('-countrycode:'):]
	elif arg.startswith('-textfile:'):
	    textfile = arg [len('-textfile:'):]
    	elif arg.startswith('-daysback:'):
	    daysBack = int(arg [len('-daysback:'):])
	elif arg == u'-fullupdate':
	    fullUpdate = True
	else:
		raise Exception("Bad parameters. Expected -countrycode, -textfile, -daysback, -fullupdate or  pywikipediabot args.")

    if countrycode:
        lang = wikipedia.getSite().language()
	if not mconfig.countries.get((countrycode, lang)):
	    wikipedia.output(u'I have no config for countrycode "%s" in language "%s"' % (countrycode, lang))
	    return False
	wikipedia.output(u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
	if textfile:
	    wikipedia.output(u'Going to work on textfile.')
	    processTextfile(textfile, mconfig.countries.get((countrycode, lang)), conn, cursor)
	else:
	    processCountry(mconfig.countries.get((countrycode, lang)), conn, cursor, fullUpdate, daysBack)
    else:
	for (countrycode, lang), countryconfig in mconfig.countries.iteritems():
	    wikipedia.output(u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
	    processCountry(countryconfig, conn, cursor, fullUpdate, daysBack)
    '''


	generator = genFactory.getCombinedGenerator()
	if not generator:
	    wikipedia.output(u'You have to specify what to work on. This can either be -textfile:<filename> to work on a local file or you can use one of the standard pagegenerators (in pagegenerators.py)')
	else:
	    pregenerator = pagegenerators.PreloadingGenerator(generator)
	    for page in pregenerator:
		if page.exists() and not page.isRedirectPage():
		    # Do some checking
		    processText(page.get(), page.permalink(), conn, cursor, page=page)
    '''

if __name__ == "__main__":
    try:
        main()
    finally:
        wikipedia.stopme()
