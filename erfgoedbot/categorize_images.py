#!/usr/bin/python
# -*- coding: utf-8  -*-
'''

Bot to move images from commonsCategoryBase to subcategories based on the monument template and Commonscat links at the Wikipedia.
First checks if monument article or it's categories have commonscat template,
 if not then checks if monuments list or it's categories have commonscat template.


Usage:
* To process all:
python categorize_images.py

* Just process one source:
python categorize_images.py -countrycode:ee -lang:et

'''
import sys
import monuments_config as mconfig
sys.path.append("/home/project/e/r/f/erfgoed/pywikipedia")
import wikipedia, config, pagegenerators, catlib
import re, imagerecat
import MySQLdb, config
import commonscat # Contains the commonscat templates for most Wikipedia's


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
    if not commonsCategoryBase in currentcats:
        wikipedia.output(u'%s category not found at: %s. Someone probably already categorized it.' % (commonsCategoryBase, page.title()) )
        return False
    
    if u'Wikipedia image placeholders for cultural heritage monuments' in currentcats:
        wikipedia.output(u'%s in %s is a placeholder, skipping it.' % (page.title(), commonsCategoryBase ) )

    templates = page.templates()
    if not commonsTemplate in templates:
        wikipedia.output(u'%s template not found at: %s' % (commonsTemplate, page.title()) )
        return False

    monumentId = None

    for (template, params) in page.templatesWithParams():
        if template==commonsTemplate:
            if len(params)>=1:
                try:
                    monumentId = params[0]
                except ValueError:
                    wikipedia.output(u'Unable to extract a valid id')
                break

    # No valid id found, skip the image            
    if not monumentId:
	wikipedia.output(u'Didn\'t find a valid monument identifier')
        return False
 
    monData = getMonData(countrycode, lang, monumentId, conn, cursor)
    if not monData:
	try:
	    monumentId = int(monumentId)
	    monData = getMonData(countrycode, lang, monumentId, conn, cursor)
	except ValueError:
	    wikipedia.output(u'Can\'t convert %s to an integer' % (monumentId,))

    if not monData:
        wikipedia.output(u'Monument with id %s not in monuments database' % (monumentId, ) )
        return False
    
    (monumentName, monumentCommonscat, monumentArticleTitle, monumentSource) = monData

    newcats = []

    # First try to add a category based on the commonscat field in the list
    if monumentCommonscat:
        # Might want to include some error checking here
        site = wikipedia.getSite(u'commons', u'commons')
	try:
	    cat = catlib.Category(site, monumentCommonscat)
	    newcats.append(cat)
	except ValueError:
	    wikipedia.output(u'The Commonscat field for %s contains an invalid category %s' % (monumentId, monumentCommonscat))

    # Option two is to use the article about the monument and see if it has Commonscat links    
    if not newcats:
        monumentArticle = None
        if monumentArticleTitle:
            site = wikipedia.getSite(lang, u'wikipedia')
            monumentArticle = wikipedia.Page(site, monumentArticleTitle)
    
    
        if monumentArticle:
            if monumentArticle.isRedirectPage():
                monumentArticle = monumentArticle.getRedirectTarget()
            try:
                for commonsCatTemplate in commonsCatTemplates:
                    if commonsCatTemplate in monumentArticle.templates():
                        newcats = []
                        newcats.append(getCategoryFromCommonscat(monumentArticle, commonsCatTemplates))
            except wikipedia.exceptions.SectionError:
               wikipedia.output(u'Incorrect redirect at %s' % (monumentArticle.title(),))

    # Option three is to see if the list contains Commonscat links (whole list)
    if not newcats:
        monumentList = getList(lang, monumentSource)
	#print monumentList
        if not monumentList:
            return False
        if monumentList.isRedirectPage():
	    monumentList = monumentList.getRedirectTarget()
        newcats = getCategories(monumentList, commonsCatTemplates)

    # See if one of the three options worked
    if newcats:
        oldtext = page.get()
        for currentcat in currentcats:
            if not currentcat.titleWithoutNamespace()==commonsCategoryBase.titleWithoutNamespace():
                newcats.append(currentcat)
        # Remove dupes
        newcats = list(set(newcats))
	if not set(currentcats) == set(newcats):
	    newtext = wikipedia.replaceCategoryLinks(oldtext, newcats)

	    comment = u'Adding categories based on [[Template:%s]] with identifier %s' % (commonsTemplate, monumentId)
	    wikipedia.showDiff(oldtext, newtext)
	    try:
		page.put(newtext, comment)
		return True
	    except wikipedia.exceptions.EditConflict:
		wikipedia.output( u'Got an edit conflict. Someone else beat me to it at %s' % page.title() )
    else:
        wikipedia.output( u'Categories not found for %s' % page.title() )

