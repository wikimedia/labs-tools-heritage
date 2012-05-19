#!/usr/bin/python
# -*- coding: utf-8  -*-
'''
Make a list of top streets for a municipality. Bot expects two things on the commandline:
* -countrycode : The country code (as it is in the database)
* -municipality : The name of the municipality (as it is in the database)
* -minimum : (optional) The minimum of hits before we show the item
'''
import sys
import monuments_config as mconfig
sys.path.append("/home/project/e/r/f/erfgoed/pywikipedia")
import wikipedia, config
import MySQLdb, time
from collections import Counter

def connectDatabase():
    '''
    Connect to the monuments mysql database, if it fails, go down in flames.
    This database is utf-8 encoded.
    '''
    conn = MySQLdb.connect(host=mconfig.db_server, db=mconfig.db, user = config.db_username, passwd = config.db_password, use_unicode=True, charset='utf8')
    cursor = conn.cursor()
    return (conn, cursor)

def getAddresses(countrycode, lang, municipality, conn, cursor):
    '''
    Get a list of addresses of a municipality in a country in a certain language
    '''
    result = []
    query = u"""SELECT address FROM monuments_all WHERE country=%s AND lang=%s AND municipality=%s ORDER BY address ASC""";
    cursor.execute(query, (countrycode, lang, municipality))
    
    while True:
	try:
	    row = cursor.fetchone()
	    (address,) = row
	    result.append(address)
	except TypeError:
	    break
    
    return result

def printTopStreets (addresses, minimum):
    '''
    Print the top streets with a minimum number of hits
    '''
    streets = Counter() #collections.Counter
    for address in addresses:
	address = address.replace(u'{{sorteer|', u'')
	temp = u''
	partslist = []
	for addrPart in address.split(u' '):
	    temp = temp + u' ' + addrPart
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

    wikipedia.output(u'Filtered out the following. These are probably street parts:')
    for street in streets.most_common():
	if street[1] < minimum:
	    break
	if street[0] in filteredStreets:
	    wikipedia.output(u'* %s - %s' % street)

    wikipedia.output(u'Found the following entries which are probably real streets:')
    for street in streets.most_common():
	if street[1] < minimum:
	    break
	if not street[0] in filteredStreets:
	    wikipedia.output(u'* %s - %s' % street)


def main():
    countrycode = u''
    lang = u''
    municipality = u''
    minimum = 15
    conn = None
    cursor = None
    # Connect database, we need that
    (conn, cursor) = connectDatabase()
    
    for arg in wikipedia.handleArgs():
        if arg.startswith('-countrycode:'):
            countrycode = arg [len('-countrycode:'):]
	elif arg.startswith('-municipality:'):
	    municipality = arg [len('-municipality:'):]
	elif arg.startswith('-minimum:'):
	    minimum = int(arg [len('-minimum:'):])

    if countrycode and municipality:
	lang = wikipedia.getSite().language()
	addresses = getAddresses(countrycode, lang, municipality, conn, cursor)
	printTopStreets (addresses, minimum)
    else:
	print u'Usage'

if __name__ == "__main__":
    try:
        main()
    finally:
        wikipedia.stopme()
