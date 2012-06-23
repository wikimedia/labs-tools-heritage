/* Create view for all country tables 
 * 
 * Please keep this list sorted by country code!
 *
 * If you change something please test it. 
 */

-- Update monuments_all_tmp when you change this table
CREATE TABLE IF NOT EXISTS `monuments_all` (
	  `country` varchar(10) NOT NULL DEFAULT '',
	  `lang` varchar(10) NOT NULL DEFAULT '',
	  `id` varchar(25) NOT NULL DEFAULT '0',
	  `adm0` varchar(5) NOT NULL DEFAULT '',
	  `adm1` varchar(10) DEFAULT NULL,
	  `adm2` varchar(255) DEFAULT NULL,
	  `adm3` varchar(255) DEFAULT NULL,
	  `adm4` varchar(255) DEFAULT NULL,
	  `name` varchar(255) NOT NULL DEFAULT '',
	  `address` varchar(255) NOT NULL DEFAULT '',
	  `municipality` varchar(255) NOT NULL DEFAULT '',
	  `lat` double NOT NULL DEFAULT '0',
	  `lon` double NOT NULL DEFAULT '0',
	  `coord` POINT NOT NULL,
	  `image` varchar(255) NOT NULL DEFAULT '',
	  `source` varchar(255) NOT NULL DEFAULT '',
	  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	  `monument_article` varchar(255) NOT NULL DEFAULT '',
	  `registrant_url` varchar(255) NOT NULL DEFAULT '',
	  PRIMARY KEY (`country`,`lang`,`id`),
	  KEY `adm0` (`adm0`),
	  KEY `adm1` (`adm1`),
	  KEY `adm2` (`adm2`),
	  KEY `adm3` (`adm3`),
	  KEY `adm4` (`adm4`),
	  KEY `name` (`name`),
	  FULLTEXT KEY `name_ft` (`name`),
	  SPATIAL KEY `coord_spatial` (`coord`)
	) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- Just an index-free version of `monuments_all`, used for staging data
CREATE TABLE IF NOT EXISTS `monuments_all_tmp` (
	  `country` varchar(10) NOT NULL DEFAULT '',
	  `lang` varchar(10) NOT NULL DEFAULT '',
	  `id` varchar(25) NOT NULL DEFAULT '0',
	  `adm0` varchar(5) NOT NULL DEFAULT '',
	  `adm1` varchar(10) DEFAULT NULL,
	  `adm2` varchar(255) DEFAULT NULL,
	  `adm3` varchar(255) DEFAULT NULL,
	  `adm4` varchar(255) DEFAULT NULL,
	  `name` varchar(255) NOT NULL DEFAULT '',
	  `address` varchar(255) NOT NULL DEFAULT '',
	  `municipality` varchar(255) NOT NULL DEFAULT '',
	  `lat` double NOT NULL DEFAULT '0',
	  `lon` double NOT NULL DEFAULT '0',
	  `coord` POINT NOT NULL,
	  `image` varchar(255) NOT NULL DEFAULT '',
	  `source` varchar(255) NOT NULL DEFAULT '',
	  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	  `monument_article` varchar(255) NOT NULL DEFAULT '',
	  `registrant_url` varchar(255) NOT NULL DEFAULT '',
	  PRIMARY KEY (`country`,`lang`,`id`)
	) ENGINE=MyISAM DEFAULT CHARSET=utf8;
	
TRUNCATE TABLE monuments_all_tmp;
/* Andorra in Catalan */
REPLACE INTO `monuments_all_tmp`
SELECT 'ad' AS `country`, 
       'ca' AS `lang`,
       `id`AS `id`,
	   'ad' AS `adm0`,
	   `municipi` AS `adm1`,
		NULL AS `adm2`,
		NULL AS `adm3`,
		NULL AS `adm4`,
        `nomcoor` AS `name`,
        `lloc` AS `address`,
        `municipi` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
		POINT(`lat`, `lon`) AS `coord`,
        `imatge` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
        FROM `monuments_ad_(ca)`;
