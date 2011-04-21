#!/usr/bin/python
# -*- coding: utf-8  -*-
'''

Make a gallery of rijksmonumenten without an id at Commons

FIXME: Encoding issues.

'''
import sys
import monuments_config as mconfig
sys.path.append("/home/project/e/r/f/erfgoed/pywikipedia")
import wikipedia, config, pagegenerators, catlib
import re, imagerecat
import MySQLdb, config, time

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
    if not countryconfig.get('commonsTemplate'):
        # No template found, just skip silently.
        return False
    
    commonsTemplate = countryconfig.get('commonsTemplate')
    imagesWithoutIdPage = countryconfig.get('imagesWithoutIdPage')

    # All items in the list with a photo
    withPhoto = getMonumentsWithPhoto(countrycode, lang, countryconfig, conn, cursor)

    # All items on Commons with the id template
    withTemplate= getMonumentsWithTemplate(countrycode, lang, countryconfig, conn2, cursor2)

    # All items on Commons in the monument tree without the id template
    withoutTemplate = getMonumentsWithoutTemplate(countrycode, lang, countryconfig, conn2, cursor2)

    print withPhoto
    print withTemplate
    print withoutTemplate

    #incorrectTemplate = getRijksmonumentenWitIncorrectTemplate(conn2, cursor2)
    #ignoreList = [u'Monumentenschildje.jpg', u'Rijksmonument-Schildje-NL.jpg']

    text = u'<gallery>\n'
    #for image in withoutTemplate + incorrectTemplate:
    for image in withoutTemplate:
	#if not image in ignoreList:

        # An image is in the category and is in the list of used images
	if withPhoto.get(image):
	    text = text + u'File:%s|{{tl|%s|%s}}\n' % (image, commonsTemplate, withPhoto.get(image))
	# An image is in the category and is not in the list of used images
	else:
	    text = text + u'File:%s\n' % (image,)

    # An image is in the list of used images, but not in the category
    for image in withPhoto:
        # Skip images which already have the templates and the ones in without templates to prevent duplicates
        if not withTemplate.get(image) and not withoutTemplate.get(image):
            text = text + u'File:%s|{{tl|%s|%s}}\n' % (image, commonsTemplate, withPhoto.get(image))
	    
    text = text + u'</gallery>' 
    comment = u'Images without an id'
    
    site = wikipedia.getSite(lang, u'wikipedia')
    page = wikipedia.Page(site, imagesWithoutIdPage)
    wikipedia.output(text)
    #page.put(text, comment)

def getMonumentsWithPhoto(countrycode, lang, countryconfig, conn, cursor):
    result = {}

    query = u"""SELECT image, id FROM monuments_all WHERE NOT image='' AND country='%s' AND lang='%s'""";

    print query % (countrycode, lang)


    cursor.execute(query % (countrycode, lang))

    while True:
	try:
	    row = cursor.fetchone()
	    (image, id) = row
	    result[image.replace(u' ', u'_')] = id
	except TypeError:
	    break

    return result

def getMonumentsWithoutTemplate(countrycode, lang, countryconfig, conn, cursor):
    result = []

    commonsCategoryBase = countryconfig.get('commonsCategoryBase'). replace(u' ', u'_')
    commonsTemplate = countryconfig.get('commonsTemplate'). replace(u' ', u'_')

    query = u"""SELECT DISTINCT(page_title) FROM page JOIN categorylinks ON page_id=cl_from WHERE page_namespace=6 AND page_is_redirect=0 AND (cl_to='%s' OR cl_to LIKE '%s\_in\_%%') AND NOT EXISTS(SELECT * FROM templatelinks WHERE page_id=tl_from AND tl_namespace=10 AND tl_title='%s') ORDER BY page_title ASC"""

    print commonsCategoryBase
    print commonsTemplate

    print query % (commonsCategoryBase, commonsCategoryBase, commonsTemplate)

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
    Get all images of monuments which already contain the template.
    '''
    result = []

    commonsTrackerCategory = countryconfig.get('commonsTrackerCategory'). replace(u' ', u'_')

    query = u"""SELECT DISTINCT(page_title) FROM page JOIN categorylinks ON page_id=cl_from WHERE page_namespace=6 AND page_is_redirect=0 AND cl_to='%s' ORDER BY page_title ASC"""

    print query % (commonsTrackerCategory,)

    cursor.execute(query % (commonsTrackerCategory, commonsCategoryBase, commonsTemplate))

    while True:
        try:
            row = cursor.fetchone()
            (image,) = row
            result.append(image.decode('utf-8'))
        except TypeError:
            break

    return result    

def getRijksmonumentenWitIncorrectTemplate(conn, cursor):
    result = []
    query = u"""SELECT DISTINCT(page_title) FROM categorylinks JOIN page ON cl_from=page_id WHERE cl_to='Rijksmonumenten_with_known_IDs' AND (cl_sortkey=' 000000-1' OR cl_sortkey=' 00000000' OR cl_sortkey=' 0000000?' OR cl_sortkey=' onbekend') AND page_namespace=6 AND page_is_redirect=0 ORDER BY page_title ASC"""

    cursor.execute(query)

    while True:
        try:
            row = cursor.fetchone()
            (image,) = row
            result.append(image.decode('utf-8'))
        except TypeError:
            break

    return result

def main():
    # Connect database, we need that
    countrycode = u''
    conn = None
    cursor = None
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
