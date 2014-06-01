#!/usr/bin/python
# -*- coding: utf-8  -*-
'''

Make a list of monuments where a category about the monument exists, but no link is in the list yet.

Usage:
# loop thtough all countries
python missing_commonscat_links.py
# work on specific country-lang
python missing_commonscat_links.py -countrycode:XX -lang:YY

'''
import sys
import monuments_config as mconfig
import wikipedia, config, re
import MySQLdb, time

def connectDatabase():
    '''
    Connect to the p_erfoed_p mysql database, if it fails, go down in flames
    '''
    conn = MySQLdb.connect(host=mconfig.db_server, db=mconfig.db, user = config.db_username, passwd = config.db_password, use_unicode=True, charset='utf8')
    cursor = conn.cursor()
    return (conn, cursor)

def connectDatabase2():
    '''
    Connect to the commons mysql database, if it fails, go down in flames
    '''
    conn = MySQLdb.connect('commonswiki.labsdb', db='commonswiki_p', user = config.db_username, passwd = config.db_password, use_unicode=True, charset='latin1')
    cursor = conn.cursor()
    return (conn, cursor)

def processCountry(countrycode, lang, countryconfig, conn, cursor, conn2, cursor2):
    '''
    Work on a single country.
    '''
    if not countryconfig.get('missingCommonscatPage'):
        # missingCommonscatPage not set, just skip silently.
        return False

    commonscatField = lookupSourceField(u'commonscat', countryconfig)
    if not commonscatField:
        # Field is missing. Something is seriously wrong, but we just skip it silently
        return False
    
    missingCommonscatPage = countryconfig.get('missingCommonscatPage')
    commonsTrackerCategory = countryconfig.get('commonsTrackerCategory'). replace(u' ', u'_')
	
    withoutCommonscat = getMonumentsWithoutCommonscat(countrycode, lang, conn, cursor)
    commonscats = getMonumentCommonscats(commonsTrackerCategory, conn2, cursor2)

    wikipedia.output(u'withoutCommonscat %s elements' % (len(withoutCommonscat),))
    wikipedia.output(u'commonscats %s elements' % (len(commonscats),))

    text = u'{{#ifexist:{{FULLPAGENAME}}/header | {{/header}} }}\n' # People can add a /header template for with more info
    #text = text + u'<gallery>\n'
    totalCategories = 0
    maxCategories = 1000
    
    for catSortKey in sorted(commonscats.keys()):
        try:
            monumentId = unicode(catSortKey, 'utf-8')
            # Just want the first line
            mLines = monumentId.splitlines()
            monumentId = mLines[0]
            # Remove leading and trailing spaces
            monumentId = monumentId.strip()
            # Remove leading zero's. FIXME: This should be replaced with underscores
            monumentId = monumentId.lstrip(u'0')
            # Remove leading underscors.
            monumentId = monumentId.lstrip(u'_')
	    # All uppercase, same happens in other list. FIXME: Remove this
	    monumentId = monumentId.upper()
            if monumentId in withoutCommonscat:
                m = re.search('^[^\?]+\?title\=(.+?)&', withoutCommonscat.get(monumentId))
                wikiSourceList = m.group(1)
                categoryName = commonscats.get(catSortKey)
                #wikipedia.output(u'Key %s returned a result' % (monumentId,))
                #wikipedia.output(wikiSourceList)
                #wikipedia.output(imageName)
                if totalCategories <= maxCategories:
                    text = text + u'* <nowiki>|</nowiki> %s = [[:Commons:Category:%s|%s]] - %s @ [[%s]]\n' % (commonscatField, unicode(categoryName, 'utf-8'), unicode(categoryName, 'utf-8').replace(u'_', u' '), monumentId, wikiSourceList )
                totalCategories = totalCategories + 1
        except ValueError:
            wikipedia.output(u'Got value error for %s' % (monumentId,))

    #text = text + u'</gallery>' 

    if totalCategories >= maxCategories:
        text = text + u'<!-- Maximum number of categories reached: %s, total of missing commonscat links: %s -->\n' % (maxCategories, totalCategories)
        comment = u'Commonscat links to be made in monument lists: %s (list maximum reached),  total of missing commonscat links: %s' % (maxCategories, totalCategories)
    else:
        comment = u'Commonscat links to be made in monument lists: %s' % totalCategories

    text = text + getInterwikisMissingCommonscatPage(countrycode, lang)
    
    site = wikipedia.getSite(lang, u'wikipedia')
    page = wikipedia.Page(site, missingCommonscatPage)
    wikipedia.output(text)
    page.put(text, comment)

    return totalCategories

