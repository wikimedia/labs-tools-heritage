#!/usr/bin/python
# -*- coding: utf-8  -*-
'''

Add monument-ID-templates to images on Commons -- based on the image usage in the lists -- and
  make a galleries of monuments without an id at Commons

Usage:
# loop thtough all countries
python images_of_monuments_without_id.py
# work on specific country-lang
python images_of_monuments_without_id.py -countrycode:XX -lang:YY


'''
import sys
import monuments_config as mconfig
sys.path.append("/home/project/e/r/f/erfgoed/pywikipedia")
import wikipedia, config
import MySQLdb, time
##import re, imagerecat, pagegenerators, catlib

def connectDatabase():
    '''
    Connect to the monuments mysql database, if it fails, go down in flames.
    This database is utf-8 encoded.
    '''
    conn = MySQLdb.connect(host=mconfig.db_server, db=mconfig.db, user = config.db_username, passwd = config.db_password, use_unicode=True, charset='utf8')
    cursor = conn.cursor()
    return (conn, cursor)

def connectDatabase2():
    '''
    Connect to the commons mysql database, if it fails, go down in flames
    This database is latin1 encoded.
    '''
    conn = MySQLdb.connect('commonswiki-p.db.toolserver.org', db='commonswiki_p', user = config.db_username, passwd = config.db_password, use_unicode=True, charset='latin1')
    cursor = conn.cursor()
    return (conn, cursor)

def processCountry(countrycode, lang, countryconfig, conn, cursor, conn2, cursor2):
    '''
    Work on a single country.
    '''
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

    # Get the image ignore list
    # FIXME: Make an actual function of this instead of a static list.
    ignoreList = [u'Monumentenschildje.jpg', u'Rijksmonument-Schildje-NL.jpg']

    # FIXME: Do something with a header template.
    text = u'<gallery>\n'
    
    for image in withoutTemplate:
	if not image in ignoreList:
            # An image is in the category and is in the list of used images
            if withPhoto.get(image):
                added = addCommonsTemplate(image, commonsTemplate, withPhoto.get(image))
                if not added:
                    text = text + u'File:%s|<nowiki>{{%s|%s}}</nowiki>\n' % (image, commonsTemplate, withPhoto.get(image))
            # An image is in the category and is not in the list of used images
            else:
                text = text + u'File:%s\n' % (image,)

    # An image is in the list of used images, but not in the category
    for image in withPhoto:
        # Skip images which already have the templates and the ones in without templates to prevent duplicates
        if not image in ignoreList and not image in withTemplate and not image in withoutTemplate:
            added = addCommonsTemplate(image, commonsTemplate, withPhoto.get(image))
            if not added:
                text = text + u'File:%s|<nowiki>{{%s|%s}}</nowiki>\n' % (image, commonsTemplate, withPhoto.get(image))
	    
    text = text + u'</gallery>'

    # imagesWithoutIdPage isn't set for every source, just skip it if it's not set
    if imagesWithoutIdPage:
        comment = u'Images without an id'
    
        site = wikipedia.getSite(lang, u'wikipedia')
    
        page = wikipedia.Page(site, imagesWithoutIdPage)
        wikipedia.output(text)
        page.put(text, comment)

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
        # looks like default lang is 'nl'
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
