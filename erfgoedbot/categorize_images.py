#!/usr/bin/python
# -*- coding: utf-8  -*-
'''

Bot to move images from commonsCategoryBase to subcategories based on the monument
template and Commonscat links at the Wikipedia.
First checks if monument article or it's categories have commonscat template,
 if not then checks if monuments list or it's categories have commonscat template.


Usage:
* To process all:
python categorize_images.py

* Just process one source:
python categorize_images.py -countrycode:ee -lang:et

'''
import json
import os
import re

import pywikibot
from pywikibot import pagegenerators
from pywikibot import textlib

import monuments_config as mconfig
from database_connection import connect_to_monuments_database

_logger = "categorize_images"


class NoMonumentIdentifierFoundException(pywikibot.exceptions.PageRelatedError):
    message = u"No Monument Identifier could be found for %s"
    pass


class NoCommonsCatFromWikidataItemException(pywikibot.exceptions.PageRelatedError):
    message = u"No CommonsCat could be retrieved through Wikidata for %s"
    pass


class NoCategoryToAddException(Exception):
    pass


def _load_wikipedia_commonscat_templates():
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    json_file = os.path.join(data_dir, 'wikipedia_commonscat_templates.json')
    return json.load(open(json_file, 'r'))


def categorizeImage(countrycode, lang, commonsTemplateName, commonsCategoryBase, commonsCatTemplates, page, conn, cursor):
    pywikibot.log(u'Working on: %s' % page.title())
    site = pywikibot.Site(u'commons', u'commons')
    commonsTemplate = pywikibot.Page(site, 'Template:%s' % commonsTemplateName)
    currentcats = list(page.categories())
    if commonsCategoryBase not in currentcats:
        pywikibot.log(u'%s category not found at: %s. Someone probably already categorized it.' % (
            commonsCategoryBase, page.title()))
        return False

    if u'Wikipedia image placeholders for cultural heritage monuments' in currentcats:
        pywikibot.log(u'%s in %s is a placeholder, skipping it.' % (
            page.title(), commonsCategoryBase))
        return False

    templates = page.templates()
    if commonsTemplate not in templates:
        pywikibot.log(u'%s template not found at: %s' % (
            commonsTemplate, page.title()))
        return False

    try:
        monumentId = get_monument_id(page, commonsTemplate)
    except NoMonumentIdentifierFoundException:
        pywikibot.warning(u'Didn\'t find a valid monument identifier at: %s' % (
            page.title(),))
        return False

    monData = getMonData(countrycode, lang, monumentId, conn, cursor)
    if not monData:
        try:
            monumentId = int(monumentId)
            monData = getMonData(countrycode, lang, monumentId, conn, cursor)
        except ValueError:
            pywikibot.debug(
                u'Can\'t convert %s to an integer' % (monumentId,), _logger)

    if not monData:
        # Triage as log since there are plenty of valid reasons for this
        pywikibot.log(
            u'Monument with id %s not in monuments database' % (monumentId, ))
        return False

    newcats = get_new_categories(monumentId, monData, lang, commonsCatTemplates)

    # See if one of the three options worked
    if newcats:
        comment = u'Adding categories based on [[Template:%s]] with identifier %s' % (
            commonsTemplateName, monumentId)
        replace_default_cat_with_new_categories_in_image(page, commonsCategoryBase, newcats, comment, verbose=True)
    else:
        pywikibot.log(u'Categories not found for %s' % page.title())


def get_monument_id(page, commonsTemplate):
    monumentId = None
    for (template, params) in page.templatesWithParams():
        if template == commonsTemplate:
            if len(params) >= 1:
                try:
                    monumentId = params[0]
                except ValueError:
                    pywikibot.warning(
                        u'Unable to extract a valid id for %s on %s' % (
                            template, page.title()))
                break
    if not monumentId:
        raise NoMonumentIdentifierFoundException(page)
    return monumentId


