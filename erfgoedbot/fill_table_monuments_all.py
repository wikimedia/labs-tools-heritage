#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Create the fill_table_monuments_all SQL."""
from __future__ import unicode_literals
import os
import json
from collections import OrderedDict
import pywikibot


class MonumentsAllSql(object):

    """The full fill_monuments_all generation."""

    def __init__(self, datasets, domain='monuments'):
        """
        Initialize the fill_monuments_all SQL object.

        @param datasets: list of MonumentDatasetSql objects.
        """
        self.domain = domain
        self.datasets = sorted(datasets)
        self.sql_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "sql")

    def make_intro_sql(self):
        """Construct the opening SQL describing the main table."""
        filename = 'monuments_all_intro.sql'  # actually domain neutral
        with open(os.path.join(_get_template_dir(), filename), "r") as f:
            sql = f.read()
        return sql.format(domain=self.domain)

    def make_outro_sql(self):
        """Construct the ending SQL replacing the real table by the new one."""
        filename = 'monuments_all_outro.sql'  # actually domain neutral
        with open(os.path.join(_get_template_dir(), filename), "r") as f:
            sql = f.read()
        return sql.format(domain=self.domain)

    def get_sql(self):
        """Construct the full SQL needed to insert all datasets."""
        return "{intro}\n{data}{outro}".format(
            intro=self.make_intro_sql(),
            data='\n'.join([dataset.get_sql() for dataset in self.datasets]),
            outro=self.make_outro_sql())

    def write_sql(self):
        """Output the SQL to the correct file."""
        filename = "fill_table_{domain}_all.sql".format(domain=self.domain)
        with open(os.path.join(self.sql_dir, filename), "w") as f:
            f.write(self.get_sql().encode('utf-8'))


class MonumentDatasetSql(object):

    """A single dataset (country) in the fill_monuments_all generation."""

    def __init__(self, country, language, table, replacements, where=None):
        """
        Initialize the dataset SQL object.

        @param country: Full text name of country or dataset. E.g. 'Andorra'
            or 'Sweden (Listed historical ships)'.
        @param language: Full text name of the language. E.g. 'Swedish'.
        @param table: Table name (need not be "{domain}_{country}_({lang})")
        @param replacements: Dictionary with target variable as key and
            replacement SQL a value. e.g. {"adm0": "'ad'", "lat": "`lat`"}
        @param where: A WHERE SQL clause, without the "WHERE" (optional).
        """
        self.country = country
        self.language = language
        self.where = where
        self.domain = 'monuments'
        self.dataset = None  # the dataset/country code
        self.lang = None  # the language code
        self.table = table

        self.variables = OrderedDict([
            ('country', None),
            ('lang', None),
            ('project', None),
            ('id', None),
            ('adm0', None),
            ('adm1', None),
            ('adm2', None),
            ('adm3', None),
            ('adm4', None),
            ('name', None),
            ('address', None),
            ('municipality', None),
            ('lat', None),
            ('lon', None),
            ('lat_int', 'ROUND(`lat` * @granularity)'),
            ('lon_int', 'ROUND(`lon` * @granularity)'),
            ('image', None),
            ('wd_item', None),
            ('commonscat', None),
            ('source', None),
            ('changed', None),
            ('monument_article', None),
            ('registrant_url', None)
        ])

        self.load_values(replacements)

    def __lt__(self, other):
        """
        Implement less than to allow for sorting.

        Sorting is done on table name.

        @param other: a second MonumentDatasetSql object.
        """
        return self.table < other.table

    def get_replaced(self):
        """Return the list of replaced variables."""
        replaced = []
        for variable, value in self.variables.iteritems():
            if value is not None:
                replaced.append(variable)
        return replaced

    def make_where_sql(self):
        """Return the formated where clause."""
        if not self.where:
            return ''
        return "\n    WHERE {where}".format(where=self.where)

    def get_sql(self):
        """Construct the full SQL needed to insert a dataset."""
        sql = ("{intro}{variable}\n"
               "    FROM `{table}`{where};\n")
        return sql.format(
            intro=self.make_intro_sql(),
            variable=self.make_varible_sql(),
            where=self.make_where_sql(),
            table=self.table)

    def make_intro_sql(self):
        """Construct the opening SQL listing fields to be replaced."""
        replaced = self.get_replaced()
        sql = ("/* {dataset} in {lang} */\n"
               "REPLACE INTO\n"
               "  `{domain}_all_tmp` (\n"
               "    {replaced}\n"
               ") SELECT\n")
        return sql.format(
            dataset=self.country,
            lang=self.language,
            domain=self.domain,
            replaced=", ".join(["`{}`".format(x) for x in replaced]))

    def make_varible_sql(self):
        """Construct the SQL for mapping country tables variables."""
        sql_lines = []
        for variable, value in self.variables.iteritems():
            if value is not None:
                sql_lines.append("    {val} AS `{var}`".format(
                    val=value, var=variable))
        return ",\n".join(sql_lines)

    def load_values(self, replacements):
        """
        Load the dataset specific replacements into self.variables.

        Does not accept variables other than those in self.variables.
        Automatically handles lat_int and lon_int.

        @param replacements: Dictionary with target variable as key and
            replacement SQL a value. e.g. {"adm0": "'ad'", "lat": "`lat`"}
        """
        required_fields = ('country', 'lang')
        if not all(required in replacements for required in required_fields):
            raise ValueError(
                "All of the required fields '{}' must be replaced".format(
                    "','".join(required_fields)))

        if 'lat' not in replacements:
            self.variables['lat_int'] = None
        if 'lon' not in replacements:
            self.variables['lon_int'] = None

        for variable in self.variables:
            if variable in replacements:
                value = replacements[variable]
                if not isinstance(value, VariableType):
                    raise ValueError(
                        "All variables must be encoded through VariableType, "
                        "'{}' was not".format(variable))
                self.variables[variable] = value.format()

        for target in replacements:
            if target not in self.variables:
                pywikibot.warning(
                    "Unrecognized variable in {table}: {variable}".format(
                        table=self.table, variable=target))


