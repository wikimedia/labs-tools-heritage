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
python categorize_images.py -countrycode:ee -langcode:et

'''
import json
import os

import yaml

import pywikibot
from pywikibot import pagegenerators, textlib

import common as common
import monuments_config as mconfig
from database_connection import (
    close_database_connection,
    connect_to_monuments_database
)

_logger = "categorize_images"

SKIP_LIST = [
    (u'cn', u'en'),
    (u'ir', u'fa'),
    (u'it', u'it'),
    (u'jo', u'ar'),
    (u'ge', u'ka'),
    (u'np', u'en'),
]


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


def _load_ignored_categories():
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    yaml_file = os.path.join(data_dir, 'ignore_commons_categories.yml')
    raw_list = yaml.load(open(yaml_file, 'r'))
    commons_site = pywikibot.Site(u'commons', u'commons')
    return [pywikibot.Category(commons_site, cat) for cat in raw_list]


def categorizeImage(
        countrycode, lang, commonsTemplateName, commonsCategoryBase,
        commonsCatTemplates, page, conn, cursor, harvest_type):
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

    (newcats, categorisation_method) = get_new_categories(monumentId, monData, lang, commonsCatTemplates, harvest_type)

    # See if one of the three options worked
    if newcats:
        comment = u'Adding categories based on [[Template:%s]] with identifier %s (method %s)' % (
            commonsTemplateName, monumentId, categorisation_method)
        replace_default_cat_with_new_categories_in_image(
            page, commonsCategoryBase, newcats, comment, verbose=True)
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


def get_new_categories(monumentId, monData, lang, commonsCatTemplates, harvest_type):
    (monumentName, monumentCommonscat,
     monumentArticleTitle, monumentSource, project) = monData
    commons_site = pywikibot.Site(u'commons', u'commons')
    newcats = []
    categorisation_method = ''
    # First try to add a category based on the commonscat field in the list
    if monumentCommonscat:
        # Might want to include some error checking here
        try:
            cat = pywikibot.Category(commons_site, monumentCommonscat)
            newcats.append(cat)
            categorisation_method = 'A: CommonsCat in the monument list'
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
                            (new_cat, method) = getCategoryFromCommonscat(monumentArticle, commonsCatTemplates)
                            newcats.append(new_cat)
                            categorisation_method = 'B%s: CommonsCat on the monument article' % method
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
    if not newcats and harvest_type != 'sparql':
        monumentList = getList(lang, project, monumentSource)
        # print monumentList
        if not monumentList:
            return ([], '')
        if monumentList.isRedirectPage():
            monumentList = monumentList.getRedirectTarget()
        try:
            (newcats, categorisation_method) = get_categories_from_source_page(monumentList, commonsCatTemplates)
        except pywikibot.exceptions.Error as e:
            pywikibot.error(u'Error occured with monument %s: %s' % (
                monumentId, str(e)))
    return (newcats, categorisation_method)


def replace_default_cat_with_new_categories_in_image(
        page, base_category, new_categories, comment, verbose=False):
    old_text = page.get()
    old_categories = list(page.categories())

    # ensure base category is never re-added
    old_categories.append(base_category)
    categories_to_add = filter_out_categories_to_add(new_categories,
                                                     old_categories)
    try:
        final_text = replace_default_cat_with_new_categories_in_image_text(
            old_text, base_category, categories_to_add)
    except NoCategoryToAddException:
        return False
    if verbose:
        pywikibot.showDiff(old_text, final_text)
    try:
        common.save_to_wiki_or_local(page, comment, final_text)
        return True
    except pywikibot.EditConflict:
        pywikibot.log(
            u'Got an edit conflict. Someone else beat me to it at %s' % page.title())
        return False


def replace_default_cat_with_new_categories_in_image_text(
        old_text, base_category, new_categories):
    """Add new categories to page text and remove any base_category."""
    if not new_categories:
        # No categories to add. We do not want to remove the base one,
        raise NoCategoryToAddException()

    # Remove base category
    page_text_without_base_category = textlib.replaceCategoryInPlace(
        old_text, base_category, None)
    final_text = textlib.replaceCategoryLinks(
        page_text_without_base_category, new_categories, addOnly=True)
    return final_text


def filter_out_categories_to_add(new_categories, unwanted_categories):
    """
    Ensure unwanted categories are not added.

    This included hidden, duplicate, ignored or already present categories.

    Requires the inputs to be lists of pywikibot.Category.
    """
    candidate_categories = set(new_categories) - set(unwanted_categories)
    candidate_categories -= set(_load_ignored_categories())
    final_categories = filter(lambda cat: not cat.isHiddenCategory(),
                              list(candidate_categories))
    return final_categories


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
    """Get the listpage, if not harvested from a sparql query."""
    if monumentSource:
        try:
            page_title, found_site = common.get_source_page(monumentSource)
        except ValueError:
            return False
        if (project, lang) != found_site:
            return False

        site = pywikibot.Site(lang, project)
        return pywikibot.Page(site, page_title)
    else:
        return False


def is_template_present_in_page(template, page):
    """Return whether a template is present in a page (as in directly transcluded.)"""
    return template in [x[0] for x in page.templatesWithParams()]


def get_categories_from_source_page(page, commonsCatTemplates):
    """
    Get Commons categories based on page.

    1. If page contains a Commonscat template, use that category
    2. Else, try getting it from Wikidata
    3. Else pull Commonscat links from upper categories
    """
    new_categories = set()
    categorisation_method = ''
    for commonsCatTemplateName in commonsCatTemplates:
        commonsCatTemplate = pywikibot.Page(page.site, 'Template:%s' % commonsCatTemplateName)
        if is_template_present_in_page(commonsCatTemplate, page):
            (new_cat, _) = getCategoryFromCommonscat(page, commonsCatTemplates)
            new_categories.add(new_cat)
            categorisation_method = 'C1: CommonsCat on the monument list page'
    if not len(new_categories):
        try:
            site = pywikibot.Site(u'commons', u'commons')
            cat_title = get_Commons_category_via_Wikidata(page)
            cat = pywikibot.Category(site, cat_title)
            new_categories.add(cat)
            categorisation_method = 'C2: via Wikidata on the monument list page'
        except NoCommonsCatFromWikidataItemException:
            pass
    if not len(new_categories):
        new_categories = get_categories_from_upper_categories(page, commonsCatTemplates)
        categorisation_method = 'D: from upper categories of monument list page'

    return (new_categories, categorisation_method)


def get_categories_from_upper_categories(page, commonsCatTemplates):
    new_categories = set()
    for cat in page.categories():
        for commonsCatTemplateName in commonsCatTemplates:
            commonsCatTemplate = pywikibot.Page(page.site, 'Template:%s' % commonsCatTemplateName)
            if is_template_present_in_page(commonsCatTemplate, cat):
                (new_cat, method) = getCategoryFromCommonscat(cat, commonsCatTemplates)
                new_categories.add(new_cat)
        try:
            site = pywikibot.Site(u'commons', u'commons')
            new_cat_title = get_Commons_category_via_Wikidata(cat)
            new_cat = pywikibot.Category(site, new_cat_title)
            new_categories.add(new_cat)
        except NoCommonsCatFromWikidataItemException:
            pass
    return new_categories


def getCategoryFromCommonscat(page, commonsCatTemplates):
    """
    Get a Commons category based on a page.

    1. Get category from commonscat template on page
    2. Get category from commonscat property or Commons category sitelink on
       the Wikidata object corresponding to the page
    3. Get category with same name as page
    """
    cat_title = None
    categorisation_method = '1'  # By 'default', we do not rely on Wikidata
    (template, params) = get_commonscat_template_in_page(page, commonsCatTemplates)

    if len(params) >= 1:
        cat_title = params[0]

    if not cat_title:
        try:
            cat_title = get_Commons_category_via_Wikidata(page)
            categorisation_method = '2'
        except NoCommonsCatFromWikidataItemException:
            pass

    if not cat_title:
        categorisation_method = '3'
        cat_title = page.title(withNamespace=False)

    site = pywikibot.Site(u'commons', u'commons')
    cat = pywikibot.Category(site, cat_title)
    return (cat, categorisation_method)


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


def processCountry(countrycode, lang, countryconfig, commonsCatTemplates,
                   conn, cursor, overridecat=None):
    """Work on a single country."""
    if not countryconfig.get('commonsTemplate'):
        # No template found, just skip silently.
        basecat = None
        if countryconfig.get('commonsCategoryBase'):
            basecat = countryconfig.get('commonsCategoryBase')
        return {
            'code': countrycode,
            'lang': lang,
            'cat': basecat,
            'cmt': 'skipped: no template'
        }

    if not countryconfig.get('commonsCategoryBase') and not overridecat:
        # No template found, just skip silently.
        commonsTemplate = countryconfig.get('commonsTemplate')
        return {
            'code': countrycode,
            'lang': lang,
            'template': commonsTemplate,
            'cmt': 'skipped: no base category'
        }

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
    harvest_type = countryconfig.get('type')

    category_name = overridecat or countryconfig.get('commonsCategoryBase')
    commonsCategoryBase = pywikibot.Category(
        site, "%s:%s" % (site.namespace(14), category_name))

    generator = pagegenerators.CategorizedPageGenerator(commonsCategoryBase)

    # Get a preloading generator with only images
    pgenerator = pagegenerators.PreloadingGenerator(
        pagegenerators.NamespaceFilterPageGenerator(generator, [6]))
    for page in pgenerator:
        totalImages += 1
        success = False
        if not totalImages >= 10000:
            success = categorizeImage(
                countrycode, lang, commonsTemplate, commonsCategoryBase,
                commonsCatTemplates, page, conn, cursor, harvest_type)
        if success:
            categorizedImages += 1

    return {
        'code': countrycode,
        'lang': lang,
        'cat': commonsCategoryBase.title(withNamespace=False),
        'template': commonsTemplate,
        'total_images': totalImages,
        'cat_images': categorizedImages
    }


def outputStatistics(statistics):
    """Output the results of the bot as a nice wikitable."""
    output = (
        u'{| class="wikitable sortable"\n'
        u'! country '
        u'!! [[:en:List of ISO 639-1 codes|lang]] '
        u'!! Base category '
        u'!! Template '
        u'!! data-sort-type="number"|Total images '
        u'!! data-sort-type="number"|Categorized images '
        u'!! data-sort-type="number"|Images left '
        u'!! data-sort-type="number"|Current image count'
        u'\n')

    output_row = (
        u'|-\n'
        u'|| {code} \n'
        u'|| {lang} \n'
        u'|| {cat} \n'
        u'|| {template} \n'
        u'|| {total_images} \n'
        u'|| {cat_images} \n'
        u'|| {leftover} \n'
        u'|| {pages_in_cat} \n')

    totalImages = 0
    categorizedImages = 0
    leftoverImages = 0

    for row in statistics:

        leftover = '---'
        cat_link = '---'
        pages_in_cat = '---'
        template_link = '---'
        total_images = row.get('total_images')
        cat_images_or_cmt = row.get('cat_images')

        if row.get('cat_images') is not None:
            totalImages += row['total_images']
            categorizedImages += row['cat_images']
            leftover = row['total_images'] - row['cat_images']
            leftoverImages += leftover
        else:
            cat_images_or_cmt = row.get('cmt')
            total_images = '---'

        if row.get('cat'):
            cat_link = u'[[:Category:{0}]]'.format(row['cat'])
            pages_in_cat = '{{PAGESINCATEGORY:%s|files}}' % row['cat']

        if row.get('template'):
            template_link = '{{tl|%s}}' % row['template']

        output += output_row.format(
            code=row['code'],
            lang=row['lang'],
            cat=cat_link,
            template=template_link,
            total_images=total_images,
            cat_images=cat_images_or_cmt,
            leftover=leftover,
            pages_in_cat=pages_in_cat)

    output += u'|- class="sortbottom"\n'
    output += u'||\n||\n||\n||\n|| %s \n|| %s \n|| %s || \n' % (
        totalImages, categorizedImages, leftoverImages)
    output += u'|}\n'

    site = pywikibot.Site('commons', 'commons')
    page = pywikibot.Page(
        site, u'Commons:Monuments database/Categorization/Statistics')
    summary = (
        u'Updating categorization statistics. '
        u'Total: {0} Categorized: {1} Leftover: {2}'.format(
            totalImages, categorizedImages, leftoverImages))
    common.save_to_wiki_or_local(page, summary, output)


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


def skip(country_code, lang, country_config):
    """Return a outputStatistics compatible summary for a skipped country."""
    site = pywikibot.Site(u'commons', u'commons')
    commons_category_base = pywikibot.Category(site, u'{ns}:{cat}'.format(
        ns=site.namespace(14), cat=country_config.get('commonsCategoryBase')))
    commons_template = country_config.get('commonsTemplate')
    return {
        'code': country_code,
        'lang': lang,
        'cat': commons_category_base.title(withNamespace=False),
        'template': commons_template,
        'cmt': 'skipped: blacklisted'
    }


def main():

    countrycode = u''
    lang = u''
    overridecat = u''
    skip_wd = False
    conn = None
    cursor = None
    # Connect database, we need that
    (conn, cursor) = connect_to_monuments_database()

    for arg in pywikibot.handleArgs():
        option, sep, value = arg.partition(':')
        if option == '-countrycode':
            countrycode = value
        elif option == '-langcode':
            lang = value
        elif option == '-overridecat':
            overridecat = value
        elif option == '-skip_wd':
            skip_wd = True
        else:
            raise Exception(
                u'Bad parameters. Expected "-countrycode", "-langcode", '
                u'"-overridecat", "-skip_wd" or pywikibot args. '
                u'Found "{}"'.format(option))

    if countrycode and lang:
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
    elif countrycode or lang:
        raise Exception(u'The "countrycode" and "langcode" arguments must '
                        u'be used together.')
    else:
        statistics = []
        for (countrycode, lang), countryconfig in mconfig.countries.iteritems():
            if (countryconfig.get('skip') or
                    (skip_wd and (countryconfig.get('type') == 'sparql'))):
                continue

            if (countrycode, lang) in SKIP_LIST:
                pywikibot.log(
                    u'Skipping countrycode "%s" in language "%s"' % (countrycode, lang))
                statistics.append(skip(countrycode, lang, countryconfig))
                continue

            pywikibot.log(
                u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
            commonsCatTemplates = getCommonscatTemplates(
                lang, countryconfig.get('project'))
            result = processCountry(
                countrycode, lang, countryconfig, commonsCatTemplates, conn,
                cursor)
            if result:
                statistics.append(result)

        outputStatistics(statistics)

    close_database_connection(conn, cursor)


if __name__ == "__main__":
    main()
