#!/usr/bin/python
# -*- coding: utf-8  -*-
'''

get coordinates from the Monuments database and
    add coordinate template to articles in Wikipedia

@author Kentaur
    
Usage:
# loop through all countries
python add_coord_to_articles.py

# work on specific country-lang
python add_coord_to_articles.py -countrycode:XX -lang:YY    

'''

import sys, os
import monuments_config as mconfig
sys.path.append("/home/project/e/r/f/erfgoed/pywikipedia")
import wikipedia
import re, MySQLdb, time

#coordinate templates for different language wikipedias
wikiData = {
    ('et') : {
	'coordTemplate' : 'Coordinate',
    #coordTemplateSyntax % (lat, lon, countrycode.upper() )
    'coordTemplateSyntax' : u'{{Coordinate|NS=%f|EW=%f|type=landmark|region=%s}}'
    },
    ('fr') : {
	'coordTemplate' : 'coord',
    #{{coord|52.51626|13.3777|type:landmark_region:DE|format=dms|display=title}}
    'coordTemplateSyntax' : u'{{coord|%f|%f|type:landmark_region=%s|format=dms|display=title}}'
    }
}

# "constants"
# wikipedia article namespace
WP_ARTICLE_NS = 0
# wikipedia category namespace
WP_CATEGORY_NS = 14
# output debug messages
DEBUG = True


# functions

def connectMonDatabase():
    '''
    Connect to the monuments mysql database
    '''
    conn = MySQLdb.connect(host=mconfig.db_server, db=mconfig.db,
        read_default_file=os.path.expanduser("~/.my.cnf"), 
        use_unicode=True, charset='utf8')
    cursor = conn.cursor()
    return (conn, cursor)

def connectWikiDatabase(lang):
    '''
    Connect to the wiki database
    '''
    if (lang):
        hostName = lang + 'wiki-p.db.toolserver.org'
        dbName = lang + 'wiki_p'
        #coordDbName = 'u_dispenser_p'
        conn = MySQLdb.connect(host=hostName, db=dbName,
            read_default_file=os.path.expanduser("~/.my.cnf"), 
            use_unicode=True, charset='utf8')
        cursor = conn.cursor()
        return (conn, cursor)

def processCountry(countrycode, lang, countryconfig, coordconfig, connMon, cursorMon):
    '''
    Work on a single country.
    '''
    if (not coordconfig or not coordconfig.get('coordTemplate')):
        # No template found, just skip.
        wikipedia.output(u'Language %s has no coordTemplate set!' % lang)
        return False

    (connWiki, cursorWiki) = connectWikiDatabase(lang)
    
    withCoordinates = getMonumentsWithCoordinates(countrycode, lang, cursorMon)

    articleNames = []
    duplicateArticles = []
    lat = {}
    lon = {}
    
    
    for (mon_name, mon_lat, mon_lon) in withCoordinates:
        article_name = u''
        result = re.match("\[\[(.+?)\|.+?\]\]", mon_name)
        if (result and result.group(1)): 
            article_name = result.group(1)
            lat[article_name] = mon_lat
            lon[article_name] = mon_lon

        result = re.match("\[\[([^\|]+?)\]\]", mon_name)
        if (result and result.group(1)): 
            article_name = result.group(1)
            lat[article_name] = mon_lat
            lon[article_name] = mon_lon
        
        if (article_name):
            if article_name not in duplicateArticles:
                if article_name in articleNames:
                    duplicateArticles.append(article_name)
                    articleNames.remove(article_name)
                else:
                    articleNames.append(article_name)
    
    if len(duplicateArticles):
        wikipedia.output(u'Multiple references to following articles: %s in monument lists! Skipped those.' % duplicateArticles[:])
    
    for article in articleNames:
        PageNs = WP_ARTICLE_NS
        followRedirect = True  
        (retStatus, pageId, redirNs, redirTitle) = getPageId(article, connWiki, cursorWiki, PageNs, followRedirect)
        if (retStatus == 'FOLLOWED_REDIR' and redirNs == WP_ARTICLE_NS):
            lat[redirTitle] = lat[article]
            lon[redirTitle] = lon[article]
            article = redirTitle
        if (pageId):
            if not hasCoordinates(pageId, lang, cursorWiki):
                addCoords(countrycode, lang, article, lat[article], lon[article], coordconfig)
        


def getMonumentsWithCoordinates(countrycode, lang, cursor):
    '''
    Get monuments with coordinates from monuments database for a certain country/language combination.
    '''
    result = {}
    query = """SELECT name, lat, lon FROM monuments_all 
                   WHERE lat<>0 AND lon<>0 AND country=%s AND lang=%s"""
    cursor.execute(query, (countrycode, lang))

    result = cursor.fetchall ()

    return result