/* Austria in German */
REPLACE INTO `monuments_all_tmp`
SELECT 'at' AS `country`, 
       'de' AS `lang`,
	   `objektid` AS `id`,
       'at' AS `adm0`,
	   `region-iso` AS `adm1`,
	   `bezirk` AS `adm2`,
	   `gemeinde` AS `adm3`,
	   `katastralgemeinde` AS `adm4`,
       `name` AS `name`,
       `adresse` AS `address`,
       `gemeinde` AS `municipality`,
       `lat` AS `lat`,
       `lon` AS `lon`,
		POINT(`lat`, `lon`) AS `coord`,
       `foto` AS `image`,
       `source` AS `source`,
       `changed` AS `changed`,
        REPLACE( `artikel`,  ' ',  '_' ) AS `monument_article`,
        '' AS `registrant_url`
        FROM `monuments_at_(de)`;
/* Brussel */
REPLACE INTO `monuments_all_tmp`
SELECT 'be-bru' AS `country`,
       'nl' AS `lang`,
		`code` AS `id`,
		'be' AS `adm0`,
		'be-bru' AS `adm1`,
		NULL AS `adm2`,
		NULL AS `adm3`,
		NULL AS `adm4`,
        `omschrijving` AS `name`,
        `adres` AS `address`,
        `plaats` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
		POINT(`lat`, `lon`) AS `coord`,
        `image` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`, 
        '' AS `registrant_url`
        FROM `monuments_be-bru_(nl)`;
/* Vlaanderen in French */
REPLACE INTO `monuments_all_tmp`
SELECT 'be-vlg' AS `country`,
       'fr' AS `lang`,
		`id` AS `id`,
		'be' AS `adm0`,
		'be-vlg' AS `adm1`,
		NULL AS `adm2`,
		NULL AS `adm3`,
		NULL AS `adm4`,
        `nom_objet` AS `name`,
        `adresse` AS `address`,
        `commune` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
		POINT(`lat`, `lon`) AS `coord`,
        `image` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
        FROM `monuments_be-vlg_(fr)`;
/* Vlaanderen in Dutch */
REPLACE INTO `monuments_all_tmp`
SELECT 'be-vlg' AS `country`,
       'nl' AS `lang`,
		`id` AS `id`,
		'be' AS `adm0`,
		'be-vlg' AS `adm1`,
		NULL AS `adm2`,
		NULL AS `adm3`,
		NULL AS `adm4`,
        `objectnaam` AS `name`,
        `adres` AS `address`,
        `gemeente` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
		POINT(`lat`, `lon`) AS `coord`,
        `image` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
        FROM `monuments_be-vlg_(nl)`;
/* Wallonia in English */
REPLACE INTO `monuments_all_tmp`
SELECT 'be-wal' AS `country`,
       'en' AS `lang`,
		CONCAT(`niscode`, '-', `objcode`) AS `id`,
		'be' AS `adm0`,
		'be-wal' AS `adm1`,
		NULL AS `adm2`,
		NULL AS `adm3`,
		NULL AS `adm4`,
        `descr_en` AS `name`,
        `address` AS `address`,
        `section` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
		POINT(`lat`, `lon`) AS `coord`,
        `image` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`, 
        `registrant_url` AS `registrant_url`
        FROM `monuments_be-wal_(en)`;