def get_new_categories(monumentId, monData, lang, commonsCatTemplates):
    (monumentName, monumentCommonscat,
     monumentArticleTitle, monumentSource, project) = monData
    commons_site = pywikibot.Site(u'commons', u'commons')
    newcats = []
    # First try to add a category based on the commonscat field in the list
    if monumentCommonscat:
        # Might want to include some error checking here
        try:
            cat = pywikibot.Category(commons_site, monumentCommonscat)
            newcats.append(cat)
        except ValueError:
            pywikibot.warning(
                u'The Commonscat field for %s contains an invalid category %s' % (
                    monumentId, monumentCommonscat))
        except pywikibot.exceptions.InvalidTitle:
            pywikibot.warning(
                u'Incorrect category title %s' % (monumentCommonscat,))

    # Option two is to use the article about the monument and see if it has
    # Commonscat links
    if not newcats:
        monumentArticle = None
        if monumentArticleTitle:
            project_site = pywikibot.Site(lang, project)
            monumentArticle = pywikibot.Page(project_site, monumentArticleTitle)
        if monumentArticle:
            try:
                if monumentArticle.isRedirectPage():
                    monumentArticle = monumentArticle.getRedirectTarget()
                try:
                    for commonsCatTemplateName in commonsCatTemplates:
                        commonsCatTemplate = pywikibot.Page(project_site, 'Template:%s' % commonsCatTemplateName)
                        if is_template_present_in_page(commonsCatTemplate, monumentArticle):
                            newcats = []
                            newcats.append(
                                getCategoryFromCommonscat(monumentArticle, commonsCatTemplates))
                except pywikibot.SectionError:
                    pywikibot.warning(u'Incorrect redirect at %s' % (
                        monumentArticle.title(),))
            except pywikibot.exceptions.InvalidTitle:
                pywikibot.warning(u'Incorrect article title %s' % (
                    monumentArticleTitle,))
            except pywikibot.exceptions.Error as e:
                pywikibot.error(u'Error occured with monument %s: %s' % (
                    monumentId, str(e)))

    # Option three is to see if the list contains Commonscat links (whole list)
    if not newcats:
        monumentList = getList(lang, project, monumentSource)
        # print monumentList
        if not monumentList:
            return False
        if monumentList.isRedirectPage():
            monumentList = monumentList.getRedirectTarget()
        try:
            newcats = getCategories(monumentList, commonsCatTemplates)
        except pywikibot.exceptions.Error as e:
            pywikibot.error(u'Error occured with monument %s: %s' % (
                monumentId, str(e)))
    return newcats


def replace_default_cat_with_new_categories_in_image(page, commonsCategoryBase, new_categories, comment, verbose=False):
    oldtext = page.get()
    categories_to_add = deduplicate_categories(new_categories)
    categories_to_add = remove_base_category_from_categories_to_add_if_present(new_categories, commonsCategoryBase)
    try:
        final_text = replace_default_cat_with_new_categories_in_image_text(oldtext, commonsCategoryBase, categories_to_add)
    except NoCategoryToAddException:
        return False
    if verbose:
        pywikibot.showDiff(oldtext, final_text)
    try:
        page.put(final_text, comment)
        return True
    except pywikibot.EditConflict:
        pywikibot.log(
            u'Got an edit conflict. Someone else beat me to it at %s' % page.title())
        return False


def deduplicate_categories(categories):
    return list(set(categories))


def remove_base_category_from_categories_to_add_if_present(categories, base_category):
    return set(categories) - set([base_category])


def replace_default_cat_with_new_categories_in_image_text(oldtext, commonsCategoryBase, newcats):
    if not newcats:
        # No categories to add. We do not want to remove the base one
        raise NoCategoryToAddException()
    # In any case we remove the base category
    page_text_without_old_category = textlib.replaceCategoryInPlace(oldtext, commonsCategoryBase, None)
    commons_site = pywikibot.Site(u'commons', u'commons')
    currentcats = textlib.getCategoryLinks(oldtext, site=commons_site)
    final_categories = filter_out_categories_to_add(newcats, currentcats)
    if final_categories:
        final_text = textlib.replaceCategoryLinks(page_text_without_old_category, final_categories, addOnly=True)
    else:
        final_text = page_text_without_old_category
    return final_text


def filter_out_categories_to_add(new_categories, current_categories):
    """Make sure we do not add categories that were already there."""
    final_categories = set(new_categories) - set(current_categories)
    return list(final_categories)


