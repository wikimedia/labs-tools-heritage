#!/usr/bin/python
# -*- coding: utf-8  -*-
'''

Bot to add {{Object location dec}} to monuments. Location is based on information from the monuments database.

'''
import sys
import monuments_config as mconfig
sys.path.append("/home/project/e/r/f/erfgoed/pywikipedia")
import wikipedia, config, pagegenerators, catlib
import re, imagerecat
import MySQLdb, config, time

def connectDatabase():
    '''
    Connect to the monuments mysql database, if it fails, go down in flames
    '''
    conn = MySQLdb.connect(host=mconfig.db_server, db=mconfig.db, user = config.db_username, passwd = config.db_password, use_unicode=True, charset='utf8')
    cursor = conn.cursor()
    return (conn, cursor)


def connectDatabase2():
    '''
    Connect to the commons mysql database, if it fails, go down in flames
    '''
    conn = MySQLdb.connect('commonswiki-p.db.toolserver.org', db='commonswiki_p', user = config.db_username, passwd = config.db_password, use_unicode=True, charset='latin1')
    cursor = conn.cursor()
    return (conn, cursor)


def locateCountry(countrycode, lang, countryconfig, conn, cursor, conn2, cursor2):
    '''
    Locate images in a single country.
    '''
    if not countryconfig.get('commonsTemplate') or not countryconfig.get('commonsTrackerCategory'):
        # Not possible for this country. Silently return
        return False

    for (page, monumentId) in getMonumentsWithoutLocation(countryconfig, conn2, cursor2):
	locationTemplate = locateImage(page, monumentId, countrycode, lang, countryconfig, conn, cursor)
	if locationTemplate:
	    addLocation(page, locationTemplate)


def getMonumentsWithoutLocation(countryconfig, conn2, cursor2):
    site = wikipedia.getSite(u'commons', u'commons')
    query = u"""SELECT  page_title, cl_sortkey FROM page
JOIN templatelinks ON page_id=tl_from
JOIN categorylinks ON page_id=cl_from
WHERE page_namespace=6 AND page_is_redirect=0
AND tl_namespace=10 AND tl_title=%s
AND cl_to=%s
AND NOT EXISTS(
SELECT * FROM categorylinks AS loccat
WHERE page_id=loccat.cl_from
AND loccat.cl_to='Media_with_locations') LIMIT 1000""";
    commonsTemplate = countryconfig.get('commonsTemplate').replace(u' ', u'_')
    commonsTrackerCategory = countryconfig.get('commonsTrackerCategory').replace(u' ', u'_')

    cursor2.execute(query, (commonsTemplate.encode('utf-8'), commonsTrackerCategory.encode('utf-8')))

    while True:
        try:
            pageName, sortkey = cursor2.fetchone()
        except TypeError:
            # Nothing left
            break
        if pageName:
	    page = wikipedia.Page(site, 'File:' + unicode(pageName, 'utf-8'))
            try:
                monumentId = unicode(sortkey, 'utf-8')
                # Just want the first line
                mLines = monumentId.splitlines()
                monumentId = mLines[0]
                # Remove leading and trailing spaces
                monumentId = monumentId.strip()
                # Remove leading zero's
                monumentId = monumentId.lstrip(u'0')
                yield (page, monumentId)
            except ValueError:
                wikipedia.output(u'Got value error for %s' % (monumentId,))

                
def locateImage(page, monumentId, countrycode, lang, countryconfig, conn, cursor):
    wikipedia.output(u'Working on: %s with id %s' % (page.title(), monumentId))

    # First check if the identifier returns something useful
    coordinates = getCoordinates(monumentId, countrycode, lang, conn, cursor)
    if not coordinates:
	wikipedia.output(u'File contains an unknown identifier: %s' %monumentId)
	return False
    
    (lat, lon, source) = coordinates

    # Ok. We know we have coordinates. Now check to be sure to see if there's not already a template on the page.
    templates = page.templates()

    if u'Location' in page.templates() or u'Location dec' in page.templates() or u'Object location' in page.templates() or u'Object location dec' in page.templates():
	wikipedia.output(u'Location template already found at: %s' % page.title())
	return False

    locationTemplate = u'{{Object location dec|%s|%s|region:%s_type:landmark_scale:1500}}<!-- Location from %s -->' % (lat, lon, countrycode.upper(), source)

    return locationTemplate


