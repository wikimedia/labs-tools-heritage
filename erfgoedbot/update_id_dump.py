#!/usr/bin/python
#$ -l h_rt=0:30:00
#$ -j y
#$ -o $HOME/erfgoedbot/update_id_dump.out
# -*- coding: utf-8  -*-
'''
Update the id_dump table from some wiki page(s)

Usage:
# loop thtough all countries
python update_id_dump.py


'''
import sys, time
sys.path.append("/home/project/e/r/f/erfgoed/erfgoedbot")
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


def updateMonument(countrycode, lang, id, source, countryconfig, conn, cursor):
    '''
    FIXME :  cursor.execute(query, (tuple)) om het escape probleem te fixen
    '''
    fieldnames = []
    fieldvalues = []

    fieldnames.append('source')
    fieldvalues.append(source)
    fieldnames.append('id')
    fieldvalues.append(id)
    fieldnames.append('country')
    fieldvalues.append(countrycode)
    fieldnames.append('lang')
    fieldvalues.append(lang)

    query = u"""INSERT INTO `id_dump`("""

    j =0
    for fieldname in fieldnames:
	if j==0:
	    query = query + u"""`%s`""" % (fieldname,)
	else:
	    query = query + u""", `%s`""" % (fieldname,)
	j = j + 1

    query = query + u""") VALUES ("""

    j =0
    for fieldvalue in fieldvalues:
	if j==0:
	    query = query + u"""%s""" 
	else:
	    query = query + u""", %s""" 
	j = j + 1

    query = query + u""")"""


    cursor.execute(query, fieldvalues)

def processMonument(countrycode, lang, params, source, countryconfig, conn, cursor):
    '''
    Process a single instance of a monument row template
    '''
    
    id = u''	

    for param in params:
        #Split at =
        (field, sep, value) = param.partition(u'=')
        # Remove leading or trailing spaces
        field = field.strip()
        value = value.strip()

        if (field == countryconfig.get('primkey')):
            id = value
            wikipedia.output(u'Field: %s' % (field,))
            wikipedia.output(u'Value: %s' % (value,))
    
    updateMonument(countrycode, lang, id, source, countryconfig, conn, cursor)
    #print contents
    #time.sleep(5)

def processText(countrycode, lang, text, source, countryconfig, conn, cursor, page=None):
    '''
    Process a text containing one or multiple instances of the monument row template
    '''
    templates = page.templatesWithParams(thistxt=text)
    for (template, params) in templates:
	if template==countryconfig.get('rowTemplate'):
	    #print template
	    #print params
	    processMonument(countrycode, lang, params, source, countryconfig, conn, cursor)
	    #time.sleep(5)

def processCountry(countrycode, lang, countryconfig, conn, cursor):
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
	    processText(countrycode, lang, page.get(), page.permalink(), countryconfig, conn, cursor, page=page)


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
		elif arg.startswith('-textfile:'):
			textfile = arg [len('-textfile:'):]

		
	query = u"""TRUNCATE table `id_dump`"""
	cursor.execute(query)		
		
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
			processCountry(countrycode, lang, mconfig.countries.get((countrycode, lang)), conn, cursor)
	else:
		for (countrycode, lang), countryconfig in mconfig.countries.iteritems():
			wikipedia.output(u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
			processCountry(countrycode, lang, countryconfig, conn, cursor)

if __name__ == "__main__":
    try:
        main()
    finally:
        wikipedia.stopme()