def getMonData(countrycode, lang, monumentId, conn, cursor):
    """Get monument name and source from db."""
    query = u"SELECT `name`, `commonscat`, `monument_article`, `source`, `project` " \
            u"FROM monuments_all " \
            u"WHERE (country=%s AND lang=%s AND id=%s) " \
            u"LIMIT 1"

    cursor.execute(query, (countrycode, lang, monumentId))

    try:
        row = cursor.fetchone()
        return row
    except TypeError:
        pywikibot.warning(u'Didn\'t find anything for id %s' % (monumentId,))
        return False


def getList(lang, project, monumentSource):
    '''
    Get listpage
    '''
    if monumentSource:
        regex = u'^(https:)?//%s.%s.org/w/index.php\?title=(.+?)&' % (
            lang, project)
        match = re.search(regex, monumentSource)
        if not match:
            return False
        page_title = match.group(2)
        site = pywikibot.Site(lang, project)
        return pywikibot.Page(site, page_title)
    else:
        return False


def is_template_present_in_page(template, page):
    """Return whether a template is present in a page (as in directly transcluded.)"""
    return template in [x[0] for x in page.templatesWithParams()]


def getCategories(page, commonsCatTemplates):
    '''
    Get Commons categories based on page.
    1. If page contains a Commonscat template, use that category
    2. Else, try getting it from Wikidata
    3. Else pull Commonscat links from upper categories
    '''
    result = set()
    for commonsCatTemplateName in commonsCatTemplates:
        commonsCatTemplate = pywikibot.Page(page.site, 'Template:%s' % commonsCatTemplateName)
        if is_template_present_in_page(commonsCatTemplate, page):
            result.add(getCategoryFromCommonscat(page, commonsCatTemplates))
    if not len(result):
        try:
            result.add(get_Commons_category_via_Wikidata(page))
        except NoCommonsCatFromWikidataItemException:
            pass
    if not len(result):
        # print page.categories()
        for cat in page.categories():
            # print cat
            for commonsCatTemplateName in commonsCatTemplates:
                commonsCatTemplate = pywikibot.Page(page.site, 'Template:%s' % commonsCatTemplateName)
                # print commonsCatTemplate
                if is_template_present_in_page(commonsCatTemplate, cat):
                    # print u'hit!'
                    result.add(
                        getCategoryFromCommonscat(cat, commonsCatTemplates))
            try:
                site = pywikibot.Site(u'commons', u'commons')
                new_cat_title = get_Commons_category_via_Wikidata(cat)
                new_cat = pywikibot.Category(site, new_cat_title)
                result.add(new_cat)
            except NoCommonsCatFromWikidataItemException:
                pass
    return result


def getCategoryFromCommonscat(page, commonsCatTemplates):
    '''
    Get a Commons category based on a page with a Commonscat template
    '''
    cat_title = None
    (template, params) = get_commonscat_template_in_page(page, commonsCatTemplates)

    if len(params) >= 1:
        cat_title = params[0]

    if not cat_title:
        try:
            cat_title = get_Commons_category_via_Wikidata(page)
        except NoCommonsCatFromWikidataItemException:
            pass

    if not cat_title:
        cat_title = page.title(withNamespace=False)

    site = pywikibot.Site(u'commons', u'commons')
    cat = pywikibot.Category(site, cat_title)
    return cat


def get_commonscat_template_in_page(page, commonsCatTemplates):
    for (template, params) in page.templatesWithParams():
        if template.title(withNamespace=False) in commonsCatTemplates:
            return (template, params)


def get_Commons_category_via_Wikidata(page):
    """
    Get Commons Category from the linked Wikidata item and P373.

    Raises: NoCommonsCatFromWikidataItemException if either there is no linked
            item or it does not bear P373 or a sitelink to a category page on
            Commons.
    """
    try:
        data_item = page.data_item()
        claims = data_item.get()['claims']
        if 'P373' in claims:
            return 'Category:' + claims['P373'][0].getTarget()
        else:
            commons_site = pywikibot.Site(u'commons', u'commons')
            commons_page = data_item.getSitelink(commons_site)
            if commons_page.startswith('Category:'):
                return commons_page
            else:
                raise NoCommonsCatFromWikidataItemException(page)
    except (pywikibot.NoPage, KeyError, NoCommonsCatFromWikidataItemException):
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
        pywikibot.warning(
            u'Language: %s has no commonsCatTemplates set!' % lang)
        return False

    totalImages = 0
    categorizedImages = 0

    site = pywikibot.Site(u'commons', u'commons')
    generator = None
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
        totalImages += 1
        success = False
        if not totalImages >= 10000:
            success = categorizeImage(
                countrycode, lang, commonsTemplate, commonsCategoryBase, commonsCatTemplates, page, conn, cursor)
        if success:
            categorizedImages += 1

    return (countrycode, lang, commonsCategoryBase.title(withNamespace=False), commonsTemplate, totalImages, categorizedImages)


