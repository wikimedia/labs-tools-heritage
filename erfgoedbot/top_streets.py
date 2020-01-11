#!/usr/bin/python
# -*- coding: utf-8  -*-
'''
Make a list of top streets for a municipality. Bot expects two things on the commandline:
* -countrycode : The country code (as it is in the database)
* -langcode : The language code (as it is in the database)
* -municipality : The name of the municipality (as it is in the database)
* -minimum : (optional) The minimum of hits before we show the item
'''
from collections import Counter

import pywikibot

from erfgoedbot.database_connection import (
    close_database_connection,
    connect_to_monuments_database
)


def getAddresses(countrycode, lang, municipality, conn, cursor):
    '''
    Get a list of addresses of a municipality in a country in a certain language
    '''
    result = []
    query = (
        "SELECT address "
        "FROM monuments_all "
        "WHERE country=%s AND lang=%s AND municipality=%s "
        "ORDER BY address ASC")
    cursor.execute(query, (countrycode, lang, municipality))

    while True:
        try:
            row = cursor.fetchone()
            (address,) = row
            result.append(address)
        except TypeError:
            break

    return result


def printTopStreets(addresses, minimum):
    '''
    Print the top streets with a minimum number of hits
    '''
    streets = Counter()  # collections.Counter
    for address in addresses:
        address = address.replace('{{sorteer|', '')
        temp = ''
        partslist = []
        for addrPart in address.split(' '):
            temp += ' ' + addrPart
            partslist.append(temp.strip())

        streets.update(partslist)

    topStreets = []

    for street in streets.most_common():
        if street[1] < minimum:
            break
        topStreets.append(street[0])

    filteredStreets = []

    for topStreet1 in topStreets:
        for topStreet2 in topStreets:
            if topStreet1 != topStreet2 and topStreet2.startswith(topStreet1):
                filteredStreets.append(topStreet1)
                break

    pywikibot.output('Filtered out the following. These are probably '
                     'street parts:')
    for street in streets.most_common():
        if street[1] < minimum:
            break
        if street[0] in filteredStreets:
            pywikibot.output('* %s - %s' % street)

    pywikibot.output('Found the following entries which are probably '
                     'real streets:')
    for street in streets.most_common():
        if street[1] < minimum:
            break
        if not street[0] in filteredStreets:
            pywikibot.output('* %s - %s' % street)


def main():
    countrycode = ''
    lang = ''
    municipality = ''
    minimum = 15
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
        elif option == '-municipality':
            municipality = value
        elif option == '-minimum':
            minimum = int(value)
        else:
            raise Exception(
                'Bad parameters. Expected "-countrycode", "-langcode", '
                '"-municipality", "-minimum" or pywikibot args. '
                'Found "{}"'.format(option))

    if countrycode and lang and municipality:
        addresses = getAddresses(countrycode, lang, municipality, conn, cursor)
        printTopStreets(addresses, minimum)
    else:
        print('Usage')

    close_database_connection(conn, cursor)


if __name__ == "__main__":
    pywikibot.log('Start of %s' % __file__)
    try:
        main()
    finally:
        pywikibot.stopme()
