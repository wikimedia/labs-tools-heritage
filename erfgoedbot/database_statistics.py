#!/usr/bin/python
# -*- coding: utf-8  -*-
'''
Update the statistics of the monuments database at http://commons.wikimedia.org/wiki/Commons:Wiki_Loves_Monuments_2011/Monuments_database/Statistics

'''
import sys, time
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

def updateMonument(contents, source, countryconfig, conn, cursor):
    '''
    FIXME :  cursor.execute(query, (tuple)) om het escape probleem te fixen
    '''
    fieldnames = []
    fieldvalues = []

    # Source is the first field
    fieldvalues.append(source)

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

    query = query + u"""`%s`""" % (u'source')

    for fieldname in fieldnames:
	query = query + u""", `%s`""" % (fieldname,)

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
    # Add the source of information (permalink)
    contents['source'] = source
    for field in countryconfig.get('fields'):
	contents[field.get(u'source')]=u''

    for param in params:
	#Split at =
	(field, sep, value) = param.partition(u'=')
	# Remove leading or trailing spaces
	field = field.strip()
	value = value.strip()
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
	updateMonument(contents, source, countryconfig, conn, cursor)
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

    if countryconfig.get('truncate'):
	query = u"""TRUNCATE table `%s`""" % (countryconfig.get('table'),)
	cursor.execute(query)

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


def getCount(query, cursor):
    '''
    Return the result of the query
    '''
    cursor.execute(query)
    
    count, = cursor.fetchone()
    return count

def outputStatistics(statistics):
    print statistics

def getStatistics(country, language, conn, cursor):
    '''
    '''
    queries = {}
    result = {}
    
    queries['all'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s'""" 
    queries['name'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT name=''"""
    queries['address'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT address=''"""
    queries['municipality'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT municipality=''"""
    queries['coordinates'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT lat=0 AND NOT lon=0"""
    queries['image'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT image=''"""

    for (stat, query) in queries.items():
	print query % (country, language)
        result[stat] = getCount(query % (country, language), cursor)

    return result
        
def getLanguages(country, conn, cursor):
    result = []
    query = u"""SELECT DISTINCT(lang) FROM monuments_all WHERE country='%s'"""
    
    print query % (country,)
    cursor.execute(query % (country,))

    while True:
        try:
            (language,) = cursor.fetchone()
	    result.append(language)
        except TypeError:
            break
        
    return result

def getCountries(conn, cursor):
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
    (conn, cursor) = connectDatabase()

    statistics = {}

    for country in getCountries(conn, cursor):
	print country
        for language in getLanguages(country, conn, cursor):
	    print language
            statistics[(country, language)] = getStatistics(country, language, conn, cursor)

    outputStatistics(statistics)
    
    '''                

    for arg in wikipedia.handleArgs():
	if arg.startswith('-countrycode:'):
	    countrycode = arg [len('-countrycode:'):]
	elif arg.startswith('-textfile:'):
	    textfile = arg [len('-textfile:'):]

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
	    processCountry(mconfig.countries.get((countrycode, lang)), conn, cursor)
    else:
	for (countrycode, lang), countryconfig in mconfig.countries.iteritems():
	    wikipedia.output(u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
	    processCountry(countryconfig, conn, cursor)
    


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