def outputStatistics(statistics):
    '''
    Output the results of the bot as a nice wikitable
    '''
    output = u'{| class="wikitable sortable"\n'
    output += \
        u'! country !! [[:en:List of ISO 639-1 codes|lang]] !! Base category !! Template !! data-sort-type="number"|Total images !! data-sort-type="number"|Categorized images !! data-sort-type="number"|Images left !! data-sort-type="number"|Current image count\n'

    totalImages = 0
    categorizedImages = 0
    leftoverImages = 0

    for row in statistics:
        output += u'|-\n'
        output += u'|| %s \n' % (row[0],)
        output += u'|| %s \n' % (row[1],)
        output += u'|| [[:Category:%s]] \n' % (row[2],)
        output += u'|| {{tl|%s}} \n' % (row[3],)

        totalImages += row[4]
        output += u'|| %s \n' % (row[4],)

        categorizedImages += row[5]
        output += u'|| %s \n' % (row[5],)

        leftover = row[4] - row[5]
        leftoverImages += leftover

        output += u'|| %s \n' % (leftover,)
        output += u'|| {{PAGESINCATEGORY:%s|files}} \n' % (row[2],)

    output += u'|- class="sortbottom"\n'
    output += u'||\n||\n||\n||\n|| %s \n|| %s \n|| %s || \n' % (
        totalImages, categorizedImages, leftoverImages)
    output += u'|}\n'

    site = pywikibot.Site('commons', 'commons')
    page = pywikibot.Page(
        site, u'Commons:Monuments database/Categorization/Statistics')

    comment = u'Updating categorization statistics. Total: %s Categorized: %s Leftover: %s' % (
        totalImages, categorizedImages, leftoverImages)
    page.put(newtext=output, comment=comment)


def getCommonscatTemplates(lang=None, project=None):
    """
    Get the template name in a language on a project.

    Expects the language code and project.
    Return as list containing the primary template and it's alternatives
    """
    project = project or u'wikipedia'  # default to wikipedia

    wikipedia_commonscat_templates = _load_wikipedia_commonscat_templates()

    result = []
    if project == u'wikipedia' and lang in wikipedia_commonscat_templates:
        (prim, backups) = wikipedia_commonscat_templates[lang]
    else:
        (prim, backups) = wikipedia_commonscat_templates[u'_default']
    result.append(prim)
    result += backups
    return result


def main():

    countrycode = u''
    overridecat = u''
    lang = u''
    conn = None
    cursor = None
    # Connect database, we need that
    (conn, cursor) = connect_to_monuments_database()

    for arg in pywikibot.handleArgs():
        option, sep, value = arg.partition(':')
        if option == '-countrycode':
            countrycode = value
        elif option == '-overridecat':
            overridecat = value

    if countrycode:
        lang = pywikibot.Site().language()
        if not mconfig.countries.get((countrycode, lang)):
            pywikibot.warning(
                u'I have no config for countrycode "%s" in language "%s"' % (countrycode, lang))
            return False
        pywikibot.log(
            u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
        countryconfig = mconfig.countries.get((countrycode, lang))
        commonsCatTemplates = getCommonscatTemplates(
            lang, countryconfig.get('project'))
        # print commonsCatTemplates
        processCountry(countrycode, lang, countryconfig, commonsCatTemplates,
                       conn, cursor, overridecat=overridecat)
    else:
        statistics = []
        for (countrycode, lang), countryconfig in mconfig.countries.iteritems():
            pywikibot.log(
                u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
            commonsCatTemplates = getCommonscatTemplates(
                lang, countryconfig.get('project'))
            result = processCountry(
                countrycode, lang, countryconfig, commonsCatTemplates, conn, cursor)
            if result:
                statistics.append(result)

        outputStatistics(statistics)

if __name__ == "__main__":
    main()