def getCoordinates(monumentId, countrycode, lang, conn, cursor):
    '''
    Get coordinates from the erfgoed database
    '''
    result = None

    query = u"""SELECT lat, lon, source FROM monuments_all
WHERE id=%s
AND country=%s
AND lang=%s
AND NOT lat=0 AND NOT lon=0
AND NOT lat='' AND NOT lon=0
LIMIT 1""";

    cursor.execute(query, (monumentId, countrycode, lang,))

    try:
	row = cursor.fetchone()
	return row
    except TypeError:
	return False


def addLocation (page, locationTemplate):
    oldtext = page.get()

    comment = u'Adding object location based on monument identifier'

    newtext = putAfterTemplate (page, u'Information', locationTemplate, loose=True)
    
    wikipedia.showDiff(oldtext, newtext)
    page.put(newtext, comment)


def putAfterTemplate (page, template, toadd, loose=True):
    '''
    Try to put text after template.
    If the template is not found return False if loose is set to False
    If loose is set to True: Remove interwiki's, categories, add template, restore categories, restore interwiki's.

    Based on cc-by-sa-3.0 code by Dschwen
    '''
    oldtext = page.get()
    newtext = u''

    templatePosition = oldtext.find(u'{{%s' % (template,))

    if templatePosition >= 0:
	previousChar = u''
	currentChar = u''
	templatePosition += 2
	curly = 1
	square = 0
	
	while templatePosition < len(oldtext):
	    currentChar = oldtext[templatePosition]

	    if currentChar == u'[' and previousChar == u'[' :
		square += 1
                previousChar = u''
            if currentChar == u']' and previousChar == u']' :
                square -= 1
                previousChar = u''
            if currentChar == u'{' and previousChar == u'{' :
                curly += 1
                previousChar = u''
            if currentChar == u'}' and previousChar == u'}' :
                curly -= 1
                previousChar = u''

	    previousChar = currentChar
	    templatePosition +=1

	    if curly == 0 and square <= 0 :
		# Found end of template
		break
	newtext = oldtext[:templatePosition] + u'\n' + toadd + oldtext[templatePosition:]
    
    else:
	if loose:
	    newtext = oldtext
	    cats = wikipedia.getCategoryLinks(newtext)
	    ll = wikipedia.getLanguageLinks(newtext)
	    nextext = wikipedia.removeLanguageLinks (newtext)
	    newtext = wikipedia.removeCategoryLinks(newtext)
	    newtext = newtext + u'\n' + toadd
	    newtext = wikipedia.replaceCategoryLinks(newtext, cats)
	    newtext = wikipedia.replaceLanguageLinks(newtext, ll)
    
    return newtext


def main():
    countrycode = u''

    # Connect database, we need that
    (conn, cursor) = connectDatabase()
    (conn2, cursor2) = connectDatabase2()

    generator = None
    genFactory = pagegenerators.GeneratorFactory()

    for arg in wikipedia.handleArgs():
        if arg.startswith('-countrycode:'):
            countrycode = arg [len('-countrycode:'):]

    lang = wikipedia.getSite().language()
    wikipedia.setSite(wikipedia.getSite(u'commons', u'commons'))
    
    if countrycode:
	if not mconfig.countries.get((countrycode, lang)):
	    wikipedia.output(u'I have no config for countrycode "%s" in language "%s"' % (countrycode, lang))
	    return False
	wikipedia.output(u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
	locateCountry(countrycode, lang, mconfig.countries.get((countrycode, lang)), conn, cursor, conn2, cursor2)
    else:
	for (countrycode, lang), countryconfig in mconfig.countries.iteritems():
            if not countryconfig.get('autoGeocode'):
                wikipedia.output(u'"%s" in language "%s" is not supported in auto geocode mode (yet).' % (countrycode, lang))
            else:
                wikipedia.output(u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
                locateCountry(countrycode, lang, countryconfig, conn, cursor, conn2, cursor2)

if __name__ == "__main__":
    try:
        main()
    finally:
        wikipedia.stopme()
