#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
Create the monuments tables SQL from monuments_config.json files

Author: Platonides
"""
import os
import monuments_config as mconfig


def processCountry(country_code, lang, country_config):
    """
    Process the country configs to create sql files.

    @param countrycode: country code or dataset name
    @param lang: language
    @param countryconfig: country configuration
    """
    # @todo: standardise these as 'monuments_{country}_({lang})'
    table = country_config.get('table')

    try:
        if country_config.get('type') == 'sparql':
            sql = process_wikidata_config(country_config)
        else:
            sql = process_classic_config(country_config)
    except Exception as e:
        raise Exception(
            '{exception} for countrycode: {country}, lang: {lang}'.format(
                exception=e, country=country_code, lang=lang))

    f = open(os.path.join(
        get_sql_dir(), 'create_table_{}.sql'.format(table)), 'w')
    f.write(sql)
    f.close()


def process_classic_config(country_config):
    """
    Process a country configuration for wikitext lists.

    @param country_config: country configuration
    @return sql
    """
    primkey = False
    default_type = 'varchar(255)'
    source_primkey = country_config.get('primkey')
    fields_sql = []

    for field in country_config.get('fields'):
        column = field.get('dest')
        if column == '':  # An entry with no dest is intended to be skipped
            continue

        # primkey in config refers to the destination
        if not primkey and source_primkey == field.get('dest'):
            primkey = column

        if column in ['lon', 'lat']:
            fields_sql.append(
                b'`{}` double DEFAULT NULL,'.format(column.encode('utf8')))
        else:
            typ = field.get('type') or default_type
            if typ.startswith('int('):
                if field.get('auto_increment'):
                    typ += ' NOT NULL AUTO_INCREMENT'
                else:
                    typ += ' NOT NULL DEFAULT 0'
            elif typ.startswith("varchar("):
                if field.get('default'):
                    typ += " NOT NULL DEFAULT '{}'".format(
                        field.get('default'))
                else:
                    typ += " NOT NULL DEFAULT ''"

            fields_sql.append(b'`{}` {},'.format(column.encode('utf8'), typ))

    try:
        primkey = validate_primkey(source_primkey, primkey)
    except:
        raise

    sql = load_classic_template_sql().format(
        table=country_config['table'],
        rows=b'\n  '.join(fields_sql),
        primkey=primkey.encode('utf8'))

    return sql


def validate_primkey(source_primkey, primkey):
    """
    Validate that the primkey was found or construct it from list.

    @param source_primkey: the config data on the primkey
    @param primkey: the primkey, if matched
    @return primkey
    @raises Exception
    """
    if not primkey:
        if source_primkey and not isinstance(source_primkey, (str, unicode)):
            primkey = u"`,`".join(source_primkey)
        else:
            raise Exception('Primary key not found')
    return primkey


def load_classic_template_sql():
    """Fetch the SQL template for a wikidata config."""
    filename = 'classic_table.sql.template'
    with open(os.path.join(get_template_dir(), filename), 'r') as f:
        sql = f.read()
    return sql


def process_wikidata_config(country_config):
    """
    Process a country configuration for wikidata sparql queries.

    @param country_config: country configuration
    @return sql
    """
    sql = load_wikidata_template_sql().format(
        table=country_config['table'])
    return sql


def load_wikidata_template_sql():
    """Fetch the SQL template for a wikidata config."""
    filename = 'wikidata_table_template.sql'
    with open(os.path.join(get_template_dir(), filename), 'r') as f:
        sql = f.read()
    return sql


def get_sql_dir():
    """Fetch the SQL template for a wikidata config."""
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'sql')


def get_template_dir():
    """Fetch the SQL template for a wikidata config."""
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'template')


def main():
    for (countrycode, lang), countryconfig in mconfig.countries.iteritems():
        processCountry(countrycode, lang, countryconfig)


if __name__ == "__main__":
    try:
        main()
    finally:
        # pywikibot.stopme()
        pass
