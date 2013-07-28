#!/usr/bin/python
# -*- coding: utf-8  -*-
'''

Update the image table with all the images tracked by a template in https://commons.wikimedia.org/wiki/Category:Cultural_heritage_monuments_with_known_IDs

The fields:
* country - same as country field in the monuments_all table
* id - same as the id field in the monuments_all table
* img_name - The filename at Commons

First the bots loops over the configuration and gets:
* countrycode
* commonsTemplate
* commonsTrackerCategory
Some countries are available in multiple languages. This is deduplicated

For each combination the bot will loop over the Commons database and insert the information into the image table


Make a gallery of unused photos so people can add them to monument lists

Usage:
# Do everything
python populate_image_table.py
# Do just a specific country
python populate_image_table.py -countrycode:xx

'''
import sys, warnings
import monuments_config as mconfig
sys.path.append("/home/project/e/r/f/erfgoed/pywikipedia")
import wikipedia, config, re
import MySQLdb, time

def connectDatabase():
    '''
    Connect to the p_erfgoed_p mysql database, if it fails, go down in flames
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

def getSources(countrycode=u''):
    '''
    Get a dictionary of sources to go harvest
    '''
    sources = {}
    for (icountrycode, lang), countryconfig in mconfig.countries.iteritems():
        if not countrycode or (countrycode and countrycode==icountrycode):
            if not icountrycode in sources:
                if countryconfig.get('commonsTemplate') and countryconfig.get('commonsTrackerCategory'):
                    sources[icountrycode] = {
                        'commonsTemplate': countryconfig.get('commonsTemplate'),
                        'commonsTrackerCategory': countryconfig.get('commonsTrackerCategory'),
                        }
    return sources
            

def processSources(sources, conn, cursor, conn2, cursor2):
    '''
    Loop over all sources and process them. Very small right now, will probably exapnded later
    '''
    result = sources
    for countrycode, countryconfig in sources.iteritems():
        totalImages = processSource(countrycode, countryconfig, conn, cursor, conn2, cursor2)
	result[countrycode]['totalImages'] = totalImages
    return result
            
def processSource(countrycode, countryconfig, conn, cursor, conn2, cursor2):
    '''
    Work on a single source (country).
    '''
   
    commonsTemplate = countryconfig.get('commonsTemplate').replace(u' ', u'_')
    commonsTrackerCategory = countryconfig.get('commonsTrackerCategory').replace(u' ', u'_')

    photos = getMonumentPhotos(commonsTrackerCategory, conn2, cursor2)

    wikipedia.output(u'For country "%s" I found %s photos tagged with "{{%s}}" in [[Category:%s]]' % (countrycode, len(photos), commonsTemplate, commonsTrackerCategory))
    
    for catSortKey, page_title in photos:
        try:
	    monumentId = unicode(catSortKey, 'utf-8')
	    name = unicode(page_title, 'utf-8')
	    # Just want the first line
	    mLines = monumentId.splitlines()
	    monumentId = mLines[0]
	    # Remove leading and trailing spaces
	    monumentId = monumentId.strip()
	    # Remove leading zero's. FIXME: This should be replaced with underscores
	    monumentId = monumentId.lstrip(u'0')
	    # Remove leading underscors.
	    monumentId = monumentId.lstrip(u'_')
	    # All uppercase, same happens in other list
	    #monumentId = monumentId.upper()
	    updateImage(countrycode, monumentId, name, conn, cursor)

	except UnicodeDecodeError:
	     wikipedia.output(u'Got unicode decode error for %s' % (monumentId,))
	# UnicodeDecodeError is a subclass of ValueError and should catch most
	except ValueError:
	    wikipedia.output(u'Got value error for %s' % (monumentId,))
  
    return len(photos)           

def getMonumentPhotos(commonsTrackerCategory, conn, cursor):
    '''
    Get all the monument photos that are in a certain tracker category at Wikimedia Commons
    '''
    result = []

    query = u"""SELECT cl_sortkey, page_title FROM page JOIN categorylinks ON page_id=cl_from WHERE page_namespace=6 AND page_is_redirect=0 AND cl_to=%s""";

    cursor.execute(query, (commonsTrackerCategory,))

    result = cursor.fetchall()
    '''
    while True:
        try:
            row = cursor.fetchone()
            #(image, id) = row
            result.append(row)
	    print row
            #result[id] = image
        except TypeError:
            break
    '''
    return result

def updateImage(countrycode, monumentId, name, conn, cursor):
    '''
    Update an entry for a single image
    '''
    query = u"""REPLACE INTO `image` (`country`, `id`, `img_name`) VALUES (%s, %s, %s)"""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        cursor.execute(query, (countrycode, monumentId, name,))          

def makeStatistics(totals):
    '''
    Make statistics on the number of indexed images and put these on Commons
    '''
    text = u'{| class="wikitable sortable"\n'
    text = text + u'! country !! total !! tracker template !! tracker category\n'
    totalImages = 0
    print totals
    for (countrycode, countryresults) in sorted(totals.iteritems()):
            text = text + u'|-\n'
            text = text + u'| %s ' % countrycode
            text = text + u'|| %s ' % countryresults.get('totalImages')
	    totalImages = totalImages + countryresults.get('totalImages')
	    text = text + u'|| {{tl|%s}}' % countryresults.get('commonsTemplate')
	    text = text + u'|| [[:Category:%s|%s]]\n' % (countryresults.get('commonsTrackerCategory'), countryresults.get('commonsTrackerCategory'))
    text = text + u'|- class="sortbottom"\n'
    text = text + u'| || %s \n' % totalImages
    text = text + u'|}\n'
    
    site = wikipedia.getSite('commons', 'commons')
    page = wikipedia.Page(site, u'Commons:Monuments database/Indexed images/Statistics')
    
    comment = u'Updating indexed image statistics. Total indexed images: %s' % totalImages
    wikipedia.output(text)
    page.put(newtext = text, comment = comment)

def main():
    countrycode = u''
    conn = None
    cursor = None
    # Connect database, we need that
    (conn, cursor) = connectDatabase()
    (conn2, cursor2) = connectDatabase2()
    
    for arg in wikipedia.handleArgs():
        if arg.startswith('-countrycode:'):
            countrycode = arg [len('-countrycode:'):]

    if countrycode:
        wikipedia.output(u'Working on countrycode "%s"' % (countrycode,))
        sources = getSources(countrycode=countrycode)
        if not sources:
            wikipedia.output(u'I have no config for countrycode "%s"' % (countrycode,))
            return False
        else:
            totals = processSources(sources, conn, cursor, conn2, cursor2)

    else:
        wikipedia.output(u'Working on all countrycodes')
        sources = getSources()
        if not sources:
            wikipedia.output(u'No sources found, something went completely wrong')
            return False
        else:
            wikipedia.output(u'Found %s countries with monument tracker templates to work on' % (len(sources),))
            totals = processSources(sources, conn, cursor, conn2, cursor2)

	    makeStatistics(totals)

		
if __name__ == "__main__":
    try:
        main()
    finally:
        wikipedia.stopme()