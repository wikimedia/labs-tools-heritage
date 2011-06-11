#!/usr/bin/python
# -*- coding: utf-8  -*-
'''
Configuration for the monuments bot.

'''

db_server='sql.toolserver.org'
db = 'p_erfgoed_p'

countries = {
    ('ad', 'ca') : {
        'project' : 'wikipedia',
	'lang' : 'ca',
	'headerTemplate' : 'Capçalera BIC And',
	'rowTemplate' : 'Filera BIC And',
	'namespaces' : [0],
	'table' : 'monuments_ad_(ca)',
	'truncate' : False,
	'primkey' : 'id',
	'fields' : [
	    {
		'source' : 'id',
		'dest' : 'id',
		'conv' : '',
	    },
            {
		'source' : 'nom',
		'dest' : 'nom',
		'conv' : '',
	    },
            {
		'source' : 'estil',
		'dest' : 'estil',
		'conv' : '',
	    },
            {
		'source' : u'època',
		'dest' : 'epoca',
		'conv' : '',
	    },
            {
		'source' : 'municipi',
		'dest' : 'municipi',
		'conv' : '',
	    },
            {
		'source' : 'lloc',
		'dest' : 'lloc',
		'conv' : '',
	    },            {
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
		'source' : 'nomcoor',
		'dest' : 'nomcoor',
		'conv' : '',
	    },
            {
		'source' : 'imatge',
		'dest' : 'imatge',
		'conv' : '',
	    },
	],
    },
    ('be-vlg', 'nl') : {
	'project' : 'wikipedia',
	'lang' : 'nl',
	'headerTemplate' : 'Tabelkop erfgoed Vlaanderen',
	'rowTemplate' : 'Tabelrij erfgoed Vlaanderen',
        'commonsTemplate' : 'Onroerend erfgoed',
        'commonsTrackerCategory' : 'Onroerend erfgoed with known IDs',
        'commonsCategoryBase' : 'Onroerend erfgoed',
        'unusedImagesPage' : 'Wikipedia:Wikiproject/Erfgoed/Belgische Erfgoed Inventarisatie/Ongebruikte foto\'s',
        'imagesWithoutIdPage' : 'Wikipedia:Wikiproject/Erfgoed/Belgische Erfgoed Inventarisatie/Foto\'s zonder id',
	'namespaces' : [0],
	'table' : 'monuments_be-vlg_(nl)',
	'truncate' : False,
	'primkey' : 'id',
	'fields' : [
	    {
		'source' : 'id',
		'dest' : 'id',
		'conv' : '',
	    },
	    {
		'source' : 'gemeente',
		'dest' : 'gemeente',
		'conv' : '',
	    },
	    {
		'source' : 'deelgem',
		'dest' : 'deelgem',
		'conv' : '',
	    },
	    {
		'source' : 'deelgem_id',
		'dest' : '',
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
	],
    },
    ('be-wal', 'nl') : {
	'project' : 'wikipedia',
	'lang' : 'nl',
	'headerTemplate' : 'Tabelkop erfgoed Wallonië',
	'rowTemplate' : 'Tabelrij erfgoed Wallonië',
        'commonsTemplate' : '',
        'commonsTrackerCategory' : '',
        'commonsCategoryBase' : '',
        'unusedImagesPage' : '',
        'imagesWithoutIdPage' : '',
	'namespaces' : [0],
	'table' : 'monuments_be-wal_(nl)',
	'truncate' : False,
	'primkey' : ('niscode', 'objcode'),
	'fields' : [
	    {
		'source' : 'niscode',
		'dest' : 'niscode',
		'conv' : '',
	    },
	    {
		'source' : 'objcode',
		'dest' : 'objcode',
		'conv' : '',
	    },
            {
		'source' : 'descr_nl',
		'dest' : 'descr_nl',
		'conv' : '',
	    },
            {
		'source' : 'descr_fr',
		'dest' : 'descr_fr',
		'conv' : '',
	    },
	    {
		'source' : 'gemeente',
		'dest' : 'gemeente',
		'conv' : '',
	    },
	    {
		'source' : 'deelgem',
		'dest' : 'deelgem',
		'conv' : '',
	    },
	    {
		'source' : 'adres',
		'dest' : 'adres',
		'conv' : '',
	    },
	    {
		'source' : 'objtype',
		'dest' : 'objtype',
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
		'source' : 'architect',
		'dest' : 'architect',
		'conv' : '',
	    },
	    {
		'source' : 'bouwjaar',
		'dest' : 'bouwjaar',
		'conv' : '',
	    },
	    {
		'source' : 'image',
		'dest' : 'image',
		'conv' : '',
	    },
	],
    },
    ('ch', 'en') : {
	'project' : 'wikipedia',
	'lang' : 'en',
	'headerTemplate' : 'SIoCPoNaRS header',
	'rowTemplate' : 'SIoCPoNaRS row',
	'namespaces' : [0],
	'table' : 'monuments_ch_(en)',
	'truncate' : True,
	'primkey' : 'KGS_nr',
	'fields' : [
	    {
		'source' : 'KGS_nr',
		'dest' : '',
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
    },
    ('ee', 'et') : {
	'project' : 'wikipedia',
	'lang' : 'et',
	'headerTemplate' : 'KRR päis',
	'rowTemplate' : 'KRR rida',
        'commonsTemplate' : 'Kultuurimälestis',
        'commonsTrackerCategory' : 'Cultural heritage monuments in Estonia (with known IDs)',
        'commonsCategoryBase' : 'Cultural heritage monuments in Estonia',
        'unusedImagesPage' : 'Vikipeedia:Vikiprojekt_Kultuuripärand/Kasutamata kultuurimälestiste pildid',
        'imagesWithoutIdPage' : 'Vikipeedia:Vikiprojekt_Kultuuripärand/Ilma registri numbrita pildid',    
	'namespaces' : [4],
	'table' : 'monuments_ee_(et)',
	'truncate' : False,
	'primkey' : 'number',
	'fields' : [
	    {
		'source' : 'number',
		'dest' : 'number',
		'conv' : '',
	    },
	    {
		'source' : 'nimi',
		'dest' : 'nimi',
		'conv' : '',
	    },
	    {
		'source' : 'liik',
		'dest' : 'liik',
		'conv' : '',
	    },
	    {
		'source' : 'aadress',
		'dest' : 'aadress',
		'conv' : '',
	    },
	    {
		'source' : 'omavalitsus',
		'dest' : 'omavalitsus',
		'conv' : '',
	    },
            {
		'source' : 'NS',
		'dest' : 'lat',
		'conv' : '',
	    },
	    {
		'source' : 'EW',
		'dest' : 'lon',
		'conv' : '',
	    },
	    {
		'source' : 'pilt',
		'dest' : 'pilt',
		'conv' : '',
	    },
	    {
		'source' : 'commons',
		'dest' : 'commons',
		'conv' : '',
	    },
	]
    },
    ('es', 'ca') : {
        'project' : 'wikipedia',
	'lang' : 'ca',
	'headerTemplate' : u'Capçalera BIC',
	'rowTemplate' : 'Filera BIC',
        'commonsTemplate' : 'BIC',
        'commonsTrackerCategory' : 'Cultural heritage monuments in Spain with known IDs',
        'commonsCategoryBase' : 'Cultural heritage monuments in Spain',
        'unusedImagesPage' : 'User:Multichill/Unused BIC',
        'imagesWithoutIdPage' : 'User:Multichill/BIC without id',
	'namespaces' : [0],
	'table' : 'monuments_es_(ca)',
	'truncate' : False,
	'primkey' : 'bic',
	'fields' : [
	    {
		'source' : 'bic',
		'dest' : 'bic',
		'conv' : '',
	    },
            {
		'source' : 'nom',
		'dest' : 'nom',
		'conv' : '',
	    },
            {
		'source' : 'tipus',
		'dest' : 'tipus',
		'conv' : '',
	    },            {
		'source' : 'municipi',
		'dest' : 'municipi',
		'conv' : '',
	    },
            {
		'source' : 'lloc',
		'dest' : 'lloc',
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
		'source' : 'nomcoor',
		'dest' : 'nomcoor',
		'conv' : '',
	    },
            {
		'source' : 'imatge',
		'dest' : 'imatge',
		'conv' : '',
	    },
	],
    },
    ('es', 'es') : {
        'project' : 'wikipedia',
	'lang' : 'es',
	'headerTemplate' : 'Cabecera BIC',
	'rowTemplate' : 'Fila BIC',
        'commonsTemplate' : 'BIC',
        'commonsTrackerCategory' : 'Cultural heritage monuments in Spain with known IDs',
        'commonsCategoryBase' : 'Cultural heritage monuments in Spain',
        'unusedImagesPage' : 'User:Multichill/Unused BIC',
        'imagesWithoutIdPage' : 'User:Multichill/BIC without id',
	'namespaces' : [104],
	'table' : 'monuments_es_(es)',
	'truncate' : False,
	'primkey' : 'bic',
	'fields' : [
	    {
		'source' : 'bic',
		'dest' : 'bic',
		'conv' : '',
	    },
            {
		'source' : 'nombre',
		'dest' : 'nombre',
		'conv' : '',
	    },
            {
		'source' : 'nombrecoor',
		'dest' : 'nombrecoor',
		'conv' : '',
	    },
            {
		'source' : 'tipobic',
		'dest' : 'tipobic',
		'conv' : '',
	    },
            {
		'source' : 'tipo',
		'dest' : 'tipo',
		'conv' : '',
	    },
            {
		'source' : 'municipio',
		'dest' : 'municipio',
		'conv' : '',
	    },
            {
		'source' : 'lugar',
		'dest' : 'lugar',
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
		'source' : 'fecha',
		'dest' : 'fecha',
		'conv' : '',
	    },
            {
		'source' : 'imagen',
		'dest' : 'imagen',
		'conv' : '',
	    },
	],
    },
    ('es-ct', 'ca') : {
        'project' : 'wikipedia',
	'lang' : 'ca',
	'headerTemplate' : 'Capçalera BCIN',
	'rowTemplate' : 'Filera BCIN',
	'namespaces' : [0],
	'table' : 'monuments_es-ct_(ca)',
	'truncate' : False,
	'primkey' : 'bic',
	'fields' : [
	    {
		'source' : 'bic',
		'dest' : 'bic',
		'conv' : '',
	    },
	    {
		'source' : 'idurl',
		'dest' : 'idurl',
		'conv' : '',
	    },
	    {
		'source' : 'bcin',
		'dest' : 'bcin',
		'conv' : '',
	    },
            {
		'source' : 'nom',
		'dest' : 'nom',
		'conv' : '',
	    },
            {
		'source' : 'estil',
		'dest' : 'estil',
		'conv' : '',
	    },
            {
		'source' : u'època',
		'dest' : 'epoca',
		'conv' : '',
	    },
            {
		'source' : 'municipi',
		'dest' : 'municipi',
		'conv' : '',
	    },
            {
		'source' : 'lloc',
		'dest' : 'lloc',
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
		'source' : 'nomcoor',
		'dest' : 'nomcoor',
		'conv' : '',
	    },
            {
		'source' : 'imatge',
		'dest' : 'imatge',
		'conv' : '',
	    },
	],
    },
        ('es-vc', 'ca') : {
        'project' : 'wikipedia',
	'lang' : 'ca',
	'headerTemplate' : 'Capçalera BIC Val',
	'rowTemplate' : 'Filera BIC Val',
	'namespaces' : [0],
	'table' : 'monuments_es-vc_(ca)',
	'truncate' : False,
	'primkey' : 'bic',
	'fields' : [
            {
		'source' : 'bic',
		'dest' : 'bic',
		'conv' : '',
	    },
	    {
		'source' : 'idurl',
		'dest' : 'idurl',
		'conv' : '',
	    },
            {
		'source' : 'nom',
		'dest' : 'nom',
		'conv' : '',
	    },
            {
		'source' : 'estil',
		'dest' : 'estil',
		'conv' : '',
	    },
            {
		'source' : 'municipi',
		'dest' : 'municipi',
		'conv' : '',
	    },
            {
		'source' : 'lloc',
		'dest' : 'lloc',
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
		'source' : 'nomcoor',
		'dest' : 'nomcoor',
		'conv' : '',
	    },
            {
		'source' : 'imatge',
		'dest' : 'imatge',
		'conv' : '',
	    },
	],
    },
    ('fr', 'ca') : {
        'project' : 'wikipedia',
	'lang' : 'ca',
	'headerTemplate' : 'Capçalera MH',
	'rowTemplate' : 'Filera MH',
	'namespaces' : [0],
	'table' : 'monuments_fr_(ca)',
	'truncate' : False,
	'primkey' : 'id',
	'fields' : [
	    {
		'source' : 'id',
		'dest' : 'id',
		'conv' : '',
	    },
            {
		'source' : 'nom',
		'dest' : 'nom',
		'conv' : '',
	    },
            {
		'source' : u'època',
		'dest' : 'epoca',
		'conv' : '',
	    },
            {
		'source' : 'municipi',
		'dest' : 'municipi',
		'conv' : '',
	    },
            {
		'source' : 'lloc',
		'dest' : 'lloc',
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
		'source' : 'nomcoor',
		'dest' : 'nomcoor',
		'conv' : '',
	    },
            {
		'source' : 'imatge',
		'dest' : 'imatge',
		'conv' : '',
	    },
	],
    },
    ('fr', 'fr') : {
        'project' : 'wikipedia',
	'lang' : 'fr',
	'headerTemplate' : 'En-tête de tableau MH',
	'rowTemplate' : 'Ligne de tableau MH',
	'namespaces' : [0],
	'table' : 'monuments_fr_(fr)',
	'truncate' : False,
	'primkey' : 'notice',
	'fields' : [
	    {
		'source' : 'tri',
		'dest' : 'tri',
		'conv' : '',
	    },
            {
		'source' : 'monument',
		'dest' : 'monument',
		'conv' : '',
	    },
            {
		'source' : 'commune',
		'dest' : 'commune',
		'conv' : '',
	    },
            {
		'source' : 'tri commune',
		'dest' : 'tri commune',
		'conv' : '',
	    },
            {
		'source' : 'adresse',
		'dest' : 'adresse',
		'conv' : '',
	    },
            {
		'source' : 'tri adresse',
		'dest' : 'tri adresse',
		'conv' : '',
	    },            {
		'source' : 'latitude',
		'dest' : 'lat',
		'conv' : '',
	    },
            {
		'source' : 'longitude',
		'dest' : 'lon',
		'conv' : '',
	    },
            {
		'source' : u'titre coordonnées',
		'dest' : 'titre_coordonnees',
		'conv' : '',
	    },
            {
		'source' : 'notice',
		'dest' : 'notice',
		'conv' : '',
	    },
            {
		'source' : 'protection',
		'dest' : 'protection',
		'conv' : '',
	    },
            {
		'source' : 'date',
		'dest' : 'date',
		'conv' : '',
	    },
            {
		'source' : 'image',
		'dest' : 'image',
		'conv' : '',
	    },
	],
    },
    ('ie', 'en') : {
        'project' : 'wikipedia',
	'lang' : 'en',
	'headerTemplate' : 'NMI list header',
	'rowTemplate' : 'NMI list item',
	'namespaces' : [0],
	'table' : 'monuments_ie_(en)',
	'truncate' : False,
	'primkey' : 'number',
	'fields' : [
	    {
		'source' : 'number',
		'dest' : 'number',
		'conv' : '',
	    },
            {
		'source' : 'name',
		'dest' : 'name',
		'conv' : '',
	    },
            {
		'source' : 'description',
		'dest' : 'description',
		'conv' : '',
	    },
            {
		'source' : 'townland',
		'dest' : 'townland',
		'conv' : '',
	    },
            {
		'source' : 'county',
		'dest' : 'county',
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
	],
    },
    ('it-88', 'ca') : {
        'project' : 'wikipedia',
	'lang' : 'ca',
	'headerTemplate' : 'Capçalera BC Sard',
	'rowTemplate' : 'Filera BC Sard',
	'namespaces' : [0],
	'table' : 'monuments_it-88_(ca)',
	'truncate' : False,
	'primkey' : 'id',
	'fields' : [
	    {
		'source' : 'id',
		'dest' : 'id',
		'conv' : '',
	    },
            {
		'source' : 'nom',
		'dest' : 'nom',
		'conv' : '',
	    },
            {
		'source' : 'municipi',
		'dest' : 'municipi',
		'conv' : '',
	    },
            {
		'source' : 'lloc',
		'dest' : 'lloc',
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
		'source' : 'nomcoor',
		'dest' : 'nomcoor',
		'conv' : '',
	    },
            {
		'source' : 'imatge',
		'dest' : 'imatge',
		'conv' : '',
	    },
	],
    },
    ('lu', 'lb') : {
        'project' : 'wikipedia',
	'lang' : 'lb',
	'headerTemplate' : 'Nationale Monumenter header',
	'rowTemplate' : 'Nationale Monumenter row',
	'namespaces' : [0],
	'table' : 'monuments_lu_(lb)',
	'truncate' : True,
	'primkey' : 'lag',
	'fields' : [
	    {
		'source' : 'id',
		'dest' : '',
		'conv' : '',
	    },
            {
		'source' : 'lag',
		'dest' : 'lag',
		'conv' : '',
	    },
            {
		'source' : 'uertschaft',
		'dest' : 'uertschaft',
		'conv' : '',
	    },            {
		'source' : 'offiziellen_numm',
		'dest' : 'offiziellen_numm',
		'conv' : '',
	    },
            {
		'source' : 'beschreiwung',
		'dest' : 'beschreiwung',
		'conv' : '',
	    },
            {
		'source' : 'niveau',
		'dest' : 'niveau',
		'conv' : '',
	    },
            {
		'source' : u'klasséiert_zënter',
		'dest' : u'klasseiert_zenter',
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
	    },           {
		'source' : 'bild',
		'dest' : 'bild',
		'conv' : '',
	    },
	],
    },
    ('nl', 'nl') : {
        'project' : 'wikipedia',
	'lang' : 'nl',
	'headerTemplate' : 'Tabelkop rijksmonumenten',
	'rowTemplate' : 'Tabelrij rijksmonument',
        'commonsTemplate' : 'Rijksmonument',
        'commonsTrackerCategory' : 'Rijksmonumenten with known IDs',
        'commonsCategoryBase' : 'Rijksmonumenten',
        'unusedImagesPage' : 'Wikipedia:Wikiproject/Erfgoed/Nederlandse Erfgoed Inventarisatie/Ongebruikte foto\'s',
        'imagesWithoutIdPage' : 'Wikipedia:Wikiproject/Erfgoed/Nederlandse Erfgoed Inventarisatie/Foto\'s zonder id',
	'namespaces' : [0],
	'table' : 'monuments_nl_(nl)',
	'truncate' : False,
	'primkey' : 'objrijksnr',
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
    ('pl', 'pl') : {
        'project' : 'wikipedia',
	'lang' : 'pl',
	'headerTemplate' : 'Lista zabytków góra',
	'rowTemplate' : 'Zabytki wiersz',
	'namespaces' : [102],
	'table' : 'monuments_pl_(pl)',
	'truncate' : True,
	'primkey' : 'numer',
	'fields' : [
	    {
		'source' : 'numer',
		'dest' : 'numer',
		'conv' : '',
	    },
	    {
		'source' : 'nazwa',
		'dest' : 'nazwa',
		'conv' : '',
	    },
	    {
		'source' : 'adres',
		'dest' : 'adres',
		'conv' : '',
	    },
	    {
		'source' : 'gmina',
		'dest' : 'gmina',
		'conv' : '',
	    },
	    {
		'source' : u'szerokość',
		'dest' : 'lat',
		'conv' : '',
	    },
	    {
		'source' : u'długość',
		'dest' : 'lon',
		'conv' : '',
	    },
	    {
		'source' : u'zdjęcie',
		'dest' : 'zdjecie',
		'conv' : '',
	    },
	],
    },
    ('pt', 'pt') : {
        'project' : 'wikipedia',
	'lang' : 'pt',
	'headerTemplate' : 'IGESPAR/cabeçalho',
	'rowTemplate' : 'IGESPAR/linha',
        'footerTemplate' : 'IGESPAR/rodapé',
	'namespaces' : [102],
	'table' : 'monuments_pt_(pt)',
	'truncate' : False,
	'primkey' : 'id',
	'fields' : [
	    {
		'source' : 'id',
		'dest' : 'id',
		'conv' : '',
	    },
	    {
		'source' : 'designacoes',
		'dest' : 'designacoes',
		'conv' : '',
	    },
	    {
		'source' : 'categoria',
		'dest' : 'categoria',
		'conv' : '',
	    },
	    {
		'source' : 'tipologia',
		'dest' : 'tipologia',
		'conv' : '',
	    },
	    {
		'source' : 'concelho',
		'dest' : 'concelho',
		'conv' : '',
	    },
	    {
		'source' : 'freguesia',
		'dest' : 'freguesia',
		'conv' : '',
	    },
	    {
		'source' : 'grau',
		'dest' : 'grau',
		'conv' : '',
	    },
	    {
		'source' : 'ano',
		'dest' : 'ano',
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
		'source' : 'imagem',
		'dest' : 'imagem',
		'conv' : '',
	    },
	],
    },
}
''' 

'''
