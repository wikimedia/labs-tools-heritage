﻿#!/usr/bin/python
# -*- coding: utf-8  -*-
'''

Bot to move images from commonsCategoryBase to subcategories based on the monument template and Commonscat links at the Wikipedia.
First checks if monument article or it's categories have commonscat template,
 if not then checks if monuments list or it's categories have commonscat template.


Usage:
python categorize_images.py -countrycode:ee -wikilang:et -cat:"Cultural heritage monuments in Estonia"

'''
import sys
import monuments_config as mconfig
sys.path.append("/home/project/e/r/f/erfgoed/pywikipedia")
import wikipedia, config, pagegenerators, catlib
import re, imagerecat
import MySQLdb, config

#commonscat templates in different wikipedias
wikiData = {
    ('et') : {
    'commonsCatTemplates' : [u'Commonskat', u'Commonscat', u'Commonsi kategooria']
    }
}

#number of initial categories (categories added by uploadwizard) on image page
INITIAL_CAT_COUNT = 2

def connectDatabase():
    '''
    Connect to the mysql database, if it fails, go down in flames
    '''
    conn = MySQLdb.connect(host=mconfig.db_server, db=mconfig.db, user = config.db_username, passwd = config.db_password, use_unicode=True, charset='utf8')
    cursor = conn.cursor()
    return (conn, cursor)

def categorizeImage(countrycode, lang, commonsTemplate, commonsCategoryBase, commonsCatTemplates, page, conn, cursor):
    wikipedia.output(u'Working on: %s' % page.title())

    currentcats = page.categories()
    if len(currentcats) > INITIAL_CAT_COUNT:
        return False

    templates = page.templates()
    if not commonsTemplate in page.templates():
        wikipedia.output(u'%s template not found at: %s' % (commonsTemplate, page.title()) )
        return False

    monumentId=-1

    for (template, params) in page.templatesWithParams():
        if template==commonsTemplate:
            if len(params)==1:
                try:
                    monumentId = int(params[0])
                except ValueError:
                    wikipedia.output(u'Unable to extract a valid id')
                break
                
    if monumentId < 0:
        return False
    monData = getMonNameSource(countrycode, lang, monumentId, conn, cursor)
    if not monData:
        wikipedia.output(u'Monument with id %s not in monuments database' % (monumentId, ) )
        return False
    (monumentName, monumentSource) = monData
    monumentArticle = getArticle(lang, monumentName)
    newcats = None
    if monumentArticle:
        if monumentArticle.isRedirectPage():
            monumentArticle = monumentArticle.getRedirectTarget()
        newcats = getCategories(monumentArticle, commonsCatTemplates)
    if not newcats:
        monumentList = getList(lang, monumentSource)
        if not monumentList:
            return False
        newcats = getCategories(monumentList, commonsCatTemplates)

    if newcats:
        oldtext = page.get()
        for currentcat in currentcats:
            if not currentcat.titleWithoutNamespace()==commonsCategoryBase:
                newcats.append(currentcat)
        # Remove dupes
        newcats = list(set(newcats))
        newtext = wikipedia.replaceCategoryLinks(oldtext, newcats)

        comment = u'Adding categories based on monument identifier'
        wikipedia.showDiff(oldtext, newtext)
        page.put(newtext, comment)
    else:
        wikipedia.output( u'Categories not found for %s' % page.title() )

def getMonNameSource(countrycode, lang, monumentId, conn, cursor):
    '''
    Get monument name and source from db
    '''
    result = None

    query = u"""SELECT name, source FROM monuments_all WHERE (country=%s AND lang=%s AND id=%s) LIMIT 1""";

    cursor.execute(query, (countrycode, lang, monumentId))
    
    #print cursor._executed
    
    try:
        row = cursor.fetchone()
        return row
    except TypeError:
        return False

def getArticle(lang, monumentName):
    '''
    Get monument article page from wikilink at monumentName
    '''

    if monumentName:
        regex = u'^\[\[(.+?)(\||\])'

        match = re.search(regex, monumentName)
        if not match:
            return False

        page_title= match.group(1)
        site = wikipedia.getSite(lang, u'wikipedia')

        return wikipedia.Page(site, page_title)
    else:
        return False


