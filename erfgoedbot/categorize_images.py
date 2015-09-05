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
import monuments_config as mconfig
import pywikibot
from pywikibot import config
from pywikibot import pagegenerators
import re
import MySQLdb


class NoCommonsCatFromWikidataItemException(pywikibot.exceptions.PageRelatedError):
    pass

# Contains the commonscat templates for most Wikipedia's (taken from ex-commonscat.py)
commonscatTemplates = {
    '_default': (u'Commonscat', []),
    'af': (u'CommonsKategorie', [u'commonscat']),
    'an': (u'Commonscat', [u'Commons cat']),
    'ar': (u'تصنيف كومنز',
           [u'Commonscat', u'تصنيف كومونز', u'Commons cat', u'CommonsCat']),
    'arz': (u'Commons cat', [u'Commoncat']),
    'az': (u'CommonsKat', [u'Commonscat']),
    'bn': (u'কমন্সক্যাট', [u'Commonscat']),
    'ca': (u'Commonscat', [u'Commons cat', u'Commons category']),
    'crh': (u'CommonsKat', [u'Commonscat']),
    'cs': (u'Commonscat', [u'Commons cat']),
    'da': (u'Commonscat',
           [u'Commons cat', u'Commons category', u'Commonscat left',
            u'Commonscat2']),
    'en': (u'Commons category',
           [u'Commoncat', u'Commonscat', u'Commons cat', u'Commons+cat',
            u'Commonscategory', u'Commons and category', u'Commonscat-inline',
            u'Commons category-inline', u'Commons2', u'Commons category multi',
            u'Cms-catlist-up', u'Catlst commons', u'Commonscat show2',
            u'Sister project links']),
    'es': (u'Commonscat',
           [u'Ccat', u'Commons cat', u'Categoría Commons',
            u'Commonscat-inline']),
    'et': (u'Commonsi kategooria',
           [u'Commonscat', u'Commonskat', u'Commons cat', u'Commons category']),
    'eu': (u'Commonskat', [u'Commonscat']),
    'fa': (u'ویکی‌انبار-رده',
           [u'Commonscat', u'Commons cat', u'انبار رده', u'Commons category',
            u'انبار-رده', u'جعبه پیوند به پروژه‌های خواهر',
            u'در پروژه‌های خواهر', u'پروژه‌های خواهر']),
    'fr': (u'Commonscat', [u'CommonsCat', u'Commons cat', u'Commons category']),
    'frp': (u'Commonscat', [u'CommonsCat']),
    'ga': (u'Catcómhaoin', [u'Commonscat']),
    'he': (u'ויקישיתוף בשורה', []),
    'hi': (u'Commonscat', [u'Commons2', u'Commons cat', u'Commons category']),
    'hu': (u'Commonskat', [u'Közvagyonkat']),
    'hy': (u'Վիքիպահեստ կատեգորիա',
           [u'Commonscat', u'Commons cat', u'Commons category']),
    'id': (u'Commonscat',
           [u'Commons cat', u'Commons2', u'CommonsCat', u'Commons category']),
    'is': (u'CommonsCat', [u'Commonscat']),
    'ja': (u'Commonscat', [u'Commons cat', u'Commons category']),
    'jv': (u'Commonscat', [u'Commons cat']),
    'kaa': (u'Commons cat', [u'Commonscat']),
    'kk': (u'Commonscat', [u'Commons2']),
    'ko': (u'Commonscat', [u'Commons cat', u'공용분류']),
    'la': (u'CommuniaCat', []),
    'mk': (u'Ризница-врска',
           [u'Commonscat', u'Commons cat', u'CommonsCat', u'Commons2',
            u'Commons category']),
    'ml': (u'Commonscat', [u'Commons cat', u'Commons2']),
    'ms': (u'Kategori Commons', [u'Commonscat', u'Commons category']),
    'nn': (u'Commonscat', [u'Commons cat']),
    'os': (u'Commonscat', [u'Commons cat']),
    'pt': (u'Commonscat', [u'Commons cat']),
    'ro': (u'Commonscat', [u'Commons cat']),
    'ru': (u'Commonscat', [u'Викисклад-кат', u'Commons category']),
    'simple': (u'Commonscat',
               [u'Commons cat', u'Commons cat multi', u'Commons category',
                u'Commons category multi', u'CommonsCompact',
                u'Commons-inline']),
    'sh': (u'Commonscat', [u'Commons cat']),
    'sl': (u'Kategorija v Zbirki',
           [u'Commonscat', u'Kategorija v zbirki', u'Commons cat',
            u'Katzbirke']),
    'sv': (u'Commonscat',
           [u'Commonscat-rad', u'Commonskat', u'Commons cat', u'Commonscatbox',
            u'Commonscat-box']),
    'sw': (u'Commonscat', [u'Commons2', u'Commons cat']),
    'te': (u'Commonscat', [u'Commons cat']),
    'tr': (u'Commons kategori',
           [u'CommonsKat', u'Commonscat', u'Commons cat']),
    'uk': (u'Commonscat', [u'Commons cat', u'Category', u'Commonscat-inline']),
    'vi': (u'Commonscat',
           [u'Commons2', u'Commons cat', u'Commons category', u'Commons+cat']),
    'zh': (u'Commonscat', [u'Commons cat', u'Commons category']),
    'zh-classical': (u'共享類', [u'Commonscat']),
    'zh-yue': (u'同享類',
               [u'Commonscat', u'共享類 ', u'Commons cat', u'Commons category']),
}

