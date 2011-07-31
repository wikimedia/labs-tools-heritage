#!/usr/bin/python
# -*- coding: utf-8  -*-
'''
Configuration for the monuments bot.

'''

db_server='sql.toolserver.org'
db = 'p_erfgoed_p'

countries = {
    ('ad', 'ca') : {
        'project' : u'wikipedia',
	'lang' : u'ca',
	'headerTemplate' : u'Capçalera BIC And',
	'rowTemplate' : u'Filera BIC And',
        'commonsTemplate': u'Béns Andorra',
        'commonsTrackerCategory': u'Cultural heritage monuments in Andorra with known IDs',
        'commonsCategoryBase': u'Cultural heritage monuments in Andorra',
	'namespaces' : [0],
	'table' : u'monuments_ad_(ca)',
	'truncate' : False,
	'primkey' : u'id',
	'fields' : [
	    {
		'source' : u'id',
		'dest' : u'id',
		'conv' : u'',
	    },
            {
		'source' : u'nom',
		'dest' : u'nom',
		'conv' : u'',
	    },
            {
		'source' : u'estil',
		'dest' : u'estil',
		'conv' : u'',
	    },
            {
		'source' : u'època',
		'dest' : u'epoca',
		'conv' : u'',
	    },
            {
		'source' : u'municipi',
		'dest' : u'municipi',
		'conv' : u'',
	    },
            {
		'source' : u'lloc',
		'dest' : u'lloc',
		'conv' : u'',
	    },            {
		'source' : u'lat',
		'dest' : u'lat',
		'conv' : u'',
	    },
            {
		'source' : u'lon',
		'dest' : u'lon',
		'conv' : u'',
	    },
            {
		'source' : u'nomcoor',
		'dest' : u'nomcoor',
		'conv' : u'',
	    },
            {
		'source' : u'imatge',
		'dest' : u'imatge',
		'conv' : u'',
	    },
	],
    },
    ('be-bru', 'nl') : {
	'project' : u'wikipedia',
	'lang' : u'nl',
	'headerTemplate' : u'Tabelkop erfgoed Brussels Hoofdstedelijk Gewest',
	'rowTemplate' : u'Tabelrij erfgoed Brussels Hoofdstedelijk Gewest',
        'commonsTemplate' : u'Monument Brussels',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Brussels with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Brussels',
        'unusedImagesPage' : u'Wikipedia:Wikiproject/Erfgoed/Belgische Erfgoed Inventarisatie/Brussel/Ongebruikte foto\'s',
        'imagesWithoutIdPage' : u'Wikipedia:Wikiproject/Erfgoed/Belgische Erfgoed Inventarisatie/Brussel/Foto\'s zonder id',
	'namespaces' : [0],
	'table' : u'monuments_be-bru_(nl)',
	'truncate' : False,
	'primkey' : u'code',
	'fields' : [
	    {
		'source' : u'omschrijving',
		'dest' : u'omschrijving',
		'conv' : u'',
	    },
            {
		'source' : u'plaats',
		'dest' : u'plaats',
		'conv' : u'',
	    },
	    {
		'source' : u'adres',
		'dest' : u'adres',
		'conv' : u'',
	    },
	    {
		'source' : u'bouwjaar',
		'dest' : u'bouwjaar',
		'conv' : u'',
	    },
	    {
		'source' : u'bouwdoor',
		'dest' : u'bouwdoor',
		'conv' : u'',
	    },
	    {
		'source' : u'bouwstijl',
		'dest' : u'bouwstijl',
		'conv' : u'',
	    },
	    {
		'source' : u'objtype',
		'dest' : u'objtype',
		'conv' : u'',
	    },
	    {
		'source' : u'beschermd',
		'dest' : u'beschermd',
		'conv' : u'',
	    },
	    {
		'source' : u'code',
		'dest' : u'code',
		'conv' : u'',
	    },
	    {
		'source' : u'lat',
		'dest' : u'lat',
		'conv' : u'',
	    },
	    {
		'source' : u'lon',
		'dest' : u'lon',
		'conv' : u'',
	    },
	    {
		'source' : u'image',
		'dest' : u'image',
		'conv' : u'',
	    },
	],
    },
    ('be-vlg', 'nl') : {
	'project' : u'wikipedia',
	'lang' : u'nl',
	'headerTemplate' : u'Tabelkop erfgoed Vlaanderen',
	'rowTemplate' : u'Tabelrij erfgoed Vlaanderen',
        'commonsTemplate' : u'Onroerend erfgoed',
        'commonsTrackerCategory' : u'Onroerend erfgoed with known IDs',
        'commonsCategoryBase' : u'Onroerend erfgoed',
        'unusedImagesPage' : u'Wikipedia:Wikiproject/Erfgoed/Belgische Erfgoed Inventarisatie/Vlaanderen/Ongebruikte foto\'s',
        'imagesWithoutIdPage' : u'Wikipedia:Wikiproject/Erfgoed/Belgische Erfgoed Inventarisatie/Vlaanderen/Foto\'s zonder id',
	'namespaces' : [0],
	'table' : u'monuments_be-vlg_(nl)',
	'truncate' : False,
	'primkey' : u'id',
	'fields' : [
	    {
		'source' : u'id',
		'dest' : u'id',
		'conv' : u'',
	    },
            {
		'source' : u'beschermd',
		'dest' : u'beschermd',
		'conv' : u'',
	    },
	    {
		'source' : u'gemeente',
		'dest' : u'gemeente',
		'conv' : u'',
	    },
	    {
		'source' : u'deelgem',
		'dest' : u'deelgem',
		'conv' : u'',
	    },
	    {
		'source' : u'deelgem_id',
		'dest' : u'',
		'conv' : u'',
	    },
	    {
		'source' : u'adres',
		'dest' : u'adres',
		'conv' : u'',
	    },
	    {
		'source' : u'objectnaam',
		'dest' : u'objectnaam',
		'conv' : u'',
	    },
	    {
		'source' : u'bouwjaar',
		'dest' : u'bouwjaar',
		'conv' : u'',
	    },
	    {
		'source' : u'architect',
		'dest' : u'architect',
		'conv' : u'',
	    },
	    {
		'source' : u'lat',
		'dest' : u'lat',
		'conv' : u'',
	    },
	    {
		'source' : u'lon',
		'dest' : u'lon',
		'conv' : u'',
	    },
	    {
		'source' : u'image',
		'dest' : u'image',
		'conv' : u'',
	    },
	],
    },
    ('be-wal', 'nl') : {
	'project' : u'wikipedia',
	'lang' : u'nl',
	'headerTemplate' : u'Tabelkop erfgoed Wallonië',
	'rowTemplate' : u'Tabelrij erfgoed Wallonië',
	'commonsTemplate' : u'Monument Wallonie',
	'commonsTrackerCategory' : u'Cultural heritage monuments in Wallonia with known IDs',
	'commonsCategoryBase' : u'Cultural heritage monuments in Wallonia',
        'unusedImagesPage' : u'Wikipedia:Wikiproject/Erfgoed/Belgische Erfgoed Inventarisatie/Wallonië/Ongebruikte foto\'s',
        'imagesWithoutIdPage' : u'Wikipedia:Wikiproject/Erfgoed/Belgische Erfgoed Inventarisatie/Wallonië/Foto\'s zonder id',
	'namespaces' : [0],
	'table' : u'monuments_be-wal_(nl)',
	'truncate' : True, #FIXME: Add combined primkeys to the code
	'primkey' : ('niscode', 'objcode'),
	'fields' : [
	    {
		'source' : u'niscode',
		'dest' : u'niscode',
		'conv' : u'',
	    },
	    {
		'source' : u'objcode',
		'dest' : u'objcode',
		'conv' : u'',
	    },
            {
		'source' : u'descr_nl',
		'dest' : u'descr_nl',
		'conv' : u'',
	    },
            {
		'source' : u'descr_fr',
		'dest' : u'descr_fr',
		'conv' : u'',
	    },
	    {
		'source' : u'gemeente',
		'dest' : u'gemeente',
		'conv' : u'',
	    },
	    {
		'source' : u'deelgemeente',
		'dest' : u'deelgemeente',
		'conv' : u'',
	    },
	    {
		'source' : u'adres',
		'dest' : u'adres',
		'conv' : u'',
	    },
	    {
		'source' : u'objtype',
		'dest' : u'objtype',
		'conv' : u'',
	    },
	    {
		'source' : u'lat',
		'dest' : u'lat',
		'conv' : u'',
	    },
	    {
		'source' : u'lon',
		'dest' : u'lon',
		'conv' : u'',
	    },
	    {
		'source' : u'architect',
		'dest' : u'architect',
		'conv' : u'',
	    },
	    {
		'source' : u'bouwjaar',
		'dest' : u'bouwjaar',
		'conv' : u'',
	    },
	    {
		'source' : u'image',
		'dest' : u'image',
		'conv' : u'',
	    },
	],
    },
    ('by', 'be-x-old') : {
	'project' : u'wikipedia',
	'lang' : u'be-x-old',
	'headerTemplate' : u'Вікі любіць славутасьці/Вяршыня сьпісу',
	'rowTemplate' : u'Вікі любіць славутасьці/Элемэнт сьпісу',
	'commonsTemplate' : u'',
	'commonsTrackerCategory' : u'',
	'commonsCategoryBase' : u'',
	'unusedImagesPage' : u'',
	'imagesWithoutIdPage' : u'',
	'namespaces' : [4],
	'table' : u'monuments_by_(be-x-old)',
	'truncate' : False,
	'primkey' : u'шыфр',
	'fields' : [
	    {
		'source' : u'шыфр',
		'dest' : u'id',
		'conv' : u'',
	    },
	    {
		'source' : u'назва',
		'dest' : u'name',
		'conv' : u'',
	    },
	    {
		'source' : u'датаваньне',
		'dest' : u'date',
		'conv' : u'',
	    },
	    {
		'source' : u'населены пункт',
		'dest' : u'place',
		'conv' : u'',
	    },
	    {
		'source' : u'адрэса',
		'dest' : u'address',
		'conv' : u'',
	    },
	    {
		'source' : u'катэгорыя',
		'dest' : u'category',
		'conv' : u'',
	    },
	    {
		'source' : u'шырата',
		'dest' : u'lat',
		'conv' : u'',
	    },
	    {
		'source' : u'даўгата',
		'dest' : u'lon',
		'conv' : u'',
	    },
	    {
		'source' : u'каардынаты',
		'dest' : u'coordinates',
		'conv' : u'',
	    },
	    {
		'source' : u'выява',
		'dest' : u'image',
		'conv' : u'',
	    },
            {
		'source' : u'грамадзкі набытак', # Boolean, not clear what the purpose is
		'dest' : u'',
		'conv' : u'',
	    },
	],
    },
    ('ch', 'en') : {
	'project' : u'wikipedia',
	'lang' : u'en',
	'headerTemplate' : u'SIoCPoNaRS header',
	'rowTemplate' : u'SIoCPoNaRS row',
	'namespaces' : [0],
	'table' : u'monuments_ch_(en)',
	'truncate' : True,
	'primkey' : u'KGS_nr',
	'fields' : [
	    {
		'source' : u'KGS_nr',
		'dest' : u'',
		'conv' : u'',
	    },
	    {
		'source' : u'name',
		'dest' : u'name',
		'conv' : u'',
	    },
	    {
		'source' : u'address',
		'dest' : u'address',
		'conv' : u'',
	    },
	    {
		'source' : u'municipality',
		'dest' : u'municipality',
		'conv' : u'',
	    },
	    {
		'source' : u'CH1903_X',
		'dest' : u'lat',
		'conv' : u'CH1903ToLat',
	    },
	    {
		'source' : u'CH1903_Y',
		'dest' : u'lon',
		'conv' : u'CH1903ToLon',
	    },
	    {
		'source' : u'image',
		'dest' : u'image',
		'conv' : u'',
	    },
	]
    },
    ('ee', 'et') : {
	'project' : u'wikipedia',
	'lang' : u'et',
	'headerTemplate' : u'KRR päis',
	'rowTemplate' : u'KRR rida',
        'commonsTemplate' : u'Kultuurimälestis',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Estonia (with known IDs)',
        'commonsCategoryBase' : u'Cultural heritage monuments in Estonia',
        'unusedImagesPage' : u'Vikipeedia:Vikiprojekt_Kultuuripärand/Kasutamata kultuurimälestiste pildid',
        'imagesWithoutIdPage' : u'Vikipeedia:Vikiprojekt_Kultuuripärand/Ilma registri numbrita pildid',    
	'namespaces' : [4],
	'table' : u'monuments_ee_(et)',
	'truncate' : False,
	'primkey' : u'number',
	'fields' : [
	    {
		'source' : u'number',
		'dest' : u'number',
		'conv' : u'',
	    },
	    {
		'source' : u'nimi',
		'dest' : u'nimi',
		'conv' : u'',
	    },
	    {
		'source' : u'liik',
		'dest' : u'liik',
		'conv' : u'',
	    },
	    {
		'source' : u'aadress',
		'dest' : u'aadress',
		'conv' : u'',
	    },
	    {
		'source' : u'omavalitsus',
		'dest' : u'omavalitsus',
		'conv' : u'',
	    },
            {
		'source' : u'NS',
		'dest' : u'lat',
		'conv' : u'',
	    },
	    {
		'source' : u'EW',
		'dest' : u'lon',
		'conv' : u'',
	    },
	    {
		'source' : u'pilt',
		'dest' : u'pilt',
		'conv' : u'',
	    },
	    {
		'source' : u'commons',
		'dest' : u'commons',
		'conv' : u'',
	    },
	]
    },
    ('es', 'ca') : {
        'project' : u'wikipedia',
	'lang' : u'ca',
	'headerTemplate' : u'Capçalera BIC',
	'rowTemplate' : u'Filera BIC',
        'commonsTemplate' : u'BIC',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Spain with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Spain',
        'unusedImagesPage' : u'User:Multichill/Unused BIC',
        'imagesWithoutIdPage' : u'User:Multichill/BIC without id',
	'namespaces' : [0],
	'table' : u'monuments_es_(ca)',
	'truncate' : False,
	'primkey' : u'bic',
	'fields' : [
	    {
		'source' : u'bic',
		'dest' : u'bic',
		'conv' : u'',
	    },
            {
		'source' : u'nom',
		'dest' : u'nom',
		'conv' : u'',
	    },
            {
		'source' : u'tipus',
		'dest' : u'tipus',
		'conv' : u'',
	    },            {
		'source' : u'municipi',
		'dest' : u'municipi',
		'conv' : u'',
	    },
            {
		'source' : u'lloc',
		'dest' : u'lloc',
		'conv' : u'',
	    },
            {
		'source' : u'lat',
		'dest' : u'lat',
		'conv' : u'',
	    },
            {
		'source' : u'lon',
		'dest' : u'lon',
		'conv' : u'',
	    },
            {
		'source' : u'nomcoor',
		'dest' : u'nomcoor',
		'conv' : u'',
	    },
            {
		'source' : u'imatge',
		'dest' : u'imatge',
		'conv' : u'',
	    },
	],
    },
    ('es', 'es') : {
        'project' : u'wikipedia',
	'lang' : u'es',
	'headerTemplate' : u'Cabecera BIC',
	'rowTemplate' : u'Fila BIC',
        'commonsTemplate' : u'BIC',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Spain with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Spain',
        'unusedImagesPage' : u'User:Multichill/Unused BIC',
        'imagesWithoutIdPage' : u'User:Multichill/BIC without id',
	'namespaces' : [104],
	'table' : u'monuments_es_(es)',
	'truncate' : False,
	'primkey' : u'bic',
	'fields' : [
	    {
		'source' : u'bic',
		'dest' : u'bic',
		'conv' : u'',
	    },
            {
		'source' : u'nombre',
		'dest' : u'nombre',
		'conv' : u'',
	    },
            {
		'source' : u'nombrecoor',
		'dest' : u'nombrecoor',
		'conv' : u'',
	    },
            {
		'source' : u'tipobic',
		'dest' : u'tipobic',
		'conv' : u'',
	    },
            {
		'source' : u'tipo',
		'dest' : u'tipo',
		'conv' : u'',
	    },
            {
		'source' : u'municipio',
		'dest' : u'municipio',
		'conv' : u'',
	    },
            {
		'source' : u'lugar',
		'dest' : u'lugar',
		'conv' : u'',
	    },
            {
		'source' : u'lat',
		'dest' : u'lat',
		'conv' : u'',
	    },
            {
		'source' : u'lon',
		'dest' : u'lon',
		'conv' : u'',
	    },
            {
		'source' : u'fecha',
		'dest' : u'fecha',
		'conv' : u'',
	    },
            {
		'source' : u'imagen',
		'dest' : u'imagen',
		'conv' : u'',
	    },
	],
    },
    ('es-ct', 'ca') : {
        'project' : u'wikipedia',
	'lang' : u'ca',
	'headerTemplate' : u'Capçalera BCIN',
	'rowTemplate' : u'Filera BCIN',
        'commonsTemplate' : u'BIC',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Spain with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Catalonia',
	'namespaces' : [0],
	'table' : u'monuments_es-ct_(ca)',
	'truncate' : False,
	'primkey' : u'bic',
	'fields' : [
	    {
		'source' : u'bic',
		'dest' : u'bic',
		'conv' : u'',
	    },
	    {
		'source' : u'idurl',
		'dest' : u'idurl',
		'conv' : u'',
	    },
	    {
		'source' : u'bcin',
		'dest' : u'bcin',
		'conv' : u'',
	    },
            {
		'source' : u'nom',
		'dest' : u'nom',
		'conv' : u'',
	    },
            {
		'source' : u'estil',
		'dest' : u'estil',
		'conv' : u'',
	    },
            {
		'source' : u'època',
		'dest' : u'epoca',
		'conv' : u'',
	    },
            {
		'source' : u'municipi',
		'dest' : u'municipi',
		'conv' : u'',
	    },
            {
		'source' : u'lloc',
		'dest' : u'lloc',
		'conv' : u'',
	    },
            {
		'source' : u'lat',
		'dest' : u'lat',
		'conv' : u'',
	    },
            {
		'source' : u'lon',
		'dest' : u'lon',
		'conv' : u'',
	    },
            {
		'source' : u'nomcoor',
		'dest' : u'nomcoor',
		'conv' : u'',
	    },
            {
		'source' : u'imatge',
		'dest' : u'imatge',
		'conv' : u'',
	    },
	],
    },
        ('es-vc', 'ca') : {
        'project' : u'wikipedia',
	'lang' : u'ca',
	'headerTemplate' : u'Capçalera BIC Val',
	'rowTemplate' : u'Filera BIC Val',
        'commonsTemplate' : u'BIC',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Spain with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in the Land of Valencia',
	'namespaces' : [0],
	'table' : u'monuments_es-vc_(ca)',
	'truncate' : False,
	'primkey' : u'bic',
	'fields' : [
            {
		'source' : u'bic',
		'dest' : u'bic',
		'conv' : u'',
	    },
	    {
		'source' : u'idurl',
		'dest' : u'idurl',
		'conv' : u'',
	    },
            {
		'source' : u'nom',
		'dest' : u'nom',
		'conv' : u'',
	    },
            {
		'source' : u'estil',
		'dest' : u'estil',
		'conv' : u'',
	    },
            {
		'source' : u'municipi',
		'dest' : u'municipi',
		'conv' : u'',
	    },
            {
		'source' : u'lloc',
		'dest' : u'lloc',
		'conv' : u'',
	    },
            {
		'source' : u'lat',
		'dest' : u'lat',
		'conv' : u'',
	    },
            {
		'source' : u'lon',
		'dest' : u'lon',
		'conv' : u'',
	    },
            {
		'source' : u'nomcoor',
		'dest' : u'nomcoor',
		'conv' : u'',
	    },
            {
		'source' : u'imatge',
		'dest' : u'imatge',
		'conv' : u'',
	    },
	],
    },
    ('fr', 'ca') : {
        'project' : u'wikipedia',
	'lang' : u'ca',
	'headerTemplate' : u'Capçalera MH',
	'rowTemplate' : u'Filera MH',
	'namespaces' : [0],
	'table' : u'monuments_fr_(ca)',
	'truncate' : False,
	'primkey' : u'id',
	'fields' : [
	    {
		'source' : u'id',
		'dest' : u'id',
		'conv' : u'',
	    },
            {
		'source' : u'nom',
		'dest' : u'nom',
		'conv' : u'',
	    },
            {
		'source' : u'època',
		'dest' : u'epoca',
		'conv' : u'',
	    },
            {
		'source' : u'municipi',
		'dest' : u'municipi',
		'conv' : u'',
	    },
            {
		'source' : u'lloc',
		'dest' : u'lloc',
		'conv' : u'',
	    },
            {
		'source' : u'lat',
		'dest' : u'lat',
		'conv' : u'',
	    },
            {
		'source' : u'lon',
		'dest' : u'lon',
		'conv' : u'',
	    },
            {
		'source' : u'nomcoor',
		'dest' : u'nomcoor',
		'conv' : u'',
	    },
            {
		'source' : u'imatge',
		'dest' : u'imatge',
		'conv' : u'',
	    },
	],
    },
    ('fr', 'fr') : {
        'project' : u'wikipedia',
	'lang' : u'fr',
	'headerTemplate' : u'En-tête de tableau MH',
	'rowTemplate' : u'Ligne de tableau MH',
	'namespaces' : [0],
	'table' : u'monuments_fr_(fr)',
	'truncate' : False,
	'primkey' : u'notice',
	'fields' : [
	    {
		'source' : u'tri',
		'dest' : u'tri',
		'conv' : u'',
	    },
            {
		'source' : u'monument',
		'dest' : u'monument',
		'conv' : u'',
	    },
            {
		'source' : u'commune',
		'dest' : u'commune',
		'conv' : u'',
	    },
            {
		'source' : u'tri commune',
		'dest' : u'tri commune',
		'conv' : u'',
	    },
            {
		'source' : u'adresse',
		'dest' : u'adresse',
		'conv' : u'',
	    },
            {
		'source' : u'tri adresse',
		'dest' : u'tri adresse',
		'conv' : u'',
	    },            {
		'source' : u'latitude',
		'dest' : u'lat',
		'conv' : u'',
	    },
            {
		'source' : u'longitude',
		'dest' : u'lon',
		'conv' : u'',
	    },
            {
		'source' : u'titre coordonnées',
		'dest' : u'titre_coordonnees',
		'conv' : u'',
	    },
            {
		'source' : u'notice',
		'dest' : u'notice',
		'conv' : u'',
	    },
            {
		'source' : u'protection',
		'dest' : u'protection',
		'conv' : u'',
	    },
            {
		'source' : u'date',
		'dest' : u'date',
		'conv' : u'',
	    },
            {
		'source' : u'image',
		'dest' : u'image',
		'conv' : u'',
	    },
	],
    },
    ('ie', 'en') : {
        'project' : u'wikipedia',
	'lang' : u'en',
	'headerTemplate' : u'NMI list header',
	'rowTemplate' : u'NMI list item',
	'namespaces' : [0],
	'table' : u'monuments_ie_(en)',
	'truncate' : False,
	'primkey' : u'number',
	'fields' : [
	    {
		'source' : u'number',
		'dest' : u'number',
		'conv' : u'',
	    },
            {
		'source' : u'name',
		'dest' : u'name',
		'conv' : u'',
	    },
            {
		'source' : u'description',
		'dest' : u'description',
		'conv' : u'',
	    },
            {
		'source' : u'townland',
		'dest' : u'townland',
		'conv' : u'',
	    },
            {
		'source' : u'county',
		'dest' : u'county',
		'conv' : u'',
	    },
            {
		'source' : u'lat',
		'dest' : u'lat',
		'conv' : u'',
	    },
            {
		'source' : u'lon',
		'dest' : u'lon',
		'conv' : u'',
	    },
            {
		'source' : u'image',
		'dest' : u'image',
		'conv' : u'',
	    },
	],
    },
    ('it-88', 'ca') : {
        'project' : u'wikipedia',
	'lang' : u'ca',
	'headerTemplate' : u'Capçalera BC Sard',
	'rowTemplate' : u'Filera BC Sard',
	'namespaces' : [0],
	'table' : u'monuments_it-88_(ca)',
	'truncate' : False,
	'primkey' : u'id',
	'fields' : [
	    {
		'source' : u'id',
		'dest' : u'id',
		'conv' : u'',
	    },
            {
		'source' : u'nom',
		'dest' : u'nom',
		'conv' : u'',
	    },
            {
		'source' : u'municipi',
		'dest' : u'municipi',
		'conv' : u'',
	    },
            {
		'source' : u'lloc',
		'dest' : u'lloc',
		'conv' : u'',
	    },
            {
		'source' : u'lat',
		'dest' : u'lat',
		'conv' : u'',
	    },
            {
		'source' : u'lon',
		'dest' : u'lon',
		'conv' : u'',
	    },
            {
		'source' : u'nomcoor',
		'dest' : u'nomcoor',
		'conv' : u'',
	    },
            {
		'source' : u'imatge',
		'dest' : u'imatge',
		'conv' : u'',
	    },
	],
    },
    ('lu', 'lb') : {
        'project' : u'wikipedia',
	'lang' : u'lb',
	'headerTemplate' : u'Nationale Monumenter header',
	'rowTemplate' : u'Nationale Monumenter row',
	'namespaces' : [0],
	'table' : u'monuments_lu_(lb)',
	'truncate' : True,
	'primkey' : u'lag',
	'fields' : [
	    {
		'source' : u'id',
		'dest' : u'',
		'conv' : u'',
	    },
            {
		'source' : u'lag',
		'dest' : u'lag',
		'conv' : u'',
	    },
            {
		'source' : u'uertschaft',
		'dest' : u'uertschaft',
		'conv' : u'',
	    },            {
		'source' : u'offiziellen_numm',
		'dest' : u'offiziellen_numm',
		'conv' : u'',
	    },
            {
		'source' : u'beschreiwung',
		'dest' : u'beschreiwung',
		'conv' : u'',
	    },
            {
		'source' : u'niveau',
		'dest' : u'niveau',
		'conv' : u'',
	    },
            {
		'source' : u'klasséiert_zënter',
		'dest' : u'klasseiert_zenter',
		'conv' : u'',
	    },
            {
		'source' : u'lat',
		'dest' : u'lat',
		'conv' : u'',
	    },
             {
		'source' : u'lon',
		'dest' : u'lon',
		'conv' : u'',
	    },           {
		'source' : u'bild',
		'dest' : u'bild',
		'conv' : u'',
	    },
	],
    },
    ('nl', 'nl') : {
        'project' : u'wikipedia',
	'lang' : u'nl',
	'headerTemplate' : u'Tabelkop rijksmonumenten',
	'rowTemplate' : u'Tabelrij rijksmonument',
        'commonsTemplate' : u'Rijksmonument',
        'commonsTrackerCategory' : u'Rijksmonumenten with known IDs',
        'commonsCategoryBase' : u'Rijksmonumenten',
        'unusedImagesPage' : u'Wikipedia:Wikiproject/Erfgoed/Nederlandse Erfgoed Inventarisatie/Ongebruikte foto\'s',
        'imagesWithoutIdPage' : u'Wikipedia:Wikiproject/Erfgoed/Nederlandse Erfgoed Inventarisatie/Foto\'s zonder id',
	'namespaces' : [0],
	'table' : u'monuments_nl_(nl)',
	'truncate' : False,
	'primkey' : u'objrijksnr',
	'fields' : [
	    {
		'source' : u'objrijksnr',
		'dest' : u'objrijksnr',
		'conv' : u'',
	    },
	    {
		'source' : u'woonplaats',
		'dest' : u'woonplaats',
		'conv' : u'',
	    },
	    {
		'source' : u'adres',
		'dest' : u'adres',
		'conv' : u'',
	    },
	    {
		'source' : u'objectnaam',
		'dest' : u'objectnaam',
		'conv' : u'',
	    },
	    {
		'source' : u'type_obj',
		'dest' : u'type_obj',
		'conv' : u'',
	    },
	    {
		'source' : u'oorspr_functie',
		'dest' : u'oorspr_functie',
		'conv' : u'',
	    },
	    {
		'source' : u'bouwjaar',
		'dest' : u'bouwjaar',
		'conv' : u'',
	    },
	    {
		'source' : u'architect',
		'dest' : u'architect',
		'conv' : u'',
	    },
	    {
		'source' : u'cbs_tekst',
		'dest' : u'cbs_tekst',
		'conv' : u'',
	    },
	    {
		'source' : u'RD_x',
		'dest' : u'',
		'conv' : u'',
	    },
	    {
		'source' : u'RD_y',
		'dest' : u'',
		'conv' : u'',
	    },
	    {
		'source' : u'lat',
		'dest' : u'lat',
		'conv' : u'',
	    },
	    {
		'source' : u'lon',
		'dest' : u'lon',
		'conv' : u'',
	    },
	    {
		'source' : u'image',
		'dest' : u'image',
		'conv' : u'',
	    },
	    {
		'source' : u'postcode',
		'dest' : u'',
		'conv' : u'',
	    },
	    {
		'source' : u'buurt',
		'dest' : u'',
		'conv' : u'',
	    },
	],
    },
    ('pt', 'pt') : {
        'project' : u'wikipedia',
	'lang' : u'pt',
	'headerTemplate' : u'IGESPAR/cabeçalho',
	'rowTemplate' : u'IGESPAR/linha',
        'footerTemplate' : u'IGESPAR/rodapé',
	'namespaces' : [102],
	'table' : u'monuments_pt_(pt)',
	'truncate' : False,
	'primkey' : u'id',
	'fields' : [
	    {
		'source' : u'id',
		'dest' : u'id',
		'conv' : u'',
	    },
	    {
		'source' : u'designacoes',
		'dest' : u'designacoes',
		'conv' : u'',
	    },
	    {
		'source' : u'categoria',
		'dest' : u'categoria',
		'conv' : u'',
	    },
	    {
		'source' : u'tipologia',
		'dest' : u'tipologia',
		'conv' : u'',
	    },
	    {
		'source' : u'concelho',
		'dest' : u'concelho',
		'conv' : u'',
	    },
	    {
		'source' : u'freguesia',
		'dest' : u'freguesia',
		'conv' : u'',
	    },
	    {
		'source' : u'grau',
		'dest' : u'grau',
		'conv' : u'',
	    },
	    {
		'source' : u'ano',
		'dest' : u'ano',
		'conv' : u'',
	    },
	    {
		'source' : u'lat',
		'dest' : u'lat',
		'conv' : u'',
	    },
	    {
		'source' : u'lon',
		'dest' : u'lon',
		'conv' : u'',
	    },
	    {
		'source' : u'imagem',
		'dest' : u'imagem',
		'conv' : u'',
	    },
	],
    },
}
''' 

'''
