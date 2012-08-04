#!/usr/bin/python
# -*- coding: utf-8  -*-
'''
Create the monuments tables SQL from monuments_config.py

Author: Platonides
'''
import sys, time, warnings
import monuments_config as mconfig
sys.path.append("/home/project/e/r/f/erfgoed/pywikipedia")
#import wikipedia, MySQLdb, config, re, pagegenerators

def processCountry(countrycode, lang, countryconfig):
	extra_cols = "  `source` varchar(255) NOT NULL DEFAULT '',\n" "  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n" # These are not listed in the monument config
	
	table = countryconfig.get('table')
	f = open("sql/create_table_" + table + ".sql","w")
	f.write("connect " + mconfig.db + " " + mconfig.db_server + ";\n")
	f.write("DROP TABLE IF EXISTS `" + table + "`;\n")
	f.write("CREATE TABLE IF NOT EXISTS `" + table + "` (\n")
	
	source_primkey = countryconfig.get('primkey')
	primkey = False
	
	for field in countryconfig.get('fields'):
		column = field.get('dest')
		if column == '': # An entry with no dest is intended to be skipped
			continue
		
		if not primkey and source_primkey == field.get('dest'): # primkey in config refers to the destination
			primkey = column
		
		if column in ['lon', 'lat']:
			f.write(b'  `' + column.encode('utf8') + b"` double DEFAULT NULL,\n")
		else:
			if column == 'monument_article':
				f.write(extra_cols)
				extra_cols =''
			type = field.get('type')
			if not type:
				type = "varchar(255) NOT NULL DEFAULT "
				if field.get('default'):
					type += "'" + field.get('default') + "'"
				else:
					type += "''"
			elif type.startswith("int("):
				if field.get('auto_increment'):
					type += " NOT NULL AUTO_INCREMENT"
				else:
					type += " NOT NULL DEFAULT  0"
			elif type.startswith("varchar("):
				if field.get('default'):
					type += " NOT NULL DEFAULT '" + field.get('default') + "'"
				else:
					type += " NOT NULL DEFAULT ''"
				
			f.write(b'  `' + column.encode('utf8') + b"` " + type + ",\n")
	
	f.write(extra_cols)
	
	if not primkey:
		if not isinstance(source_primkey, (str, unicode)):
			primkey = u"`,`".join(source_primkey)
		else:
			raise Exception("Primary key not found for countrycode: " + countrycode + ", lang: " + lang)
	
	f.write('  PRIMARY KEY (`' + primkey.encode('utf8') + '`),\n')
	f.write('  KEY `latitude` (`lat`),\n  KEY `longitude` (`lon`)\n')
	f.write(') ENGINE=MyISAM DEFAULT CHARSET=utf8;\n')
	f.close()

def main():
	for (countrycode, lang), countryconfig in mconfig.countries.iteritems():
		processCountry(countrycode, lang, countryconfig)

if __name__ == "__main__":
	try:
		main()
	finally:
		#wikipedia.stopme()
		pass