/* Wallonie in French*/
REPLACE INTO `monuments_all_tmp`
SELECT 'be-wal' AS `country`,
       'fr' AS `lang`,
		CONCAT(`id_commune`, '-', `clt-pex`, '-', `id_objet`) AS `id`,
		'be' AS `adm0`,
		'be-wal' AS `adm1`,
		NULL AS `adm2`,
		NULL AS `adm3`,
		NULL AS `adm4`,
        `nom_objet` AS `name`,
        `adresse` AS `address`,
        `commune` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
		POINT(`lat`, `lon`) AS `coord`,
        `image` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`, 
        `registrant_url` AS `registrant_url`
        FROM `monuments_be-wal_(fr)`;
/* Wallonie in Dutch*/
REPLACE INTO `monuments_all_tmp`
SELECT 'be-wal' AS `country`,
       'nl' AS `lang`,
		CONCAT(`niscode`, '-', `objcode`) AS `id`,
		'be' AS `adm0`,
		'be-wal' AS `adm1`,
		NULL AS `adm2`,
		NULL AS `adm3`,
		NULL AS `adm4`,
        `descr_nl` AS `name`,
        `adres` AS `address`,
        `gemeente` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
		POINT(`lat`, `lon`) AS `coord`,
        `image` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`, 
        `registrant_url` AS `registrant_url`
        FROM `monuments_be-wal_(nl)`;
/* Belarus */
REPLACE INTO `monuments_all_tmp`
SELECT 'by' AS `country`,
       'be-x-old' AS `lang`,
        `id` AS `id`,
		'by' AS `adm0`,
		NULL AS `adm1`,
		NULL AS `adm2`,
		NULL AS `adm3`,
		NULL AS `adm4`,
        `name` AS `name`,
        `address` AS `address`,
        `place` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
		POINT(`lat`, `lon`) AS `coord`,
        `image` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        '' AS `registrant_url`
        FROM `monuments_by_(be-x-old)`;
/* Switzerland in English*/
REPLACE INTO `monuments_all_tmp`
SELECT 'ch' AS `country`,
       'en' AS `lang`,
		`kgs_nr` AS `id`,
		'ch' AS `adm0`,
		`region-iso` AS `adm1`,
		NULL AS `adm2`,
		`municipality` AS `adm3`,
		NULL AS `adm4`,
		`name` AS `name`,
		`address` AS `address`,
		`municipality` AS `municipality`,
		`lat` AS `lat`,
		`lon` AS `lon`,
		POINT(`lat`, `lon`) AS `coord`,
		`image` AS `image`,
		`source` AS `source`,
		`changed` AS `changed`,
		`monument_article` AS `monument_article`,
		'' AS `registrant_url`
		FROM `monuments_ch_(en)`;
/* Switzerland in French */
REPLACE INTO `monuments_all_tmp`
SELECT 'ch' AS `country`,
       'fr' AS `lang`,
		`kgs-nr` AS `id`,
		'ch' AS `adm0`,
		`canton` AS `adm1`,
		NULL AS `adm2`,
		`commune` AS `adm3`,
		NULL AS `adm4`,
		`objet` AS `name`,
		`addresse` AS `address`,
		`commune` AS `municipality`,
		`lat` AS `lat`,
		`lon` AS `lon`,
		POINT(`lat`, `lon`) AS `coord`,
		`photo` AS `image`,
		`source` AS `source`,
		`changed` AS `changed`,
		`monument_article` AS `monument_article`,
		'' AS `registrant_url`
		FROM `monuments_ch_(fr)`;
/* Switzerland in German */
REPLACE INTO `monuments_all_tmp`
SELECT 'ch' AS `country`,
       'de' AS `lang`,
		`kgs-nr` AS `id`,
		'ch' AS `adm0`,
		`kanton` AS `adm1`,
		NULL AS `adm2`,
		`gemeinde` AS `adm3`,
		NULL AS `adm4`,
		`name` AS `name`,
		`addresse` AS `address`,
		`gemeinde` AS `municipality`,
		`lat` AS `lat`,
		`lon` AS `lon`,
		POINT(`lat`, `lon`) AS `coord`,
		`foto` AS `image`,
		`source` AS `source`,
		`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        '' AS `registrant_url`
		FROM `monuments_ch_(de)`;
/* Denmark bygninger */
REPLACE INTO `monuments_all_tmp`
SELECT 'dk-bygninger' AS `country`,
       'da' AS `lang`,
		CONCAT(`kommunenr`, '-', `ejendomsnr`, '-', `bygningsnr`) AS `id`,
		'dk' AS `adm0`,
		NULL AS `adm1`,
		NULL AS `adm2`,
		NULL AS `adm3`,
		NULL AS `adm4`,
		`sagsnavn` AS `name`,
		`adresse` AS `address`,
		`by` AS `municipality`,
		`lat` AS `lat`,
		`lon` AS `lon`,
		POINT(`lat`, `lon`) AS `coord`,
		`billede` AS `image`,
		`source` AS `source`,
		`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
		FROM `monuments_dk-bygninger_(da)`;
