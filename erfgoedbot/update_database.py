#!/usr/bin/python
# -*- coding: utf-8  -*-
'''
Update the monuments database either from a text file or from some wiki page(s)

'''
import sys, time
import monuments_config as mconfig
sys.path.append("/home/multichill/pywikipedia")
import wikipedia, MySQLdb, config, re, pagegenerators

def connectDatabase():
    '''
    Connect to the mysql database, if it fails, go down in flames
    '''
    conn = MySQLdb.connect(host=mconfig.db_server, db=mconfig.db, user = config.db_username, passwd = config.db_password, use_unicode=True, charset='utf8')
    cursor = conn.cursor()
    return (conn, cursor)

def CH1903Converter(x, y):
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

def convertField(field, contents):
    '''
    Convert a field
    '''
    if field.get('conv')=='CH1903ToLat':
	(lat, lon) = CH1903Converter(contents.get('CH1903_X'), contents.get('CH1903_Y'))
	return lat
    elif field.get('conv')=='CH1903ToLon':
	(lat, lon) = CH1903Converter(contents.get('CH1903_X'), contents.get('CH1903_Y'))
	return lon
    return u''

def updateMonument(contents, countryconfig, conn, cursor):
    '''
    FIXME :  cursor.execute(query, (tuple)) om het escape probleem te fixen
    '''
    fieldnames = []
    fieldvalues = []
    for field in countryconfig.get('fields'):
	if field.get('dest'):
	    fieldnames.append(field.get('dest'))
	    #Do some conversions here
	    if field.get('conv'):
		fieldvalues.append(convertField(field, contents))
	    else:
		fieldvalues.append(contents.get(field.get('source')))
    if countryconfig.get('truncate'):
	query = u"""INSERT INTO `%s`(""" % (countryconfig.get('table'),)
    else:
	query = u"""REPLACE INTO `%s`(""" % (countryconfig.get('table'),)
    i = 0
    for fieldname in fieldnames:
	if i==0:
	    query = query + u"""`%s`""" % (fieldname,)
	else:
	    query = query + u""", `%s`""" % (fieldname,)
	i = i + 1

    query = query + u""") VALUES ("""

    j =0
    for fieldvalue in fieldvalues:
	if j==0:
	    query = query + u"""%s""" # % (fieldvalue,)
	else:
	    query = query + u""", %s""" # % (fieldvalue,)
	j = j + 1

    query = query + u""")"""


    #query = u"""REPLACE INTO monumenten(objrijksnr, woonplaats, adres, objectnaam, type_obj, oorspr_functie, bouwjaar, architect, cbs_tekst, RD_x, RD_y, lat, lon, image, source)
    #VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""";
    #print query % tuple(fieldvalues)
    cursor.execute(query, fieldvalues)
    
    #print contents
    #print u'updating!'
    #time.sleep(5)

def processMonument(params, source, countryconfig, conn, cursor):
    '''
    Process a single instance of a monument row template
    '''
    
    # The regexes to find all the fields
    fields = [u'objrijksnr',
	     u'woonplaats',
             u'adres',
             u'objectnaam',
             u'type_obj',
	     u'oorspr_functie',
             u'bouwjaar',
             u'architect',
             u'cbs_tekst',
             u'RD_x',
             u'RD_y',
             u'lat',
             u'lon',
	     u'image',
             u'postcode', # Not used
             u'buurt', # Not used
	    ]
     
    # Get all the fields
    contents = {}
    #contents['source'] = source.replace("'", "\\'")
    for field in countryconfig.get('fields'):
	contents[field.get(u'source')]=u''

    for param in params:
	#Split at =
	(field, sep, value) = param.partition(u'=')	
	#See if first part is in fields list
	if field in contents:
	    #Load it with Big fucking escape hack. Stupid mysql lib
	    contents[field] = value # Do this somewhere else.replace("'", "\\'")
	else:
	    #FIXME: Include more information where it went wrong
	    wikipedia.output(u'Found unknown field: %s' % field)
	    print field
	    print sep
	    print value
	    time.sleep(5)
    
    # The first key is assumed to be the primary key, check if it is it.
    if contents.get(countryconfig.get('primkey')) or countryconfig.get('truncate'):
	updateMonument(contents, countryconfig, conn, cursor)
	#print contents
	#time.sleep(5)

def processText(text, source, countryconfig, conn, cursor, page=None):
    '''
    Process a text containing one or multiple instances of the monument row template
    '''
    if not page:
	site = site = wikipedia.getSite(countryconfig.get('lang'), countryconfig.get('project'))
	page = wikipedia.Page(site, u'User:Multichill/Zandbak')
    templates = page.templatesWithParams(thistxt=text)
    for (template, params) in templates:
	if template==countryconfig.get('rowTemplate'):
	    #print template
	    #print params
	    processMonument(params, source, countryconfig, conn, cursor)
	    #time.sleep(5)

def processCountry(countryconfig, conn, cursor):
    '''
    Process all the monuments of one country
    '''
    site = wikipedia.getSite(countryconfig.get('lang'), countryconfig.get('project'))
    rowTemplate = wikipedia.Page(site, u'%s:%s' % (site.namespace(10), countryconfig.get('rowTemplate')))

    transGen = pagegenerators.ReferringPageGenerator(rowTemplate, onlyTemplateInclusion=True)
    filteredGen = pagegenerators.NamespaceFilterPageGenerator(transGen, countryconfig.get('namespaces'))
    pregenerator = pagegenerators.PreloadingGenerator(filteredGen)
    for page in pregenerator:
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
    conn = None
    cursor = None
    (conn, cursor) = connectDatabase()

    for arg in wikipedia.handleArgs():
	if arg.startswith('-countrycode:'):
	    countrycode = arg [len('-countrycode:'):]
	if arg.startswith('-textfile:'):
	    textfile = arg [len('-textfile:'):]

    if countrycode:
	if not mconfig.countries.get(countrycode):
	    wikipedia.output(u'I have no config for countrycode "%s"' % (countrycode,))
	    return False
	wikipedia.output(u'Working on countrycode "%s"' % (countrycode,))
	if textfile:
	    wikipedia.output(u'Going to work on textfile.')
	    processTextfile(textfile, mconfig.countries.get(countrycode), conn, cursor)
	else:
	    processCountry(mconfig.countries.get(countrycode), conn, cursor)
    else:
	for countrycode, countryconfig in mconfig.countries.iteritems():
	    wikipedia.output(u'Working on countrycode "%s"' % (countrycode,))
	    processCountry(countryconfig, conn, cursor)
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
