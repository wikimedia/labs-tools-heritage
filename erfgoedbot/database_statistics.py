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
    #print statistics
    output = u'{| class="wikitable sortable"\n'
    output = output + u'! country !! [[:en:List of ISO 639-1 codes|lang]] !! total !! name !! address !! municipality !! coordinates !! image !! [[:en:ISO 3166-1 alpha-2#Officially assigned code elements|adm0]] !! [[:en:ISO 3166-2#Current codes|adm1]] !! adm2 !! adm3 !! adm4 !! source pages\n'

    totals = {}

    totals['all'] = 0
    totals['name'] = 0
    totals['address'] = 0
    totals['municipality'] = 0
    totals['coordinates'] = 0
    totals['image'] = 0

    totals['adm0'] = 0
    totals['adm1'] = 0
    totals['adm2'] = 0
    totals['adm3'] = 0
    totals['adm4'] = 0
    
    totals['source'] = 0

    for country in sorted(statistics.keys()):
        for language in sorted(statistics.get(country).keys()):
		#print country
		#print language
		#print statistics[country][language]

                output = output + u'|-\n'
                output = output + u'| [http://toolserver.org/~erfgoed/api/api.php?action=statistics&stcountry=%(country)s&format=html&limit=0 %(country)s] ' % statistics[country][language]
                output = output + u'|| %(lang)s || %(all)s ' % statistics[country][language]
                output = output + u'|| %(name)s <small>(%(namePercentage)s%%)</small>' % statistics[country][language]
                output = output + u'|| %(address)s <small>(%(addressPercentage)s%%)</small>' % statistics[country][language]
                output = output + u'|| %(municipality)s <small>(%(municipalityPercentage)s%%)</small>' % statistics[country][language]
                output = output + u'|| %(coordinates)s <small>(%(coordinatesPercentage)s%%)</small>' % statistics[country][language]
                output = output + u'|| %(image)s <small>(%(imagePercentage)s%%)</small>' % statistics[country][language]

                output = output + u'|| %(adm0)s <small>(%(adm0Percentage)s%%)</small>' % statistics[country][language]
                output = output + u'|| [http://wlm.wikimedia.org/api/api.php?action=adminlevels&format=json&admtree=%(adm0iso)s %(adm1)s] <small>(%(adm1Percentage)s%%)</small>' % statistics[country][language]
                output = output + u'|| %(adm2)s <small>(%(adm2Percentage)s%%)</small>' % statistics[country][language]
                output = output + u'|| %(adm3)s <small>(%(adm3Percentage)s%%)</small>' % statistics[country][language]
                output = output + u'|| %(adm4)s <small>(%(adm4Percentage)s%%)</small>' % statistics[country][language]
                
		output = output + u'|| %(source)s\n' % statistics[country][language]

		totals['all'] = totals['all'] + statistics[country][language]['all']
		totals['name'] = totals['name'] + statistics[country][language]['name']
		totals['address'] = totals['address'] + statistics[country][language]['address']
		totals['municipality'] = totals['municipality'] + statistics[country][language]['municipality']
		totals['coordinates'] = totals['coordinates'] + statistics[country][language]['coordinates']
		totals['image'] = totals['image'] + statistics[country][language]['image']

		totals['adm0'] = totals['adm0'] + statistics[country][language]['adm0']
		totals['adm1'] = totals['adm1'] + statistics[country][language]['adm1']
		totals['adm2'] = totals['adm2'] + statistics[country][language]['adm2']
		totals['adm3'] = totals['adm3'] + statistics[country][language]['adm3']
		totals['adm4'] = totals['adm4'] + statistics[country][language]['adm4']

		totals['source'] = totals['source'] + statistics[country][language]['source']



    totals['namePercentage'] = round(1.0 * totals['name'] / totals['all'] * 100, 2)
    totals['addressPercentage'] = round(1.0 * totals['address'] / totals['all'] * 100, 2)
    totals['municipalityPercentage'] = round(1.0 * totals['municipality'] / totals['all'] * 100, 2)
    totals['coordinatesPercentage'] = round(1.0 * totals['coordinates'] / totals['all'] * 100, 2)
    totals['imagePercentage'] = round(1.0 * totals['image'] / totals['all'] * 100, 2)

    totals['adm0Percentage'] = round(1.0 * totals['adm0'] / totals['all'] * 100, 2)
    totals['adm1Percentage'] = round(1.0 * totals['adm1'] / totals['all'] * 100, 2)
    totals['adm2Percentage'] = round(1.0 * totals['adm2'] / totals['all'] * 100, 2)
    totals['adm3Percentage'] = round(1.0 * totals['adm3'] / totals['all'] * 100, 2)
    totals['adm4Percentage'] = round(1.0 * totals['adm4'] / totals['all'] * 100, 2)

    output = output + u'|-\n'
    output = output + u'| '
    output = output + u'|| || %(all)s' % totals
    output = output + u'|| %(name)s <small>(%(namePercentage)s%%)</small>' % totals
    output = output + u'|| %(address)s <small>(%(addressPercentage)s%%)</small>' % totals
    output = output + u'|| %(municipality)s <small>(%(municipalityPercentage)s%%)</small>' % totals
    output = output + u'|| %(coordinates)s <small>(%(coordinatesPercentage)s%%)</small>' % totals
    output = output + u'|| %(image)s <small>(%(imagePercentage)s%%)</small>' % totals

    output = output + u'|| %(adm0)s <small>(%(adm0Percentage)s%%)</small>' % totals
    output = output + u'|| %(adm1)s <small>(%(adm1Percentage)s%%)</small>' % totals
    output = output + u'|| %(adm2)s <small>(%(adm2Percentage)s%%)</small>' % totals
    output = output + u'|| %(adm3)s <small>(%(adm3Percentage)s%%)</small>' % totals
    output = output + u'|| %(adm4)s <small>(%(adm4Percentage)s%%)</small>' % totals
    
    output = output + u'|| %(source)s\n' % totals

    output = output + u'|}\n'
    site = wikipedia.getSite('commons', 'commons')
    page = wikipedia.Page(site, u'Commons:Monuments database/Statistics')
    
    comment = u'Updating monument database statistics'
    page.put(newtext = output, comment = comment)