/* Denmark fortidsminder */
REPLACE INTO `monuments_all_tmp`
SELECT 'dk-fortidsminder' AS `country`,
       'da' AS `lang`,
		`systemnummer` AS `id`,
		'dk' AS `adm0`,
		NULL AS `adm1`,
		NULL AS `adm2`,
		NULL AS `adm3`,
		NULL AS `adm4`,
		`stednavn` AS `name`,
		'' AS `address`,
		'' AS `municipality`,
		`lat` AS `lat`,
		`lon` AS `lon`,
		POINT(`lat`, `lon`) AS `coord`,
		`billede` AS `image`,
		`source` AS `source`,
		`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
	FROM `monuments_dk-fortidsminder_(da)`;
/* Bergheim, NRW, Germany in German */
REPLACE INTO `monuments_all_tmp`
SELECT 'de-nrw-bm' AS `country`, 
    'de' AS `lang`,
	`nummer` AS `id`,
	'de' AS `adm0`,
	'de-nw' AS `adm1`,
	'Köln' AS `adm2`,
	'Rhein-Erft-Kreis' AS `adm3`,
	'Bergheim' AS `adm4`,
    `bezeichnung` AS `name`,
    `adresse` AS `address`,
    `ortsteil` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
	POINT(`lat`, `lon`) AS `coord`,
    `bild` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        REPLACE( `artikel`,  ' ',  '_' ) AS `monument_article`,
        '' AS `registrant_url`
	FROM `monuments_de-nrw-bm_(de)`;
/* Bavaria, Germany in German */
REPLACE INTO `monuments_all_tmp`
SELECT 'de-by' AS `country`, 
    'de' AS `lang`,
	`nummer` AS `id`,
	'de' AS `adm0`,
	'de-by' AS `adm1`,
	NULL AS `adm2`,
	NULL AS `adm3`,
	`stadt` AS `adm4`,
    `bezeichnung` AS `name`,
    `adresse` AS `address`,
    `stadt` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
	POINT(`lat`, `lon`) AS `coord`,
    `bild` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
    REPLACE( `artikel`,  ' ',  '_' ) AS `monument_article`,
    '' AS `registrant_url`
	FROM `monuments_de-by_(de)`;
/* Hessen, Germany in German */
REPLACE INTO `monuments_all_tmp`
SELECT 'de-he' AS `country`, 
    'de' AS `lang`,
	`nummer` AS `id`,
	'de' AS `adm0`,
	'de-he' AS `adm1`,
		NULL AS `adm2`,
		NULL AS `adm3`,
	`stadt` AS `adm4`,
    `bezeichnung` AS `name`,
    `adresse` AS `address`,
    `stadt` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
	POINT(`lat`, `lon`) AS `coord`,
    `bild` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        REPLACE( `artikel`,  ' ',  '_' ) AS `monument_article`,
        `registrant_url` AS `registrant_url`
	FROM `monuments_de-he_(de)`;
/* Cologne, Germany in German */
REPLACE INTO `monuments_all_tmp`
SELECT 'de-nrw-k' AS `country`, 
    'de' AS `lang`,
	`nummer_denkmalliste` AS `id`,
	'de' AS `adm0`,
	'de-nw' AS `adm1`,
	'Köln' AS `adm2`,
	'Köln' AS `adm3`,
	`ortsteil` AS `adm4`,
    `bezeichnung` AS `name`,
    `adresse` AS `address`,
    `ortsteil` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
	POINT(`lat`, `lon`) AS `coord`,
    `bild` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url`
	FROM `monuments_de-nrw-k_(de)`;
