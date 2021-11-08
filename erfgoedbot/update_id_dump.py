#!/usr/bin/python
# $ -l h_rt=0:30:00
# $ -j y
# $ -o $HOME/erfgoedbot/update_id_dump.out
# -*- coding: utf-8  -*-
'''
Update the id_dump table from some wiki page(s)

Usage:
# loop through all countries
python update_id_dump.py


'''
import pywikibot
from pywikibot import pagegenerators

import erfgoedbot.monuments_config as mconfig
from erfgoedbot.converters import extract_elements_from_template_param
from erfgoedbot.database_connection import (
    close_database_connection,
    connect_to_monuments_database
)


def updateMonument(countryconfig, identifier, source, conn, cursor):
    '''
    FIXME :  cursor.execute(query, (tuple)) om het escape probleem te fixen
    '''
    fieldnames = []
    fieldvalues = []

    fieldnames.append('source')
    fieldvalues.append(source)
    fieldnames.append('id')
    fieldvalues.append(identifier)
    fieldnames.append('country')
    fieldvalues.append(countryconfig.get('country'))
    fieldnames.append('lang')
    fieldvalues.append(countryconfig.get('lang'))

    query = """INSERT INTO `id_dump`("""

    j = 0
    for fieldname in fieldnames:
        if j == 0:
            query += """`%s`""" % (fieldname,)
        else:
            query += """, `%s`""" % (fieldname,)
        j += 1

    query += """) VALUES ("""

    j = 0
    for fieldvalue in fieldvalues:
        if j == 0:
            query += """%s"""
        else:
            query += """, %s"""
        j += 1

    query += """)"""
    cursor.execute(query, fieldvalues)


def processMonument(countryconfig, params, source, conn, cursor):
    '''
    Process a single instance of a monument row template
    '''

    identifier = ''

    for param in params:
        (field, value) = extract_elements_from_template_param(param)

        if (field == countryconfig.get('primkey')):
            identifier = value

    updateMonument(countryconfig, identifier, source, conn, cursor)


def processPage(countryconfig, source, conn, cursor, page=None):
    '''
    Process a page containing one or multiple instances of the monument row template
    '''
    templates = page.templatesWithParams()

    for (template, params) in templates:
        template_name = template.title(with_ns=False)
        if template_name == countryconfig.get('rowTemplate'):
            processMonument(countryconfig, params, source, conn, cursor)


def processCountry(countryconfig, conn, cursor):
    '''
    Process all the monuments of one country
    '''

    site = pywikibot.getSite(
        countryconfig.get('lang'), countryconfig.get('project'))
    rowTemplate = pywikibot.Page(
        site, '%s:%s' % (site.namespace(10), countryconfig.get('rowTemplate')))

    transGen = rowTemplate.getReferences(only_template_inclusion=True)
    filteredGen = pagegenerators.NamespaceFilterPageGenerator(
        transGen, countryconfig.get('namespaces'))
    pregenerator = pagegenerators.PreloadingGenerator(filteredGen)
    for page in pregenerator:
        if page.exists() and not page.isRedirectPage():
            # Do some checking
            processPage(countryconfig, page.permalink(percent_encoded=False),
                        conn, cursor, page=page)


def main():
    '''
    The main loop
    '''
    # First find out what to work on

    countrycode = ''
    lang = ''
    skip_wd = False
    conn = None
    cursor = None
    (conn, cursor) = connect_to_monuments_database()

    for arg in pywikibot.handle_args():
        option, sep, value = arg.partition(':')
        if option == '-countrycode':
            countrycode = value
        elif option == '-langcode':
            lang = value
        elif option == '-skip_wd':
            skip_wd = True
        else:
            raise Exception(
                'Bad parameters. Expected "-countrycode", "-langcode", '
                '"-skip_wd" or pywikibot args. Found "{}"'.format(option))

    query = """TRUNCATE table `id_dump`"""
    cursor.execute(query)

    if countrycode and lang:
        if not mconfig.countries.get((countrycode, lang)):
            pywikibot.warning(
                'I have no config for countrycode "%s" in language "%s"' % (countrycode, lang))
            return False
        pywikibot.log(
            'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
        processCountry(
            mconfig.countries.get((countrycode, lang)), conn, cursor)
    elif countrycode or lang:
        raise Exception('The "countrycode" and "langcode" arguments must '
                        'be used together.')
    else:
        for (countrycode, lang), countryconfig in mconfig.filtered_countries(
                skip_wd=skip_wd):
            pywikibot.log(
                'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
            try:
                processCountry(countryconfig, conn, cursor)
            except Exception as e:
                pywikibot.error(
                    'Unknown error occurred when processing country '
                    '{0} in lang {1}\n{2}'.format(countrycode, lang, str(e)))
                continue

    close_database_connection(conn, cursor)


if __name__ == "__main__":
    pywikibot.log('Start of %s' % __file__)
    try:
        main()
    finally:
        pywikibot.stopme()
