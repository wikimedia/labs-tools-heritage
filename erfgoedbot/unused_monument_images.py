#!/usr/bin/python
# -*- coding: utf-8  -*-
'''

Make a gallery of unused photos so people can add them to monument lists

Usage:
# loop thtough all countries
python unused_monument_images.py
# work on specific country-lang
python unused_monument_images.py -countrycode:XX -lang:YY

'''
import sys
import monuments_config as mconfig
sys.path.append("/home/project/e/r/f/erfgoed/pywikipedia")
import wikipedia, config, re
import MySQLdb, time

def connectDatabase():
    '''
    Connect to the rijksmonumenten mysql database, if it fails, go down in flames
    '''
    conn = MySQLdb.connect(host=mconfig.db_server, db=mconfig.db, user = config.db_username, passwd = config.db_password, use_unicode=True, charset='utf8')
    cursor = conn.cursor()
    return (conn, cursor)

def connectDatabase2():
    '''
    Connect to the commons mysql database, if it fails, go down in flames
    '''
    conn = MySQLdb.connect('commonswiki-p.db.toolserver.org', db='commonswiki_p', user = config.db_username, passwd = config.db_password, use_unicode=True, charset='utf8')
    cursor = conn.cursor()
    return (conn, cursor)

def processCountry(countrycode, lang, countryconfig, conn, cursor, conn2, cursor2):
    '''
    Work on a single country.
    '''
    if not countryconfig.get('unusedImagesPage'):
        # unusedImagesPage not set, just skip silently.
        return False
    
    unusedImagesPage = countryconfig.get('unusedImagesPage')
    commonsTrackerCategory = countryconfig.get('commonsTrackerCategory'). replace(u' ', u'_')
	
    withoutPhoto = getMonumentsWithoutPhoto(countrycode, lang, conn, cursor)
    photos = getMonumentPhotos(commonsTrackerCategory, conn2, cursor2)

    wikipedia.output(u'withoutPhoto %s elements' % (len(withoutPhoto),))
    wikipedia.output(u'photos %s elements' % (len(photos),))

    text = u'<gallery>\n'
    for catSortKey in sorted(photos.keys()):
        try:
            monumentId = unicode(catSortKey, 'utf-8')
            mLines = monumentId.splitlines()
            monumentId = mLines[0]
            monumentId = monumentId[1:]
            monumentId = re.sub("^0+", "", monumentId)
            if monumentId in withoutPhoto:
                m = re.search('^(.+?)&', withoutPhoto.get(monumentId))
                wikiSourceList = m.group(1)
                imageName = photos.get(catSortKey)
                wikipedia.output(u'Key %s returned a result' % (monumentId,))
                wikipedia.output(wikiSourceList)
                wikipedia.output(imageName)
                text = text + u'File:%s|[%s %s]\n' % (unicode(imageName, 'utf-8'), wikiSourceList, monumentId)
        except ValueError:
            wikipedia.output(u'Got value error for %s' % (monumentId,))

    text = text + u'</gallery>'
    comment = u'Images to be used in monument lists'

    site = wikipedia.getSite(lang, u'wikipedia')
    page = wikipedia.Page(site, unusedImagesPage)
    wikipedia.output(text)
    page.put(text, comment)
	
	
def getMonumentsWithoutPhoto(countrycode, lang, conn, cursor):
    result = {}

    query = u"""SELECT id, source FROM monuments_all WHERE image='' AND country=%s AND lang=%s""";

    cursor.execute(query, (countrycode, lang))

    while True:
        try:
            row = cursor.fetchone()
            (id, source) = row
            result[id] = source
        except TypeError:
            break

    return result

def getMonumentPhotos(commonsTrackerCategory, conn, cursor):
    result = {}

    query = u"""SELECT page_title, cl_sortkey FROM page JOIN categorylinks ON page_id=cl_from WHERE page_namespace=6 AND page_is_redirect=0 AND cl_to=%s""";

    cursor.execute(query, (commonsTrackerCategory,))

    while True:
        try:
            row = cursor.fetchone()
            (image, id) = row
            result[id] = image
        except TypeError:
            break

    return result


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
        lang = wikipedia.getSite().language()
	if not mconfig.countries.get((countrycode, lang)):
	    wikipedia.output(u'I have no config for countrycode "%s" in language "%s"' % (countrycode, lang))
	    return False
	wikipedia.output(u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
	processCountry(countrycode, lang, mconfig.countries.get((countrycode, lang)), conn, cursor, conn2, cursor2)
    else:
	for (countrycode, lang), countryconfig in mconfig.countries.iteritems():
	    wikipedia.output(u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
	    processCountry(countrycode, lang, countryconfig, conn, cursor, conn2, cursor2)

		
if __name__ == "__main__":
    try:
        main()
    finally:
        wikipedia.stopme()