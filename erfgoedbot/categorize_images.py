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
from collections import OrderedDict

import yaml

import pywikibot
from pywikibot import pagegenerators, textlib

import erfgoedbot.common as common
import erfgoedbot.monuments_config as mconfig
from erfgoedbot.database_connection import (
    close_database_connection,
    connect_to_monuments_database
)
from erfgoedbot.statistics_table import StatisticsTable

_logger = "categorize_images"

SKIP_LIST = [
    ('au', 'en'),  # Australia in English
    ('cn', 'en'),
    ('gb-sct', 'en'),  # Scotland in English
    ('dz', 'ar'),  # Algeria in Arabic
    ('ir', 'fa'),
    ('it', 'it'),
    ('jo', 'ar'),
    ('ge', 'ka'),
    ('gh', 'en'),  # Ghana in English
    ('mt', 'de'),  # Malta in German
    ('np', 'en'),
    ('pe', 'es'),  # Peru in Spanish
    ('sv', 'es'),  # El Salvador in Spanish
    ('ve', 'es'),  # Venezuela in Spanish
]


class NoMonumentIdentifierFoundException(pywikibot.exceptions.PageRelatedError):
    message = "No Monument Identifier could be found for %s"
    pass


class NoCommonsCatFromWikidataItemException(pywikibot.exceptions.PageRelatedError):
    message = "No CommonsCat could be retrieved through Wikidata for %s"
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
    commons_site = pywikibot.Site('commons', 'commons')
    return [pywikibot.Category(commons_site, cat) for cat in raw_list]


def _get_commons_template(template_name):
    site = pywikibot.Site('commons', 'commons')
    return pywikibot.Page(site, 'Template:%s' % template_name)


def categorizeImage(
        countrycode, lang, commonsTemplateName, commonsCategoryBase,
        commonsCatTemplates, page, conn, cursor, harvest_type):
    pywikibot.log('Working on: %s' % page.title())
    commonsTemplate = _get_commons_template(commonsTemplateName)
    currentcats = list(page.categories())
    if commonsCategoryBase not in currentcats:
        pywikibot.log('%s category not found at: %s. Someone probably already categorized it.' % (
            commonsCategoryBase, page.title()))
        return False

    if 'Wikipedia image placeholders for cultural heritage monuments' in currentcats:
        pywikibot.log('%s in %s is a placeholder, skipping it.' % (
            page.title(), commonsCategoryBase))
        return False

    templates = page.templates()
    if commonsTemplate not in templates:
        pywikibot.log('%s template not found at: %s' % (
            commonsTemplate, page.title()))
        return False

    try:
        monumentId = get_monument_id(page, commonsTemplate)
    except NoMonumentIdentifierFoundException:
        pywikibot.warning('Didn\'t find a valid monument identifier at: %s' % (
            page.title(),))
        return False

    monData = getMonData(countrycode, lang, monumentId, conn, cursor)
    if not monData:
        try:
            monumentId = int(monumentId)
            monData = getMonData(countrycode, lang, monumentId, conn, cursor)
        except ValueError:
            pywikibot.debug(
                'Can\'t convert %s to an integer' % (monumentId,), _logger)

    if not monData:
        # Triage as log since there are plenty of valid reasons for this
        pywikibot.log(
            'Monument with id %s not in monuments database' % (monumentId, ))
        return False

    (newcats, categorisation_method) = get_new_categories(monumentId, monData, lang, commonsCatTemplates, harvest_type)

    # See if one of the three options worked
    if newcats:
        comment = 'Adding categories based on [[Template:%s]] with identifier %s (method %s)' % (
            commonsTemplateName, monumentId, categorisation_method)
        return replace_default_cat_with_new_categories_in_image(
            page, commonsCategoryBase, newcats, comment, verbose=True)
    else:
        pywikibot.log('Categories not found for %s' % page.title())


def get_monument_id(page, commonsTemplate):
    monumentId = None
    for (template, params) in page.templatesWithParams():
        if template == commonsTemplate:
            if len(params) >= 1:
                try:
                    monumentId = params[0]
                except ValueError:
                    pywikibot.warning(
                        'Unable to extract a valid id for %s on %s' % (
                            template, page.title()))
                break
    if not monumentId:
        raise NoMonumentIdentifierFoundException(page)
    return monumentId