def getList(lang, monumentSource):
    '''
    Get listpage
    '''

    if monumentSource:
        regex = u'^http://%s.wikipedia.org/w/index.php\?title=(.+)&redirect=' % (lang,)

        match = re.search(regex, monumentSource)
        if not match:
            return False

        page_title= match.group(1)
        site = wikipedia.getSite(lang, u'wikipedia')

        return wikipedia.Page(site, page_title)
    else:
        return False

def getCategories(page, commonsCatTemplates):
    '''
    Get Commons categories based on page.
    1. If page contains a Commonscat template, use that category
    2. Else pull Commonscat links from upper categories
    '''
    result = []
    for commonsCatTemplate in commonsCatTemplates:
        if commonsCatTemplate in page.templates():
            result.append(getCategoryFromCommonscat(page, commonsCatTemplates))
    if not len(result):
        for cat in page.categories():
            for commonsCatTemplate in commonsCatTemplates:
                if commonsCatTemplate in cat.templates():
                    result.append(getCategoryFromCommonscat(cat, commonsCatTemplates))

    return result


def getCategoryFromCommonscat(page, commonsCatTemplates):
    '''
    Get a Commons category based on a page with a Commonscat template
    '''
    
    for (template, params) in page.templatesWithParams():
        if template in commonsCatTemplates:
            if len(params)>=1:
                cat_title = params[0]
                break
            # commonscat template without parameter
            else:
                cat_title = page.titleWithoutNamespace()
                break            
    site = wikipedia.getSite(u'commons', u'commons')
    cat = catlib.Category(site, cat_title)

    return cat

    
def processCountry(countrycode, lang, countryconfig, commonsCatTemplates, conn, cursor):
    '''
    Work on a single country.
    '''
    if not countryconfig.get('commonsTemplate'):
        # No template found, just skip silently.
        return False
    
    if (not commonsCatTemplates):
        # No commonsCatTemplates found, just skip.
        wikipedia.output(u'Language: %s has no commonsCatTemplates set!' % lang)
        return False
    
    wikipedia.setSite(wikipedia.getSite(u'commons', u'commons'))
    generator = None
    genFactory = pagegenerators.GeneratorFactory()
    commonsTemplate = countryconfig.get('commonsTemplate')
    commonsCategoryBase = countryconfig.get('commonsCategoryBase')
    
    for arg in wikipedia.handleArgs():
        genFactory.handleArg(arg)

    generator = genFactory.getCombinedGenerator()

    if generator:
        # Get a preloading generator with only images
        pgenerator = pagegenerators.PreloadingGenerator(pagegenerators.NamespaceFilterPageGenerator(generator, [6]))
        for page in pgenerator:
            categorizeImage(countrycode, lang, commonsTemplate, commonsCategoryBase, commonsCatTemplates, page, conn, cursor)
    
    
def main():

    countrycode = u''
    lang = u''
    conn = None
    cursor = None
    # Connect database, we need that
    (conn, cursor) = connectDatabase()
    
    for arg in wikipedia.handleArgs():
        if arg.startswith('-countrycode:'):
            countrycode = arg [len('-countrycode:'):]
        elif arg.startswith('-wikilang:'):
            lang = arg [len('-wikilang:'):]

    if countrycode:
########        lang = wikipedia.getSite().language()
        if not mconfig.countries.get((countrycode, lang)):
            wikipedia.output(u'I have no config for countrycode "%s" in language "%s"' % (countrycode, lang))
            return False
        wikipedia.output(u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
        commonsCatTemplates = wikiData.get(lang).get('commonsCatTemplates')
        processCountry(countrycode, lang, mconfig.countries.get((countrycode, lang)), commonsCatTemplates, conn, cursor)
    else:
        for (countrycode, lang), countryconfig in mconfig.countries.iteritems():
            wikipedia.output(u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
            commonsCatTemplates = wikiData.get(lang).get('commonsCatTemplates')
            processCountry(countrycode, lang, countryconfig, commonsCatTemplates, conn, cursor)

if __name__ == "__main__":
    try:
        main()
    finally:
        wikipedia.stopme()