/* Estonia */
REPLACE INTO `monuments_all_tmp`
SELECT 'ee' AS `country`,
       'et' AS `lang`,
		`number` AS `id`, 
		'ee' AS `adm0`,
		`maakond` AS `adm1`,
		`omavalitsus` AS `adm2`,
		NULL AS `adm3`,
		NULL AS `adm4`,
	`nimi` AS `name`,
	`aadress` AS `address`,
	`omavalitsus` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	POINT(`lat`, `lon`) AS `coord`,
	`pilt` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
	FROM `monuments_ee_(et)`;
/* Spain in Catalan */
REPLACE INTO `monuments_all_tmp`
SELECT 'es' AS `country`,
       'ca' AS `lang`,
        `bic` AS `id`,
		'es' AS `adm0`,
		NULL AS `adm1`,
		NULL AS `adm2`,
		`municipi` AS `adm3`,
		NULL AS `adm4`,
        `nomcoor` AS `name`,
        `lloc` AS `address`,
        `municipi` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
	    POINT(`lat`, `lon`) AS `coord`,
        `imatge` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        '' AS `registrant_url`
        FROM `monuments_es_(ca)`;
/* Spain in Spanish */
REPLACE INTO `monuments_all_tmp`
SELECT 'es' AS `country`,
       'es' AS `lang`,
		`bic` AS `id`,
		'es' AS `adm0`,
		NULL AS `adm1`,
		NULL AS `adm2`,
		`municipio` AS `adm3`,
		NULL AS `adm4`,
        `nombrecoor` AS `name`,
        `lugar` AS `address`,
        `municipio` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
	    POINT(`lat`, `lon`) AS `coord`,
        `imagen` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        '' AS `registrant_url`
        FROM `monuments_es_(es)`;
/* Catalunya in Catalan */
REPLACE INTO `monuments_all_tmp`
SELECT 'es-ct' AS `country`,
       'ca' AS `lang`,
        `bic` AS `id`,
		'es' AS `adm0`,
		'es-ct' AS `adm1`,
		NULL AS `adm2`,
		`municipi` AS `adm3`,
		NULL AS `adm4`,
        `nomcoor` AS `name`,
        `lloc` AS `address`,
        `municipi` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
	    POINT(`lat`, `lon`) AS `coord`,
        `imatge` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
        FROM `monuments_es-ct_(ca)`;
/* Galicia province (Spain) in Galician */
REPLACE INTO `monuments_all_tmp`
SELECT 'es' AS `country`,
       'gl' AS `lang`,
        `bic` AS `id`,
		'es' AS `adm0`,
		'es-ga' AS `adm1`,
		NULL AS `adm2`,
		`concello` AS `adm3`,
		NULL AS `adm4`,
        `nomeoficial` AS `name`,
        `lugar` AS `address`,
        `concello` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
	    POINT(`lat`, `lon`) AS `coord`,
        `imaxe` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        '' AS `registrant_url`
        FROM `monuments_es-gl_(gl)`;
/* Valencia in Catalan */
REPLACE INTO `monuments_all_tmp`
SELECT 'es-vc' AS `country`,
       'ca' AS `lang`,
       `bic` AS `id`,
	   'es' AS `adm0`,
		'es-vc' AS `adm1`,
		NULL AS `adm2`,
		`municipi` AS `adm3`,
		NULL AS `adm4`,
        `nomcoor` AS `name`,
        `lloc` AS `address`,
        `municipi` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
	    POINT(`lat`, `lon`) AS `coord`,
        `imatge` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        '' AS `registrant_url`
        FROM `monuments_es-vc_(ca)`;
/* France in Catalan */
REPLACE INTO `monuments_all_tmp`
SELECT 'fr' AS `country`,
       'ca' AS `lang`,
        `id` AS `id`,
		'fr' AS `adm0`,
		NULL AS `adm1`,
		NULL AS `adm2`,
		NULL AS `adm3`,
		`municipi` AS `adm4`,
        `nomcoor` AS `name`,
        `lloc` AS `address`,
        `municipi` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
	    POINT(`lat`, `lon`) AS `coord`,
        `imatge` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
        FROM `monuments_fr_(ca)`;