def lookupSourceField(destination, countryconfig):
    '''
    Lookup the source field of a destination.
    '''
    for field in countryconfig.get('fields'):
	if field.get('dest')==destination:
	    return field.get('source')

def getInterwikisMissingCommonscatPage(countrycode, lang):
    result = u''
    for (countrycode2, lang2), countryconfig in mconfig.countries.iteritems():
        if countrycode==countrycode2 and lang!=lang2:
            if countryconfig.get('missingCommonscatPage'):
                result = result + u'[[%s:%s]]\n' % (lang2, countryconfig.get('missingCommonscatPage'))

    return result

def getMonumentsWithoutCommonscat(countrycode, lang, conn, cursor):
    result = {}

    query = u"""SELECT id, source FROM monuments_all WHERE (commonscat IS NULL or commonscat='') AND country=%s AND lang=%s""";

    cursor.execute(query, (countrycode, lang))

    while True:
        try:
            row = cursor.fetchone()
            (id, source) = row
	    # To uppercase, same happens in the other list
            result[id.upper()] = source
        except TypeError:
            break

    return result

def getMonumentCommonscats(commonsTrackerCategory, conn, cursor):
    result = {}

    query = u"""SELECT page_title, cl_sortkey FROM page JOIN categorylinks ON page_id=cl_from WHERE page_namespace=14 AND page_is_redirect=0 AND cl_to=%s""";

    cursor.execute(query, (commonsTrackerCategory,))

    while True:
        try:
            row = cursor.fetchone()
            (category, id) = row
            result[id] = category
        except TypeError:
            break

    return result

def makeStatistics(mconfig, totals):
    text = u'{| class="wikitable sortable"\n'
    text = text + u'! country !! lang !! total !! page !! row template !! Commons template\n'
    
    totalCategories = 0
    for ((countrycode, lang), countryconfig) in sorted(mconfig.countries.items()):
        if countryconfig.get('missingCommonscatPage') and countryconfig.get('commonsTemplate'):
            text = text + u'|-\n'
            text = text + u'| %s ' % countrycode
            text = text + u'|| %s ' % lang
            text = text + u'|| %s ' % totals.get((countrycode, lang))
            totalCategories = totalCategories + totals.get((countrycode, lang))
            text = text + u'|| [[:%s:%s|%s]] ' % (lang, countryconfig.get('missingCommonscatPage'), countryconfig.get('missingCommonscatPage'))
            text = text + u'|| [[:%s:Template:%s|%s]] ' % (lang, countryconfig.get('rowTemplate'), countryconfig.get('rowTemplate'))
            text = text + u'|| {{tl|%s}}\n' % countryconfig.get('commonsTemplate')
    text = text + u'|- class="sortbottom"\n'
    text = text + u'| || || %s \n' % totalCategories
    text = text + u'|}\n'
    
    site = wikipedia.getSite('commons', 'commons')
    page = wikipedia.Page(site, u'Commons:Monuments database/Missing commonscat links/Statistics')
    
    comment = u'Updating missing commonscat links statistics. Total missing links: %s' % totalCategories
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
        lang = wikipedia.getSite().language()
	if not mconfig.countries.get((countrycode, lang)):
	    wikipedia.output(u'I have no config for countrycode "%s" in language "%s"' % (countrycode, lang))
	    return False
	wikipedia.output(u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
	processCountry(countrycode, lang, mconfig.countries.get((countrycode, lang)), conn, cursor, conn2, cursor2)
    else:
        totals = {}
	for (countrycode, lang), countryconfig in mconfig.countries.iteritems():
	    wikipedia.output(u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
	    totals[(countrycode, lang)] = processCountry(countrycode, lang, countryconfig, conn, cursor, conn2, cursor2)
	makeStatistics(mconfig, totals)

		
if __name__ == "__main__":
    try:
        main()
    finally:
        wikipedia.stopme()