def getStatistics(country, language, conn, cursor):
    '''
    '''
    queries = {}
    result = {}
    
    queries['all'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s'""" 
    queries['name'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (name='' OR name IS NULL)"""
    queries['address'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (address='' OR address IS NULL)"""
    queries['municipality'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (municipality='' OR municipality IS NULL)"""
    queries['coordinates'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (lat=0 OR lat IS NULL) AND NOT (lon=0 OR lon IS NULL)"""
    queries['image'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (image='' OR image IS NULL)"""

    queries['adm0iso'] = u"""SELECT adm0 FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (adm0='' OR adm0 IS NULL) LIMIT 1"""
    queries['adm0'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (adm0='' OR adm0 IS NULL)"""
    queries['adm1'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (adm1='' OR adm1 IS NULL)"""
    queries['adm2'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (adm2='' OR adm2 IS NULL)"""
    queries['adm3'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (adm3='' OR adm3 IS NULL)"""
    queries['adm4'] = u"""SELECT COUNT(*) FROM monuments_all WHERE country='%s' AND lang='%s' AND NOT (adm4='' OR adm4 IS NULL)"""
    
    queries['source'] = u"""SELECT COUNT(DISTINCT(source)) FROM monuments_all WHERE country='%s' AND lang='%s'"""

    result['country'] = country
    result['lang'] = language

    for (stat, query) in queries.items():
	#print query % (country, language)
        result[stat] = getCount(query % (country, language), cursor)

    result['namePercentage'] = round(1.0 * result['name'] / result['all'] * 100, 2)
    result['addressPercentage'] = round(1.0 * result['address'] / result['all'] * 100, 2)
    result['municipalityPercentage'] = round(1.0 * result['municipality'] / result['all'] * 100, 2)
    result['coordinatesPercentage'] = round(1.0 * result['coordinates'] / result['all'] * 100, 2)
    result['imagePercentage'] = round(1.0 * result['image'] / result['all'] * 100, 2)

    result['adm0Percentage'] = round(1.0 * result['adm0'] / result['all'] * 100, 2)
    result['adm1Percentage'] = round(1.0 * result['adm1'] / result['all'] * 100, 2)
    result['adm2Percentage'] = round(1.0 * result['adm2'] / result['all'] * 100, 2)
    result['adm3Percentage'] = round(1.0 * result['adm3'] / result['all'] * 100, 2)
    result['adm4Percentage'] = round(1.0 * result['adm4'] / result['all'] * 100, 2)

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