/* France in French */
REPLACE INTO `monuments_all_tmp`
SELECT 'fr' AS `country`,
       'fr' AS `lang`,
        `notice` AS `id`,
		'fr' AS `adm0`,
		NULL AS `adm1`,
		NULL AS `adm2`,
		NULL AS `adm3`,
		`commune` AS `adm4`,
        `monument` AS `name`,
        `adresse` AS `address`,
        `commune` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
	    POINT(`lat`, `lon`) AS `coord`,
        `image` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
        FROM `monuments_fr_(fr)`;
/* Ireland in English */
REPLACE INTO `monuments_all_tmp`
SELECT 'ie' AS `country`,
       'en' AS `lang`,
        `number` AS `id`,
		'ie' AS `adm0`,
		NULL AS `adm1`,
		NULL AS `adm2`,
		NULL AS `adm3`,
		NULL AS `adm4`,
        `name` AS `name`,
	'' AS `address`,
	`townland` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	POINT(`lat`, `lon`) AS `coord`,
	`image` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        '' AS `registrant_url`
	FROM `monuments_ie_(en)`;
/* Sardinia in Catalan */
REPLACE INTO `monuments_all_tmp`
SELECT 'it-88' AS `country`,
       'ca' AS `lang`,
        `id` AS `id`,
		'it' AS `adm0`,
		'it-88' AS `adm1`,
		NULL AS `adm2`,
		`municipi` AS `adm3`,
		NULL AS `adm4`,
        `nomcoor` AS `name`,
        `lloc` AS `address`,
        `municipi` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
	    POINT(`lat`, `lon`) AS `coord`,
        `imatge` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
        FROM `monuments_it-88_(ca)`;
/* South Tyrol in German */
REPLACE INTO `monuments_all_tmp`
SELECT 'it-bz' AS `country`, 
       'de' AS `lang`,
        `objektid` AS `id`,
		'it' AS `adm0`,
		'it-32' AS `adm1`,
		'it-bz' AS `adm2`,
		`gemeinde` AS `adm3`,
		NULL AS `adm4`,
        `name` AS `name`,
        `adresse` AS `address`,
        `gemeinde` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
	    POINT(`lat`, `lon`) AS `coord`,
        `foto` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        REPLACE( `artikel`,  ' ',  '_' ) AS `monument_article`,
        `registrant_url` AS `registrant_url`
        FROM `monuments_it-bz_(de)`;
/* Luxemburg in Luxemburgish */
REPLACE INTO `monuments_all_tmp`
SELECT 'lu' AS `country`,
       'lb' AS `lang`,
		`id` AS `id`,
		'lu' AS `adm0`,
		NULL AS `adm1`,
		NULL AS `adm2`,
		`uertschaft` AS `adm3`,
		NULL AS `adm4`,
        `offiziellen_numm` AS `name`,
        `lag` AS `address`,
        `uertschaft` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
	    POINT(`lat`, `lon`) AS `coord`,
        `bild` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        '' AS `registrant_url`
        FROM `monuments_lu_(lb)`;
/* Malta in German */
REPLACE INTO `monuments_all_tmp`
SELECT 'mt' AS `country`, 
       'de' AS `lang`,
	   `inventarnummer` AS `id`,
	   'mt' AS `adm0`,
	   `region-iso` AS `adm1`,
		`gemeinde` AS `adm2`,
		NULL AS `adm3`,
		NULL AS `adm4`,
       `name-de` AS `name`,
       `adresse` AS `address`,
       `gemeinde` AS `municipality`,
       `lat` AS `lat`,
       `lon` AS `lon`,
	   POINT(`lat`, `lon`) AS `coord`,
       `foto` AS `image`,
       `source` AS `source`,
       `changed` AS `changed`,
        REPLACE( `artikel`,  ' ',  '_' ) AS `monument_article`,
        `registrant_url` AS `registrant_url`
        FROM `monuments_mt_(de)`;		
