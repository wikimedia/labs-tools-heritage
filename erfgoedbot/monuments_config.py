#!/usr/bin/python
# -*- coding: utf-8  -*-
'''
Configuration for the monuments bot.

'''
import os
import json


def _get_config_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'monuments_config')


def _read_config_from_file(config_file):
    with open(config_file, 'r') as fp:
        return json.load(fp)


def _read_country_config(config_file):
    data = _read_config_from_file(config_file)
    # Trick to convert back into tuples
    if type(data['primkey']) is list:
        data['primkey'] = tuple(data['primkey'])
    return data


def get_countries():
    countries = {}

    config_dir = _get_config_dir()
    for filename in os.listdir(config_dir):
        config_file = os.path.join(config_dir, filename)
        data = _read_country_config(config_file)
        key = (data['country'], data['lang'])
        countries[key] = data
    return countries


countries = get_countries()