ignoreTemplates = {
    'af': [u'commons'],
    'ar': [u'تحويلة تصنيف', u'كومنز', u'كومونز', u'Commons'],
    'be-x-old': [u'Commons', u'Commons category'],
    'cs': [u'Commons', u'Sestřičky', u'Sisterlinks'],
    'da': [u'Commons', u'Commons left', u'Commons2', u'Commonsbilleder',
           u'Commonskat', u'Commonscat2', u'GalleriCommons', u'Søsterlinks'],
    'de': [u'Commons', u'ZhSZV', u'Bauwerk-stil-kategorien',
           u'Bauwerk-funktion-kategorien', u'KsPuB',
           u'Kategoriesystem Augsburg-Infoleiste',
           u'Kategorie Ge', u'Kategorie v. Chr. Ge',
           u'Kategorie Geboren nach Jh. v. Chr.', u'Kategorie Geboren nach Jh.',
           u'!Kategorie Gestorben nach Jh. v. Chr.',
           u'!Kategorie Gestorben nach Jh.',
           u'Kategorie Jahr', u'Kategorie Jahr v. Chr.',
           u'Kategorie Jahrzehnt', u'Kategorie Jahrzehnt v. Chr.',
           u'Kategorie Jahrhundert', u'Kategorie Jahrhundert v. Chr.',
           u'Kategorie Jahrtausend', u'Kategorie Jahrtausend v. Chr.'],
    'en': [u'Category redirect', u'Commons', u'Commonscat1A', u'Commoncats',
           u'Commonscat4Ra',
           u'Sisterlinks', u'Sisterlinkswp', u'Sister project links',
           u'Tracking category', u'Template category', u'Wikipedia category'],
    'eo': [u'Commons',
           (u'Projekto/box', 'commons='),
           (u'Projekto', 'commons='),
           (u'Projektoj', 'commons='),
           (u'Projektoj', 'commonscat=')],
    'es': [u'Commons', u'IprCommonscat'],
    'eu': [u'Commons'],
    'fa': [u'Commons', u'ویکی‌انبار', u'Category redirect', u'رده بهتر',
           u'جعبه پیوند به پروژه‌های خواهر', u'در پروژه‌های خواهر',
           u'پروژه‌های خواهر'],
    'fi': [u'Commonscat-rivi', u'Commons-rivi', u'Commons'],
    'fr': [u'Commons', u'Commons-inline', (u'Autres projets', 'commons=')],
    'fy': [u'Commons', u'CommonsLyts'],
    'he': [u'מיזמים'],
    'hr': [u'Commons', (u'WProjekti', 'commonscat=')],
    'is': [u'Systurverkefni', u'Commons'],
    'it': [(u'Ip', 'commons='), (u'Interprogetto', 'commons=')],
    'ja': [u'CommonscatS', u'SisterlinksN', u'Interwikicat'],
    'ms': [u'Commons', u'Sisterlinks', u'Commons cat show2'],
    'nds-nl': [u'Commons'],
    'nl': [u'Commons', u'Commonsklein', u'Commonscatklein', u'Catbeg',
           u'Catsjab', u'Catwiki'],
    'om': [u'Commons'],
    'pt': [u'Correlatos',
           u'Commons',
           u'Commons cat multi',
           u'Commons1',
           u'Commons2'],
    'simple': [u'Sisterlinks'],
    'ru': [u'Навигация', u'Навигация для категорий', u'КПР', u'КБР',
           u'Годы в России', u'commonscat-inline'],
    'tt': [u'Навигация'],
    'zh': [u'Category redirect', u'cr', u'Commons',
           u'Sisterlinks', u'Sisterlinkswp',
           u'Tracking category', u'Trackingcatu',
           u'Template category', u'Wikipedia category'
           u'分类重定向', u'追蹤分類', u'共享資源', u'追蹤分類'],
}


