#!/usr/bin/python
# -*- coding: utf-8  -*-
'''
Configuration for the monuments bot.

'''

db_server='sql.toolserver.org'
db = 'p_erfgoed_p'

countries = {
    'nl' : {
        'project' : 'wikipedia',
	'lang' : 'nl',
	'headerTemplate' : 'Tabelkop rijksmonumenten',
	'rowTemplate' : 'Tabelrij rijksmonument',
	'namespaces' : [0],
	'table' : 'monuments_nl',
	'fields' : [
	    {
		'source' : 'objrijksnr',
		'dest' : 'objrijksnr',
		'conv' : '',
	    },
	    {
		'source' : 'woonplaats',
		'dest' : 'woonplaats',
		'conv' : '',
	    },
	    {
		'source' : 'adres',
		'dest' : 'adres',
		'conv' : '',
	    },
	    {
		'source' : 'objectnaam',
		'dest' : 'objectnaam',
		'conv' : '',
	    },
	    {
		'source' : 'type_obj',
		'dest' : 'type_obj',
		'conv' : '',
	    },
	    {
		'source' : 'oorspr_functie',
		'dest' : 'oorspr_functie',
		'conv' : '',
	    },
	    {
		'source' : 'bouwjaar',
		'dest' : 'bouwjaar',
		'conv' : '',
	    },
	    {
		'source' : 'architect',
		'dest' : 'architect',
		'conv' : '',
	    },
	    {
		'source' : 'cbs_tekst',
		'dest' : 'cbs_tekst',
		'conv' : '',
	    },
	    {
		'source' : 'RD_x',
		'dest' : '',
		'conv' : '',
	    },
	    {
		'source' : 'RD_y',
		'dest' : '',
		'conv' : '',
	    },
	    {
		'source' : 'lat',
		'dest' : 'lat',
		'conv' : '',
	    },
	    {
		'source' : 'lon',
		'dest' : 'lon',
		'conv' : '',
	    },
	    {
		'source' : 'image',
		'dest' : 'image',
		'conv' : '',
	    },
	    {
		'source' : 'postcode',
		'dest' : '',
		'conv' : '',
	    },
	    {
		'source' : 'buurt',
		'dest' : '',
		'conv' : '',
	    },
	],
    },
    'ch' : {
	'project' : 'wikipedia',
	'lang' : 'en',
	'headerTemplate' : 'SIoCPoNaRS header',
	'rowTemplate' : 'SIoCPoNaRS row',
	'namespaces' : [0],
	'table' : 'monuments_ch',
	'fields' : [
	    {
		'source' : 'KGS_nr',
		'dest' : 'kgs_nr',
		'conv' : '',
	    },
	    {
		'source' : 'name',
		'dest' : 'name',
		'conv' : '',
	    },
	    {
		'source' : 'address',
		'dest' : 'address',
		'conv' : '',
	    },
	    {
		'source' : 'municipality',
		'dest' : 'municipality',
		'conv' : '',
	    },
	    {
		'source' : 'CH1903_X',
		'dest' : 'lat',
		'conv' : 'CH1903ToLat',
	    },
	    {
		'source' : 'CH1903_Y',
		'dest' : 'lon',
		'conv' : 'CH1903ToLon',
	    },
	    {
		'source' : 'image',
		'dest' : 'image',
		'conv' : '',
	    },
	]
    }
}