/* Netherlands */
REPLACE INTO `monuments_all_tmp`
SELECT 'nl' AS `country`,
       'nl' AS `lang`,
		`objrijksnr` AS `id`, 
		'nl' AS `adm0`,
		`prov-iso` AS `adm1`,
		`woonplaats` AS `adm2`,
		NULL AS `adm3`,
		NULL AS `adm4`,
	`objectnaam` AS `name`,
	`adres` AS `address`,
	`woonplaats` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	POINT(`lat`, `lon`) AS `coord`,
	`image` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
	FROM `monuments_nl_(nl)`;
/* Norway */
REPLACE INTO `monuments_all_tmp`
SELECT 'no' AS `country`,
       'no' AS `lang`,
		`id` AS `id`,
		'no' AS `adm0`,
		NULL AS `adm1`,
		`kommune` AS `adm2`,
		NULL AS `adm3`,
		NULL AS `adm4`,
	`navn` AS `name`,
	'' AS `address`,
	`kommune` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	POINT(`lat`, `lon`) AS `coord`,
	`bilde` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
	FROM `monuments_no_(no)`;
/* Poland */
REPLACE INTO `monuments_all_tmp`
SELECT 'pl' AS `country`,
       'pl' AS `lang`,
		`numer` AS `id`, 
		'pl' AS `adm0`,
		NULL AS `adm1`,
		NULL AS `adm2`,
	`gmina` AS `adm3`,
		NULL AS `adm4`,
	`nazwa` AS `name`,
	`adres` AS `address`,
	`gmina` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	POINT(`lat`, `lon`) AS `coord`,
	`zdjecie` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        '' AS `registrant_url`
	FROM `monuments_pl_(pl)`;
/* Portugal */
REPLACE INTO `monuments_all_tmp`
SELECT 'pt' AS `country`,
       'pt' AS `lang`,
		`id` AS `id`,
		'pt' AS `adm0`,
		NULL AS `adm1`,
		`concelho` AS `adm2`,
		`freguesia` AS `adm3`,
		NULL AS `adm4`,
	`designacoes` AS `name`,
	'' AS `address`,
	`concelho` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	POINT(`lat`, `lon`) AS `coord`,
	`imagem` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
	FROM `monuments_pt_(pt)`;
/* Romania */
REPLACE INTO `monuments_all_tmp`
SELECT 'ro' AS `country`,
       'ro' AS `lang`,
	`cod` AS `id`, 
	'ro' AS `adm0`,
	NULL AS `adm1`,
		NULL AS `adm2`,
		NULL AS `adm3`,
	`localitate` AS `adm4`,
	`denumire` AS `name`,
	`adresa` AS `address`,
	`localitate` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	POINT(`lat`, `lon`) AS `coord`,
	`imagine` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        '' AS `registrant_url`
	FROM `monuments_ro_(ro)`;
/* Russia */
REPLACE INTO `monuments_all_tmp`
SELECT 'ru' AS `country`,
       'ru' AS `lang`,
	`id` AS `id`, 
	'ru' AS `adm0`,
	NULL AS `adm1`,
		NULL AS `adm2`,
		NULL AS `adm3`,
		NULL AS `adm4`,
	`name` AS `name`,
	`address` AS `address`,
	`region` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	POINT(`lat`, `lon`) AS `coord`,
	`image` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        '' AS `registrant_url`
	FROM `monuments_ru_(ru)`;
/* Scotland */
REPLACE INTO `monuments_all_tmp`
SELECT 'sct' AS `country`,
       'en' AS `lang`,
	`hbnum` AS `id`, 
	'gb' AS `adm0`,
	'sct' AS `adm1`,
		NULL AS `adm2`,
		NULL AS `adm3`,
		NULL AS `adm4`,
	`name` AS `name`,
	'' AS `address`,
	`parbur` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	POINT(`lat`, `lon`) AS `coord`,
	`image` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
	FROM `monuments_sct_(en)`;