def connectDatabase():
    '''
    Connect to the mysql database, if it fails, go down in flames
    '''
    conn = MySQLdb.connect(host=mconfig.db_server, db=mconfig.db, user=config.db_username,
                           passwd=config.db_password, use_unicode=True, charset='utf8')
    cursor = conn.cursor()
    return (conn, cursor)


def categorizeImage(countrycode, lang, commonsTemplateName, commonsCategoryBase, commonsCatTemplates, page, conn, cursor):
    pywikibot.output(u'Working on: %s' % page.title())
    site = pywikibot.Site(u'commons', u'commons')
    commonsTemplate = pywikibot.Page(site, 'Template:%s' % commonsTemplateName)
    currentcats = list(page.categories())
    if commonsCategoryBase not in currentcats:
        pywikibot.output(u'%s category not found at: %s. Someone probably already categorized it.' % (
            commonsCategoryBase, page.title()))
        return False

    if u'Wikipedia image placeholders for cultural heritage monuments' in currentcats:
        pywikibot.output(u'%s in %s is a placeholder, skipping it.' % (
            page.title(), commonsCategoryBase))

    templates = page.templates()
    if commonsTemplate not in templates:
        pywikibot.output(u'%s template not found at: %s' %
                         (commonsTemplate, page.title()))
        return False

    monumentId = None

    for (template, params) in page.templatesWithParams():
        if template == commonsTemplate:
            if len(params) >= 1:
                try:
                    monumentId = params[0]
                except ValueError:
                    pywikibot.output(u'Unable to extract a valid id')
                break

    # No valid id found, skip the image
    if not monumentId:
        pywikibot.output(u'Didn\'t find a valid monument identifier')
        return False

    monData = getMonData(countrycode, lang, monumentId, conn, cursor)
    if not monData:
        try:
            monumentId = int(monumentId)
            monData = getMonData(countrycode, lang, monumentId, conn, cursor)
        except ValueError:
            pywikibot.output(
                u'Can\'t convert %s to an integer' % (monumentId,))

    if not monData:
        pywikibot.output(
            u'Monument with id %s not in monuments database' % (monumentId, ))
        return False

    newcats = get_new_categories(monumentId, monData, lang, commonsCatTemplates)

    # See if one of the three options worked
    if newcats:
        oldtext = page.get()
        for currentcat in currentcats:
            if not currentcat.title(withNamespace=False) == commonsCategoryBase.title(withNamespace=False):
                if currentcat.title(withNamespace=False) in oldtext:
                    newcats.append(currentcat)

        # Remove dupes
        newcats = list(set(newcats))
        if not set(currentcats) == set(newcats):
            newtext = pywikibot.replaceCategoryLinks(oldtext, newcats)

            comment = u'Adding categories based on [[Template:%s]] with identifier %s' % (
                commonsTemplateName, monumentId)
            pywikibot.showDiff(oldtext, newtext)
            try:
                page.put(newtext, comment)
                return True
            except pywikibot.EditConflict:
                pywikibot.output(
                    u'Got an edit conflict. Someone else beat me to it at %s' % page.title())
    else:
        pywikibot.output(u'Categories not found for %s' % page.title())