def getMonData(countrycode, lang, monumentId, conn, cursor):
    '''
    Get monument name and source from db
    '''
    query = u"""SELECT `name`, `commonscat`, `monument_article`, `source` FROM monuments_all WHERE (country=%s AND lang=%s AND id=%s) LIMIT 1""";

    cursor.execute(query, (countrycode, lang, monumentId))
    
    try:
        row = cursor.fetchone()
        return row
    except TypeError:
	wikipedia.output(u'Didn\'t find anything for id %s' % (monumentId,))
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
        regex = u'^https://%s.wikipedia.org/w/index.php\?title=(.+)&redirect=' % (lang,)

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
	#print page.categories()
        for cat in page.categories():
	    #print cat
            for commonsCatTemplate in commonsCatTemplates:
		#print commonsCatTemplate
                if commonsCatTemplate in cat.templates():
		    #print u'hit!'
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

    
def processCountry(countrycode, lang, countryconfig, commonsCatTemplates, conn, cursor, overridecat=None):
    '''
    Work on a single country.
    '''
    if not countryconfig.get('commonsTemplate'):
        # No template found, just skip silently.
	basecat = u''
	if countryconfig.get('commonsCategoryBase'):
	    basecat = countryconfig.get('commonsCategoryBase')
	return (countrycode, lang, basecat, 0, 0, 0)
    
    if (not commonsCatTemplates):
        # No commonsCatTemplates found, just skip.
        wikipedia.output(u'Language: %s has no commonsCatTemplates set!' % lang)
        return False
    
    totalImages = 0
    categorizedImages = 0

    site = wikipedia.getSite(u'commons', u'commons')
    generator = None
    genFactory = pagegenerators.GeneratorFactory()
    commonsTemplate = countryconfig.get('commonsTemplate')
 
    if overridecat:
	commonsCategoryBase = catlib.Category(site, "%s:%s" % (site.namespace(14), overridecat))
    else:
        commonsCategoryBase = catlib.Category(site, "%s:%s" % (site.namespace(14), countryconfig.get('commonsCategoryBase')))

    generator = pagegenerators.CategorizedPageGenerator(commonsCategoryBase)
    
    # Get a preloading generator with only images
    pgenerator = pagegenerators.PreloadingGenerator(pagegenerators.NamespaceFilterPageGenerator(generator, [6]))
    for page in pgenerator:
	totalImages = totalImages + 1
	success = False
	if not totalImages >= 10000:
            success = categorizeImage(countrycode, lang, commonsTemplate, commonsCategoryBase, commonsCatTemplates, page, conn, cursor)
	if success:
	    categorizedImages = categorizedImages + 1

    return (countrycode, lang, commonsCategoryBase.titleWithoutNamespace(), commonsTemplate, totalImages, categorizedImages)

def outputStatistics(statistics):
    '''
    Output the results of the bot as a nice wikitable
    '''
    output = u'{| class="wikitable sortable"\n'
    output = output + u'! country !! [[:en:List of ISO 639-1 codes|lang]] !! Base category !! Template !! Total images !! Categorized images !! Images left !! Current image count\n'

    totalImages = 0
    categorizedImages = 0
    leftoverImages = 0

    for row in statistics:
        output = output + u'|-\n'
	output = output + u'|| %s \n' % (row[0],)
	output = output + u'|| %s \n' % (row[1],)
	output = output + u'|| [[:Category:%s]] \n' % (row[2],)
	output = output + u'|| {{tl|%s}} \n' % (row[3],)
	
	totalImages = totalImages + row[4]
	output = output + u'|| %s \n' % (row[4],)

	categorizedImages = categorizedImages + row[5]
	output = output + u'|| %s \n' % (row[5],)

	leftover = row[4] - row[5]
	leftoverImages = leftoverImages + leftover

	output = output + u'|| %s \n' % (leftover,)
	output = output + u'|| {{PAGESINCATEGORY:%s|files}} \n' % (row[2],)

    output = output + u'|- class="sortbottom"\n'
    output = output + u'||\n||\n||\n||\n|| %s \n|| %s \n|| %s || \n' % (totalImages, categorizedImages, leftoverImages)
    output = output + u'|}\n'

    site = wikipedia.getSite('commons', 'commons')
    page = wikipedia.Page(site, u'Commons:Monuments database/Categorization/Statistics')

    comment = u'Updating categorization statistics. Total: %s Categorized: %s Leftover: %s' % (totalImages, categorizedImages, leftoverImages)
    page.put(newtext = output, comment = comment)

def getCommonscatTemplates(lang=None):
    '''Get the template name in a language. Expects the language code.
    Return as tuple containing the primary template and it's alternatives

    '''
    result = []
    if lang in commonscat.commonscatTemplates:
        (prim, backups) = commonscat.commonscatTemplates[lang]
    else:
        (prim, backups) = commonscat.commonscatTemplates[u'_default']
    result.append(prim)
    result = result + backups
    return result

    
def main():

    countrycode = u''
    overridecat = u''
    lang = u''
    conn = None
    cursor = None
    # Connect database, we need that
    (conn, cursor) = connectDatabase()
    
    for arg in wikipedia.handleArgs():
        if arg.startswith('-countrycode:'):
            countrycode = arg [len('-countrycode:'):]
	elif arg.startswith('-overridecat:'):
	    overridecat = arg [len('-overridecat:'):]

    if countrycode:
        lang = wikipedia.getSite().language()
        if not mconfig.countries.get((countrycode, lang)):
            wikipedia.output(u'I have no config for countrycode "%s" in language "%s"' % (countrycode, lang))
            return False
        wikipedia.output(u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
        commonsCatTemplates = getCommonscatTemplates(lang)
	#print commonsCatTemplates
        processCountry(countrycode, lang, mconfig.countries.get((countrycode, lang)), commonsCatTemplates, conn, cursor, overridecat=overridecat)
    else:
	statistics = []
        for (countrycode, lang), countryconfig in mconfig.countries.iteritems():
            wikipedia.output(u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
            commonsCatTemplates = getCommonscatTemplates(lang)
            result = processCountry(countrycode, lang, countryconfig, commonsCatTemplates, conn, cursor)
	    if result:
	        statistics.append(result)

        outputStatistics(statistics)

if __name__ == "__main__":
    try:
        main()
    finally:
        wikipedia.stopme()
