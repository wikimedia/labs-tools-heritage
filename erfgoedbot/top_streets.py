#!/usr/bin/python
# -*- coding: utf-8  -*-
'''
Make a list of top streets for a municipality. Bot expects two things on the commandline:
* -countrycode : The country code (as it is in the database)
* -municipality : The name of the municipality (as it is in the database)

'''
import sys
import monuments_config as mconfig
#sys.path.append("/home/project/e/r/f/erfgoed/pywikipedia")
sys.path.append("/home/multichill/pywikipedia")
import wikipedia, config
import MySQLdb, time
from collections import Counter

def connectDatabase():
    '''
    Connect to the monuments mysql database, if it fails, go down in flames.
    This database is utf-8 encoded.
    '''
    conn = MySQLdb.connect(host=mconfig.db_server, db=mconfig.db, user = config.db_username, passwd = config.db_password, use_unicode=True, charset='utf8')
    cursor = conn.cursor()
    return (conn, cursor)

def getMonumentsWithPhoto(countrycode, lang, countryconfig, conn, cursor):
    '''
    Get a dictionary of images which are in the monuments database for a certain country/language combination.
    '''
    result = {}
    query = u"""SELECT image, id FROM monuments_all WHERE NOT image='' AND country=%s AND lang=%s""";
    cursor.execute(query, (countrycode, lang))

    while True:
	try:
	    row = cursor.fetchone()
	    (image, id) = row
	    image = image.replace(u' ', u'_') # Spaces are lowercase in the other database
	    image = image[0].upper() + image[1:] # First char always needs to be uppercase
	    result[image] = id
	except TypeError:
	    break

    return result

def getMonumentsWithoutTemplate(countrycode, lang, countryconfig, conn, cursor):
    '''
    Get a list of images which are in the relevant monuments category tree, but don't contain the identification template.
    '''
    
    commonsCategoryBase = countryconfig.get('commonsCategoryBase'). replace(u' ', u'_')
    commonsTemplate = countryconfig.get('commonsTemplate').replace(u' ', u'_')   

    result = []
    query = u"""SELECT DISTINCT(page_title) FROM page JOIN categorylinks ON page_id=cl_from WHERE page_namespace=6 AND page_is_redirect=0 AND (cl_to='%s' OR cl_to LIKE '%s\_in\_%%') AND NOT EXISTS(SELECT * FROM templatelinks WHERE page_id=tl_from AND tl_namespace=10 AND tl_title='%s') ORDER BY page_title ASC"""
    cursor.execute(query % (commonsCategoryBase, commonsCategoryBase, commonsTemplate))    

    while True:
        try:
            row = cursor.fetchone()
            (image,) = row
            result.append(image.decode('utf-8'))
        except TypeError:
            break

    return result

def getMonumentsWithTemplate(countrycode, lang, countryconfig, conn, cursor):
    '''
    Get all images of monuments which already contain the identification template.
    '''
    
    commonsTrackerCategory = countryconfig.get('commonsTrackerCategory'). replace(u' ', u'_')
    
    result = []
    query = u"""SELECT DISTINCT(page_title) FROM page JOIN categorylinks ON page_id=cl_from WHERE page_namespace=6 AND page_is_redirect=0 AND cl_to=%s ORDER BY page_title ASC"""
    cursor.execute(query, (commonsTrackerCategory,))

    while True:
        try:
            row = cursor.fetchone()
            (image,) = row
            result.append(image.decode('utf-8'))
        except TypeError:
            break

    return result    

def addCommonsTemplate(image, commonsTemplate, identifier):
    '''
    Add the commonsTemplate with identifier to the image.
    '''
    site = wikipedia.getSite('commons', 'commons')
    page = wikipedia.ImagePage(site, image)
    if not page.exists() or page.isRedirectPage() or page.isEmpty():
        return False
    
    if commonsTemplate in page.templates():
        return False

    text = page.get()
    newtext = u'{{%s|%s}}\n' % (commonsTemplate, identifier) + text

    comment = u'Adding template %s based on usage in list' % (commonsTemplate,)

    wikipedia.showDiff(text, newtext)
    page.put(newtext, comment)
    return True

def getAddresses(countrycode, lang, municipality, conn, cursor):
    result = []
    query = u"""SELECT address FROM monuments_all WHERE country=%s AND lang=%s AND municipality=%s ORDER BY address ASC""";
    cursor.execute(query, (countrycode, lang, municipality))
    
    while True:
	try:
	    row = cursor.fetchone()
	    (address,) = row
	    result.append(address)
	except TypeError:
	    break
    
    return result

def printTopStreets (addresses):
    streets = Counter() #collections.Counter
    for address in addresses:
	temp = u''
	partslist = []
	for addrPart in address.split(u' '):
	    temp = temp + u' ' + addrPart
	    partslist.append(temp)
	
	streets.update(partslist)
    
    for street in streets.most_common(50):
	print street

def main():
    countrycode = u''
    lang = u''
    municipality = u''
    conn = None
    cursor = None
    # Connect database, we need that
    (conn, cursor) = connectDatabase()
    
    for arg in wikipedia.handleArgs():
        if arg.startswith('-countrycode:'):
            countrycode = arg [len('-countrycode:'):]
	elif arg.startswith('-municipality:'):
	    municipality = arg [len('-municipality:'):]

    if countrycode and municipality:
	lang = wikipedia.getSite().language()
	addresses = getAddresses(countrycode, lang, municipality, conn, cursor)
	printTopStreets (addresses)
    else:
	print u'Usage'

if __name__ == "__main__":
    try:
        main()
    finally:
        wikipedia.stopme()
