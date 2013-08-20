#!/usr/bin/python
# -*- coding: utf-8  -*-
'''
Configuration for the monuments bot.

'''

db_server='sql.toolserver.org'
db = 'p_erfgoed_p'

countries = {
    ('ad', 'ca') : { # Monuments in Andorra in Catalan table
        'project' : u'wikipedia',
        'lang' : u'ca',
        'headerTemplate' : u'Capçalera BIC And',
        'rowTemplate' : u'Filera BIC And',
        'commonsTemplate': u'Béns Andorra',
        'commonsTrackerCategory': u'Cultural heritage monuments in Andorra with known IDs',
        'unusedImagesPage' : u'Portal:Wiki Loves Monuments/Imatges per utilitzar Andorra',
        'commonsCategoryBase': u'Cultural heritage monuments in Andorra',
        'registrantUrlBase' : u'http://www.patrimonicultural.ad/banc/article.php?id=%s',    
        'namespaces' : [0],
        'table' : u'monuments_ad_(ca)',
        'truncate' : False,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'id',
                'type' : 'int(11)',
            },
            {
                'source' : u'nom',
                'dest' : u'nom',
            },
            {
                'source' : u'estil',
                'dest' : u'estil',
            },
            {
                'source' : u'època',
                'dest' : u'epoca',
            },
            {
                'source' : u'municipi',
                'dest' : u'municipi',
            },
            {
                'source' : u'region',
                'dest' : u'region',
            },
            {
                'source' : u'lloc',
                'dest' : u'lloc',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'nomcoor',
                'dest' : u'nomcoor',
            },
            {
                'source' : u'imatge',
                'dest' : u'imatge',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'nom',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'id',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('am', 'hy') : { # Monuments in Armenia in Armenian
        'project' : u'wikipedia',
        'lang' : u'hy',
        'headerTemplate' : u'Հուշարձան վերնագիր',
        'rowTemplate' : u'Հուշարձան ցանկ',
        'commonsTemplate' : u'Cultural Heritage Armenia',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Armenia with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Armenia',
        'autoGeocode' : True,
        'unusedImagesPage' : u'Վիքիպեդիա:Վիքին սիրում է հուշարձաններ 2013/Unused images of Cultural heritage monuments in Armenia', # FIXME: Translation needed
        'imagesWithoutIdPage' : u'Վիքիպեդիա:Վիքին սիրում է հուշարձաններ 2013/Images of Cultural heritage monuments in Armenia without an ID', # FIXME: Translation needed
        'registrantUrlBase' : u'http://www.arlis.am/DocumentView.aspx?DocID=%s', # Won't work yet, but put it in anyway
        'namespaces' : [0],
        'table' : u'monuments_am_(hy)',
        'truncate' : False,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'համարանիշ',
                'dest' : u'id',
                'type' : 'varchar(11)',
            },
            {
                'source' : u'մարզ',
                'dest' : u'prov_iso',
            },
            {
                'source' : u'համայնք',
                'dest' : u'municipality',
            },
            {
                'source' : u'հուշարձան',
                'dest' : u'description',
            },
            {
                'source' : u'հոդված',
                'dest' : u'monument_article',
            },
            {
                'source' : u'նշանակություն',
                'dest' : u'importance',
            },
            {
                'source' : u'կառուցված',
                'dest' : u'date',
            },
            {
                'source' : u'հասցե',
                'dest' : u'address',
            },
            {
                'source' : u'լայն',
                'dest' : u'lat',
            },
            {
                'source' : u'երկ',
                'dest' : u'lon',
            },
            {
                'source' : u'հղում',
                'dest' : u'gov_doc_id',
            },
            {
                'source' : u'պատկեր',
                'dest' : u'image',
            },
            {
                'source' : u'վիքիպահեստ',
                'dest' : u'commonscat',
            },
            {
                'source' : u'նշում',
                'dest' : u'notes',
            },
            {
                'source' : u'gov_doc_id',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('aq', 'en') : { # Monuments in Antarctica in English
        'project' : u'wikipedia',
        'lang' : u'en',
        'headerTemplate' : u'Antarctic Protected Area header',
        'rowTemplate' : u'Antarctic Protected Area row',
        'commonsTemplate': u'Antarctic Protected Area',
        'commonsTrackerCategory': u'Antarctic Protected Areas with known IDs',
        'unusedImagesPage' : u'Wikipedia:WikiProject Historic sites/Unused images of Antarctic Protected Areas',
        'commonsCategoryBase': u'Antarctic Protected Areas',
        #'registrantUrlBase' : Url is in the template    
        'namespaces' : [0],
        'table' : u'monuments_aq_(en)',
        'truncate' : False,
        'primkey' : ('type', 'number'),
        'fields' : [
            {
                'source' : u'type',
                'dest' : u'type',
                'type' : 'varchar(4)',
            },
            {
                'source' : u'number',
                'dest' : u'number',
                'type' : 'int(4)',
            },
            {
                'source' : u'name',
                'dest' : u'name',
            },
            {
                'source' : u'description',
                'dest' : u'description',
            },
            {
                'source' : u'proponent',
                'dest' : u'proponent',
            },
            {
                'source' : u'management',
                'dest' : u'management',
            },
            {
                'source' : u'adopted',
                'dest' : u'adopted',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'area',
                'dest' : u'area',
            },
            {
                'source' : u'M_plan',
                'dest' : u'M_plan',
            },
            {
                'source' : u'alt_country1',
                'dest' : u'alt_country1',
            },
            {
                'source' : u'alt_number1',
                'dest' : u'alt_number1',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'url',
                'dest' : u'registrant_url',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'name',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
        ],
    },
    ('ar', 'es') : { # Monuments in Argentina in Spanish
        'project' : u'wikipedia',
        'lang' : u'es',
        'headerTemplate' : u'MonumentoArgentina/encabezado',
        'rowTemplate' : u'MonumentoArgentina',
        'commonsTemplate' : u'Monumento Argentino',
        'commonsTrackerCategory' : u'Monuments in Argentina with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Argentina',
        'autoGeocode' : True,
        'unusedImagesPage' : u'Wikiproyecto:Patrimonio histórico/Fotos de monumentos de Argentina sin usar',
        'imagesWithoutIdPage' : u'Wikiproyecto:Patrimonio histórico/Fotos de monumentos de Argentina sin id',
        'namespaces' : [104],
        'table' : u'monuments_ar_(es)',
        'truncate' : False,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'id',
                'type' : 'varchar(15)',
            },
            {
                'source' : u'prov-iso',
                'dest' : u'prov-iso',
            },
            {
                'source' : u'monumento',
                'dest' : u'monumento',
            },
            {
                'source' : u'municipio',
                'dest' : u'municipio',
            },
            {
                'source' : u'localidad',
                'dest' : u'localidad',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'long',
                'dest' : u'lon',
            },
            {
                'source' : u'dirección',
                'dest' : u'direccion',
            },
            {
                'source' : u'tipo',
                'dest' : u'tipo',
            },
            {
                'source' : u'monumento_enlace',
                'dest' : u'monumento_enlace',
                'default' : u'monumento',
            },
            {
                'source' : u'enlace',
                'dest' : u'enlace',
            },
            {
                'source' : u'monumento_desc',
                'dest' : u'monumento_desc',
            },
            {
                'source' : u'monumento_categoría',
                'dest' : u'monumento_categoria',
            },
            {
                'source' : u'imagen',
                'dest' : u'imagen',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'monumento_enlace',
                'dest' : u'monument_article',
                # 'conv' : u'extractWikilink',
            },
        ],
    },
    ('at', 'de') : { # Monuments in Austria in German
        'project' : u'wikipedia',
        'lang' : u'de',
        'headerTemplate' : u'Denkmalliste Österreich Tabellenkopf',
        'rowTemplate' : u'Denkmalliste Österreich Tabellenzeile',
        'footerTemplate' : u'Denkmalliste Österreich Tabellenfuß',
        'commonsTemplate' : u'Denkmalgeschütztes Objekt Österreich',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Austria with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Austria',
        'autoGeocode' : True,
        'unusedImagesPage' : u'User:Multichill/Unused Denkmal Österreich',
        'imagesWithoutIdPage' : u'User:Multichill/Denkmal Österreich without ID',
        'namespaces' : [0],
        'table' : u'monuments_at_(de)',
        'truncate' : False, # Not all ids are filled, just overwrite it
        'primkey' : u'objektid',
        'fields' : [
            {
                'source' : u'ObjektID',
                'dest' : u'objektid',
                'type' : 'varchar(11)',
                'default' : '0',
            },
            {
                'source' : u'Foto',
                'dest' : u'foto',
            },
            {
                'source' : u'Fotobeschreibung',
                'dest' : u'fotobeschreibung',
            },
            {
                'source' : u'Commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'Name',
                'dest' : u'name',
            },
            {
                'source' : u'Artikel',
                'dest' : u'artikel',
            },
            {
                'source' : u'Anzeige-Name',
                'dest' : u'anzeige-Name',
            },
            {
                'source' : u'Adresse',
                'dest' : u'adresse',
            },
            {
                'source' : u'Adresse-Sort',
                'dest' : u'adresse-sort',
            },
            {
                'source' : u'Region-ISO',
                'dest' : u'region-iso',
            },
            {
                'source' : u'Katastralgemeinde',
                'dest' : u'katastralgemeinde',
            },
            {
                'source' : u'Gemeinde',
                'dest' : u'gemeinde',
            },
            {
                'source' : u'Gemeindekennzahl',
                'dest' : u'gemeindekennzahl',
                'type' : 'int(11)',
            },
            {
                'source' : u'Bezirk',
                'dest' : u'bezirk',
            },
            {
                'source' : u'Bezirkskennzahl',
                'dest' : u'bezirkskennzahl',
                'type' : 'int(11)',
            },
            {
                'source' : u'Grundstücksnummer',
                'dest' : u'grundstucksnummer',
            },
            {
                'source' : u'Status',
                'dest' : u'status',
            },
            {
                'source' : u'Beschreibung',
                'dest' : u'beschreibung',
            },
            {
                'source' : u'Bearbeitungsdatum',
                'dest' : u'bearbeitungsdatum',
            },
            {
                'source' : u'Breitengrad',
                'dest' : u'lat',
            },
            {
                'source' : u'Längengrad',
                'dest' : u'lon',
            },
        ],
    },
    ('be-bru', 'nl') : { # Monuments in Brussels in Dutch
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
                'source' : u'code',
                'dest' : u'code',
                'type' : 'varchar(25)',
                'default' : '0',
            },
            {
                'source' : u'omschrijving',
                'dest' : u'omschrijving',
            },
            {
                'source' : u'plaats',
                'dest' : u'plaats',
            },
            {
                'source' : u'adres',
                'dest' : u'adres',
            },
            {
                'source' : u'bouwjaar',
                'dest' : u'bouwjaar',
            },
            {
                'source' : u'bouwdoor',
                'dest' : u'bouwdoor',
            },
            {
                'source' : u'bouwstijl',
                'dest' : u'bouwstijl',
            },
            {
                'source' : u'objtype',
                'dest' : u'objtype',
            },
            {
                'source' : u'beschermd',
                'dest' : u'beschermd',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'omschrijving',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
        ],
    },
    ('be-vlg', 'en') : { # Onroerend Erfgoed in Vlaanderen in English
        'project' : u'wikipedia',
        'lang' : u'en',
        'headerTemplate' : u'Table header BE',
        'rowTemplate' : u'Table row BE',
        'commonsTemplate' : u'Onroerend erfgoed',
        'commonsTrackerCategory' : u'Onroerend erfgoed with known IDs',
        'commonsCategoryBase' : u'Onroerend erfgoed in Flanders',
        'autoGeocode' : False,
        #'unusedImagesPage' : u'',
        #'imagesWithoutIdPage' : u'', #u'',
        'registrantUrlBase' : u'https://inventaris.onroerenderfgoed.be/dibe/relict/%s',
        'namespaces' : [0],
        'table' : u'monuments_be-vlg_(en)',
        'truncate' : False,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'id',
                'type' : 'int(11)',
            },
            {
                'source' : u'town',
                'dest' : u'town',
            },
            {
                'source' : u'commune',
                'dest' : u'commune',
            },
            {
                'source' : u'prov-iso',
                'dest' : u'prov-iso',
            },
            {
                'source' : u'section',
                'dest' : u'section',
            },
            {
                'source' : u'address',
                'dest' : u'address',
            },
            {
                'source' : u'descr_en',
                'dest' : u'descr_en',
            },
            {
                'source' : u'objectnaam',
                'dest' : u'objectnaam',
            },
            {
                'source' : u'descr_de',
                'dest' : u'descr_de',
            },
            {
                'source' : u'nom_objet',
                'dest' : u'nom_objet',
            },
            {
                'source' : u'date',
                'dest' : u'date',
            },
            {
                'source' : u'architect',
                'dest' : u'architect',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'descr_en',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'id',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('be-vlg', 'fr') : { # Onroerend Erfgoed in Vlaanderen in French
        'project' : u'wikipedia',
        'lang' : u'fr',
        'headerTemplate' : u'En-tête de tableau MH-Fla',
        'rowTemplate' : u'Ligne de tableau MH-Fla',
        'commonsTemplate' : u'Onroerend erfgoed',
        'commonsTrackerCategory' : u'Onroerend erfgoed with known IDs',
        'commonsCategoryBase' : u'Onroerend erfgoed in Flanders',
        'autoGeocode' : True,
        'unusedImagesPage' : u'Projet:Monuments historiques/Images de monuments en Région flamande non utilisées',
        #'imagesWithoutIdPage' : u'', #u'Wikipedia:Wikiproject/Erfgoed/Belgische Erfgoed Inventarisatie/Vlaanderen/Foto\'s zonder id',
        'registrantUrlBase' : u'https://inventaris.onroerenderfgoed.be/dibe/relict/%s',
        'namespaces' : [0],
        'table' : u'monuments_be-vlg_(fr)',
        'truncate' : False,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'id',
                'type' : 'int(11)',
            },
            {
                'source' : u'classement',
                'dest' : u'classement',
            },
            {
                'source' : u'commune',
                'dest' : u'commune',
            },
            {
                'source' : u'section_communale',
                'dest' : u'section_communale',
            },
            {
                'source' : u'section_communale_id',
                'dest' : u'section_communale_id',
                'type' : 'varchar(25)',
            },
            {
                'source' : u'prov-iso',
                'dest' : u'prov-iso',
            },
            {
                'source' : u'adresse',
                'dest' : u'adresse',
            },
            {
                'source' : u'nom_objet',
                'dest' : u'nom_objet',
            },
            {
                'source' : u'année_construction',
                'dest' : u'annee_construction',
            },
            {
                'source' : u'architecte',
                'dest' : u'architecte',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'nom_objet',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'id',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('be-vlg', 'nl') : { # Onroerend Erfgoed in Vlaanderen in Dutch
        'project' : u'wikipedia',
        'lang' : u'nl',
        'headerTemplate' : u'Tabelkop erfgoed Vlaanderen',
        'rowTemplate' : u'Tabelrij erfgoed Vlaanderen',
        'commonsTemplate' : u'Onroerend erfgoed',
        'commonsTrackerCategory' : u'Onroerend erfgoed with known IDs',
        'commonsCategoryBase' : u'Onroerend erfgoed in Flanders',
        'autoGeocode' : True,
        'unusedImagesPage' : u'Wikipedia:Wikiproject/Erfgoed/Belgische Erfgoed Inventarisatie/Vlaanderen/Ongebruikte foto\'s',
        'imagesWithoutIdPage' : u'Wikipedia:Wikiproject/Erfgoed/Belgische Erfgoed Inventarisatie/Vlaanderen/Foto\'s zonder id',
        'registrantUrlBase' : u'https://inventaris.onroerenderfgoed.be/dibe/relict/%s',
        'namespaces' : [0],
        'table' : u'monuments_be-vlg_(nl)',
        'truncate' : False,
        'primkey' : u'id',
        'countryBbox' : u'2.3,49.4,6.8,51.74',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'id',
                'type' : 'int(11)',
            },
            {
                'source' : u'beschermd',
                'dest' : u'beschermd',
            },
            {
                'source' : u'gemeente',
                'dest' : u'gemeente',
            },
            {
                'source' : u'deelgem',
                'dest' : u'deelgem',
            },
            {
                'source' : u'deelgem_id',
                'dest' : u'deelgem_id',
                'type' : 'varchar(25)',
            },
            {
                'source' : u'prov-iso',
                'dest' : u'prov-iso',
            },
            {
                'source' : u'adres',
                'dest' : u'adres',
            },
            {
                'source' : u'objectnaam',
                'dest' : u'objectnaam',
            },
            {
                'source' : u'bouwjaar',
                'dest' : u'bouwjaar',
            },
            {
                'source' : u'architect',
                'dest' : u'architect',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
                'check' : u'checkLat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
                'check' : u'checkLon',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'objectnaam',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'id',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('be-wal', 'en') : { # Protected heritage sites in Wallona in English
        'project' : u'wikipedia',
        'lang' : u'en',
        'headerTemplate' : u'Table header Wallonia', # Should get a better name
        'rowTemplate' : u'Table row Wallonia', # Should get a better name
        'commonsTemplate' : u'Monument Wallonie',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Wallonia with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Wallonia',
        'autoGeocode' : True,
        'unusedImagesPage' : u'Wikipedia:WikiProject Historic sites/Unused images of protected heritage sites in Wallonia',
        #'imagesWithoutIdPage' : u'Wikipedia:Wikiproject/Erfgoed/Belgische Erfgoed Inventarisatie/Wallonië/Foto\'s zonder id',
        'registrantUrlBase' : u'',
        'namespaces' : [0],
        'table' : u'monuments_be-wal_(en)',
        'truncate' : False,
        'primkey' : ('niscode', 'objcode'),
        'fields' : [
            {
                'source' : u'niscode',
                'dest' : u'niscode',
                'type' : 'int(8)',
            },
            {
                'source' : u'objcode',
                'dest' : u'objcode',
                'type' : 'varchar(15)',
                'default' : '0',
            },
            {
                'source' : u'descr_en',
                'dest' : u'descr_en',
            },
            {
                'source' : u'descr_de',
                'dest' : u'descr_de',
            },
            {
                'source' : u'descr_nl',
                'dest' : u'descr_nl',
            },
            {
                'source' : u'descr_fr',
                'dest' : u'descr_fr',
            },
            {
                'source' : u'section', # Commune, something is wrong here
                'dest' : u'section',
            },
            {
                'source' : u'town', # Deelgemeente, something is wrong here
                'dest' : u'town',
            },
            {
                'source' : u'prov-iso',
                'dest' : u'prov-iso',
            },
            {
                'source' : u'address',
                'dest' : u'address',
            },
            {
                'source' : u'objtype',
                'dest' : u'objtype',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'architect',
                'dest' : u'architect',
            },
            {
                'source' : u'date',
                'dest' : u'date',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'descr_en',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'', # niscode + '-' + objcode
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('be-wal', 'fr') : { # Patrimoine immobilier classé in Wallonië in French
        'project' : u'wikipedia',
        'lang' : u'fr',
        'headerTemplate' : u'En-tête de tableau MH-Wal',
        'rowTemplate' : u'Ligne de tableau MH-Wal',
        'commonsTemplate' : u'Monument Wallonie',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Wallonia with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Wallonia',
        'autoGeocode' : True,
        'unusedImagesPage' : u'Projet:Monuments_historiques/Images de monuments en Région wallonne non utilisées',
        #'imagesWithoutIdPage' : u'Wikipedia:Wikiproject/Erfgoed/Belgische Erfgoed Inventarisatie/Wallonië/Foto\'s zonder id',
        'registrantUrlBase' : u'',
        'namespaces' : [0],
        'table' : u'monuments_be-wal_(fr)',
        'truncate' : False,
        'primkey' : ('id_commune', 'clt-pex','id_objet'), # or do I use CLT/PEX here?
        'fields' : [
            {
                'source' : u'id_commune',
                'dest' : u'id_commune',
                'type' : 'int(8)',
            },
            {
                'source' : u'CLT/PEX',
                'dest' : u'clt-pex',
                'type' : 'varchar(6)',
                'default' : '0',
            },
            {
                'source' : u'id_objet',
                'dest' : u'id_objet',
                'type' : 'varchar(15)',
                'default' : '0',
            },
            {
                'source' : u'descr_de',
                'dest' : u'descr_de',
            },
            {
                'source' : u'descr_nl',
                'dest' : u'descr_nl',
            },
            {
                'source' : u'nom_objet',
                'dest' : u'nom_objet',
            },
            {
                'source' : u'commune',
                'dest' : u'commune',
            },
            {
                'source' : u'section_communale',
                'dest' : u'section_communale',
            },
            {
                'source' : u'adresse',
                'dest' : u'adresse',
            },
            {
                'source' : u'prov-iso',
                'dest' : u'prov-iso',
            },
            {
                'source' : u'objtype',
                'dest' : u'objtype',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'architecte',
                'dest' : u'architecte',
            },
            {
                'source' : u'année_construction',
                'dest' : u'annee_construction',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'portrait',
                'dest' : u'',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'titre coordonnées',
                'dest' : u'',
            },
            {
                'source' : u'nom_objet',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'', # niscode + '-' + objcode
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('be-wal', 'nl') : { # Beschermd Erfgoed in Wallonië in Dutch
        'project' : u'wikipedia',
        'lang' : u'nl',
        'headerTemplate' : u'Tabelkop erfgoed Wallonië',
        'rowTemplate' : u'Tabelrij erfgoed Wallonië',
        'commonsTemplate' : u'Monument Wallonie',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Wallonia with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Wallonia',
        'autoGeocode' : True,
        'unusedImagesPage' : u'Wikipedia:Wikiproject/Erfgoed/Belgische Erfgoed Inventarisatie/Wallonië/Ongebruikte foto\'s',
        'imagesWithoutIdPage' : u'Wikipedia:Wikiproject/Erfgoed/Belgische Erfgoed Inventarisatie/Wallonië/Foto\'s zonder id',
        'registrantUrlBase' : u'',
        'namespaces' : [0],
        'table' : u'monuments_be-wal_(nl)',
        'truncate' : False, 
        'primkey' : ('niscode', 'objcode'),
        'fields' : [
            {
                'source' : u'niscode',
                'dest' : u'niscode',
                'type' : 'int(8)',
            },
            {
                'source' : u'objcode',
                'dest' : u'objcode',
                'type' : 'varchar(15)',
                'default' : '0',
            },
            {
                'source' : u'descr_de',
                'dest' : u'descr_de',
            },
            {
                'source' : u'descr_nl',
                'dest' : u'descr_nl',
            },
            {
                'source' : u'descr_fr',
                'dest' : u'descr_fr',
            },
            {
                'source' : u'gemeente',
                'dest' : u'gemeente',
            },
            {
                'source' : u'deelgemeente',
                'dest' : u'deelgemeente',
            },
            {
                'source' : u'adres',
                'dest' : u'adres',
            },
            {
                'source' : u'prov-iso',
                'dest' : u'prov-iso',
            },
            {
                'source' : u'objtype',
                'dest' : u'objtype',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'architect',
                'dest' : u'architect',
            },
            {
                'source' : u'bouwjaar',
                'dest' : u'bouwjaar',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'descr_nl',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'', # niscode + '-' + objcode
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('bo', 'es') : { # Monuments in Bolivia in Spanish
        'project' : u'wikipedia',
        'lang' : u'es',
        'headerTemplate' : u'MonumentoBolivia/encabezado',
        'rowTemplate' : u'MonumentoBolivia',
        'commonsTemplate' : u'Monumento Bolivia',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Bolivia with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Bolivia',
        'autoGeocode' : True,
        'unusedImagesPage' : u'Wikiproyecto:Patrimonio histórico/Fotos de monumentos de Bolivia sin usar',
        'imagesWithoutIdPage' : u'Wikiproyecto:Patrimonio histórico/Fotos de monumentos de Bolivia sin id',
        'namespaces' : [104],
        'table' : u'monuments_bo_(es)',
        'truncate' : False,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'id',
                'type' : 'varchar(11)',
            },
            {
                'source' : u'enlace',
                'dest' : u'enlace',
            },
            {
                'source' : u'monumento_enlace',
                'dest' : u'monumento_enlace',
            },
            {
                'source' : u'monumento_desc',
                'dest' : u'monumento_desc',
            },
            {
                'source' : u'monumento',
                'dest' : u'monumento',
            },
            {
                'source' : u'ISO',
                'dest' : u'iso',
            },
            {
                'source' : u'departamento',
                'dest' : u'departamento',
            },
            {
                'source' : u'municipio',
                'dest' : u'municipio',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'long',
                'dest' : u'lon',
            },
            {
                'source' : u'dirección',
                'dest' : u'direccion',
            },
            {
                'source' : u'imagen',
                'dest' : u'image',
            },
            {
                'source' : u'tipo',
                'dest' : u'tipo',
            },
            {
                'source' : u'monumento_categoría',
                'dest' : u'commonscat',
            },
        ],
    },
    ('by', 'be-x-old') : { # Belarus in Belarussian
        'project' : u'wikipedia',
        'lang' : u'be-x-old',
        'headerTemplate' : u'Вікі любіць славутасьці/Вяршыня сьпісу',
        'rowTemplate' : u'Вікі любіць славутасьці/Элемэнт сьпісу',
        'commonsTemplate' : u'Belarus heritage',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Belarus with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Belarus',
        'autoGeocode' : True,
        'unusedImagesPage' : u'User:ErfgoedBot/Unused images of Belarusian heritage monuments',
        'imagesWithoutIdPage' : u'User:ErfgoedBot/Images of Belarusian heritage monuments without ID',
        'namespaces' : [4],
        'table' : u'monuments_by_(be-x-old)',
        'truncate' : False,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'шыфр',
                'dest' : u'id',
                'type' : u'varchar(25)',
                'default' : '0'
            },
            {
                'source' : u'назва',
                'dest' : u'name',
            },
            {
                'source' : u'vobłaść-iso',
                'dest' : u'oblast-iso',
            },
            {
                'source' : u'rajon',
                'dest' : u'rajon',
            },
            {
                'source' : u'датаваньне',
                'dest' : u'date',
            },
            {
                'source' : u'населены пункт',
                'dest' : u'place',
            },
            {
                'source' : u'адрэса',
                'dest' : u'address',
            },
            {
                'source' : u'катэгорыя',
                'dest' : u'category',
            },
            {
                'source' : u'шырата',
                'dest' : u'lat',
            },
            {
                'source' : u'даўгата',
                'dest' : u'lon',
            },
            {
                'source' : u'каардынаты',
                'dest' : u'coordinates',
            },
            {
                'source' : u'выява',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'грамадзкі набытак', # Boolean, not clear what the purpose is
                'dest' : u'',
            },
            {
                'source' : u'name',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
        ],
    },
    ('ca', 'en') : { # Historic Places of Canada in English
        'project' : u'wikipedia',
        'lang' : u'en',
        'headerTemplate' : u'HPC header',
        'rowTemplate' : u'HPC row',
        'commonsTemplate' : u'Historic Places in Canada',
        'commonsTrackerCategory' : u'Heritage properties in Canada with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Canada',
        'autoGeocode' : False, # Wait for corrections
        'unusedImagesPage' : u'Wikipedia:WikiProject Historic sites/Unused images of Historic Places in Canada',
        #'imagesWithoutIdPage' : u'Wikipedia:WikiProject Historic sites/Images of Historic Places in Canada without id',
        'registrantUrlBase' : u'http://www.historicplaces.ca/en/rep-reg/place-lieu.aspx?id=%s',
        'namespaces' : [0],
        'table' : u'monuments_ca_(en)',
        'truncate' : True,
        'primkey' : u'dummyid', # Work with a dummy id for now. Three fields with ids, messy!
        'fields' : [
            {
                'source' : u'dummyid',
                'dest' : u'dummyid',
                'type' : 'int(11)',
                'auto_increment' : True,
            },
            {
                'source' : u'name',
                'dest' : u'name',
                'type' : '',
            },
            {
                'source' : u'address',
                'dest' : u'address',
            },
            {
                'source' : u'municipality',
                'dest' : u'municipality',
            },
            {
                'source' : u'prov_iso',
                'dest' : u'prov_iso',
            },
            {
                'source' : u'pc',
                'dest' : u'pc',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'idf',
                'dest' : u'idf',
                'type' : 'int(11)',
            },
            {
                'source' : u'idp',
                'dest' : u'idp',
                'type' : 'int(11)',
            },
            {
                'source' : u'idm',
                'dest' : u'idm',
                'type' : 'int(11)',
            },
            {
                'source' : u'name',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'idf', #FIXME: Should be a list or tuple of the 3 fields
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('ca', 'fr') : { # Historic Places of Canada in French
        'project' : u'wikipedia',
        'lang' : u'fr',
        'headerTemplate' : u'En-tête de tableau LPC',
        'rowTemplate' : u'Ligne de tableau LPC',
        'commonsTemplate' : u'Historic Places in Canada',
        'commonsTrackerCategory' : u'Heritage properties in Canada with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Canada',
        'autoGeocode' : False, # Wait for other tables
        'unusedImagesPage' : u'Projet:Monuments historiques/Images de monuments canada non utilisées',
        #'imagesWithoutIdPage' : u'',
        'registrantUrlBase' : u'http://www.historicplaces.ca/fr/rep-reg/place-lieu.aspx?id=%s',
        'namespaces' : [0, 100],
        'table' : u'monuments_ca_(fr)',
        'truncate' : False,
        'primkey' : u'numero',
        'fields' : [
            {
                'source' : u'numéro',
                'dest' : u'numero',
                'type' : 'int(11)',
            },
            {
                'source' : u'id', # (optionnel) ancre, par exemple une lettre majuscule pour l'utilisation d'un
                'dest' : u'id',
            },
            {
                'source' : u'niveau',
                'dest' : u'niveau',
            },
            {
                'source' : u'tri',
                'dest' : u'tri',
            },
            {
                'source' : u'lieu',
                'dest' : u'lieu',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'portrait',
                'dest' : u'portrait',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'municipalité',
                'dest' : u'municipalite',
            },
            {
                'source' : u'tri municipalité',
                'dest' : u'tri_municipalite',
            },
            {
                'source' : u'adresse',
                'dest' : u'adresse',
            },
            {
                'source' : u'tri adresse',
                'dest' : u'tri_adresse',
            },
            {
                'source' : u'prov_iso',
                'dest' : u'prov_iso',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'construction',
                'dest' : u'construction',
            },
            {
                'source' : u'protection',
                'dest' : u'protection',
            },
            {
                'source' : u'reconnaissance',
                'dest' : u'reconnaissance',
            },
            {
                'source' : u'notes',
                'dest' : u'notes',
            },
            {
                'source' : u'lieu',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'numero',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
	('ch', 'fr') : { # Monuments in Switzerland in French
        'project' : u'wikipedia',
        'lang' : u'fr',
        'headerTemplate' : u'En-tête de tableau Monuments (Suisse)',
        'rowTemplate' : u'Ligne de tableau Monuments (Suisse)',
        'commonsTemplate' : u'Cultural property of national significance in Switzerland',
        'commonsTrackerCategory' : u'Cultural properties of national significance in Switzerland with known IDs',
        'commonsCategoryBase' : u'Cultural properties of national significance in Switzerland',
        'unusedImagesPage' : u'Projet:Monuments historiques/Images de monuments suisse non utilisées',
        #'imagesWithoutIdPage' : u'',
        'namespaces' : [0],
        'table' : u'monuments_ch_(fr)',
        'truncate' : False,
        'primkey' : u'no pbc',
        'fields' : [
            {
                'source' : u'no PBC',
                'dest' : u'no pbc',
                'type' : 'int(11)',
            },
            {
                'source' : u'photo',
                'dest' : u'photo',
            },
			{
                'source' : u'description-photo',
                'dest' : u'description-photo',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'objet',
                'dest' : u'objet',
            },
            {
                'source' : u'objet-affiché',
                'dest' : u'objet-affiché',
            },
            {
                'source' : u'catégorie',
                'dest' : u'categorie',
            },
            {
                'source' : u'type',
                'dest' : u'type',
            },
            {
                'source' : u'adresse',
                'dest' : u'addresse',
            },
			{
                'source' : u'adresse-affichée',
                'dest' : u'adresse-affichee',
            },
            {
                'source' : u'latitude',
                'dest' : u'lat',
            },
            {
                'source' : u'longitude',
                'dest' : u'lon',
            },			
			{
                'source' : u'région-ISO',
                'dest' : u'region-iso',
            },			
            {
                'source' : u'commune',
                'dest' : u'commune',
            },
            {
                'source' : u'canton',
                'dest' : u'canton',
            },
            {
                'source' : u'Objet',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
        ]
    },	
    ('ch-old', 'de') : { # Monuments in Switzerland in German
        'project' : u'wikipedia',
        'lang' : u'de',
        'headerTemplate' : u'Kulturgüter Schweiz Tabellenkopf',
        'rowTemplate' : u'Kulturgüter Schweiz Tabellenzeile',
        'commonsTemplate' : u'Cultural property of national significance in Switzerland',
        'commonsTrackerCategory' : u'Cultural properties of national significance in Switzerland with known IDs',
        'commonsCategoryBase' : u'Cultural properties of national significance in Switzerland',
        'unusedImagesPage' : u'User:Multichill/Unused Schweizerisches Inventar der Kulturgüter von nationaler und regionaler Bedeutung images', # FIXME: Better name
        #'imagesWithoutIdPage' : u'',
        'namespaces' : [0],
        'table' : u'monuments-old_ch_(de)',
        'truncate' : False,
        'primkey' : u'kgs-nr',
        'fields' : [
            {
                'source' : u'KGS-Nr',
                'dest' : u'kgs-nr',
                'type' : 'int(11)',
            },
            {
                'source' : u'Name',
                'dest' : u'name',
            },
            {
                'source' : u'Adresse',
                'dest' : u'addresse',
            },
            {
                'source' : u'Gemeinde',
                'dest' : u'gemeinde',
            },
            {
                'source' : u'Kanton',
                'dest' : u'kanton',
            },
            {
                'source' : u'Breitengrad',
                'dest' : u'lat',
            },
            {
                'source' : u'Längengrad',
                'dest' : u'lon',
            },
            {
                'source' : u'Foto',
                'dest' : u'foto',
            },
            {
                'source' : u'Commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'Name',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
			{
                'source' : u'Typ',
                'dest' : u'typ',
            },
			{
                'source' : u'Region-ISO',
                'dest' : u'region-iso',
            },
        ]
    },
    ('ch-old', 'en') : { # Monuments in Switzerland in English
        'project' : u'wikipedia',
        'lang' : u'en',
        'headerTemplate' : u'SIoCPoNaRS header',
        'rowTemplate' : u'SIoCPoNaRS row',
        'commonsTemplate' : u'Cultural property of national significance in Switzerland',
        'commonsTrackerCategory' : u'Cultural properties of national significance in Switzerland with known IDs',
        'commonsCategoryBase' : u'Cultural properties of national significance in Switzerland',
        'unusedImagesPage' : u'Wikipedia:WikiProject Historic sites/Unused images of Cultural properties of national significance in Switzerland',
        #'imagesWithoutIdPage' : u'',
        'namespaces' : [0],
        'table' : u'monuments-old_ch_(en)',
        'truncate' : False,
        'primkey' : u'kgs_nr',
        'fields' : [
            {
                'source' : u'KGS_nr',
                'dest' : u'kgs_nr',
                'type' : 'int(11)',
            },
            {
                'source' : u'name',
                'dest' : u'name',
            },
            {
                'source' : u'address',
                'dest' : u'address',
            },
            {
                'source' : u'municipality',
                'dest' : u'municipality',
            },
            {
                'source' : u'canton',
                'dest' : u'canton',
            },
            {
                'source' : u'region-iso',
                'dest' : u'region-iso',
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
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'name',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
        ]
    },
    ('ch-old', 'it') : { # Monuments in Switzerland in Italian
        'project' : u'wikipedia',
        'lang' : u'it',
        'headerTemplate' : u'SIoCPoNaRS header',
        'rowTemplate' : u'SIoCPoNaRS row',
        'commonsTemplate' : u'Cultural property of national significance in Switzerland',
        'commonsTrackerCategory' : u'Cultural properties of national significance in Switzerland with known IDs',
        'commonsCategoryBase' : u'Cultural properties of national significance in Switzerland',
        'unusedImagesPage' : u'',
        #'imagesWithoutIdPage' : u'',
        'namespaces' : [0],
        'table' : u'monuments-old_ch_(it)',
        'truncate' : False,
        'primkey' : u'kgs_nr',
        'fields' : [
            {
                'source' : u'KGS_nr',
                'dest' : u'kgs_nr',
                'type' : 'int(11)',
            },
            {
                'source' : u'name',
                'dest' : u'name',
            },
            {
                'source' : u'address',
                'dest' : u'address',
            },
            {
                'source' : u'municipality',
                'dest' : u'municipality',
            },
            {
                'source' : u'canton',
                'dest' : u'canton',
            },
            {
                'source' : u'region-iso',
                'dest' : u'region-iso',
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
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'name',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
        ]
    },
    ('ch-old', 'fr') : { # Monuments in Switzerland in French
        'project' : u'wikipedia',
        'lang' : u'fr',
        'headerTemplate' : u'En-tête de tableau CH',
        'rowTemplate' : u'Ligne de tableau CH',
        'commonsTemplate' : u'Cultural property of national significance in Switzerland',
        'commonsTrackerCategory' : u'Cultural properties of national significance in Switzerland with known IDs',
        'commonsCategoryBase' : u'Cultural properties of national significance in Switzerland',
        'unusedImagesPage' : u'Projet:Monuments historiques/Images de monuments suisse non utilisées',
        #'imagesWithoutIdPage' : u'',
        'namespaces' : [0],
        'table' : u'monuments-old_ch_(fr)',
        'truncate' : False,
        'primkey' : u'kgs-nr',
        'fields' : [
            {
                'source' : u'kgs-nr',
                'dest' : u'kgs-nr',
                'type' : 'int(11)',
            },
            {
                'source' : u'Objet',
                'dest' : u'objet',
            },
            {
                'source' : u'Adresse',
                'dest' : u'addresse',
            },
            {
                'source' : u'Commune',
                'dest' : u'commune',
            },
            {
                'source' : u'canton',
                'dest' : u'canton',
            },
            {
                'source' : u'latitude',
                'dest' : u'lat',
            },
            {
                'source' : u'longitude',
                'dest' : u'lon',
            },
            {
                'source' : u'Photo',
                'dest' : u'photo',
            },
            {
                'source' : u'Commonscat',
                'dest' : u'commonscat',
            },
	    {
                'source' : u'region-iso',
                'dest' : u'region-iso',
            },
			{
                'source' : u'A',
                'dest' : u'typ_a',
            },
			{
                'source' : u'Arch',
                'dest' : u'typ_arch',
            },
			{
                'source' : u'B',
                'dest' : u'typ_b',
            },
			{
                'source' : u'E',
                'dest' : u'typ_e',
            },
			{
                'source' : u'M',
                'dest' : u'typ_m',
            },
			{
                'source' : u'O',
                'dest' : u'typ_o',
            },
			{
                'source' : u'S',
                'dest' : u'typ_s',
            },
            {
                'source' : u'Objet',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
        ]
    },
    ('cz', 'cs') : { # Monuments in Czech Republic in Czech language
        'project' : u'wikipedia',
        'lang' : u'cs',
        'headerTemplate' : u'Památky v Česku/začátek',
        'rowTemplate' : u'Památky v Česku',
        'commonsTemplate' : u'Cultural Heritage Czech Republic',
        'commonsTrackerCategory' : u'Cultural monuments in the Czech Republic with known IDs',
        'commonsCategoryBase' : u'Cultural monuments in the Czech Republic',
        'autoGeocode' : True,
        'unusedImagesPage' : u'Wikipedie:WikiProjekt Wiki Loves Monuments/Nevyužité obrázky',
        'imagesWithoutIdPage' : u'User:Multichill/Images of cultural heritage monuments in Czech Republic without id',
        'namespaces' : [0],
        'table' : u'monuments_cz_(cs)',
        'truncate' : False,
        'primkey' : u'id_objektu',
        'fields' : [
            {
                'source' : u'Id_objektu',
                'dest' : u'id_objektu',
                'type' : 'varchar(20)',
            },
            {
                'source' : u'Obrázek',
                'dest' : u'image',
            },
            {
                'source' : u'Commons',
                'dest' : u'commonscat',
            },
            {
                'source' : u'Název',
                'dest' : u'name',
            },
            {
                'source' : u'Článek',
                'dest' : u'monument_article',
            },
            {
                'source' : u'Adresa',
                'dest' : u'address',
            },
            {
                'source' : u'kraj-iso',
                'dest' : u'kraj-iso',
            },
            {
                'source' : u'okres-iso',
                'dest' : u'okres-iso',
            },
            {
                'source' : u'Obec',
                'dest' : u'municipality',
            },
            {
                'source' : u'Obec_článek',
                'dest' : u'municipality_article',
            },
			{
                'source' : u'Zeměpisná_šířka',
                'dest' : u'lat',
            },
			{
                'source' : u'Zeměpisná_délka',
                'dest' : u'lon',
            },
			{
                'source' : u'Popis',
                'dest' : u'description',
            },
			{
                'source' : u'Památkou_od',
                'dest' : u'monument_since',
            },
			{
                'source' : u'Poznámka',
                'dest' : u'remark',
            },
        ]
    },

    ('cl', 'es') : { # National monuments in Chile in Spanish
        'project' : u'wikipedia',
        'lang' : u'es',
        'headerTemplate' : u'MonumentoChile/encabezado',
        'rowTemplate' : u'MonumentoChile',
        'commonsTemplate' : u'Monumento Nacional de Chile',
        'commonsTrackerCategory' : u'National monuments in Chile with known IDs',
        'commonsCategoryBase' : u'National monuments in Chile',
        'unusedImagesPage' : u'Wikiproyecto:Patrimonio histórico/Fotos de Monumentos nacionales de Chile sin usar',
        'imagesWithoutIdPage' : u'Wikiproyecto:Patrimonio histórico/Fotos de Monumentos nacionales de Chile sin id',
        'namespaces' : [104],
        'table' : u'monuments_cl_(es)',
        'truncate' : False,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'id',
                'type' : 'int(5)',
            },
            {
                'source' : u'monumento',
                'dest' : u'monumento',
            },
            {
                'source' : u'monumento_enlace',
                'dest' : u'monumento_enlace',
            },
            {
                'source' : u'enlace',
                'dest' : u'enlace',
            },
            {
                'source' : u'monumento_categoría',
                'dest' : u'monumento_categoria',
            },
            {
                'source' : u'monumento_desc',
                'dest' : u'monumento_desc',
            },
            {
                'source' : u'comuna',
                'dest' : u'comuna',
            },
            {
                'source' : u'ISO',
                'dest' : u'ISO',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'long',
                'dest' : u'lon',
            },
            {
                'source' : u'dirección',
                'dest' : u'direccion',
            },
            {
                'source' : u'decreto',
                'dest' : u'decreto',
            },
            {
                'source' : u'fecha',
                'dest' : u'fecha',
            },
            {
                'source' : u'imagen',
                'dest' : u'imagen',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
               'source' : u'tipo',
               'dest' : u'tipo',
               'type' : "enum('Error', 'MH','ZT','SN')",
            },
            {
                'source' : u'monumento',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
        ],
    },
    ('co', 'es') : { # Monuments in Colombia in Spanish
        'project' : u'wikipedia',
        'lang' : u'es',
        'headerTemplate' : u'MonumentoColombia/encabezado',
        'rowTemplate' : u'MonumentoColombia',
        'commonsTemplate' : u'Monumento Nacional de Colombia',
        'commonsTrackerCategory' : u'National monuments in Colombia with known IDs',
        'commonsCategoryBase' : u'National monuments in Colombia',
        'unusedImagesPage' : u'Wikiproyecto:Patrimonio histórico/Fotos de monumentos de Colombia sin id',
        'imagesWithoutIdPage' : u'Wikiproyecto:Patrimonio histórico/Fotos de monumentos de Colombia sin usar',
        'namespaces' : [104],
        'table' : u'monuments_co_(es)',
        'truncate' : False,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'id',
                'type' : 'varchar(8)',
            },
            {
                'source' : u'monumento',
                'dest' : u'monumento',
            },
            {
                'source' : u'municipio',
                'dest' : u'municipio',
            },
            {
                'source' : u'departamento',
                'dest' : u'departamento',
            },
            {
                'source' : u'ISO',
                'dest' : u'iso',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'long',
                'dest' : u'lon',
            },
            {
                'source' : u'dirección',
                'dest' : u'direccion',
            },
            {
                'source' : u'tipo',
                'dest' : u'tipo',
            },
            {
                'source' : u'monumento_enlace',
                'dest' : u'monumento_enlace',
                'default' : u'monumento',
            },
            {
                'source' : u'enlace',
                'dest' : u'enlace',
            },
            {
                'source' : u'monumento_desc',
                'dest' : u'monumento_desc',
            },
            {
                'source' : u'monumento_categoría',
                'dest' : u'monumento_categoria',
            },
            {
                'source' : u'imagen',
                'dest' : u'imagen',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'monumento_enlace',
                'dest' : u'monument_article',
                # 'conv' : u'extractWikilink',
            },
        ],
    },
    ('de-by', 'de') : { # Baudenkmäler in Bayern in German
        'project' : u'wikipedia',
        'lang' : u'de',
        'headerTemplate' : u'Denkmalliste Bayern Tabellenkopf',
        'rowTemplate' : u'Denkmalliste Bayern Tabellenzeile',
        'commonsTemplate' : u'Baudenkmal Bayern',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Bavaria with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Bavaria',
        'unusedImagesPage' : u'Wikipedia:WikiProjekt Denkmalpflege/Deutschland/Bayern/Ungenutzte Bilder',
        'imagesWithoutIdPage' : u'Wikipedia:WikiProjekt Denkmalpflege/Deutschland/Bayern/Bilder ohne Nummer',
        'namespaces' : [0],
        'table' : u'monuments_de-by_(de)',
        'truncate' : False, # Not all ids are filled, just overwrite it
        'primkey' : u'nummer',
        'fields' : [
            {
                'source' : u'Nummer',
                'dest' : u'nummer',
                'type' : 'varchar(15)',
                'default' : '0',
            },
            {
                'source' : u'Gemeinde',
                'dest' : u'stadt',
            },
            {
                'source' : u'Ortsteil',
                'dest' : u'ortsteil',
            },
            {
                'source' : u'Adresse',
                'dest' : u'adresse',
            },
            {
                'source' : u'Bezeichnung',
                'dest' : u'bezeichnung',
            },
            {
                'source' : u'Artikel',
                'dest' : u'artikel',
            },
            {
                'source' : u'Beschreibung',
                'dest' : u'beschreibung',
            },
            {
                'source' : u'Bild',
                'dest' : u'bild',
            },
            {
                'source' : u'Commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'NS',
                'dest' : u'lat',
            },
            {
                'source' : u'EW',
                'dest' : u'lon',
            },
        ],
    },
    ('de-he', 'de') : { # Kulturdenkmäler in Hessen in German
        'project' : u'wikipedia',
        'lang' : u'de',
        'headerTemplate' : u'Denkmalliste Hessen Tabellenkopf',
        'rowTemplate' : u'Denkmalliste Hessen Tabellenzeile',
        'commonsTemplate' : u'Kulturdenkmal Hessen',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Hesse with known ID',
        'commonsCategoryBase' : u'Cultural heritage monuments in Hesse',
        'unusedImagesPage' : u'Wikipedia:WikiProjekt Denkmalpflege/Deutschland/Hessen/Ungenutzte Bilder',
        'imagesWithoutIdPage' : u'Wikipedia:WikiProjekt Denkmalpflege/Deutschland/Hessen/Bilder ohne Nummer',
        'registrantUrlBase' : u'http://denkxweb.denkmalpflege-hessen.de/cgi-bin/mapwalk.pl?event=Query.Details&obj=%s',    
        'namespaces' : [0],
        'table' : u'monuments_de-he_(de)',
        'truncate' : False, # Not all ids are filled, just overwrite it
        'primkey' : u'nummer',
        'fields' : [
            {
                'source' : u'Nummer',
                'dest' : u'nummer',
                'type' : 'int(11)',
            },
            {
                'source' : u'StadtOderGemeinde',
                'dest' : u'stadt',
            },
            {
                'source' : u'Ortsteil',
                'dest' : u'ortsteil',
            },
            {
                'source' : u'Adresse',
                'dest' : u'adresse',
            },
            {
                'source' : u'Bezeichnung',
                'dest' : u'bezeichnung',
            },
            {
                'source' : u'Artikel',
                'dest' : u'artikel',
            },
            {
                'source' : u'Beschreibung',
                'dest' : u'beschreibung',
            },
            {
                'source' : u'Bild',
                'dest' : u'bild',
            },
            {
                'source' : u'Commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'NS',
                'dest' : u'lat',
            },
            {
                'source' : u'EW',
                'dest' : u'lon',
            },
            {
                'source' : u'Nummer',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
            {
                'source' : u'Flur',
                'dest' : u'flur',
            },
            {
                'source' : u'Flurstück',
                'dest' : u'flurst',
            },
        ],
    },
    ('de-nrw-bm', 'de') : { # Baudenkmaeler in Bergheim in German
        'project' : u'wikipedia',
        'lang' : u'de',
        'headerTemplate' : u'Denkmalliste Bergheim Tabellenkopf',
        'rowTemplate' : u'Denkmalliste Bergheim Tabellenzeile',
        'commonsTemplate' : u'Kulturdenkmal Bergheim',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Bergheim with known ID',
        'commonsCategoryBase' : u'Cultural heritage monuments in Bergheim',
        'unusedImagesPage' : u'Wikipedia:Wiki Loves Monuments Bergheim/Ungenutzte Bilder',
        'imagesWithoutIdPage' : u'Wikipedia:Wiki Loves Monuments Bergheim/Bilder ohne Nummer',
        'namespaces' : [0],
        'table' : u'monuments_de-nrw-bm_(de)',
        'truncate' : False, # Not all ids are filled, just overwrite it
        'primkey' : u'nummer',
        'fields' : [
            {
                'source' : u'Nummer',
                'dest' : u'nummer',
                'type' : 'int(11)',
            },
            {
                'source' : u'Ortsteil',
                'dest' : u'ortsteil',
            },
            {
                'source' : u'Adresse',
                'dest' : u'adresse',
            },
            {
                'source' : u'Bezeichnung',
                'dest' : u'bezeichnung',
            },
            {
                'source' : u'Artikel',
                'dest' : u'artikel',
            },
            {
                'source' : u'Beschreibung',
                'dest' : u'beschreibung',
            },
            {
                'source' : u'Bauzeit',
                'dest' : u'bauzeit',
            },
            {
                'source' : u'Eintragung',
                'dest' : u'eintragung',
            },
            {
                'source' : u'Aktenzeichen',
                'dest' : u'aktenzeichen',
            },
            {
                'source' : u'Bild',
                'dest' : u'bild',
            },
            {
                'source' : u'Commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'NS',
                'dest' : u'lat',
            },
            {
                'source' : u'EW',
                'dest' : u'lon',
            },
        ],
    },
    ('de-nrw-k', 'de') : { #  Baudenkmäler in Cologne in German
        'project' : u'wikipedia',
        'lang' : u'de',
        'headerTemplate' : u'Denkmalliste Köln Tabellenkopf',
        'rowTemplate' : u'Denkmalliste Köln Tabellenzeile',
        'commonsTemplate' : u'Kulturdenkmal Köln',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Cologne with known ID',
        'commonsCategoryBase' : u'Cultural heritage monuments in Cologne',
        'unusedImagesPage' : u'Benutzer:Elya/Ungenutzte Bilder',
        'imagesWithoutIdPage' : u'Benutzer:Elya/Bilder ohne Nummer',
        'namespaces' : [0],
        'table' : u'monuments_de-nrw-k_(de)',
        'truncate' : False, # Not all ids are filled, just overwrite it
        'primkey' : u'nummer_denkmalliste',
        'fields' : [
            {
                'source' : u'Nummer_Denkmalliste',
                'dest' : u'nummer_denkmalliste',
                'type' : 'int(11)',
            },
            {
                'source' : u'Ortsteil',
                'dest' : u'ortsteil',
            },
            {
                'source' : u'Adresse',
                'dest' : u'adresse',
            },
            {
                'source' : u'Bezeichnung',
                'dest' : u'bezeichnung',
            },
            {
                'source' : u'Bauzeit',
                'dest' : u'bauzeit',
            },
            {
                'source' : u'Beschreibung',
                'dest' : u'beschreibung',
            },
            {
                'source' : u'Bild',
                'dest' : u'bild',
            },
            {
                'source' : u'Commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'NS',
                'dest' : u'lat',
            },
            {
                'source' : u'EW',
                'dest' : u'lon',
            },
            {
                'source' : u'bezeichnung',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
        ],
    },
    ('de-nrw', 'de') : { #  Baudenkmäler in NRW in German
        'project' : u'wikipedia',
        'lang' : u'de',
        'headerTemplate' : u'Denkmalliste Tabellenkopf de-nrw',
        'rowTemplate' : u'Denkmalliste Tabellenzeile de-nrw', # used for other monuments, too - fix later 
        'commonsTemplate' : u'Kulturdenkmal',
        'commonsTrackerCategory' : u'Cultural heritage monuments in NRW with known ID',
        'commonsCategoryBase' : u'Cultural heritage monuments in North Rhine-Westphalia',
        #'unusedImagesPage' : u'Benutzer:Elya/Ungenutzte Bilder',
        #'imagesWithoutIdPage' : u'Benutzer:Elya/Bilder ohne Nummer',
        'namespaces' : [0],
        'table' : u'monuments_de-nrw_(de)',
        'truncate' : False, # Not all ids are filled, just overwrite it
        'primkey' : (u'ags' ,u'nummer'),
        'fields' : [
            {
                'source' : u'Nummer',
                'dest' : u'nummer',
                'type' : 'int(11)',
            },
            {
                'source' : u'Bild',
                'dest' : u'bild',
            },
            {
                'source' : u'Abmessungen',
                'dest' : u'abmessungen',
            },
            {
                'source' : u'Commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'Bezeichnung',
                'dest' : u'bezeichnung',
            },
            {
                'source' : u'Ortsteil',
                'dest' : u'ortsteil',
            },
            {
                'source' : u'Adresse',
                'dest' : u'adresse',
            },
            {
                'source' : u'NS',
                'dest' : u'lat',
            },
            {
                'source' : u'EW',
                'dest' : u'lon',
            },
            {
                'source' : u'Region',
                'dest' : u'state-iso',
            },
            {
                'source' : u'Beschriftung',
                'dest' : u'beschriftung',
            },
            {
                'source' : u'Beschreibung',
                'dest' : u'beschreibung',
            },
            {
                'source' : u'Bauzeit',
                'dest' : u'bauzeit',
            },
            {
                'source' : u'Eintragung',
                'dest' : u'eintragung',
            },
            {
                'source' : u'ags',
                'dest' : u'ags', #header tpl
            },
            {
                'source' : u'ort',
                'dest' : u'ort', #header tpl
            },
            {
                'source' : u'stadtteil',
                'dest' : u'stadtteil', #header tpl
            },
            {
                'source' : u'bezeichnung',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
        ],
    },
    ('dk-bygning', 'da') : { # Bygninger in Denmark in Danish
        'project' : u'wikipedia',
        'lang' : u'da',
        'headerTemplate' : u'Tabelheader FBB',
        'rowTemplate' : u'Tabelrække FBB',
        'commonsTemplate' : u'Fredet bygning',
        'commonsTrackerCategory' : u'Listed buildings in Denmark with known IDs',
        'commonsCategoryBase' : u'Listed buildings in Denmark',
        'unusedImagesPage' : u'Wikipedia:Wiki Loves Monuments/Ubrugte filer med fredede bygninger i Danmark',
        'imagesWithoutIdPage' : u'User:Multichill/Protected buildings in Denmark without id',
        'registrantUrlBase' : u'https://www.kulturarv.dk/fbb/sagvis.pub?sag=%s',
        'namespaces' : [0],
        'table' : u'monuments_dk-bygninger_(da)',
        'truncate' : False,
        'primkey' : (u'kommunenr', u'ejendomsnr', u'bygningsnr'),
        'fields' : [
            {
                'source' : u'systemnrbyg',
                'dest' : u'systemnrbyg',
                'type' : 'int(11)',
            },
            {
                'source' : u'region-iso',
                'dest' : u'region-iso',
            },
            {
                'source' : u'kommune',
                'dest' : u'kommune',
            },
            {
                'source' : u'sagsnavn',
                'dest' : u'sagsnavn',
            },
            {
                'source' : u'komplekstype',
                'dest' : u'komplekstype',
            },
            {
                'source' : u'opførelsesår',
                'dest' : u'opforelsesar',
            },
            {
                'source' : u'adresse',
                'dest' : u'adresse',
            },
            {
                'source' : u'postnr',
                'dest' : u'postnr',
            },
            {
                'source' : u'by',
                'dest' : u'by',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'kommunenr',
                'dest' : u'kommunenr',
                'type' : 'int(11)',
            },
            {
                'source' : u'ejendomsnr',
                'dest' : u'ejendomsnr',
                'type' : 'int(11)',
            },
            {
                'source' : u'bygningsnr',
                'dest' : u'bygningsnr',
                'type' : 'int(11)',
            },
            {
                'source' : u'fredår',
                'dest' : u'fredar',
            },
            {
                'source' : u'sagsnr',
                'dest' : u'sagsnr',
                'type' : 'int(11)',
            },
            {
                'source' : u'billede',
                'dest' : u'billede',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'sagsnavn',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'sagsnr',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('dk-fortids', 'da') : { # Fortidsminder in Denmark in Danish
        'project' : u'wikipedia',
        'lang' : u'da',
        'headerTemplate' : u'Tabelheader FF',
        'rowTemplate' : u'Tabelrække FF',
        'commonsTemplate' : u'Fortidsminde',
        'commonsTrackerCategory' : u'Archaeological monuments in Denmark with known IDs',
        'commonsCategoryBase' : u'Archaeological monuments in Denmark',
        'unusedImagesPage' : u'Wikipedia:Wiki Loves Monuments/Ubrugte filer med fredede fortidsminder i Danmark',
        'imagesWithoutIdPage' : u'User:Multichill/Archaeological monuments in Denmark without id',
        'registrantUrlBase' : u'http://www.kulturarv.dk/fundogfortidsminder/Lokalitet/%s',
        'namespaces' : [0],
        'table' : u'monuments_dk-fortidsminder_(da)',
        'truncate' : False,
        'primkey' : u'systemnummer',
        'fields' : [
            {
                'source' : u'fredningsnummer',
                'dest' : u'fredningsnummer',
                'type' : 'int(11)',
            },
            {
                'source' : u'region-iso',
                'dest' : u'region-iso',
            },
            {
                'source' : u'kommune',
                'dest' : u'kommune',
            },
            {
                'source' : u'stednavn',
                'dest' : u'stednavn',
            },
            {
                'source' : u'type',
                'dest' : u'type',
            },
            {
                'source' : u'datering',
                'dest' : u'datering',
            },
            {
                'source' : u'seværdighed',
                'dest' : u'sevaedighed',
            },
            {
                'source' : u'systemnummer',
                'dest' : u'systemnummer',
                'type' : 'int(11)',
            },
            {
                'source' : u'anlnr',
                'dest' : u'anlnr',
                'type' : 'int(11)',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'billede',
                'dest' : u'billede',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'bemærkning',
                'dest' : u'bemaerkning',
            },
            {
                'source' : u'stednavn',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'systemnummer',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('ee', 'et') : { # Rijksmonumenten in the Estonia in Estoian
        'project' : u'wikipedia',
        'lang' : u'et',
        'headerTemplate' : u'KRR päis',
        'rowTemplate' : u'KRR rida',
        'commonsTemplate' : u'Kultuurimälestis',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Estonia (with known IDs)',
        'commonsCategoryBase' : u'Cultural heritage monuments in Estonia',
        'unusedImagesPage' : u'Vikipeedia:Vikiprojekt_Kultuuripärand/Kasutamata kultuurimälestiste pildid',
        'imagesWithoutIdPage' : u'Vikipeedia:Vikiprojekt_Kultuuripärand/Ilma registri numbrita pildid',    
        'registrantUrlBase' : u'http://register.muinas.ee/?menuID=monument&action=view&id=%s',    
        'namespaces' : [4],
        'table' : u'monuments_ee_(et)',
        'truncate' : False,
        'primkey' : u'number',
        'countryBbox' : u'20.72,57.36,28.6,60.03',
        'fields' : [
            {
                'source' : u'number',
                'dest' : u'number',
                'type' : 'int(11)',
            },
            {
                'source' : u'maakond',
                'dest' : u'maakond',
            },
            {
                'source' : u'region-iso',
                'dest' : u'region-iso',
            },

            {
                'source' : u'nimi',
                'dest' : u'nimi',
            },
            {
                'source' : u'liik',
                'dest' : u'liik',
            },
            {
                'source' : u'aadress',
                'dest' : u'aadress',
            },
            {
                'source' : u'omavalitsus',
                'dest' : u'omavalitsus',
            },
            {
                'source' : u'NS',
                'dest' : u'lat',
                'check' : u'checkLat',
            },
            {
                'source' : u'EW',
                'dest' : u'lon',
                'check' : u'checkLon',
            },
            {
                'source' : u'pilt',
                'dest' : u'pilt',
            },
            {
                'source' : u'commons',
                'dest' : u'commonscat',
            },
            {
                'source' : u'nimi',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'number',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ]
    },
    ('es', 'ca') : { # Spain in Catalan table
        'project' : u'wikipedia',
        'lang' : u'ca',
        'headerTemplate' : u'Capçalera BIC',
        'rowTemplate' : u'Filera BIC',
        'commonsTemplate' : u'BIC',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Spain with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Spain',
        'unusedImagesPage' : u'Viquiprojecte:Monuments/Imatges_per_utilitzar',
        'imagesWithoutIdPage' : u'User:Multichill/BIC without id',
        'registrantUrlBase' : u'',
        'namespaces' : [0],
        'table' : u'monuments_es_(ca)',
        'truncate' : False,
        'primkey' : u'bic',
        'fields' : [
            {
                'source' : u'bic',
                'dest' : u'bic',
                'type' : 'varchar(25)',
                'default' : '0',
            },
            {
                'source' : u'prot',
                'dest' : u'prot',
                'type' : "enum('BC','BIC')",
            },
            {
                'source' : u'idurl',
                'dest' : u'idurl',
            },
            {
                'source' : u'nom',
                'dest' : u'nom',
            },
            {
                'source' : u'tipus',
                'dest' : u'tipus',
            },
            {
                'source' : u'municipi',
                'dest' : u'municipi',
            },
            {
                'source' : u'lloc',
                'dest' : u'lloc',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'nomcoor',
                'dest' : u'nomcoor',
            },
            {
                'source' : u'imatge',
                'dest' : u'imatge',
            },
            {
                'source' : u'title',
                'dest' : u'title',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'regió1',
                'dest' : u'CCAA_iso',
            },
            {
                'source' : u'regió2',
                'dest' : u'provincia_iso',
            },
            {
                'source' : u'nom',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'',  # idurl: sipca/<IDFIELD>
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('es', 'es') : { # Rijksmonumenten in Spain in Spanish
        'project' : u'wikipedia',
        'lang' : u'es',
        'headerTemplate' : u'Cabecera BIC',
        'rowTemplate' : u'Fila BIC',
        'commonsTemplate' : u'BIC',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Spain with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Spain',
        'unusedImagesPage' : u'Wikiproyecto:Patrimonio histórico/Fotos de Bienes de Interés Cultural sin usar',
        'imagesWithoutIdPage' : u'User:Multichill/BIC without id',
        'namespaces' : [104],
        'table' : u'monuments_es_(es)',
        'truncate' : False,
        'primkey' : u'bic',
        'fields' : [
            {
                'source' : u'bic',
                'dest' : u'bic',
                'type' : 'varchar(25)',
                'default' : '0',
            },
            {
                'source' : u'nombre',
                'dest' : u'nombre',
            },
            {
                'source' : u'nombrecoor',
                'dest' : u'nombrecoor',
            },
            {
                'source' : u'tipobic',
                'dest' : u'tipobic',
            },
            {
                'source' : u'tipo',
                'dest' : u'tipo',
            },
            {
                'source' : u'municipio',
                'dest' : u'municipio',
            },
            {
                'source' : u'lugar',
                'dest' : u'lugar',
                'type' : 'varchar(400)',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'id_aut',
                'dest' : u'id_aut',
                'type' : 'varchar(21)',
            },
            {
                'source' : u'fecha',
                'dest' : u'fecha',
            },
            {
                'source' : u'imagen',
                'dest' : u'imagen',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
               'source' : u'title',
               'dest' : u'title',
            },
            {
                'source' : u'CCAA_iso',
		'dest' : u'CCAA_iso',
            },
            {
		'source' : u'provincia_iso',
		'dest' : u'provincia_iso',
            },
            {
                'source' : u'nombre',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
        ],
    },
    ('es-ct', 'ca') : { # Monuments in Catalunya in Catalan table
        'project' : u'wikipedia',
        'lang' : u'ca',
        'headerTemplate' : u'Capçalera IPA',
        'rowTemplate' : u'Filera IPA',
        'commonsTemplate' : u'BIC',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Spain with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Spain',
        'registrantUrlBase' : u'http://cultura.gencat.cat/invarquit/Fitxa.asp?idregistre=%s',
        'namespaces' : [0],
        'table' : u'monuments_es-ct_(ca)',
        'truncate' : False,
        'primkey' : u'bic',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'bic',
                'type' : 'varchar(25)',
                'default' : '0',
            },
            {
                'source' : u'idurl',
                'dest' : u'idurl',
            },
            {
                'source' : u'idurl2',
                'dest' : u'idurl2',
            },
            {
                'source' : u'prot',
                'dest' : u'prot',
                'type' : "enum('BCIN','BCIL')",
            },
            {
                'source' : u'idprot',
                'dest' : u'idprot',
            },
            {
                'source' : u'nom',
                'dest' : u'nom',
            },
            {
                'source' : u'estil',
                'dest' : u'estil',
            },
            {
                'source' : u'època',
                'dest' : u'epoca',
            },
            {
                'source' : u'municipi',
                'dest' : u'municipi',
            },
            {
                'source' : u'lloc',
                'dest' : u'lloc',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'nomcoor',
                'dest' : u'nomcoor',
            },
            {
                'source' : u'imatge',
                'dest' : u'imatge',
            },
            {
                'source' : u'title',
                'dest' : u'title',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'regió1',
                'dest' : u'CCAA_iso',
            },
            {
                'source' : u'regió2',
                'dest' : u'provincia_iso',
            },
            {
                'source' : u'nom',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'idurl',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('es-gl', 'gl') : { # Rijksmonumenten in Spain in Spanish
        'project' : u'wikipedia',
        'lang' : u'gl',
        'headerTemplate' : u'BIC-comezo',
        'rowTemplate' : u'BIC',
        'commonsTemplate' : u'BIC',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Spain with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Spain',
        'unusedImagesPage' : u'User:Multichill/Unused BIC',
        'imagesWithoutIdPage' : u'User:Multichill/BIC without id',
        'namespaces' : [0],
        'table' : u'monuments_es-gl_(gl)',
        'truncate' : False,
        'primkey' : u'bic',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'bic',
                'type' : 'varchar(25)',
            },
            {
                'source' : u'idurl',
                'dest' : u'idurl',
                'type' : 'int(3)',
            },
            {
                'source' : u'nomeoficial',
                'dest' : u'nomeoficial',
            },
            {
                'source' : u'outrosnomes',
                'dest' : u'outrosnomes',
            },
            {
                'source' : u'paxina',
                'dest' : u'paxina',
            },
            {
                'source' : u'concello',
                'dest' : u'concello',
            },
            {
                'source' : u'lugar',
                'dest' : u'lugar',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'notas',
                'dest' : u'notas',
            },
            {
                'source' : u'data_declaracion',
                'dest' : u'data_declaracion',
            },
            {
                'source' : u'imaxe',
                'dest' : u'imaxe',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
               'source' : u'title',
               'dest' : u'title',
            },
            {
               'source' : u'provincia_iso',
               'dest' : u'provincia_iso',
            },
            {
                'source' : u'nomeoficial',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
        ],
    },
    ('es-vc', 'ca') : { # Monuments in Valencia in Catalan table
        'project' : u'wikipedia',
        'lang' : u'ca',
        'headerTemplate' : u'Capçalera BIC Val',
        'rowTemplate' : u'Filera BIC Val',
        'commonsTemplate' : u'BIC',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Spain with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Spain',
        'registrantUrlBase' : u'http://www.cult.gva.es/dgpa/bics/Detalles_bics.asp?IdInmueble=%s',
        'namespaces' : [0],
        'table' : u'monuments_es-vc_(ca)',
        'truncate' : False,
        'primkey' : u'bic',
        'fields' : [
            {
                'source' : u'bic',
                'dest' : u'bic',
                'type' : 'varchar(25)',
                'default' : '0',
            },
            {
                'source' : u'idurl',
                'dest' : u'idurl',
                'type' : 'int(11)',
            },
            {
                'source' : u'nom',
                'dest' : u'nom',
            },
            {
                'source' : u'prot',
                'dest' : u'prot',
                'type' : "enum('BIC','BRL')",
            },
            {
                'source' : u'estil',
                'dest' : u'estil',
            },
            {
                'source' : u'època',
                'dest' : u'epoca',
            },
            {
                'source' : u'municipi',
                'dest' : u'municipi',
            },
            {
                'source' : u'lloc',
                'dest' : u'lloc',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'nomcoor',
                'dest' : u'nomcoor',
            },
            {
                'source' : u'imatge',
                'dest' : u'imatge',
            },
            {
               'source' : u'title',
               'dest' : u'title',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'regió1',
                'dest' : u'CCAA_iso',
            },
            {
                'source' : u'regió2',
                'dest' : u'provincia_iso',
            },
            {
                'source' : u'nom',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'idurl',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('fr', 'ca') : { # Monuments in France in Catalan table
        'project' : u'wikipedia',
        'lang' : u'ca',
        'headerTemplate' : u'Capçalera MH',
        'rowTemplate' : u'Filera MH',
        'commonsTemplate' : u'Mérimée',
        'commonsTrackerCategory' : u'Cultural heritage monuments in France with known IDs',
        'commonsCategoryBase' : u'Monuments historiques in France',
        'registrantUrlBase' : u'http://www.culture.gouv.fr/public/mistral/merimee_fr?ACTION=CHERCHER&FIELD_1=REF&VALUE_1=%s',
        'namespaces' : [0],
        'table' : u'monuments_fr_(ca)',
        'truncate' : False,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'id',
                'type' : 'varchar(11)',
                'default' : '0',
            },
            {
                'source' : u'nom',
                'dest' : u'nom',
            },
            {
                'source' : u'prot',
                'dest' : u'prot',
                'type' : "enum('Error', 'C','I')",
            },
            {
                'source' : u'època',
                'dest' : u'epoca',
            },
            {
                'source' : u'municipi',
                'dest' : u'municipi',
            },
            {
                'source' : u'lloc',
                'dest' : u'lloc',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'nomcoor',
                'dest' : u'nomcoor',
            },
            {
                'source' : u'imatge',
                'dest' : u'imatge',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'nom',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'id',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('fr', 'fr') : { # Monuments in France in French
        'project' : u'wikipedia',
        'lang' : u'fr',
        'headerTemplate' : u'En-tête de tableau MH',
        'rowTemplate' : u'Ligne de tableau MH',
        'commonsTemplate' : u'Mérimée',
        'commonsTrackerCategory' : u'Cultural heritage monuments in France with known IDs',
        'commonsCategoryBase' : u'Monuments historiques in France',
        'autoGeocode' : True,
        'unusedImagesPage' : u'Projet:Monuments historiques/Images de monuments français non utilisées',
        'imagesWithoutIdPage' : u'User:Multichill/Monument photos without an ID',
        'registrantUrlBase' : u'http://www.culture.gouv.fr/public/mistral/merimee_fr?ACTION=CHERCHER&FIELD_1=REF&VALUE_1=%s',
        'namespaces' : [0],
        'table' : u'monuments_fr_(fr)',
        'truncate' : False,
        'primkey' : u'notice',
        'fields' : [
            {
                'source' : u'tri',
                'dest' : u'tri',
                'default' : '0',
            },
            {
                'source' : u'monument',
                'dest' : u'monument',
            },
            {
                'source' : u'région_iso',
                'dest' : u'region_iso',
            },
            {
                'source' : u'département_iso',
                'dest' : u'departement_iso',
            },
            {
                'source' : u'commune',
                'dest' : u'commune',
            },
            {
                'source' : u'tri commune',
                'dest' : u'tri commune',
            },
            {
                'source' : u'adresse',
                'dest' : u'adresse',
            },
            {
                'source' : u'tri adresse',
                'dest' : u'tri adresse',
            },            {
                'source' : u'latitude',
                'dest' : u'lat',
            },
            {
                'source' : u'longitude',
                'dest' : u'lon',
            },
            {
                'source' : u'titre coordonnées',
                'dest' : u'titre_coordonnees',
            },
            {
                'source' : u'notice',
                'dest' : u'notice',
                'type' : 'varchar(11)',
                'default' : '0',
            },
            {
                'source' : u'protection',
                'dest' : u'protection',
            },
            {
                'source' : u'date',
                'dest' : u'date',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'portrait',
                'dest' : u'portrait',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'id',
                'dest' : u'id',
            },
            {
                'source' : u'monument',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'notice',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('gb-eng', 'en') : { # United Kingdom: Listed buildings in England in English
        'project' : u'wikipedia',
        'lang' : u'en',
        'headerTemplate' : u'EH listed building header',
        'rowTemplate' : u'EH listed building row',
        'commonsTemplate' : u'Listed building England',
        'commonsTrackerCategory' : u'Listed buildings in England with known IDs',
        'commonsCategoryBase' : u'Listed buildings in England',
        'autoGeocode' : True,
        'unusedImagesPage' : u'Wikipedia:WikiProject Historic sites/Unused images of listed buildings in England',
        'missingCommonscatPage' : u'',
        'imagesWithoutIdPage' : u'Wikipedia:WikiProject Historic sites/Images of listed buildings in England without ID',
        'registrantUrlBase' : u'http://list.english-heritage.org.uk/resultsingle.aspx?uid=%s',
        'namespaces' : [0],
        'table' : u'monuments_gb-eng_(en)',
        'truncate' : False,
        'primkey' : u'uid',
        'fields' : [
            {
                'source' : u'uid',
                'dest' : u'uid',
                'type' : 'int(11)',
            },
            {
                'source' : u'name',
                'dest' : u'name',
            },
            {
                'source' : u'location',
                'dest' : u'location',
            },
            {
                'source' : u'subdivision_iso',
                'dest' : u'subdivision_iso',
            },
            {
                'source' : u'type',
                'dest' : u'type',
            },
            {
                'source' : u'grade',
                'dest' : u'grade',
            },
            {
                'source' : u'architect',
                'dest' : u'architect',
            },
            {
                'source' : u'show_architect',
                'dest' : u'',
            },
            {
                'source' : u'date_listed', # I expect parser problems here
                'dest' : u'date_listed',
            },
            {
                'source' : u'show_listed',
                'dest' : u'',
            },
            {
                'source' : u'completed',
                'dest' : u'completed',
            },
            {
                'source' : u'grid_ref',
                'dest' : u'grid_ref',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'show_notes',
                'dest' : u'',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'show_img',
                'dest' : u'',
            },
            {
                'source' : u'upload_desc',
                'dest' : u'upload_desc',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'reference',
                'dest' : u'reference',
            },
            {
                'source' : u'show_ref',
                'dest' : u'',
            },
            {
                'source' : u'name',  # No links at the moment, this will cause problems
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'uid',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('gb-nir', 'en') : { # United Kingdom: Listed buildings in Northern Ireland in English
        'project' : u'wikipedia',
        'lang' : u'en',
        'headerTemplate' : u'NIEA listed building header',
        'rowTemplate' : u'NIEA listed building row',
        'commonsTemplate' : u'Listed building Northern Ireland',
        'commonsTrackerCategory' : u'Listed buildings in Northern Ireland with known IDs',
        'commonsCategoryBase' : u'Listed buildings in Northern Ireland',
        'autoGeocode' : True,
        'unusedImagesPage' : u'Wikipedia:WikiProject Historic sites/Unused images of listed buildings in Northern Ireland',
        'missingCommonscatPage' : u'',
        'imagesWithoutIdPage' : u'Wikipedia:WikiProject Historic sites/Images of listed buildings in Northern Ireland without ID',
        'registrantUrlBase' : u'http://www.doeni.gov.uk/niea/built/buildview?id=%s&js=true',
        'namespaces' : [0],
        'table' : u'monuments_gb-nir_(en)',
        'truncate' : False,
        'primkey' : u'hb',
        'fields' : [
            {
                'source' : u'hb',
                'dest' : u'hb',
                'type' : 'varchar(11)',
            },
            {
                'source' : u'address',
                'dest' : u'address',
            },
            {
                'source' : u'grid_ref',
                'dest' : u'grid_ref',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'type',
                'dest' : u'type',
            },
            {
                'source' : u'authority',
                'dest' : u'authority',
            },
            {
                'source' : u'subdivision_iso',
                'dest' : u'subdivision_iso',
            },
            {
                'source' : u'2nd_survey',
                'dest' : u'2nd_survey',
            },
            {
                'source' : u'1st_survey',
                'dest' : u'1st_survey',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'name',  # No links at the moment, this will cause problems
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'uid',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('gb-sct', 'en') : { # United Kingdom: Listed buildings in Scotland in English
        'project' : u'wikipedia',
        'lang' : u'en',
        'headerTemplate' : u'HB Scotland header',
        'rowTemplate' : u'HB Scotland row',
        'commonsTemplate' : u'Listed building Scotland',
        'commonsTrackerCategory' : u'Listed buildings in Scotland with known IDs',
        'commonsCategoryBase' : u'Listed buildings in Scotland',
        'autoGeocode' : True,
        'unusedImagesPage' : u'Wikipedia:WikiProject Historic sites/Unused images of listed buildings in Scotland',
        'imagesWithoutIdPage' : u'Wikipedia:WikiProject Historic sites/Images of listed buildings in Scotland without ID',
        'registrantUrlBase' : u'http://hsewsf.sedsh.gov.uk/hslive/portal.hsstart?P_HBNUM=%s',
        'namespaces' : [0],
        'table' : u'monuments_gb-sct_(en)',
        'truncate' : False,
        'primkey' : u'hbnum',
        'fields' : [
            {
                'source' : u'hbnum',
                'dest' : u'hbnum',
                'type' : 'int(11)',
            },
            {
                'source' : u'name',
                'dest' : u'name',
            },
            {
                'source' : u'notes',
                'dest' : u'notes',
            },
            {
                'source' : u'county',
                'dest' : u'county',
            },
            {
                'source' : u'subdivision_iso',
                'dest' : u'subdivision_iso',
            },
            {
                'source' : u'parbur',
                'dest' : u'parbur',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'category',
                'dest' : u'category',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'name',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'hbnum',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('gb-wls', 'en') : { # United Kingdom: Listed buildings in Wales in English
        'project' : u'wikipedia',
        'lang' : u'en',
        'headerTemplate' : u'Cadw listed building header',
        'rowTemplate' : u'Cadw listed building row',
        'commonsTemplate' : u'Listed building Wales',
        'commonsTrackerCategory' : u'Listed buildings in Wales with known IDs',
        'commonsCategoryBase' : u'Listed buildings in Wales',
        'autoGeocode' : True,
        'unusedImagesPage' : u'Wikipedia:WikiProject Historic sites/Unused images of listed buildings in Wales',
        'missingCommonscatPage' : u'',
        'imagesWithoutIdPage' : u'Wikipedia:WikiProject Historic sites/Images of listed buildings in Wales without ID',
        'registrantUrlBase' : u'', # No direct link possible. http://www.britishlistedbuildings.co.uk/wa-13539 is possible, but that's an external site
        'namespaces' : [0],
        'table' : u'monuments_gb-wls_(en)',
        'truncate' : False,
        'primkey' : u'hb',
        'fields' : [
            {
                'source' : u'hb',
                'dest' : u'hb',
                'type' : 'int(11)',
            },
            {
                'source' : u'name',
                'dest' : u'name',
            },
            {
                'source' : u'location',
                'dest' : u'location',
            },
            {
                'source' : u'subdivision_iso',
                'dest' : u'subdivision_iso',
            },
            {
                'source' : u'date_listed',
                'dest' : u'date_listed',
            },
            {
                'source' : u'grid_ref',
                'dest' : u'grid_ref',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'function',
                'dest' : u'function',
            },
            {
                'source' : u'notes',
                'dest' : u'notes',
            },
            {
                'source' : u'url',
                'dest' : u'url',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'upload_desc',
                'dest' : u'upload_desc',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'name', 
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'hb',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('gh', 'en') : { # Ghana monuments in English
        'project' : u'wikipedia',
        'lang' : u'en',
        'headerTemplate' : u'Ghana Monument header',
        'rowTemplate' : u'Ghana Monument row',
        'commonsTemplate' : u'Cultural Heritage Ghana',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Ghana with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Ghana',
        'autoGeocode' : False,
        'unusedImagesPage' : u'Wikipedia:WikiProject Historic sites/Unused images of Ghana\’s material cultural heritage',
        #'imagesWithoutIdPage' : u'Wikipedia:Wikiproject/Erfgoed/Nederlandse Erfgoed Inventarisatie/Foto\'s zonder id',
        'registrantUrlBase' : u'http://www.ghanamuseums.org/what-is-gmmb.php',
        'namespaces' : [0],
        'table' : u'monuments_gh_(en)',
        'truncate' : False,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'id',
                'type' : 'varchar(11)',
            },
            {
                'source' : u'name',
                'dest' : u'name',
            },
			 {
                'source' : u'alternative_names',
                'dest' : u'alternative_names',
            },
            {
                'source' : u'region',
                'dest' : u'region',
            }, 
            {
                'source' : u'region_iso',
                'dest' : u'region_iso',
            },
            {
                'source' : u'original_function',
                'dest' : u'original_function',
            }, 
            {
                'source' : u'built',
                'dest' : u'built',
            }, 
            {
                'source' : u'location',
                'dest' : u'location',
            }, 
            {
                'source' : u'comment',
                'dest' : u'comment',
            }, 
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'name',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
        ],
    },
    ('in', 'en') : { # Monuments in India in English
        'project' : u'wikipedia',
        'lang' : u'en',
        'headerTemplate' : u'ASI Monument header',
        'rowTemplate' : u'ASI Monument row',
        'commonsTemplate' : u'ASI Monument',
        'unusedImagesPage' : u'Wikipedia:WikiProject India/Wiki Loves Monuments/Unused ASI Monuments images',
        'commonsTrackerCategory' : u'ASI Monuments with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in India',
        'namespaces' : [0,4],
        'table' : u'monuments_in_(en)',
        'truncate' : True,
        'primkey' : u'number',
        'fields' : [
            {
                'source' : u'number',
                'dest' : u'number',
                'type' : 'varchar(20)',
            },
            {
                'source' : u'description',
                'dest' : u'description',
            },
            {
                'source' : u'location',
                'dest' : u'location',
            },
            {
                'source' : u'address',
                'dest' : u'address',
            },
            {
                'source' : u'district',
                'dest' : u'district',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'state_iso',
                'dest' : u'state_iso',
            },
 			 {
                'source' : u'circle',
                'dest' : u'circle',
                'type' : 'varchar(1)',
            },

        ],
    },
    ('ie', 'en') : { # Monuments in Ireland
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
                'type' : 'int(11)',
            },
            {
                'source' : u'name',
                'dest' : u'name',
            },
            {
                'source' : u'description',
                'dest' : u'description',
            },
            {
                'source' : u'townland',
                'dest' : u'townland',
            },
            {
                'source' : u'county',
                'dest' : u'county',
            },
            {
                'source' : u'region-iso',
                'dest' : u'region-iso',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'name',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
        ],
    },
    ('il', 'he') : { # Israel monuments in Hebrew
        'project' : u'wikipedia',
        'lang' : u'he',
        'headerTemplate' : u'אתר מורשת בישראל כותרת',
        'rowTemplate' : u'אתר מורשת בישראל בשורה',
        'commonsTemplate' : u'Heritage site in Israel',
        'commonsTrackerCategory' : u'Heritage sites in Israel with known IDs',
        'commonsCategoryBase' : u'Heritage sites in Israel',
        'autoGeocode' : False,
        'unusedImagesPage' : u'ויקיפדיה:מיזמי ויקיפדיה/Wiki Loves Monuments/Unused images',
        #'imagesWithoutIdPage' : u'Wikipedia:WikiProject National Register of Historic Places/Images without refnum',
        'namespaces' : [0, 4],
        'table' : u'monuments_il_(he)',
        'truncate' : False,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'מספר אתר',
                'dest' : u'id',
                'type' : 'varchar(20)',
            },
            {
                'source' : u'מחוז',
                'dest' : u'district',
            },
            {
                'source' : u'district-iso',
                'dest' : u'district-iso',
            },
            {
                'source' : u'שם אתר',
                'dest' : u'name',
            },
            {
                'source' : u'שם ערך',
                'dest' : u'article',
            },
            {
                'source' : u'שם אתר באנגלית',
                'dest' : u'name-en',
            },
            {
                'source' : u'תיאור אתר',
                'dest' : u'description',
            },
            {
                'source' : u'תיאור אתר באנגלית',
                'dest' : u'description-en',
            },
            {
                'source' : u'אדריכל',
                'dest' : u'architect',
            },
            {
                'source' : u'שנת הקמה',
                'dest' : u'year',
            },
            {
                'source' : u'סוג אתר',
                'dest' : u'type',
            },
            {
                'source' : u'קטגוריה בוויקישיתוף',
                'dest' : u'commonscat',
            },
            {
                'source' : u'כתובת',
                'dest' : u'address',
            },
            {
                'source' : u'רשות מקומית',
                'dest' : u'municipality',
            },
            {
                'source' : u'גוש',
                'dest' : u'area',
            },
            {
                'source' : u'חלקה',
                'dest' : u'lot',
            },
            {
                'source' : u'LAT',
                'dest' : u'lat',
            },
            {
                'source' : u'LONG',
                'dest' : u'lon',
            },
            {
                'source' : u'תמונה',
                'dest' : u'image',
            },
        ],
    },
    ('it', 'it') : { # Monuments in Italy in Italian 
        'project' : u'wikipedia',
        'lang' : u'it',
        'headerTemplate' : u'WLM-intestazione',
        'rowTemplate' : u'WLM-riga',
        'commonsTemplate' : u'Monumento italiano',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Italy with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Italy',
        'unusedImagesPage' : u'Progetto:Wiki Loves Monuments 2012/immagini inutilizzate',
        #'registrantUrlBase' : u'http://www.sardegnacultura.it/j/v/253?v=2&s=%s',
        'namespaces' : [102],
        'table' : u'monuments_it_(it)',
        'truncate' : False,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'id',
                'type' : 'varchar(20)'
            },
            {
                'source' : u'monumento',
                'dest' : u'monumento',
            },
            {
                'source' : u'wikivoce',
                'dest' : u'wikivoce',
            },
            {
                'source' : u'comune',
                'dest' : u'comune',
            },
            {
                'source' : u'comune-id',
                'dest' : u'comune-id',
            },
            {
                'source' : u'indirizzo',
                'dest' : u'indirizzo',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'long',
                'dest' : u'lon',
            },
            {
                'source' : u'regione',
                'dest' : u'regione',
            },
            {
                'source' : u'regione-iso',
                'dest' : u'regione-iso',
            },
            {
                'source' : u'prov-iso',
                'dest' : u'prov-iso',
            },
            {
                'source' : u'ente',
                'dest' : u'ente',
            },
            {
                'source' : u'immagine',
                'dest' : u'immagine',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
        ],
    },

    ('it-88', 'ca') : { # Monuments in Sardinia 
        'project' : u'wikipedia',
        'lang' : u'ca',
        'headerTemplate' : u'Capçalera BC Sard',
        'rowTemplate' : u'Filera BC Sard',
        'registrantUrlBase' : u'http://www.sardegnacultura.it/j/v/253?v=2&s=%s',
        'namespaces' : [0],
        'table' : u'monuments_it-88_(ca)',
        'truncate' : False,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'id',
                'type' : 'int(11)'
            },
            {
                'source' : u'nom',
                'dest' : u'nom',
            },
            {
                'source' : u'municipi',
                'dest' : u'municipi',
            },
            {
                'source' : u'lloc',
                'dest' : u'lloc',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'nomcoor',
                'dest' : u'nomcoor',
            },
            {
                'source' : u'imatge',
                'dest' : u'imatge',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'nom',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'id',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('it-bz', 'de') : { # Monuments in South Tirol in German
        'project' : u'wikipedia',
        'lang' : u'de',
        'headerTemplate' : u'Denkmalliste Südtirol Tabellenkopf',
        'rowTemplate' : u'Denkmalliste Südtirol Tabellenzeile',
        'footerTemplate' : u'Denkmalliste Südtirol Tabellenfuß',
        'commonsTemplate' : u'Denkmalgeschütztes Objekt Südtirol',
        'commonsTrackerCategory' : u'Cultural heritage monuments in South Tyrol with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in South Tyrol',
        'autoGeocode' : True,
        'unusedImagesPage' : u'Portal:Südtirol/Mitmachen/WLM2012/Ungenutzte Bilder',
        'imagesWithoutIdPage' : u'Portal:Südtirol/Mitmachen/WLM2012/Bilder ohne ID',
        'registrantUrlBase' : u'http://www.provinz.bz.it/denkmalpflege/themen/1071.asp?status=detail&id=%s',
        'namespaces' : [0],
        'table' : u'monuments_it-bz_(de)',
        'truncate' : False, # Not all ids are filled, just overwrite it
        'primkey' : u'objektid',
        'fields' : [
            {
                'source' : u'ObjektID',
                'dest' : u'objektid',
                'type' : 'varchar(11)',
                'default' : '0',
            },
            {
                'source' : u'Foto',
                'dest' : u'foto',
            },
            {
                'source' : u'Fotobeschreibung',
                'dest' : u'fotobeschreibung',
            },
            {
                'source' : u'Commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'Name',
                'dest' : u'name',
            },
            {
                'source' : u'Artikel',
                'dest' : u'artikel',
            },
            {
                'source' : u'Anzeige-Name',
                'dest' : u'anzeige-Name',
            },
            {
                'source' : u'Adresse',
                'dest' : u'adresse',
            },
            {
                'source' : u'Adresse-Sort',
                'dest' : u'adresse-sort',
            },
            {
                'source' : u'Region-ISO',
                'dest' : u'region-iso',
            },
            {
                'source' : u'Gemeinde',
                'dest' : u'gemeinde',
            },
            {
                'source' : u'Gemeindekennzahl',
                'dest' : u'gemeindekennzahl',
                'type' : 'int(15)'
            },
            {
                'source' : u'Katastralgemeinde',
                'dest' : u'katastralgemeinde',
            },
            {
                'source' : u'Beschreibung',
                'dest' : u'beschreibung',
            },
            {
                'source' : u'Eintragung Datum',
                'dest' : u'eintragung',
            },
            {
                'source' : u'Beschluss',
                'dest' : u'beschluss',
            },
            {
                'source' : u'Breitengrad',
                'dest' : u'lat',
            },
            {
                'source' : u'Längengrad',
                'dest' : u'lon',
            },
            {
                'source' : u'ObjektID',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('ke', 'en') : { # Kenya in English
        'project' : u'wikipedia',
        'lang' : u'en',
        'headerTemplate' : u'Kenya Monument header',
        'rowTemplate' : u'Kenya Monument row',
        'commonsTemplate' : u'Kenya Monument',
        'commonsTrackerCategory' : u'Kenya Monuments with known IDs',
        #'commonsCategoryBase' : u'',
        'autoGeocode' : False,
        'unusedImagesPage' : u'Wikipedia:Wiki Loves Monuments Kenya/Unused images',
        #'imagesWithoutIdPage' : u'',
        'namespaces' : [0],
        'table' : u'monuments_ke_(en)',
        'truncate' : False,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'id',
                'type' : 'int(11)',
            },
            {
                'source' : u'name',
                'dest' : u'name',
            },
            {
                'source' : u'alternative_names',
                'dest' : u'alternative_names',
            },
            {
                'source' : u'gazette',
                'dest' : u'gazette',
            },
            {
                'source' : u'original_function',
                'dest' : u'original_function',
            },
            {
                'source' : u'built',
                'dest' : u'built',
            },
            {
                'source' : u'county',
                'dest' : u'county',
            },
            {
                'source' : u'location',
                'dest' : u'location',
            },
            {
                'source' : u'address',
                'dest' : u'address',
            },
            {
                'source' : u'comment',
                'dest' : u'comment',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'name',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },        
        ],
    },
    ('lu', 'lb') : { # Monuments in Luxemburg in Luxemburgish
        'project' : u'wikipedia',
        'lang' : u'lb',
        'headerTemplate' : u'Nationale Monumenter header',
        'rowTemplate' : u'Nationale Monumenter row',
        #'commonsTemplate' : u'Denkmalgeschütztes Objekt Südtirol',
        #'commonsTrackerCategory' : u'Cultural heritage monuments in South Tyrol with known IDs',
        #'unusedImagesPage' : u'Lëscht vun de klasséierte Monumenter/Unused images', Not possible, no strong ids
        'commonsCategoryBase' : u'Cultural heritage monuments in Luxembourg',
        'namespaces' : [0],
        'table' : u'monuments_lu_(lb)',
        'truncate' : True,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'id',
                'type' : 'varchar(7)',
            },
            {
                'source' : u'lag',
                'dest' : u'lag',
            },
			{
                'source' : u'region-iso',
                'dest' : u'region-iso',
            },
            {
                'source' : u'uertschaft',
                'dest' : u'uertschaft',
            },            
			{
                'source' : u'offiziellen_numm',
                'dest' : u'offiziellen_numm',
            },
            {
                'source' : u'beschreiwung',
                'dest' : u'beschreiwung',
            },
            {
                'source' : u'niveau',
                'dest' : u'niveau',
            },
            {
                'source' : u'klasséiert_zënter',
                'dest' : u'klasseiert_zenter',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'bild',
                'dest' : u'bild',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'offiziellen_numm',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
        ],
    },
    ('nl', 'nl') : { # Rijksmonumenten in the Netherlands in Dutch
        'project' : u'wikipedia',
        'lang' : u'nl',
        'headerTemplate' : u'Tabelkop rijksmonumenten',
        'rowTemplate' : u'Tabelrij rijksmonument',
        'commonsTemplate' : u'Rijksmonument',
        'commonsTrackerCategory' : u'Rijksmonumenten with known IDs',
        'commonsCategoryBase' : u'Rijksmonumenten',
        'autoGeocode' : True,
        'unusedImagesPage' : u'Wikipedia:Wikiproject/Erfgoed/Nederlandse Erfgoed Inventarisatie/Ongebruikte foto\'s',
        'missingCommonscatPage' : u'Wikipedia:Wikiproject/Erfgoed/Nederlandse Erfgoed Inventarisatie/Missende commonscat links',
        'imagesWithoutIdPage' : u'Wikipedia:Wikiproject/Erfgoed/Nederlandse Erfgoed Inventarisatie/Foto\'s zonder id',
        'registrantUrlBase' : u'http://monumentenregister.cultureelerfgoed.nl/php/main.php?cAction=search&sCompMonNr=%s',
        'namespaces' : [0],
        'table' : u'monuments_nl_(nl)',
        'truncate' : False,
        'primkey' : u'objrijksnr',
        'fields' : [
            {
                'source' : u'objrijksnr',
                'dest' : u'objrijksnr',
                'type' : 'int(11)',
            },
            {
                'source' : u'prov-iso',
                'dest' : u'prov-iso',
                'type' : '',
            },
            {
                'source' : u'woonplaats',
                'dest' : u'woonplaats',
            },
            {
                'source' : u'adres',
                'dest' : u'adres',
            },
            {
                'source' : u'adres_sort',
                'dest' : u'',
            },
            {
                'source' : u'objectnaam',
                'dest' : u'objectnaam',
            },
            {
                'source' : u'type_obj',
                'dest' : u'type_obj',
                'type' : "enum('G','A')",
            },
            {
                'source' : u'oorspr_functie',
                'dest' : u'oorspr_functie',
                'type' : 'varchar(128)',
            },
            {
                'source' : u'bouwjaar',
                'dest' : u'bouwjaar',
            },
            {
                'source' : u'bouwjaar_sort',
                'dest' : u'',
            },
            {
                'source' : u'architect',
                'dest' : u'architect',
            },
            {
                'source' : u'architect_sort',
                'dest' : u'',
            },
            {
                'source' : u'cbs_tekst',
                'dest' : u'cbs_tekst',
            },
            {
                'source' : u'RD_x',
                'dest' : u'',
            },
            {
                'source' : u'RD_y',
                'dest' : u'',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'postcode',
                'dest' : u'postcode',
            },
            {
                'source' : u'buurt',
                'dest' : u'buurt',
            },
            {
                'source' : u'objectnaam',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'objrijksnr',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('nl-gem', 'nl') : { # Gemeentelijke monumenten in the Netherlands in Dutch
        'project' : u'wikipedia',
        'lang' : u'nl',
        'headerTemplate' : u'Tabelkop gemeentelijke monumenten',
        'rowTemplate' : u'Tabelrij gemeentelijk monument',
        'commonsTemplate' : u'Gemeentelijk monument',
        'commonsTrackerCategory' : u'Gemeentelijke monumenten with known IDs',
        'commonsCategoryBase' : u'Gemeentelijke monumenten',
        #'autoGeocode' : True,
        'unusedImagesPage' : u'Wikipedia:Wikiproject/Erfgoed/Nederlandse Erfgoed Inventarisatie/Ongebruikte foto\'s van gemeentelijke monumenten',
        'imagesWithoutIdPage' : u'Wikipedia:Wikiproject/Erfgoed/Nederlandse Erfgoed Inventarisatie/Foto\'s van gemeentelijke monumenten zonder id',
        #'registrantUrlBase' : u'http://monumentenregister.cultureelerfgoed.nl/php/main.php?cAction=search&sCompMonNr=%s',
        'namespaces' : [0],
        'table' : u'monuments_nl-gem_(nl)',
        'truncate' : False,
        'primkey' : (u'gemcode', u'objnr'),
        'fields' : [
            {
                'source' : u'gemcode',
                'dest' : u'gemcode',
                'type' : 'varchar(4)',
            },
            {
                'source' : u'objnr',
                'dest' : u'objnr',
                'type' : 'varchar(10)',
            },
            {
                'source' : u'prov-iso',
                'dest' : u'prov-iso',
                'type' : '',
            },
            {
                'source' : u'gemeente',
                'dest' : u'gemeente',
                'type' : '',
            },
            {
                'source' : u'object',
                'dest' : u'object',
            },
            {
                'source' : u'bouwjaar',
                'dest' : u'bouwjaar',
            },
            {
                'source' : u'architect',
                'dest' : u'architect',
            },
            {
                'source' : u'adres',
                'dest' : u'adres',
            },
            {
                'source' : u'RD_x',
                'dest' : u'',
            },
            {
                'source' : u'RD_y',
                'dest' : u'',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'object',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
        ],
    },
    ('mt', 'de') : { # Monuments in Malta in German
        'project' : u'wikipedia',
        'lang' : u'de',
        'headerTemplate' : u'Denkmalliste Malta Tabellenkopf',
        'rowTemplate' : u'Denkmalliste Malta Tabellenzeile',
        'commonsTemplate' : u'National Inventory of Cultural Property of the Maltese Islands',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Malta with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Malta',
        'autoGeocode' : True,
        'unusedImagesPage' : u'User:Multichill/Unused Denkmal Malta',
        'imagesWithoutIdPage' : u'User:Multichill/Denkmal Malta without ID',
        'namespaces' : [0],
        'table' : u'monuments_mt_(de)',
        'registrantUrlBase' : u'http://www.culturalheritage.gov.mt/filebank/inventory/000%s.pdf',
        'truncate' : False, # Not all ids are filled, just overwrite it
        'primkey' : u'inventarnummer',
        'fields' : [
            {
                'source' : u'Inventarnummer',
                'dest' : u'inventarnummer',
                'type' : 'varchar(11)',
                'default' : '0',
            },
            {
                'source' : u'Foto',
                'dest' : u'foto',
            },
            {
                'source' : u'Commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'Artikel',
                'dest' : u'artikel',
            },
            {
                'source' : u'Name-de',
                'dest' : u'name-de',
            },
            {
                'source' : u'Name-en',
                'dest' : u'name-en',
            },
            {
                'source' : u'Name-mt',
                'dest' : u'name-mt',
            },
            {
                'source' : u'Gemeinde',
                'dest' : u'gemeinde',
            },
            {
                'source' : u'Adresse',
                'dest' : u'adresse',
            },
            {
                'source' : u'Breitengrad',
                'dest' : u'lat',
            },
            {
                'source' : u'Längengrad',
                'dest' : u'lon',
            },
            {
                'source' : u'Region-ISO',
                'dest' : u'region-iso',
            },
            {
                'source' : u'Beschreibung',
                'dest' : u'beschreibung',
            },
            {
                'source' : u'Inventarnummer',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('mx', 'es') : { # Monuments in Mexico in Spanish
        'project' : u'wikipedia',
        'lang' : u'es',
        'headerTemplate' : u'MonumentoMéxico/encabezado',
        'rowTemplate' : u'MonumentoMéxico',
        'commonsTemplate' : u'Monumento de México',
        'commonsTrackerCategory' : u'Monuments in Mexico with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Mexico',
        'unusedImagesPage' : u'Wikiproyecto:Patrimonio histórico/Fotos de monumentos de México sin id',
        'imagesWithoutIdPage' : u'Wikiproyecto:Patrimonio histórico/Fotos de monumentos de México sin usar',
        'namespaces' : [104],
        'table' : u'monuments_mx_(es)',
        'truncate' : False,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'id',
                'type' : 'varchar(25)',
            },
            {
                'source' : u'ISO',
                'dest' : u'iso',
            },
            {
                'source' : u'monumento',
                'dest' : u'monumento',
            },
            {
                'source' : u'municipio',
                'dest' : u'municipio',
            },
            {
                'source' : u'localidad',
                'dest' : u'localidad',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'long',
                'dest' : u'lon',
            },
            {
                'source' : u'dirección',
                'dest' : u'direccion',
            },
            {
                'source' : u'tipo',
                'dest' : u'tipo',
                'type' : u"ENUM('Federal', 'Estatal', 'Municipal')",
            },
            {
                'source' : u'monumento_enlace',
                'dest' : u'monumento_enlace',
                'default' : u'monumento',
            },
            {
                'source' : u'enlace',
                'dest' : u'enlace',
            },
            {
                'source' : u'monumento_desc',
                'dest' : u'monumento_desc',
            },
            {
                'source' : u'monumento_categoría',
                'dest' : u'monumento_categoria',
            },
            {
                'source' : u'imagen',
                'dest' : u'imagen',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'monumento_enlace',
                'dest' : u'monument_article',
                # 'conv' : u'extractWikilink',
            },
        ],
    },
    ('no', 'no') : { # Monuments in Norway in No
        'project' : u'wikipedia',
        'lang' : u'no',
        'headerTemplate' : u'Kulturminner header',
        'rowTemplate' : u'Kulturminner row',
        'commonsTemplate' : u'Monument Norge',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Norway with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Norway',
        'unusedImagesPage' : u'User:Multichill/Unused monument photos',
        'imagesWithoutIdPage' : u'User:Multichill/Monument photos without an ID',
        'registrantUrlBase' : u'http://www.kulturminnesok.no/kulturminnesok/kulturminne/?LOK_ID=%s',
        'namespaces' : [0, 4], #FIXME : Remove 4 when we're done moving
        'table' : u'monuments_no_(no)',
        'truncate' : False,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'id',
                'type' : 'int(11)',
            },
            {
                'source' : u'navn',
                'dest' : u'navn',
            },
            {
                'source' : u'artikkel',
                'dest' : u'artikkel',
            },
            {
                'source' : u'kategori',
                'dest' : u'kategori',
            },
            {
                'source' : u'datering',
                'dest' : u'datering',
                'type' : 'varchar(128)',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'county_iso',
                'dest' : u'county_iso',
            },
            {
                'source' : u'kommunenr',
                'dest' : u'kommunenr',
                'type' : 'int(10)',
            },
            {
                'source' : u'kommune',
                'dest' : u'kommune',
            },
            {
                'source' : u'vernetype',
                'dest' : u'vernetype',
            },
            {
                'source' : u'kat',
                'dest' : u'kat',
            },
            {
                'source' : u'tilrettel',
                'dest' : u'tilrettel',
            },
            {
                'source' : u'verdensarv',
                'dest' : u'verdensarv',
            },
            {
                'source' : u'bilde',
                'dest' : u'bilde',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'artikkel',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'id',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('pa', 'es') : { # Monuments in Panama in Spanish
        'project' : u'wikipedia',
        'lang' : u'es',
        'headerTemplate' : u'Fila PCN',
        'rowTemplate' : u'Fila PCN',
        'commonsTemplate' : u'PCN',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Panama with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Panama',
        'unusedImagesPage' : u'Wikiproyecto:Patrimonio histórico/Fotos del Patrimonio Cultural de la Nación sin usar',
        'imagesWithoutIdPage' : u'User:Multichill/PCN without id',
        'namespaces' : [104],
        'table' : u'monuments_pa_(es)',
        'truncate' : False,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'registro',
                'dest' : u'id',
                'type' : 'varchar(25)',
                'default' : '',
            },
            {
                'source' : u'imagen',
                'dest' : u'imagen',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'nombre',
                'dest' : u'nombre',
            },
            {
                'source' : u'descripción',
                'dest' : u'descripcion',
            },
            {
                'source' : u'artículo',
                'dest' : u'articulo',
            },
            {
                'source' : u'dirección',
                'dest' : u'direccion',
            },
            {
                'source' : u'véase',
                'dest' : u'vease',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'provincia',
                'dest' : u'provincia',
            },
            {
                'source' : u'prov-iso',
                'dest' : u'prov-iso',
            },
            {
               'source' : u'title',
               'dest' : u'title',
            },
        ],
    },
    ('ph', 'en') : { # Monuments in the Philippines in English
        'project' : u'wikipedia',
        'lang' : u'en',
        'headerTemplate' : u'Philippine cultural property header',
        'rowTemplate' : u'Philippine cultural property row',
        'commonsTemplate' : u'WMPH-ID',
        'commonsTrackerCategory' : u'Cultural heritage monuments in the Philippines with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in the Philippines',
        'unusedImagesPage' : u'Wikipedia:WikiProject Historic sites/Unused images of Cultural heritage monuments in the Philippines',
        'namespaces' : [0],
        'table' : u'monuments_ph_(en)',
        'truncate' : False,
        'primkey' : u'cp-wmph-id',
        'fields' : [
            {
                'source' : u'cp-wmph-id',
                'dest' : u'cp-wmph-id',
                'type' : 'varchar(15)',
            },
            {
                'source' : u'site_name',
                'dest' : u'site_name',
            },
            {
                'source' : u'description',
                'dest' : u'description',
            },
            {
                'source' : u'region-iso',
                'dest' : u'region-iso',
            },
            {
                'source' : u'province',
                'dest' : u'province',
            },
            {
                'source' : u'province-iso',
                'dest' : u'province-iso',
            },
            {
                'source' : u'location',
                'dest' : u'location',
            },
            {
                'source' : u'barangay',
                'dest' : u'barangay',
            },
            {
                'source' : u'address',
                'dest' : u'address',
            },
            
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
        ],
    },
    ('pk', 'en') : { # Monuments in Pakistan in English
        'project' : u'wikipedia',
        'lang' : u'en',
        'headerTemplate' : u'PKmonument header',
        'rowTemplate' : u'PKmonument row',
        'commonsTemplate' : u'Cultural Heritage Pakistan',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Pakistan with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Pakistan',
        'autoGeocode' : True,
        'unusedImagesPage' : u'Wikipedia:WikiProject Historic sites/Unused images of Cultural heritage monuments in Pakistan',
        'imagesWithoutIdPage' : u'Wikipedia:WikiProject Historic sites/Images of Cultural heritage monuments in Pakistan without an ID',
        'registrantUrlBase' : u'', # Nothing yet
        'namespaces' : [0],
        'table' : u'monuments_pk_(en)',
        'truncate' : False,
        'primkey' : u'number',
        'fields' : [
            {
                'source' : u'number',
                'dest' : u'number',
                'type' : 'varchar(11)',
            },
            {
                'source' : u'prov_iso',
                'dest' : u'prov_iso',
            },
            {
                'source' : u'description',
                'dest' : u'description',
            },
            {
                'source' : u'address',
                'dest' : u'address',
            },
            {
                'source' : u'district',
                'dest' : u'district',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'color',
                'dest' : u'color',
            },
            {
                'source' : u'description',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'number',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('pl', 'pl') : { # Monuments in Poland in Polish
        'project' : u'wikipedia',
        'lang' : u'pl',
        'headerTemplate' : u'Lista zabytków góra',
        'rowTemplate' : u'Zabytki wiersz',
        'commonsTemplate' : u'Zabytek',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Poland with known IDs',
        'unusedImagesPage' : u'Wikiprojekt:Wiki Lubi Zabytki/Niewykorzystywane',
        'missingCommonscatPage' : u'Wikiprojekt:Wiki Lubi Zabytki/Missing_commonscat_links',
        'commonsCategoryBase' : u'Cultural heritage monuments in Poland',
        'namespaces' : [102],
        'table' : u'monuments_pl_(pl)',
        'truncate' : True,
        'primkey' : ('prov-iso', u'numer'),
        'fields' : [
            {
                'source' : u'numer',
                'dest' : u'numer',
                'type' : 'varchar(22)',
                'default' : '0',
            },
            {
                'source' : u'nazwa',
                'dest' : u'nazwa',
            },
            {
                'source' : u'województwo',
                'dest' : u'prov-iso',
            },
            {
                'source' : u'powiat',
                'dest' : u'powiat',
            },
            {
                'source' : u'gmina',
                'dest' : u'gmina',
            },
            {
                'source' : u'adres',
                'dest' : u'adres',
            },
            {
                'source' : u'szerokość',
                'dest' : u'lat',
            },
            {
                'source' : u'długość',
                'dest' : u'lon',
            },
            {
                'source' : u'koordynaty', # To get rid of errors
                'dest' : u'koordynaty',
            },
            {
                'source' : u'zdjęcie',
                'dest' : u'zdjecie',
            },
            {
                'source' : u'commons',
                'dest' : u'commonscat',
            },
            {
                'source' : u'nazwa',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
        ],
    },
    ('pt', 'pt') : { # Monuments in Portugal (IGESPAR) in Portugese
        'project' : u'wikipedia',
        'lang' : u'pt',
        'headerTemplate' : u'IGESPAR/cabeçalho',
        'rowTemplate' : u'IGESPAR/linha',
        'footerTemplate' : u'IGESPAR/rodapé',
        'commonsTemplate' : u'IGESPAR',
        'commonsTrackerCategory' : u'IGESPAR with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Portugal',
        'unusedImagesPage' : u'Wikipédia:Projetos/Património de Portugal/Fotos IGESPAR não usadas',
        'imagesWithoutIdPage' : u'User:Multichill/IGESPAR without an ID',
        'registrantUrlBase' : u'http://www.igespar.pt/pt/patrimonio/pesquisa/geral/patrimonioimovel/detail/%s',
        'namespaces' : [102],
        'table' : u'monuments_pt_(pt)',
        'truncate' : False,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'id',
                'type' : 'int(11)',
            },
            {
                'source' : u'region-iso',
                'dest' : u'region-iso',
            },
            {
                'source' : u'designacoes',
                'dest' : u'designacoes',
            },
            {
                'source' : u'categoria',
                'dest' : u'categoria',
            },
            {
                'source' : u'tipologia',
                'dest' : u'tipologia',
            },
            {
                'source' : u'concelho',
                'dest' : u'concelho',
            },
            {
                'source' : u'freguesia',
                'dest' : u'freguesia',
            },
            {
                'source' : u'grau',
                'dest' : u'grau',
            },
            {
                'source' : u'ano',
                'dest' : u'ano',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'imagem',
                'dest' : u'imagem',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'designacoes',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'id',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('ro', 'ro') : { # Monuments in Romania
        'project' : u'wikipedia',
        'lang' : u'ro',
        'headerTemplate' : u'ÎnceputTabelLMI',
        'rowTemplate' : u'ElementLMI',
        'footerTemplate' : u'SfârșitTabelLMI',
        'commonsTemplate' : u'Monument istoric',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Romania with known IDs',
        'commonsCategoryBase' : u'Historical monuments in Romania',
        'autoGeocode' : True,
        'unusedImagesPage' : u'User:Multichill/Unused Monument istoric',
        'imagesWithoutIdPage' : u'User:Multichill/Monument istoric without ID',
        'namespaces' : [0],
        'table' : u'monuments_ro_(ro)',
        'truncate' : False, 
        'primkey' : u'cod',
        'fields' : [
            {
                'source' : u'Cod',
                'dest' : u'cod',
                'type' : 'varchar(25)',
                'default' : '0',
            },
            {
                'source' : u'Denumire',
                'dest' : u'denumire',
            },
            {
                'source' : u'Județul-iso',
                'dest' : u'judetul-iso',
            },
            {
                'source' : u'Localitate',
                'dest' : u'localitate',
            },
            {
                'source' : u'Adresă',
                'dest' : u'adresa',
            },
            {
                'source' : u'Datare',
                'dest' : u'datare',
            },
            {
                'source' : u'Arhitect',
                'dest' : u'arhitect',
            },
            {
                'source' : u'Lat',
                'dest' : u'lat',
            },
            {
                'source' : u'Coordonate',
                'dest' : u'',
            },
            {
                'source' : u'Lon',
                'dest' : u'lon',
            },
            {
                'source' : u'Imagine',
                'dest' : u'imagine',
            },
            {
                'source' : u'Commons',
                'dest' : u'commonscat',
            },
            {
                'source' : u'denumire',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
        ],
    },
    ('rs', 'sr') : { # Monuments in Serbia in Serbian
        'project' : u'wikipedia',
        'lang' : u'sr',
        'headerTemplate' : u'Споменици заглавље',
        'rowTemplate' : u'Споменици ред',
        'commonsTemplate' : u'Cultural Heritage Serbia',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Serbia with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Serbia',
        'autoGeocode' : True,
        'unusedImagesPage' : u'Википедија:Списак знаменитих места у Србији/Неискоришћени слике',
        #'imagesWithoutIdPage' : u'Wikipedia:Wikiproject/Erfgoed/Nederlandse Erfgoed Inventarisatie/Foto\'s zonder id',
        #'registrantUrlBase' : u'http://monumentenregister.cultureelerfgoed.nl/php/main.php?cAction=search&sCompMonNr=%s',
        'namespaces' : [0],
        'table' : u'monuments_rs_(sr)',
        'truncate' : False,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'ИД',
                'dest' : u'id',
                'type' : 'varchar(11)',
            },
            {
                'source' : u'Насеље',
                'dest' : u'city',
            },
            {
                'source' : u'Адреса',
                'dest' : u'address',
            },
            {
                'source' : u'Назив',
                'dest' : u'name',
            },
            {
                'source' : u'Општина',
                'dest' : u'district',
            },
            {
                'source' : u'iso',
                'dest' : u'iso_okrug',
            },
            {
                'source' : u'Градска_општина',
                'dest' : u'city_district',
            },
            {
                'source' : u'Надлежни_завод',
                'dest' : u'authority',
            },
            {
                'source' : u'гшир',
                'dest' : u'lat',
            },
            {
                'source' : u'гдуж',
                'dest' : u'lon',
            },
            {
                'source' : u'Слика',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'Назив',
                'dest' : u'monument_article',
            },
        ],
    },
    ('ru', 'ru') : { # Monuments in Russia in Russian. Field table names are English already
        'project' : u'wikipedia',
        'lang' : u'ru',
        'headerTemplate' : u'ПамАрх header',
        'rowTemplate' : u'ПамАрх row',
        'commonsTemplate' : u'Cultural Heritage Russia',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Russia with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Russia',
        'autoGeocode' : False,
        'unusedImagesPage' : u'User:Multichill/Unused cultural heritage monuments',
        'imagesWithoutIdPage' : u'User:Multichill/Cultural heritage monuments without ID',
        'namespaces' : [104],
        'table' : u'monuments_ru_(ru)',
        'truncate' : False,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'id',
                'type' : 'varchar(25)',
                'default' : '0',
            },
            {
                'source' : u'имя',
                'dest' : u'name',
            },
            {
                'source' : u'комплекс',
                'dest' : u'complex',
            },
            {
                'source' : u'адрес',
                'dest' : u'address',
            },
            {
                'source' : u'информация',
                'dest' : u'description',
            },
            {
                'source' : u'субъект_федерации',
                'dest' : u'region',
            },
            {
                'source' : u'широта',
                'dest' : u'lat',
            },
            {
                'source' : u'долгота',
                'dest' : u'lon',
            },
            {
                'source' : u'изображение',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'name',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
        ],
    },
    ('se-bbr', 'sv') : { # BBR Monuments in Sweden in Swedish
        'project' : u'wikipedia',
        'lang' : u'sv',
        'headerTemplate' : u'BBR-huvud',
        'rowTemplate' : u'BBR',
        'footerTemplate' : u'',
        'commonsTemplate' : u'BBR',
        'commonsTrackerCategory' : u'Protected buildings in Sweden with known IDs',
        'commonsCategoryBase' : u'Protected buildings in Sweden',
        'unusedImagesPage' : u'User:Multichill/Unused protected buildings in Sweden',
        'imagesWithoutIdPage' : u'User:Multichill/Protected buildings in Sweden without ID',
        'registrantUrlBase' : u'http://www.bebyggelseregistret.raa.se/bbr2/anlaggning/visaHistorik.raa?page=historik&visaHistorik=true&anlaggningId=%s',
        'namespaces' : [0],
        'table' : u'monuments_se-bbr_(sv)',
        'truncate' : False, 
        'primkey' : u'bbr',
        'fields' : [
            {
                'source' : u'bbr',
                'dest' : u'bbr',
                'type' : 'varchar(25)',
                'default' : '0',
            },
            {
                'source' : u'namn',
                'dest' : u'namn',
            },
            {
                'source' : u'region-iso',
                'dest' : u'region-iso',
            },
            {
                'source' : u'funktion',
                'dest' : u'funktion',
            },
            {
                'source' : u'byggår',
                'dest' : u'byggar',
            },
            {
                'source' : u'arkitekt',
                'dest' : u'arkitekt',
            },
            {
                'source' : u'plats',
                'dest' : u'plats',
            },
            {
                'source' : u'kommun',
                'dest' : u'kommun',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'long',
                'dest' : u'lon',
            },
            {
                'source' : u'bild',
                'dest' : u'bild',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'namn',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'bbr',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('se-fornmin', 'sv') : { # Fornminne Monuments in Sweden in Swedish
        'project' : u'wikipedia',
        'lang' : u'sv',
        'headerTemplate' : u'FMIS-huvud',
        'rowTemplate' : u'FMIS', # Not completed yet.
        'footerTemplate' : u'',
        'commonsTemplate' : u'Fornminne',
        'commonsTrackerCategory' : u'Archaeological monuments in Sweden with known IDs',
        'commonsCategoryBase' : u'Archaeological monuments in Sweden',
        'unusedImagesPage' : u'User:Multichill/Unused archaeological monuments in Sweden',
        'imagesWithoutIdPage' : u'User:Multichill/Archaeological monuments in Sweden without ID',
        'registrantUrlBase' : u'http://kulturarvsdata.se/raa/fmi/html/%s',
        'namespaces' : [0],
        'table' : u'monuments_se-fornminne_(sv)',
        'truncate' : False, 
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'id',
                'type' : 'varchar(25)',
                'default' : '0',
            },
            {
                'source' : u'namn',
                'dest' : u'namn',
            },
            {
                'source' : u'raä-nr',
                'dest' : u'raa-nr',
            },
            {
                'source' : u'region-iso',
                'dest' : u'region-iso',
            },
            {
                'source' : u'artikel',
                'dest' : u'artikel',
            },
            {
                'source' : u'typ',
                'dest' : u'typ',
            },
            {
                'source' : u'tillkomst',
                'dest' : u'tillkomst',
            },
            {
                'source' : u'kommun',
                'dest' : u'kommun',
            },
            {
                'source' : u'socken',
                'dest' : u'socken',
            },
            {
                'source' : u'landskap',
                'dest' : u'landskap',
            },
            {
                'source' : u'plats',
                'dest' : u'plats',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'bild',
                'dest' : u'bild',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'id',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('se-ship', 'sv') : { # Listed historical ships in Sweden in Swedish
        'project' : u'wikipedia',
        'lang' : u'sv',
        'headerTemplate' : u'K-fartyg-huvud',
        'rowTemplate' : u'K-fartyg',
        'footerTemplate' : u'',
        'commonsTemplate' : u'K-Fartyg',
        'commonsTrackerCategory' : u'Listed historical ships in Sweden with known IDs',
        'commonsCategoryBase' : u'Listed historical ships in Sweden',
        'unusedImagesPage' : u'User:Multichill/Unused listed historical ships in Sweden',
        'imagesWithoutIdPage' : u'User:Multichill/Listed historical ships in Sweden without ID',
        'registrantUrlBase' : u'http://www.sjohistoriska.se/sv/Kusten-runt/Fartyg--batar/K-markning-av-fartyg/K-markta-fartyg/%s',
        'namespaces' : [0],
        'table' : u'monuments_se-ship_(sv)',
        'truncate' : False, 
        'primkey' : u'signal',
        'fields' : [
            {
                'source' : u'signal',
                'dest' : u'signal',
                'type' : 'varchar(25)',
                'default' : '0',
            },
            {
                'source' : u'namn',
                'dest' : u'namn',
            },
            {
                'source' : u'artikel',
                'dest' : u'artikel',
            },
            {
                'source' : u'funktion',
                'dest' : u'funktion',
            },
            {
                'source' : u'byggår',
                'dest' : u'byggar',
            },
            {
                'source' : u'varv',
                'dest' : u'varv',
            },
            {
                'source' : u'hemmahamn',
                'dest' : u'hemmahamn',
            },
            {
                'source' : u'material',
                'dest' : u'material',
            },
            {
                'source' : u'dimensioner',
                'dest' : u'dimensioner',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'long',
                'dest' : u'lon',
            },
            {
                'source' : u'bild',
                'dest' : u'bild',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'signal',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl-sv-ship',
            },
        ],
    },
    ('sk', 'de') : { # Monuments in Slovakia in German
        'project' : u'wikipedia',
        'lang' : u'de',
        'headerTemplate' : u'Denkmalliste Slowakei Tabellenkopf',
        'rowTemplate' : u'Denkmalliste Slowakei Tabellenzeile',
        'footerTemplate' : u'Denkmalliste Slowakei Tabellenfuß',
        'commonsTemplate' : u'Cultural Heritage Slovakia',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Slovakia with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Slovakia',
        'autoGeocode' : True,
        'unusedImagesPage' : u'User:Multichill/Unused Denkmal Slowakei',
        'imagesWithoutIdPage' : u'User:Multichill/Denkmal Slowakei without ID',
        'namespaces' : [0],
        'table' : u'monuments_sk_(de)',
        'truncate' : False, # Not all ids are filled, just overwrite it
        'primkey' : u'objektid',
        'fields' : [
            {
                'source' : u'ObjektID',
                'dest' : u'objektid',
                'type' : 'varchar(11)',
                'default' : '0',
            },
            {
                'source' : u'Foto',
                'dest' : u'foto',
            },
            {
                'source' : u'Commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'Name',
                'dest' : u'name-sk',
            },
            {
                'source' : u'Name-de',
                'dest' : u'name-de',
            },
            {
                'source' : u'Artikel',
                'dest' : u'artikel',
            },
            {
                'source' : u'Adresse',
                'dest' : u'adresse',
            },
            {
                'source' : u'Adresse-Sort',
                'dest' : u'adresse-sort',
            },
            {
                'source' : u'Region-ISO',
                'dest' : u'region-iso',
            },
            {
                'source' : u'Katastralgemeinde',
                'dest' : u'katastralgemeinde',
            },
            {
                'source' : u'Bearbeitungsdatum',
                'dest' : u'bearbeitungsdatum',
            },
            {
                'source' : u'Beschreibung-de',
                'dest' : u'beschreibung-de',
            },
            {
                'source' : u'Offizielle Beschr.',
                'dest' : u'offiziellebeschreibung',
            },
            {
               'source' : u'Anzeige-Artikel',
                'dest' : u'anzeige-artikel',
            },
            {
                'source' : u'Konskriptionsnr',
                'dest' : u'konskriptionsnr',
            },
            {
                'source' : u'Obec',
                'dest' : u'obec',
            },
            {
                'source' : u'Kód obce',
                'dest' : u'kod_obce',
                'type' : 'int(11)',
            },
            {
                'source' : u'Okres',
                'dest' : u'okres',
            },
            {
                'source' : u'Kód okresu',
                'dest' : u'kod_okresu',
                'type' : 'int(11)',
            },
            {
                'source' : u'Breitengrad',
                'dest' : u'lat',
            },
            {
                'source' : u'Längengrad',
                'dest' : u'lon',
            },
        ],
    },
    ('sk', 'sk') : { # Monuments in Slovakia in Slovak
        'project' : u'wikipedia',
        'lang' : u'sk',
        'headerTemplate' : u'Monuments tablehead-SK',
        'rowTemplate' : u'Monuments tableline-SK',
        'footerTemplate' : u'Monuments tablefoot-SK',
        'commonsTemplate' : u'Cultural Heritage Slovakia',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Slovakia with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Slovakia',
        'autoGeocode' : True,
        'unusedImagesPage' : u'User:Multichill/Unused Monument Slovakia',
        'imagesWithoutIdPage' : u'User:Multichill/Monument Slovakia without ID',
        'namespaces' : [0],
        'table' : u'monuments_sk_(sk)',
        'truncate' : False, # Not all ids are filled, just overwrite it
        'primkey' : u'idobjektu',
        'fields' : [
            {
                'source' : u'IDobjektu',
                'dest' : u'idobjektu',
                'type' : 'varchar(11)',
                'default' : '0',
            },
            {
                'source' : u'Fotka',
                'dest' : u'fotka',
            },
            {
                'source' : u'Commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'Názov',
                'dest' : u'nazov-sk',
            },
            {
                'source' : u'Názov-de',
                'dest' : u'nazov-de',
            },
            {
                'source' : u'Článok',
                'dest' : u'clanok',
            },
            {
                'source' : u'Názov_článku',
                'dest' : u'nazov_clanku',
            },
            {
                'source' : u'Adresa',
                'dest' : u'adresa',
            },
            {
                'source' : u'Adresa_pre_triedenie',
                'dest' : u'adresa_pre_triedenie',
            },
            {
                'source' : u'šírka',
                'dest' : u'airka',
            },
            {
                'source' : u'dĺžka',
                'dest' : u'dlzka',
            },
            {
                'source' : u'ISO-regiónu',
                'dest' : u'iso-regionu',
            },
            {
                'source' : u'Katastrálne_územie',
                'dest' : u'katastralne_uzemie',
            },
            {
               'source' : u'Súpisné_číslo',
                'dest' : u'supisne_cislo',
            },
            {
                'source' : u'Stav',
                'dest' : u'stav',
            },
			{
                'source' : u'popis',
                'dest' : u'popis',
            },
            {
                'source' : u'Unifikovaný názov NKP',
                'dest' : u'unifikovany_nazov_nkp',
            },			
            {
                'source' : u'Obec',
                'dest' : u'obec',
            },
            {
                'source' : u'Kód obce',
                'dest' : u'kod_obce',
                'type' : 'int(11)',
            },
            {
                'source' : u'Okres',
                'dest' : u'okres',
            },
            {
                'source' : u'Kód okresu',
                'dest' : u'kod_okresu',
                'type' : 'int(11)',
            },
            {
                'source' : u'šírka',
                'dest' : u'lat',
            },
            {
                'source' : u'dĺžka',
                'dest' : u'lon',
            },
			{
                'source' : u'Beschreibung-de',
                'dest' : u'beschreibung-de',
            },
        ],
    },
    ('th', 'th') : { # Cultural heritage monuments in land in Thai
        'project' : u'wikipedia',
        'lang' : u'th',
        'headerTemplate' : u'หัวโบราณสถาน',
        'rowTemplate' : u'แถวโบราณสถาน',
        'commonsTemplate' : u'Cultural Heritage Thailand',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Thailand with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Thailand',
        'autoGeocode' : True,
        'unusedImagesPage' : u'วิกิพีเดีย:Wiki Loves Monuments/ภาพโบราณสถานในประเทศไทยที่ไม่ได้ใช้', 
        'missingCommonscatPage' : u'',
        'imagesWithoutIdPage' : u'วิกิพีเดีย:Wiki Loves Monuments/ภาพโบราณสถานในประเทศไทยที่ไม่มีรหัส',
        'registrantUrlBase' : u'',
        'namespaces' : [0],
        'table' : u'monuments_th_(th)',
        'truncate' : False,
        'primkey' : u'register',
        'fields' : [
            {
                'source' : u'ทะเบียน',
                'dest' : u'register',
                'type' : 'varchar(15)',
            },
            {
                'source' : u'ชื่อ',
                'dest' : u'name',
            },
            {
                'source' : u'หมายเหตุ',
                'dest' : u'note',
            },
            {
                'source' : u'จังหวัด',
                'dest' : u'province',
            },
            {
                'source' : u'code',
                'dest' : u'prov_iso',
            },
            {
                'source' : u'อำเภอ',
                'dest' : u'district',
            },
            {
                'source' : u'ตำบล',
                'dest' : u'tambon',
            },
            {
                'source' : u'ที่ตั้ง',
                'dest' : u'location',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'ภาพ',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'ประกาศ',
                'dest' : u'announced',
            },
            {
                'source' : u'ลิงก์', # FIXME: Can't use the current format
                'dest' : u'url',
            },
            {
                'source' : u'อ้างอิง',
                'dest' : u'reference',
            },
            {
                'source' : u'name',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'register',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('tn', 'fr') : { # Monuments in Tunisia in French
        'project' : u'wikipedia',
        'lang' : u'fr',
        'headerTemplate' : u'En-tête de tableau monument Tunisie',
        'rowTemplate' : u'Ligne de tableau monument Tunisie',
        'commonsTemplate' : u'Cultural Heritage Tunisia',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Tunisia with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Tunisia',
        'autoGeocode' : True,
        'unusedImagesPage' : u'Projet:Monuments historiques/Images de monuments tunisiens non utilisées',
        #'imagesWithoutIdPage' : u'User:Multichill/Monument photos without an ID',
        'registrantUrlBase' : u'',
        'namespaces' : [0],
        'table' : u'monuments_tn_(fr)',
        'truncate' : False,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'id',
                'type' : 'varchar(11)',
            },
            {
                'source' : u'gouvernorat_iso',
                'dest' : u'gouvernorat_iso',
            },
            {
                'source' : u'site',
                'dest' : u'site',
            },
            {
                'source' : u'monument',
                'dest' : u'monument',
            },
            {
                'source' : u'tri monument',
                'dest' : u'tri_monument',
            },
            {
                'source' : u'adresse',
                'dest' : u'adresse',
            },
            {
                'source' : u'tri adresse',
                'dest' : u'tri_adresse',
            },
            {
                'source' : u'date',
                'dest' : u'date',
            },
            {
                'source' : u'decret',
                'dest' : u'decret',
            },
            {
                'source' : u'latitude',
                'dest' : u'lat',
            },
            {
                'source' : u'longitude',
                'dest' : u'lon',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'monument',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'id',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl',
            },
        ],
    },
    ('ua', 'uk') : { # Monuments in Ukraine in Ukrainian
        'project' : u'wikipedia',
        'lang' : u'uk',
        'headerTemplate' : u'WLM-шапка',
        'rowTemplate' : u'ВЛП-рядок',
        'commonsTemplate' : u'Monument Ukraine',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Ukraine with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Ukraine',
        'autoGeocode' : True,
        'unusedImagesPage' : u'User:ErfgoedBot/Unused images of Cultural heritage monuments',
        'imagesWithoutIdPage' : u'User:ErfgoedBot/Images of Cultural heritage monuments without ID',
        'namespaces' : [4],
        'table' : u'monuments_ua_(uk)',
        'truncate' : False,
        'primkey' : u'id',
        'countryBbox' : u'21.6,43.9,40.7,52.5',
        'fields' : [
            {
                'source' : u'ID',
                'dest' : u'id',
                'type' : 'varchar(25)',
            },
            {
                'source' : u'назва',
                'dest' : u'name',
            },
            {
                'source' : u'адреса',
                'dest' : u'address',
            },
            {
                'source' : u'нас_пункт',
                'dest' : u'municipality',
            },
            {
                'source' : u'широта',
                'dest' : u'lat',
                'check' : u'checkLat',
            },
            {
                'source' : u'довгота',
                'dest' : u'lon',
                'check' : u'checkLon',
            },
            {
                'source' : u'фото',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'рік',
                'dest' : u'year_of_construction',
            },
            {
                'source' : u'охоронний номер',
                'dest' : u'registrant_id',
            },
            {
                'source' : u'тип',
                'dest' : u'type',
            },
            {
                'source' : u'галерея',
                'dest' : u'gallery',
            },
            {
                'source' : u'iso',
                'dest' : u'iso_oblast',
            },
			 {
                'source' : u'район',
                'dest' : u'rayon',
            },
            {
                'source' : u'назва',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
        ]
    },
    ('us', 'en') : { # National Register of Historic Places listings in the United States in English
        'project' : u'wikipedia',
        'lang' : u'en',
        'headerTemplate' : u'NRHP header',
        'rowTemplate' : u'NRHP row',
        'commonsTemplate' : u'NRHP',
        'commonsTrackerCategory' : u'National Register of Historic Places with known IDs',
        'commonsCategoryBase' : u'National Register of Historic Places',
        'autoGeocode' : False,
        'unusedImagesPage' : u'Wikipedia:WikiProject National Register of Historic Places/Unused images',
        'imagesWithoutIdPage' : u'Wikipedia:WikiProject National Register of Historic Places/Images without refnum',
        'namespaces' : [0],
        'table' : u'monuments_us_(en)',
        'truncate' : False,
        'primkey' : u'refnum',
        'fields' : [
            {
                'source' : u'refnum',
                'dest' : u'refnum',
                'type' : 'int(11)',
            },
            {
                'source' : u'pos',
                'dest' : u'pos',
                'type' : 'int(3)',
            },
            {
                'source' : u'type',
                'dest' : u'type',
                'type' : 'varchar(25)',
                'default' : 'NRHP',
            },
            {
                'source' : u'article',
                'dest' : u'article',
            },
            {
                'source' : u'name',
                'dest' : u'name',
            },
            {
                'source' : u'name_extra',
                'dest' : u'name_extra',
            },
            {
                'source' : u'address',
                'dest' : u'address',
            },
            {
                'source' : u'city',
                'dest' : u'city',
            },
            {
                'source' : u'nocity',
                'dest' : u'nocity',
            },
            {
                'source' : u'county',
                'dest' : u'county',
            },
            {
                'source' : u'state_iso',
                'dest' : u'state_iso',
            },
            {
                'source' : u'date',
                'dest' : u'date',
            },
            {
                'source' : u'date_extra',
                'dest' : u'date_extra',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'nolatlon',
                'dest' : u'nolatlon',
            },
            {
                'source' : u'description',
                'dest' : u'description',
            },
        ],
    },
    ('us-ca', 'en') : { # State monuments in California
        'project' : u'wikipedia',
        'lang' : u'en',
        'headerTemplate' : u'CHL header',
        'rowTemplate' : u'CHL row',
        'commonsTemplate' : u'US-CHL',
        'commonsTrackerCategory' : u'California Historical Landmarks with known IDs',
        'commonsCategoryBase' : u'California Historical Landmarks',
        'autoGeocode' : False,
        #'unusedImagesPage' : u'Wikipedia:WikiProject National Register of Historic Places/Unused images',
        #'imagesWithoutIdPage' : u'Wikipedia:WikiProject National Register of Historic Places/Images without refnum',
        'namespaces' : [0, 2],
        'table' : u'monuments_us-ca_(en)',
        'truncate' : False,
        'primkey' : u'refnum',
        'fields' : [
            {
                'source' : u'refnum',
                'dest' : u'refnum',
                'type' : 'int(11)',
            },
            {
                'source' : u'pos',
                'dest' : u'pos',
                'type' : 'int(3)',
            },
            {
                'source' : u'type',
                'dest' : u'type',
                'type' : 'varchar(25)',
                'default' : 'CHL',
            },
            {
                'source' : u'article',
                'dest' : u'article',
            },
            {
                'source' : u'name',
                'dest' : u'name',
            },
            {
                'source' : u'name_extra',
                'dest' : u'name_extra',
            },
            {
                'source' : u'address',
                'dest' : u'address',
            },
            {
                'source' : u'city',
                'dest' : u'city',
            },
            {
                'source' : u'nocity',
                'dest' : u'nocity',
            },
            {
                'source' : u'county',
                'dest' : u'county',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'nolatlon',
                'dest' : u'nolatlon',
            },
            {
                'source' : u'description',
                'dest' : u'description',
            },
        ],
    },
    ('uy', 'es') : { # Monuments in Uruguay in Spanish
        'project' : u'wikipedia',
        'lang' : u'es',
        'headerTemplate' : u'MonumentoUruguay/encabezado',
        'rowTemplate' : u'MonumentoUruguay',
        'commonsTemplate' : u'Monumento Uruguay',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Uruguay with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Uruguay',
        'autoGeocode' : True,
        'unusedImagesPage' : u'Wikiproyecto:Patrimonio histórico/Fotos de monumentos de Uruguay sin usar',
        'imagesWithoutIdPage' : u'Wikiproyecto:Patrimonio histórico/Fotos de monumentos de Uruguay sin id',
        'namespaces' : [104],
        'table' : u'monuments_uy_(es)',
        'truncate' : False,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'id',
                'type' : 'varchar(11)',
            },
            {
                'source' : u'enlace',
                'dest' : u'enlace',
            },
            {
                'source' : u'monumento_enlace',
                'dest' : u'monumento_enlace',
            },
            {
                'source' : u'monumento_desc',
                'dest' : u'monumento_desc',
            },
            {
                'source' : u'monumento',
                'dest' : u'monumento',
            },
            {
                'source' : u'dep_iso',
                'dest' : u'dep_iso',
            },
            {
                'source' : u'departamento',
                'dest' : u'departamento',
            },
            {
                'source' : u'localidad',
                'dest' : u'localidad',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'long',
                'dest' : u'lon',
            },
            {
                'source' : u'dirección',
                'dest' : u'direccion',
            },
            {
                'source' : u'imagen',
                'dest' : u'image',
            },
            {
                'source' : u'autores',
                'dest' : u'autores',
            },
            {
                'source' : u'construido',
                'dest' : u'construido',
            },
            {
                'source' : u'tipo',
                'dest' : u'tipo',
            },
            {
                'source' : u'monumento_categoría',
                'dest' : u'commonscat',
            },
        ],
    },
    ('ve', 'es') : { # Monuments in Venezuela in Spanish
        'project' : u'wikipedia',
        'lang' : u'es',
        'headerTemplate' : u'MonumentoVenezuela/encabezado',
        'rowTemplate' : u'MonumentoVenezuela',
        'commonsTemplate' : u'Monumento Venezuela',
        'commonsTrackerCategory' : u'Cultural heritage monuments in Venezuela with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in Venezuela',
        'autoGeocode' : True,
        'unusedImagesPage' : u'Wikiproyecto:Patrimonio histórico/Fotos de monumentos de Venezuela sin usar',
        'imagesWithoutIdPage' : u'Wikiproyecto:Patrimonio histórico/Fotos de monumentos de Venezuela sin id',
        'namespaces' : [104],
        'table' : u'monuments_ve_(es)',
        'truncate' : False,
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'id',
                'type' : 'varchar(11)',
            },
            {
                'source' : u'enlace',
                'dest' : u'enlace',
            },
            {
                'source' : u'monumento_enlace',
                'dest' : u'monumento_enlace',
            },
            {
                'source' : u'monumento_desc',
                'dest' : u'monumento_desc',
            },
            {
                'source' : u'monumento',
                'dest' : u'monumento',
            },
            {
                'source' : u'estado_iso',
                'dest' : u'estado_iso',
            },
            {
                'source' : u'estado',
                'dest' : u'estado',
            },
            {
                'source' : u'municipio',
                'dest' : u'municipio',
            },
            {
                'source' : u'ciudad',
                'dest' : u'ciudad',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'long',
                'dest' : u'lon',
            },
            {
                'source' : u'dirección',
                'dest' : u'direccion',
            },
            {
                'source' : u'imagen',
                'dest' : u'image',
            },
            {
                'source' : u'monumento_categoría',
                'dest' : u'commonscat',
            },
        ],
    },
    ('za', 'en') : { # Monuments in South Africa
        'project' : u'wikipedia',
        'lang' : u'en',
        'headerTemplate' : u'SAHRA heritage site header',
        'rowTemplate' : u'SAHRA heritage site row',
        'commonsTemplate' : u'South African Heritage Site',
        'commonsTrackerCategory' : u'South Africa Heritage Resources with known IDs',
        'commonsCategoryBase' : u'Cultural heritage monuments in South Africa',
        'autoGeocode' : False,
        'unusedImagesPage' : u'Wikipedia:WikiProject Historic sites/Unused images of heritage sites in South Africa',
        'imagesWithoutIdPage' : u'Wikipedia:WikiProject Historic sites/Heritage sites in South Africa without ID',
        'namespaces' : [0],
        'table' : u'monuments_za_(en)',
        'truncate' : False, # Not all ids are filled, just overwrite it
        'primkey' : u'sitereference',
        'fields' : [
            {
                'source' : u'SiteReference',
                'dest' : u'sitereference',
                'type' : 'varchar(20)',
                'default' : '0',
            },
             {
                'source' : u'guid',
                'dest' : u'guid',
            },
             {
                'source' : u'Site_name',
                'dest' : u'site_name',
            },
            {
                'source' : u'Magisterial_district',
                'dest' : u'magisterial_district',
            },
            {
                'source' : u'Municipal_name',
                'dest' : u'municipal_name',
            },
            {
                'source' : u'Town',
                'dest' : u'town',
            },
            {
                'source' : u'Erf number',
                'dest' : u'erf_number',
            },
            {
                'source' : u'Farm number',
                'dest' : u'farm_number',
            },
            {
                'source' : u'Portion',
                'dest' : u'portion',
            },
            {
                'source' : u'NHRA status',
                'dest' : u'nhra_status',
            },
            {
                'source' : u'NMC status',
                'dest' : u'nmc_status',
            },
            {
                'source' : u'Description',
                'dest' : u'description',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'Province_iso',
                'dest' : u'province_iso',
            },
            {
                'source' : u'Latitude',
                'dest' : u'lat',
            },
            {
                'source' : u'Longitude',
                'dest' : u'lon',
            },
        ],
    },

	# Wiki Loves Public Art configuration
    ('wlpa-at', 'de') : { # WLPA in Austria in German
        'project' : u'wikipedia',
        'lang' : u'de',
        'headerTemplate' : u'WLPA-AT-Kopf',
        'rowTemplate' : u'WLPA-AT-Zeile',
        'footerTemplate' : u'',
        'commonsTemplate' : u'Public Art Austria',
        'commonsTrackerCategory' : u'Public art in Austria with known IDs',
        'commonsCategoryBase' : u'Public art in Austria',
        'unusedImagesPage' : u'User:Multichill/Unused public art in Austria',
        'imagesWithoutIdPage' : u'User:Multichill/Public art in Austria without ID',
        #'registrantUrlBase' : {'AT-9':u'http://www.wien.gv.at/kulturportal/public/grafik.aspx?FeatureClass=kunstkultur&ThemePage=4&FeatureByID=%s','AT-401':u'http://www.linz.at/archiv/denkmal/Default.asp?action=denkmaldetail&id=%s'},
        'namespaces' : [0],
        'table' : u'wlpa_at_(de)',
        'truncate' : False, 
        'primkey' : (u'Region', u'ID'),
        'fields' : [
            {
                'source' : u'ID',
                'dest' : u'ID',
                'type' : 'varchar(25)',
                'default' : '0',
            },
            {
                'source' : u'Name',
                'dest' : u'Name',
            },
            {
                'source' : u'Name-Vulgo',
                'dest' : u'Name-Vulgo',
            },
            {
                'source' : u'Foto',
                'dest' : u'Foto',
            },
            {
                'source' : u'Commonscat',
                'dest' : u'Commonscat',
            },
            {
                'source' : u'Artikel',
                'dest' : u'Artikel',
            },
            {
                'source' : u'Typ',
                'dest' : u'Typ',
            },
            {
                'source' : u'Adresse',
                'dest' : u'Adresse',
            },
            {
                'source' : u'Adresse-Sort',
                'dest' : u'Adresse-Sort',
            },
            {
                'source' : u'Anzeige-Adresse',
                'dest' : u'Anzeige-Adresse',
            },
            {
                'source' : u'Längengrad',
                'dest' : u'lon',
            },
            {
                'source' : u'Breitengrad',
                'dest' : u'lat',
            },
            {
                'source' : u'Beschreibung',
                'dest' : u'Beschreibung',
            },
            {
                'source' : u'Standort',
                'dest' : u'Standort',
            },
            {
                'source' : u'Künstler',
                'dest' : u'Kunstler',
            },
            {
                'source' : u'Datierung',
                'dest' : u'Datierung',
            },
            {
                'source' : u'Region',
                'dest' : u'Region',
                'default' : u'AT-9',
            },
        ],
    },
	('wlpa-es-ct', 'ca') : { # WLPA in Catalonia in Catalan
        'project' : u'wikipedia',
        'lang' : u'ca',
        'headerTemplate' : u'Capçalera art públic',
        'rowTemplate' : u'Filera art públic',
        'footerTemplate' : u'',
        'commonsTemplate' : u'Art públic Barcelona',
        'commonsTrackerCategory' : u'Public art in Spain with known IDs',
        'commonsCategoryBase' : u'Public art in Catalonia',
        'unusedImagesPage' : u'User:Multichill/Unused public art in Spain',
        'imagesWithoutIdPage' : u'User:Multichill/Public art in Spain without ID',
        'registrantUrlBase' : u'http://w10.bcn.es/APPS/gmocataleg_monum/FitxaMonumentAc.do?idioma=CA&codiMonumIntern=/%s',
        'namespaces' : [0],
        'table' : u'wlpa_es-ct_(ca)',
        'truncate' : False, 
        'primkey' : u'codi',
        'fields' : [
            {
                'source' : u'codi',
                'dest' : u'codi',
                'type' : 'varchar(25)',
                'default' : '0',
            },
            {
                'source' : u'nom',
                'dest' : u'nom',
            },
            {
                'source' : u'títol',
                'dest' : u'titol',
            },
            {
                'source' : u'descripció',
                'dest' : u'descripcio',
            },
            {
                'source' : u'autor',
                'dest' : u'autor',
            },
            {
                'source' : u'data',
                'dest' : u'data',
            },
            {
                'source' : u'material',
                'dest' : u'material',
            },
            {
                'source' : u'lloc',
                'dest' : u'lloc',
            },
            {
                'source' : u'municipi',
                'dest' : u'municipi',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'idurl',
                'dest' : u'idurl',
            },
            {
                'source' : u'panorama',
                'dest' : u'fop',
                'conv' : u'es-ct-fop',
            },
            {
                'source' : u'imatge',
                'dest' : u'imatge',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'idurl',
                'dest' : u'registrant_url',
                'conv' : u'generateRegistrantUrl-wlpa-es-ct',
            },
            {
                'source' : u'títol',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
        ],
    },
    ('wlpa-fi', 'fi') : { # WLPA in Finland in Finnish
        'project' : u'wikipedia',
        'lang' : u'fi',
        'headerTemplate' : u'Wlpa-teokset-alku',
        'rowTemplate' : u'Wlpa-teokset-rivi',
        'footerTemplate' : u'Wlpa-teokset-loppu',
        'commonsTemplate' : u'Public Art Finland',
        'commonsTrackerCategory' : u'Public art in Finland with known IDs',
        'commonsCategoryBase' : u'Public art in Finland',
        'unusedImagesPage' : u'User:Multichill/Unused public art in Finland',
        'imagesWithoutIdPage' : u'User:Multichill/Public art in Finland without ID',
        'namespaces' : [0],
        'table' : u'wlpa_fi_(fi)',
        'truncate' : False, 
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'id',
                'type' : 'varchar(25)',
                'default' : '0',
            },
            {
                'source' : u'nimi',
                'dest' : u'nimi',
            },
            {
                'source' : u'tekijä',
                'dest' : u'tekija',
            },
            {
                'source' : u'omistaja',
                'dest' : u'omistaja',
            },
            {
                'source' : u'valmistumisvuosi',
                'dest' : u'valmistumisvuosi',
            },
            {
                'source' : u'materiaali',
                'dest' : u'materiaali',
            },
            {
                'source' : u'tekijän_kuolinvuosi',
                'dest' : u'tekijan_kuolinvuosi',
            },
            {
                'source' : u'tekijän_kuolinvuosi',
                'dest' : u'fop',
                'conv' : u'fi-fop',
            },
            {
                'source' : u'url',
                'dest' : u'url',
            },
            {
                'source' : u'sijainti',
                'dest' : u'sijainti',
            },
            {
                'source' : u'maakunta',
                'dest' : u'maakunta',
            },
            {
                'source' : u'kunta',
                'dest' : u'kunta',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'lon',
                'dest' : u'lon',
            },
            {
                'source' : u'kuva',
                'dest' : u'kuva',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
            {
                'source' : u'nimi',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
        ],
    },
    ('wlpa-il', 'en') : { # WLPA in Israel in English
        'project' : u'wikipedia',
        'lang' : u'en',
        'headerTemplate' : u'Public art in Israel - header',
        'rowTemplate' : u'Public art in Israel - row',
        'footerTemplate' : u'',
        'commonsTemplate' : u'Public Art Israel',
        'commonsTrackerCategory' : u'Public art in Israel with known IDs',
        'commonsCategoryBase' : u'Public art in Israel',
        'unusedImagesPage' : u'User:Multichill/Unused public art in Israel',
        'imagesWithoutIdPage' : u'User:Multichill/Public art in Israel without ID',
        'namespaces' : [0],
        'table' : u'wlpa_il_(en)',
        'truncate' : False, 
        'primkey' : u'id',
        'fields' : [
            {
                'source' : u'id',
                'dest' : u'id',
                'type' : 'int(6)',
                'default' : 0,
            },
            {
                'source' : u'title',
                'dest' : u'title',
            },
            {
                'source' : u'artist',
                'dest' : u'artist',
            },
            {
                'source' : u'extArtistLink',
                'dest' : u'extArtistLink',
            },
            {
                'source' : u'description',
                'dest' : u'description',
            },
            {
                'source' : u'year',
                'dest' : u'year',
            },
            {
                'source' : u'type',
                'dest' : u'type',
            },
            {
                'source' : u'fop',
                'dest' : u'fop',
                'conv' : u'il-fop',
            },
            {
                'source' : u'address',
                'dest' : u'address',
            },
            {
                'source' : u'district',
                'dest' : u'district',
            },
            {
                'source' : u'municipality',
                'dest' : u'municipality',
            },
            {
                'source' : u'lat',
                'dest' : u'lat',
            },
            {
                'source' : u'long',
                'dest' : u'lon',
            },
            {
                'source' : u'image',
                'dest' : u'image',
            },
            {
                'source' : u'title',
                'dest' : u'monument_article',
                'conv' : u'extractWikilink',
            },
            {
                'source' : u'commonscat',
                'dest' : u'commonscat',
            },
        ],
    },
}