def get_new_categories(monumentId, monData, lang, commonsCatTemplates):
    (monumentName, monumentCommonscat,
     monumentArticleTitle, monumentSource) = monData
    newcats = []
    # First try to add a category based on the commonscat field in the list
    if monumentCommonscat:
        # Might want to include some error checking here
        site = pywikibot.Site(u'commons', u'commons')
        try:
            cat = pywikibot.Category(site, monumentCommonscat)
            newcats.append(cat)
        except ValueError:
            pywikibot.output(u'The Commonscat field for %s contains an invalid category %s' % (
                monumentId, monumentCommonscat))

    # Option two is to use the article about the monument and see if it has
    # Commonscat links
    if not newcats:
        monumentArticle = None
        if monumentArticleTitle:
            site = pywikibot.Site(lang, u'wikipedia')
            monumentArticle = pywikibot.Page(site, monumentArticleTitle)

        if monumentArticle:
            if monumentArticle.isRedirectPage():
                monumentArticle = monumentArticle.getRedirectTarget()
            try:
                for commonsCatTemplateName in commonsCatTemplates:
                    commonsCatTemplate = pywikibot.Page(site, 'Template:%s' % commonsCatTemplateName)
                    if commonsCatTemplate in monumentArticle.templates():
                        newcats = []
                        newcats.append(
                            getCategoryFromCommonscat(monumentArticle, commonsCatTemplates))
            except pywikibot.SectionError:
                pywikibot.output(u'Incorrect redirect at %s' %
                                 (monumentArticle.title(),))

    # Option three is to see if the list contains Commonscat links (whole list)
    if not newcats:
        monumentList = getList(lang, monumentSource)
        # print monumentList
        if not monumentList:
            return False
        if monumentList.isRedirectPage():
            monumentList = monumentList.getRedirectTarget()
        newcats = getCategories(monumentList, commonsCatTemplates)


def getMonData(countrycode, lang, monumentId, conn, cursor):
    '''
    Get monument name and source from db
    '''
    query = u"""SELECT `name`, `commonscat`, `monument_article`, `source` FROM monuments_all WHERE (country=%s AND lang=%s AND id=%s) LIMIT 1"""

    cursor.execute(query, (countrycode, lang, monumentId))

    try:
        row = cursor.fetchone()
        return row
    except TypeError:
        pywikibot.output(u'Didn\'t find anything for id %s' % (monumentId,))
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

        page_title = match.group(1)
        site = pywikibot.Site(lang, u'wikipedia')

        return pywikibot.Page(site, page_title)
    else:
        return False


def getList(lang, monumentSource):
    '''
    Get listpage
    '''

    if monumentSource:
        regex = u'^https://%s.wikipedia.org/w/index.php\?title=(.+)&redirect=' % (
            lang,)

        match = re.search(regex, monumentSource)
        if not match:
            return False

        page_title = match.group(1)
        site = pywikibot.Site(lang, u'wikipedia')

        return pywikibot.Page(site, page_title)
    else:
        return False


def getCategories(page, commonsCatTemplates):
    '''
    Get Commons categories based on page.
    1. If page contains a Commonscat template, use that category
    2. Else pull Commonscat links from upper categories
    '''
    result = []
    for commonsCatTemplateName in commonsCatTemplates:
        commonsCatTemplate = pywikibot.Page(page.site, 'Template:%s' % commonsCatTemplateName)
        if commonsCatTemplate in page.templates():
            result.append(getCategoryFromCommonscat(page, commonsCatTemplates))
    if not len(result):
        # print page.categories()
        for cat in page.categories():
            # print cat
            for commonsCatTemplateName in commonsCatTemplates:
                commonsCatTemplate = pywikibot.Page(page.site, 'Template:%s' % commonsCatTemplateName)
                # print commonsCatTemplate
                if commonsCatTemplate in cat.templates():
                    # print u'hit!'
                    result.append(
                        getCategoryFromCommonscat(cat, commonsCatTemplates))

    return result


def getCategoryFromCommonscat(page, commonsCatTemplates):
    '''
    Get a Commons category based on a page with a Commonscat template
    '''
    for (template, params) in page.templatesWithParams():
        if template.title(withNamespace=False) in commonsCatTemplates:
            if len(params) >= 1:
                cat_title = params[0]
            # commonscat template without parameter
            else:
                # That may be inferred from Wikidata
                try:
                    cat_title = get_Commons_category_via_Wikidata(page)
                except NoCommonsCatFromWikidataItemException:
                    cat_title = page.title(withNamespace=False)
            break
    site = pywikibot.Site(u'commons', u'commons')
    cat = pywikibot.Category(site, cat_title)
    return cat