def hasCoordinates(pageId, lang, cursor):
    '''
    check if Article has Article coords in WP coords DB
    '''
    
    if (pageId and lang):
        coordTable = 'u_dispenser_p.coord_' + lang + 'wiki'

        # check if primary coordinate i.e. article coordinate exists for pageId
        query = """SELECT gc_from FROM %s
                      WHERE gc_from = %s AND gc_primary = 1""" 
        # FIXME escape & sanitize coordTable and pageId
        cursor.execute(query % (coordTable, int(pageId) ))

        if (cursor.rowcount > 0):
            return True
        else:
            return False
    else:
        return False

def getPageId(pageName, conn, cursor, pageNamespace = WP_ARTICLE_NS, followRedirect = False):
    '''
    get Wikipedia pagename pageId
    '''
    
    #underscores
    pageName = pageName.replace(u' ', u'_')
    retStatus = ''
    pageId = ''
    redirNs = ''
    redirTitle = u''

    query = """SELECT page_id, page_is_redirect FROM page 
                   WHERE page_namespace = %s AND page_title = %s"""
    cursor.execute(query, (pageNamespace, pageName))
    if DEBUG:
        print cursor._executed
        print u'rowcount: %d ' % cursor.rowcount

    if (cursor.rowcount > 0):
        row = cursor.fetchone()
        (pageId, IsRedirect) = row
        if (IsRedirect):
            if (followRedirect):
                (redirNs, redirTitle) = getRedirPageNsTitle(pageId, cursor)
                redirTitle = unicode(redirTitle, "utf-8")
                (retStatus, pageId, dummy1, dummy2) = getPageId(redirTitle, conn, cursor, redirNs)
                retStatus = 'FOLLOWED_REDIR'
            else:
                retStatus = 'REDIRECT'
        else:
            retStatus = 'OK'
    
    return (retStatus, pageId, redirNs, redirTitle)

def getRedirPageNsTitle(pageId, cursor):
    '''
    Get redirect page namespace and title.
    '''

    pageNs = ''
    pageTitle = u''
    
    query = """SELECT rd_namespace, rd_title FROM redirect
                WHERE rd_from = %s"""
    cursor.execute(query, (pageId,))

    if (cursor.rowcount > 0):
        row = cursor.fetchone()
        (pageNs, pageTitle) = row
    
    return (pageNs, pageTitle)
    
    
def addCoords(countrycode, lang, article, lat, lon, coordconfig):
    '''
    Add the coordinates to article.
    '''

    coordTemplate = coordconfig.get('coordTemplate')
    coordTemplateSyntax = coordconfig.get('coordTemplateSyntax')
    site = wikipedia.getSite(lang, 'wikipedia')

    page = wikipedia.Page(site, article)
    try:
        text = page.get()
    except wikipedia.NoPage: # First except, prevent empty pages
        return False
    except wikipedia.IsRedirectPage: # second except, prevent redirect
        wikipedia.output(u'%s is a redirect!' % article)
        return False
    except wikipedia.Error: # third exception, take the problem and print
        wikipedia.output(u"Some error, skipping..")
        return False       
    
    if coordTemplate in page.templates():
        return False

    newtext = text
    replCount = 1
    coordText = coordTemplateSyntax % (lat, lon, countrycode.upper() )
    localCatName = wikipedia.getSite().namespace(WP_CATEGORY_NS)
    catStart = r'\[\[(' + localCatName + '|Category):'
    catStartPlain = u'[[' + localCatName + ':'
    replacementText = u''
    replacementText = coordText + '\n\n' + catStartPlain
    
    # insert coordinate template before categories
    newtext = re.sub(catStart, replacementText, newtext, replCount, flags=re.IGNORECASE)

    if text != newtext:
        comment = u'Adding template %s based on data from monuments list' % (coordTemplate,)
        wikipedia.showDiff(text, newtext)
        page.put(newtext, comment)
        return True
    else:
        return False
    
    
def main():
    countrycode = u''
    connMon = None
    cursorMon = None

    (connMon, cursorMon) = connectMonDatabase()
    
    for arg in wikipedia.handleArgs():
        if arg.startswith('-countrycode:'):
            countrycode = arg [len('-countrycode:'):]

    if countrycode:
        lang = wikipedia.getSite().language()
	if not mconfig.countries.get((countrycode, lang)):
	    wikipedia.output(u'I have no config for countrycode "%s" in language "%s"' % (countrycode, lang))
	    return False
	wikipedia.output(u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
	processCountry(countrycode, lang, mconfig.countries.get((countrycode, lang)), wikiData.get(lang), connMon, cursorMon)
    else:
	for (countrycode, lang), countryconfig in mconfig.countries.iteritems():
	    wikipedia.output(u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
	    processCountry(countrycode, lang, countryconfig, wikiData.get(lang), connMon, cursorMon)


if __name__ == "__main__":
    try:
        main()
    finally:
        wikipedia.stopme()
