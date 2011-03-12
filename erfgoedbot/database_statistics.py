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

def getCount(query, cursor):
    '''
    Return the result of the query
    '''
    cursor.execute(query)
    
    count, = cursor.fetchone()
    return count

def outputStatistics(statistics):
    ouput = u'{| class="wikitable sortable"\n'
    output = output + u'! country !! lang !! total !! name !! address !! municipality !! coordinates !! image\n'

    for country in sorted(statistics.keys()):
        for language in sorted(statistics.get(country).keys()):
                output = output + u'|-\n'
                output = output + u'| %(country)s || %(lang)s || %(all)s '
                output = output + u'|| %(name)s <small>(%(namePercentage)s%%)</small>'
                output = output + u'|| %(address)s <small>(%(addressPercentage)s%%)</small>'
                output = output + u'|| %(municipality)s <small>(%(municipalityPercentage)s%%)</small>'
                output = output + u'|| %(coordinates)s <small>(%(coordinatesPercentage)s%%)</small>'
                output = output + u'|| %(image)s <small>(%(imagePercentage)s%%)</small>\n' % statistics[country][language]

    output = output + u'|}\n'

    
    print output

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

    result['country'] = country
    result['lang'] = language

    for (stat, query) in queries.items():
	#print query % (country, language)
        result[stat] = getCount(query % (country, language), cursor)

    result['namePercentage'] = 1.0 * result['name'] / result['all'] * 100
    result['addressPercentage'] = 1.0 * result['address'] / result['all'] * 100
    result['municipalityPercentage'] = 1.0 * result['municipality'] / result['all'] * 100
    result['coordinatesPercentage'] = 1.0 * result['coordinates'] / result['all'] * 100
    result['imagePercentage'] = 1.0 * result['image'] / result['all'] * 100

    return result
        
def getLanguages(country, conn, cursor):
    result = []
    query = u"""SELECT DISTINCT(lang) FROM monuments_all WHERE country='%s'"""
    
    #print query % (country,)
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
	statistics[country] = {}
        for language in getLanguages(country, conn, cursor):
            statistics[country][language] = getStatistics(country, language, conn, cursor)

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