/* Sweden */
REPLACE INTO `monuments_all_tmp`
SELECT 'se' AS `country`,
       'sv' AS `lang`,
	`bbr` AS `id`,
	'se' AS `adm0`,
	NULL AS `adm1`,
	`kommun` AS `adm2`,
	NULL AS `adm3`,
	NULL AS `adm4`,
	`namn` AS `name`,
	`plats` AS `address`,
	`kommun` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	POINT(`lat`, `lon`) AS `coord`,
	`bild` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
	FROM `monuments_se_(sv)`;
/* Slovakia in German */
REPLACE INTO `monuments_all_tmp`
SELECT 'sk' AS `country`,
       'de' AS `lang`,
       `objektid` AS `id`,
	   'sk' AS `adm0`,
	   `region-iso` AS `adm1`,
	   `okres` AS `adm2`,
	   `obec` AS `adm3`,
	   `katastralgemeinde` AS `adm4`,
       `name-de` AS `name`,
       `adresse` AS `address`,
       `obec` AS `municipality`,
       `lat` AS `lat`,
       `lon` AS `lon`,
	   POINT(`lat`, `lon`) AS `coord`,
       `foto` AS `image`,
       `source` AS `source`,
       `changed` AS `changed`,
       REPLACE( `artikel`,  ' ',  '_' ) AS `monument_article`,
       '' AS `registrant_url` /* FIXME: Add this field to source table */
       FROM `monuments_sk_(de)`;
/* Slovakia in Slovak */
REPLACE INTO `monuments_all_tmp`
SELECT 'sk' AS `country`,
       'sk' AS `lang`,
       `idobjektu` AS `id`,
	   'sk' AS `adm0`,
	   `iso-regionu` AS `adm1`,
	   `okres` AS `adm2`,
	   `obec` AS `adm3`,
	   `katastralne_uzemie` AS `adm4`,
       `nazov-sk` AS `name`,
       `adresa` AS `address`,
       `obec` AS `municipality`,
       `lat` AS `lat`,
       `lon` AS `lon`,
	   POINT(`lat`, `lon`) AS `coord`,
       `fotka` AS `image`,
       `source` AS `source`,
       `changed` AS `changed`,
       REPLACE( `clanok`,  ' ',  '_' ) AS `monument_article`,
       '' AS `registrant_url` /* FIXME: Add this field to source table */
       FROM `monuments_sk_(sk)`;
/* United States */
REPLACE INTO `monuments_all_tmp`
SELECT 'us' AS `country`,
       'en' AS `lang`,
		`refnum` AS `id`, 
		'us' AS `adm0`,
		NULL AS `adm1`, /* State  AS `adm1`, */
		`county` AS `adm2`,
		NULL AS `adm3`,
		NULL AS `adm4`,
	CONCAT('[[', `article`, '|', `name`, ']]') AS `name`,
	CONCAT(`address`, ' ', `city`) AS `address`,
	`county` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	POINT(`lat`, `lon`) AS `coord`,
	`image` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        REPLACE( `article`,  ' ',  '_' ) AS `monument_article`,
        '' AS `registrant_url`
	FROM `monuments_us_(en)`;

START TRANSACTION;

DELETE FROM monuments_all
	USING monuments_all LEFT JOIN monuments_all_tmp
		ON monuments_all.country = monuments_all_tmp.country
				AND monuments_all.lang = monuments_all_tmp.lang
				AND monuments_all.id = monuments_all_tmp.id
	WHERE monuments_all_tmp.id IS NULL;

REPLACE INTO monuments_all
	SELECT monuments_all_tmp.*
		FROM monuments_all_tmp LEFT JOIN monuments_all
			ON monuments_all.country = monuments_all_tmp.country
				AND monuments_all.lang = monuments_all_tmp.lang
				AND monuments_all.id = monuments_all_tmp.id
		WHERE monuments_all.id IS NULL OR monuments_all_tmp.changed > monuments_all.changed;

COMMIT;