class MonumentWikidataDatasetSql(MonumentDatasetSql):

    """A single dataset (country) in the fill_monuments_all generation."""

    def __init__(self, country, language, table, replacements, where=None):
        """
        Initialize the dataset SQL object.

        @param country: Full text name of country or dataset. E.g. 'Andorra'
            or 'Sweden (Listed historical ships)'.
        @param language: Full text name of the language. E.g. 'Swedish'.
        @param table: Table name (need not be "{domain}_{country}_({lang})")
        @param replacements: Dictionary with target variable as key and
            replacement SQL a value. e.g. {"adm0": "'ad'", "lat": "`lat`"}
        @param where: A WHERE SQL clause, without the "WHERE" (optional).
        """
        super(MonumentWikidataDatasetSql, self).__init__(
            country, language, table, replacements, where)

    def get_replaced(self):
        """Return the list of replaced variables."""
        # the following list is determined by the sql template
        return ['country', 'lang', 'id', 'adm0', 'name', 'address',
                'municipality', 'lat', 'lon', 'lat_int', 'lon_int', 'image',
                'wd_item', 'commonscat', 'source', 'changed',
                'monument_article', 'registrant_url']

    def load_values(self, replacements):
        """
        Load the dataset specific replacements.

        Does not accept variables other than those in self.variables.
        Automatically handles lat_int and lon_int.

        @param replacements: Dictionary with target variable as key and
            replacement SQL a value. e.g. {"adm0": "'ad'", "lat": "`lat`"}
        """
        required_fields = ('dataset', 'lang', 'adm0')
        if not all(required in replacements for required in required_fields):
            raise ValueError(
                "All of the required fields '{}' must be replaced".format(
                    "','".join(required_fields)))

        self.dataset = replacements['dataset'].format()
        self.lang = replacements['lang'].format()
        self.adm0 = replacements['adm0'].format()

    def make_varible_sql(self):
        """Make the main body of the sql file, i.e. the mapping."""
        sql = MonumentWikidataDatasetSql.load_wikidata_template_sql()
        return sql.format(
            dataset=self.dataset,
            lang=self.lang,
            adm0=self.adm0
        )

    @staticmethod
    def load_wikidata_template_sql():
        """Fetch the SQL template for a wikidata config."""
        filename = 'fill_monument_all_wikidata.sql.template'
        filepath = os.path.join(_get_template_dir(), filename)
        with open(filepath, 'r') as f:
            sql = f.read()
        return sql.rstrip()


class VariableType(object):

    """Abstract class to hold the variable type for a replacement variable."""

    def __init__(self, text):
        self.text = text

    def format(self):
        """Output the variable in a sql compatible mode."""
        raise NotImplementedError


class Text(VariableType):

    """A plain string."""

    def format(self):
        return "'{}'".format(self.text)


class Field(VariableType):

    """A field reference."""

    def format(self):
        return "`{}`".format(self.text)


class Raw(VariableType):

    """Raw sql."""

    def format(self):
        return self.text


def _get_config_dir():
    """Return directory containing config files."""
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'monuments_config')


def _get_template_dir():
    """Return directory containing template files."""
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'template')


def _read_config_from_file(config_file):
    """Load config file as json."""
    with open(config_file, 'r') as fp:
        return json.load(fp)


def monuments_dataset_sql_from_json(data):
    """Construct MonumentDatasetSql from json data."""
    sql_data = process_json_data(data['sql_data'])
    cls = MonumentDatasetSql
    if data.get('type') == 'sparql':
        cls = MonumentWikidataDatasetSql
    return cls(data['sql_country'], data['sql_lang'],
               data['table'], sql_data, data.get('sql_where'))


def process_json_data(data):
    """Convert loaded sql data entries to objects."""
    mapping = {
        'Text': Text,
        'Field': Field,
        'Raw': Raw
    }
    for k, v in data.iteritems():
        try:
            func = mapping.get(v['type'])
            data[k] = func(v['value'])
        except TypeError:
            raise ValueError('Unknown type detected: {}'.format(v['type']))
    return data


def get_all_dataset_sql(domain='monuments'):
    """Return all MonumentDatasetSql which can be constructed from configs."""
    datasets = []

    config_dir = _get_config_dir()
    for filename in os.listdir(config_dir):
        base, ext = os.path.splitext(filename)
        if ext != '.json':
            continue
        config_file = os.path.join(config_dir, filename)
        data = _read_config_from_file(config_file)
        if not data.get('table').startswith(domain):  # skip e.g. wlpa ones
            continue
        datasets.append(monuments_dataset_sql_from_json(data))
    return datasets


def make_fill_monuments_all(domain='monuments'):
    """Make and write the fill_monuments_all.sql file."""
    datasets = get_all_dataset_sql(domain)
    MonumentsAllSql(datasets, domain).write_sql()


if __name__ == "__main__":
    make_fill_monuments_all()
