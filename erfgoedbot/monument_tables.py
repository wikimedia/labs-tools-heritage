#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
Create the monuments tables SQL from monuments_config.json files

Author: Platonides
"""

import os
import monuments_config as mconfig


def processCountry(countrycode, lang, countryconfig):
    """
    Process the country configs to create sql files.

    @param countrycode: country code or dataset name
    @param lang: language
    @param countryconfig: country configuration
    """
    # These are not listed in the monument config
    extra_cols = "  `source` varchar(510) NOT NULL DEFAULT '',\n" \
                 "  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n"  # noqa E501

    table = countryconfig.get('table')
    sql_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sql")
    f = open(os.path.join(sql_dir, "create_table_%s.sql" % table), "w")
    f.write("DROP TABLE IF EXISTS `%s`;\n" % table)
    f.write("CREATE TABLE IF NOT EXISTS `%s` (\n" % table)

    source_primkey = countryconfig.get('primkey')
    primkey = process_classic_config(f, countryconfig, source_primkey,
                                     extra_cols)

    if not primkey:
        if not isinstance(source_primkey, (str, unicode)):
            primkey = u"`,`".join(source_primkey)
        else:
            raise Exception(
                "Primary key not found for countrycode: %s, lang: %s"
                % (countrycode, lang))

    f.write('  PRIMARY KEY (`%s`),\n' % primkey.encode('utf8'))
    f.write('  KEY `latitude` (`lat`),\n  KEY `longitude` (`lon`)\n')
    f.write(') ENGINE=InnoDB DEFAULT CHARSET=utf8;\n')
    f.close()


def process_classic_config(f, country_config, source_primkey, extra_cols):
    """
    Process a country configuration for wikitext lists.

    @param f: file-like object to write output to
    @param country_config: country configuration
    @param source_primkey: the key to the value used as a primary key
    @param extra_cols: sql for source and changed columns
    @return primkey
    """
    primkey = False
    default_type = "varchar(255)"

    for field in country_config.get('fields'):
        column = field.get('dest')
        if column == '':  # An entry with no dest is intended to be skipped
            continue

        # primkey in config refers to the destination
        if not primkey and source_primkey == field.get('dest'):
            primkey = column

        if column in ['lon', 'lat']:
            f.write(b"  `%s` double DEFAULT NULL,\n" % column.encode('utf8'))
        else:
            # why are we forcing extra_cols to be inserted early?
            if column == 'monument_article':
                f.write(extra_cols)
                extra_cols = ''
            typ = field.get('type') or default_type
            if typ.startswith("int("):
                if field.get('auto_increment'):
                    typ += " NOT NULL AUTO_INCREMENT"
                else:
                    typ += " NOT NULL DEFAULT 0"
            elif typ.startswith("varchar("):
                if field.get('default'):
                    typ += " NOT NULL DEFAULT '%s'" % field.get('default')
                else:
                    typ += " NOT NULL DEFAULT ''"

            f.write(b"  `%s` %s,\n" % (column.encode('utf8'), typ))

    f.write(extra_cols)
    return primkey


def main():
    for (countrycode, lang), countryconfig in mconfig.countries.iteritems():
        processCountry(countrycode, lang, countryconfig)


if __name__ == "__main__":
    try:
        main()
    finally:
        # pywikibot.stopme()
        pass
