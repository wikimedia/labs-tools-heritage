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
import monuments_config as mconfig
import pywikibot
import MySQLdb
from pywikibot import config
from pywikibot import pagegenerators

from converters import (
    extract_elements_from_template_param
)


def connectDatabase():
    '''
    Connect to the mysql database, if it fails, go down in flames
    '''
    conn = MySQLdb.connect(host=mconfig.db_server, db=mconfig.db, user=config.db_username,
                           passwd=config.db_password, use_unicode=True, charset='utf8')
    conn.ping(True)
    cursor = conn.cursor()
    return (conn, cursor)


def updateMonument(countrycode, lang, identifier, source, countryconfig, conn, cursor):
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
    fieldvalues.append(countrycode)
    fieldnames.append('lang')
    fieldvalues.append(lang)

    query = u"""INSERT INTO `id_dump`("""

    j = 0
    for fieldname in fieldnames:
        if j == 0:
            query = query + u"""`%s`""" % (fieldname,)
        else:
            query = query + u""", `%s`""" % (fieldname,)
        j = j + 1

    query = query + u""") VALUES ("""

    j = 0
    for fieldvalue in fieldvalues:
        if j == 0:
            query = query + u"""%s"""
        else:
            query = query + u""", %s"""
        j = j + 1

    query = query + u""")"""
    cursor.execute(query, fieldvalues)


def processMonument(countrycode, lang, params, source, countryconfig, conn, cursor):
    '''
    Process a single instance of a monument row template
    '''

    identifier = u''

    for param in params:
        (field, value) = extract_elements_from_template_param(param)

        if (field == countryconfig.get('primkey')):
            identifier = value

    updateMonument(countrycode, lang, identifier, source, countryconfig, conn, cursor)


def processPage(countrycode, lang, source, countryconfig, conn, cursor, page=None):
    '''
    Process a page containing one or multiple instances of the monument row template
    '''
    templates = page.templatesWithParams()

    for (template, params) in templates:
        template_name = template.title(withNamespace=False)
        if template_name == countryconfig.get('rowTemplate'):
            processMonument(
                countrycode, lang, params, source, countryconfig, conn, cursor)


def processCountry(countrycode, lang, countryconfig, conn, cursor):
    '''
    Process all the monuments of one country
    '''

    site = pywikibot.getSite(
        countryconfig.get('lang'), countryconfig.get('project'))
    rowTemplate = pywikibot.Page(
        site, u'%s:%s' % (site.namespace(10), countryconfig.get('rowTemplate')))

    transGen = pagegenerators.ReferringPageGenerator(
        rowTemplate, onlyTemplateInclusion=True)
    filteredGen = pagegenerators.NamespaceFilterPageGenerator(
        transGen, countryconfig.get('namespaces'))
    pregenerator = pagegenerators.PreloadingGenerator(filteredGen)
    for page in pregenerator:
        if page.exists() and not page.isRedirectPage():
            # Do some checking
            processPage(countrycode, lang,
                        page.permalink(), countryconfig, conn, cursor, page=page)


def main():
    '''
    The main loop
    '''
    # First find out what to work on

    countrycode = u''
    conn = None
    cursor = None
    (conn, cursor) = connectDatabase()

    for arg in pywikibot.handleArgs():
        option, sep, value = arg.partition(':')
        if option == '-countrycode':
            countrycode = value

    query = u"""TRUNCATE table `id_dump`"""
    cursor.execute(query)

    if countrycode:
        lang = pywikibot.getSite().language()
        if not mconfig.countries.get((countrycode, lang)):
            pywikibot.warning(
                u'I have no config for countrycode "%s" in language "%s"' % (countrycode, lang))
            return False
        pywikibot.log(
            u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
        processCountry(
            countrycode, lang, mconfig.countries.get((countrycode, lang)), conn, cursor)
    else:
        for (countrycode, lang), countryconfig in mconfig.countries.iteritems():
            pywikibot.log(
                u'Working on countrycode "%s" in language "%s"' % (countrycode, lang))
            processCountry(countrycode, lang, countryconfig, conn, cursor)

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