def get_new_categories(monumentId, monData, lang, commonsCatTemplates, harvest_type):
    (monumentName, monumentCommonscat,
     monumentArticleTitle, monumentSource, project) = monData
    commons_site = pywikibot.Site('commons', 'commons')
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
                'The Commonscat field for %s contains an invalid category %s' % (
                    monumentId, monumentCommonscat))
        except pywikibot.exceptions.InvalidTitle:
            pywikibot.warning(
                'Incorrect category title %s' % (monumentCommonscat,))

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
                    pywikibot.warning('Incorrect redirect at %s' % (
                        monumentArticle.title(),))
            except pywikibot.exceptions.InvalidTitle:
                pywikibot.warning('Incorrect article title %s' % (
                    monumentArticleTitle,))
            except pywikibot.exceptions.Error as e:
                pywikibot.error('Error occured with monument %s: %s' % (
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
            pywikibot.error('Error occured with monument %s: %s' % (
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
            'Got an edit conflict. Someone else beat me to it at %s' % page.title())
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
    final_categories = [cat for cat in list(candidate_categories) if not cat.isHiddenCategory()]
    return final_categories


def getMonData(countrycode, lang, monumentId, conn, cursor):
    """Get monument name and source from db."""
    query = (
        "SELECT `name`, `commonscat`, `monument_article`, `source`, `project` "
        "FROM monuments_all "
        "WHERE (country=%s AND lang=%s AND id=%s) "
        "LIMIT 1")

    cursor.execute(query, (countrycode, lang, monumentId))

    try:
        row = cursor.fetchone()
        return row
    except TypeError:
        pywikibot.warning('Didn\'t find anything for id %s' % (monumentId,))
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
            site = pywikibot.Site('commons', 'commons')
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
            site = pywikibot.Site('commons', 'commons')
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
        cat_title = page.title(with_ns=False)

    site = pywikibot.Site('commons', 'commons')
    cat = pywikibot.Category(site, cat_title)
    return (cat, categorisation_method)


def get_commonscat_template_in_page(page, commonsCatTemplates):
    for (template, params) in page.templatesWithParams():
        if template.title(with_ns=False) in commonsCatTemplates:
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
            commons_site = pywikibot.Site('commons', 'commons')
            commons_page = data_item.getSitelink(commons_site)
            if commons_page.startswith('Category:'):
                return commons_page
            else:
                raise NoCommonsCatFromWikidataItemException(page)
    except (pywikibot.exceptions.NoPageError, KeyError, NoCommonsCatFromWikidataItemException):
        raise NoCommonsCatFromWikidataItemException(page)


def processCountry(countryconfig, commonsCatTemplates, conn, cursor,
                   overridecat=None):
    """Work on a single country."""
    if not countryconfig.get('commonsTemplate'):
        # No template found, just skip silently.
        basecat = None
        if countryconfig.get('commonsCategoryBase'):
            basecat = countryconfig.get('commonsCategoryBase')
        return {
            'code': countryconfig.get('country'),
            'lang': countryconfig.get('lang'),
            'cat': basecat,
            'cmt': 'skipped: no template'
        }

    if not countryconfig.get('commonsCategoryBase') and not overridecat:
        # No template found, just skip silently.
        commonsTemplate = countryconfig.get('commonsTemplate')
        return {
            'code': countryconfig.get('country'),
            'lang': countryconfig.get('lang'),
            'template': commonsTemplate,
            'cmt': 'skipped: no base category'
        }

    if (not commonsCatTemplates):
        # No commonsCatTemplates found, just skip.
        pywikibot.warning(
            'Language: {0} has no commonsCatTemplates set!'.format(
                countryconfig.get('lang')))
        return False

    totalImages = 0
    categorizedImages = 0

    site = pywikibot.Site('commons', 'commons')
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
                countryconfig.get('country'), countryconfig.get('lang'),
                commonsTemplate, commonsCategoryBase, commonsCatTemplates,
                page, conn, cursor, harvest_type)
        if success:
            categorizedImages += 1

    return {
        'code': countryconfig.get('country'),
        'lang': countryconfig.get('lang'),
        'cat': commonsCategoryBase.title(with_ns=False),
        'template': commonsTemplate,
        'total_images': totalImages,
        'cat_images': categorizedImages
    }


def outputStatistics(statistics):
    """Output the results of the bot as a nice wikitable."""
    site = pywikibot.Site('commons', 'commons')
    page = pywikibot.Page(
        site, 'Commons:Monuments database/Categorization/Statistics')

    title_column = OrderedDict([
        ('code', 'country'),
        ('lang', '[[:en:List of ISO 639-1 codes|lang]]'),
        ('cat', 'Base category'),
        ('template', 'Template'),
        ('total_images', 'Total images'),
        ('cat_images', 'Categorized images'),
        ('leftover', 'Images left'),
        ('pages_in_cat', 'Current image count')
    ])
    numeric_columns = ('total_images', 'cat_images', 'leftover',
                       'pages_in_cat')
    table = StatisticsTable(title_column, numeric_columns)

    total_images_sum = 0
    categorized_images_sum = 0
    leftover_images_sum = 0

    for row in statistics:

        leftover = None
        cat_link = None
        pages_in_cat = None
        template_link = None
        total_images = row.get('total_images')
        cat_images_or_cmt = row.get('cat_images')

        if row.get('cat_images') is not None:
            leftover = row['total_images'] - row['cat_images']
        else:
            cat_images_or_cmt = row.get('cmt')
            total_images = None

        if row.get('cat'):
            cat_link = '[[:Category:{0}]]'.format(row['cat'])
            pages_in_cat = '{{PAGESINCATEGORY:%s|files}}' % row['cat']

        if row.get('template'):
            template_link = '{{tl|%s}}' % row['template']

        table.add_row({
            'code': row['code'],
            'lang': row['lang'],
            'cat': cat_link,
            'template': template_link,
            'total_images': total_images,
            'cat_images': cat_images_or_cmt,
            'leftover': leftover,
            'pages_in_cat': pages_in_cat
        })

    # we want pages_in_cat numerically sorted but not summed
    table.totals['pages_in_cat'] = None
    output = table.to_wikitext()

    summary = (
        'Updating categorization statistics. '
        'Total: {total_images} Categorized: {cat_images} '
        'Leftover: {leftover}'.format(**table.get_sum()))
    common.save_to_wiki_or_local(page, summary, output)


def getCommonscatTemplates(lang=None, project=None):
    """
    Get the template name in a language on a project.

    Expects the language code and project.
    Return as list containing the primary template and it's alternatives
    """
    project = project or 'wikipedia'  # default to wikipedia

    wikipedia_commonscat_templates = _load_wikipedia_commonscat_templates()

    result = []
    if project == 'wikipedia' and lang in wikipedia_commonscat_templates:
        (prim, backups) = wikipedia_commonscat_templates[lang]
    else:
        (prim, backups) = wikipedia_commonscat_templates['_default']
    result.append(prim)
    result += backups
    return result


def custom_output_statistics_message(country_config, message):
    """Return a outputStatistics compatible summary for a missing dataset (skipped or failed)."""
    site = pywikibot.Site('commons', 'commons')
    commons_category_base = pywikibot.Category(site, '{ns}:{cat}'.format(
        ns=site.namespace(14), cat=country_config.get('commonsCategoryBase')))
    return {
        'code': country_config.get('country'),
        'lang': country_config.get('lang'),
        'cat': commons_category_base.title(with_ns=False),
        'template': country_config.get('commonsTemplate'),
        'cmt': message
    }


def main():

    countrycode = ''
    lang = ''
    overridecat = ''
    skip_wd = False
    conn = None
    cursor = None

    for arg in pywikibot.handle_args():
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
                'Bad parameters. Expected "-countrycode", "-langcode", '
                '"-overridecat", "-skip_wd" or pywikibot args. '
                'Found "{}"'.format(option))

    if countrycode and lang:
        if not mconfig.countries.get((countrycode, lang)):
            pywikibot.warning(
                'I have no config for countrycode "%s" in language "%s"' % (countrycode, lang))
            return False
        pywikibot.log(
            'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
        countryconfig = mconfig.countries.get((countrycode, lang))
        commonsCatTemplates = getCommonscatTemplates(
            lang, countryconfig.get('project'))
        # print commonsCatTemplates
        (conn, cursor) = connect_to_monuments_database()
        processCountry(countryconfig, commonsCatTemplates, conn, cursor,
                       overridecat=overridecat)
        close_database_connection(conn, cursor)
    elif countrycode or lang:
        raise Exception('The "countrycode" and "langcode" arguments must '
                        'be used together.')
    else:
        statistics = []
        for (countrycode, lang), countryconfig in mconfig.filtered_countries(
                skip_wd=skip_wd):

            if (countrycode, lang) in SKIP_LIST:
                pywikibot.log(
                    'Skipping countrycode "%s" in language "%s"' % (countrycode, lang))
                statistics.append(custom_output_statistics_message(countryconfig, 'skipped: on the skip-list'))
                continue

            pywikibot.log(
                'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
            commonsCatTemplates = getCommonscatTemplates(
                lang, countryconfig.get('project'))
            (conn, cursor) = connect_to_monuments_database()
            try:
                result = processCountry(
                    countryconfig, commonsCatTemplates, conn, cursor)
            except Exception as e:
                pywikibot.error(
                    'Unknown error occurred when processing country '
                    '{0} in lang {1}\n{2}'.format(countrycode, lang, str(e)))
                statistics.append(custom_output_statistics_message(countryconfig, 'failed: unexpected error during processing'))
                continue
            finally:
                close_database_connection(conn, cursor)
            if result:
                statistics.append(result)

        outputStatistics(statistics)


if __name__ == "__main__":
    pywikibot.log('Start of %s' % __file__)
    main()