def get_Commons_category_via_Wikidata(page):
    '''
    Get Commons Category from the linked Wikidata item and P373.

    Raises: NoCommonsCatFromWikidataItemException if either there is no linked item
            or it does not bear P373
    '''
    try:
        data_item = page.data_item()
        claims = data_item.get()['claims']
        return claims['P373'][0].getTarget()
    except (pywikibot.NoPage, KeyError):
        raise NoCommonsCatFromWikidataItemException(page)


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
        pywikibot.output(
            u'Language: %s has no commonsCatTemplates set!' % lang)
        return False

    totalImages = 0
    categorizedImages = 0

    site = pywikibot.Site(u'commons', u'commons')
    generator = None
    genFactory = pagegenerators.GeneratorFactory()
    commonsTemplate = countryconfig.get('commonsTemplate')

    if overridecat:
        commonsCategoryBase = pywikibot.Category(site, "%s:%s" % (site.namespace(14), overridecat))
    else:
        commonsCategoryBase = pywikibot.Category(site, "%s:%s" % (site.namespace(14), countryconfig.get('commonsCategoryBase')))

    generator = pagegenerators.CategorizedPageGenerator(commonsCategoryBase)

    # Get a preloading generator with only images
    pgenerator = pagegenerators.PreloadingGenerator(
        pagegenerators.NamespaceFilterPageGenerator(generator, [6]))
    for page in pgenerator:
        totalImages = totalImages + 1
        success = False
        if not totalImages >= 10000:
            success = categorizeImage(
                countrycode, lang, commonsTemplate, commonsCategoryBase, commonsCatTemplates, page, conn, cursor)
        if success:
            categorizedImages = categorizedImages + 1

    return (countrycode, lang, commonsCategoryBase.title(withNamespace=False), commonsTemplate, totalImages, categorizedImages)


def outputStatistics(statistics):
    '''
    Output the results of the bot as a nice wikitable
    '''
    output = u'{| class="wikitable sortable"\n'
    output = output + \
        u'! country !! [[:en:List of ISO 639-1 codes|lang]] !! Base category !! Template !! data-sort-type="number"|Total images !! data-sort-type="number"|Categorized images !! data-sort-type="number"|Images left !! data-sort-type="number"|Current image count\n'

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
    output = output + u'||\n||\n||\n||\n|| %s \n|| %s \n|| %s || \n' % (
        totalImages, categorizedImages, leftoverImages)
    output = output + u'|}\n'

    site = pywikibot.Site('commons', 'commons')
    page = pywikibot.Page(
        site, u'Commons:Monuments database/Categorization/Statistics')

    comment = u'Updating categorization statistics. Total: %s Categorized: %s Leftover: %s' % (
        totalImages, categorizedImages, leftoverImages)
    page.put(newtext=output, comment=comment)


def getCommonscatTemplates(lang=None):
    '''Get the template name in a language. Expects the language code.
    Return as tuple containing the primary template and it's alternatives

    '''
    result = []
    if lang in commonscatTemplates:
        (prim, backups) = commonscatTemplates[lang]
    else:
        (prim, backups) = commonscatTemplates[u'_default']
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

    for arg in pywikibot.handleArgs():
        if arg.startswith('-countrycode:'):
            countrycode = arg[len('-countrycode:'):]
        elif arg.startswith('-overridecat:'):
            overridecat = arg[len('-overridecat:'):]

    if countrycode:
        lang = pywikibot.Site().language()
        if not mconfig.countries.get((countrycode, lang)):
            pywikibot.output(
                u'I have no config for countrycode "%s" in language "%s"' % (countrycode, lang))
            return False
        pywikibot.output(
            u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
        commonsCatTemplates = getCommonscatTemplates(lang)
        # print commonsCatTemplates
        processCountry(countrycode, lang, mconfig.countries.get(
            (countrycode, lang)), commonsCatTemplates, conn, cursor, overridecat=overridecat)
    else:
        statistics = []
        for (countrycode, lang), countryconfig in mconfig.countries.iteritems():
            pywikibot.output(
                u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
            commonsCatTemplates = getCommonscatTemplates(lang)
            result = processCountry(
                countrycode, lang, countryconfig, commonsCatTemplates, conn, cursor)
            if result:
                statistics.append(result)

        outputStatistics(statistics)

if __name__ == "__main__":
    main()
