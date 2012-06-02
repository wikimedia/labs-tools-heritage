/* Create view for all country tables 
 * 
 * Please keep this list sorted by country code!
 *
 * If you change something please test it. 
 *
 * FIXME : Don't hardcode database and server
 */
connect p_erfgoed_p sql.toolserver.org;
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
	  KEY `latitude` (`lat`),
	  KEY `longitude` (`lon`)
	) ENGINE=MyISAM DEFAULT CHARSET=utf8;
TRUNCATE TABLE monuments_all;
/* Andorra in Catalan */
REPLACE INTO `monuments_all`
SELECT 'ad' AS `country`, 
       'ca' AS `lang`,
        `id` AS `id`,
		'ad' AS `adm0`,
        `nomcoor` AS `name`,
        `lloc` AS `address`,
        `municipi` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `imatge` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
        FROM `monuments_ad_(ca)`;
/* Austria in German */
REPLACE INTO `monuments_all`
SELECT 'at' AS `country`, 
       'de' AS `lang`,
		`objektid` AS `id`,
		'at' AS `adm0`,
        `name` AS `name`,
        `adresse` AS `address`,
        `gemeinde` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `foto` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        REPLACE( `artikel`,  ' ',  '_' ) AS `monument_article`,
        '' AS `registrant_url`
        FROM `monuments_at_(de)`;
/* Brussel */
REPLACE INTO `monuments_all`
SELECT 'be-bru' AS `country`,
       'nl' AS `lang`,
		`code` AS `id`,
		'be' AS `adm0`,
		'be-bru' AS `adm1`,
        `omschrijving` AS `name`,
        `adres` AS `address`,
        `plaats` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `image` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`, 
        '' AS `registrant_url`
        FROM `monuments_be-bru_(nl)`;
/* Vlaanderen in French */
REPLACE INTO `monuments_all`
SELECT 'be-vlg' AS `country`,
       'fr' AS `lang`,
		`id` AS `id`,
		'be' AS `adm0`,
		'be-vlg' AS `adm1`,
        `nom_objet` AS `name`,
        `adresse` AS `address`,
        `commune` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `image` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
        FROM `monuments_be-vlg_(fr)`;
/* Vlaanderen in Dutch */
REPLACE INTO `monuments_all`
SELECT 'be-vlg' AS `country`,
       'nl' AS `lang`,
		`id` AS `id`,
		'be' AS `adm0`,
		'be-vlg' AS `adm1`,
        `objectnaam` AS `name`,
        `adres` AS `address`,
        `gemeente` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `image` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
        FROM `monuments_be-vlg_(nl)`;
/* Wallonia in English */
REPLACE INTO `monuments_all`
SELECT 'be-wal' AS `country`,
       'en' AS `lang`,
		CONCAT(`niscode`, '-', `objcode`) AS `id`,
		'be' AS `adm0`,
		'be-wal' AS `adm1`,
        `descr_en` AS `name`,
        `address` AS `address`,
        `section` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `image` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`, 
        `registrant_url` AS `registrant_url`
        FROM `monuments_be-wal_(en)`;
/* Wallonie in French*/
REPLACE INTO `monuments_all`
SELECT 'be-wal' AS `country`,
       'fr' AS `lang`,
		CONCAT(`id_commune`, '-', `clt-pex`, '-', `id_objet`) AS `id`,
		'be' AS `adm0`,
		'be-wal' AS `adm1`,
        `nom_objet` AS `name`,
        `adresse` AS `address`,
        `commune` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `image` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`, 
        `registrant_url` AS `registrant_url`
        FROM `monuments_be-wal_(fr)`;
/* Wallonie in Dutch*/
REPLACE INTO `monuments_all`
SELECT 'be-wal' AS `country`,
       'nl' AS `lang`,
		CONCAT(`niscode`, '-', `objcode`) AS `id`,
		'be' AS `adm0`,
		'be-wal' AS `adm1`,
        `descr_nl` AS `name`,
        `adres` AS `address`,
        `gemeente` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `image` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`, 
        `registrant_url` AS `registrant_url`
        FROM `monuments_be-wal_(nl)`;
/* Belarus */
REPLACE INTO `monuments_all`
SELECT 'by' AS `country`,
       'be-x-old' AS `lang`,
        `id` AS `id`,
		'by' AS `adm0`,
        `name` AS `name`,
        `address` AS `address`,
        `place` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `image` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        '' AS `registrant_url`
        FROM `monuments_by_(be-x-old)`;
/* Switzerland in English*/
REPLACE INTO `monuments_all`
SELECT 'ch' AS `country`,
       'en' AS `lang`,
		`kgs_nr` AS `id`,
		'ch' AS `adm0`,
		`name` AS `name`,
		`address` AS `address`,
		`municipality` AS `municipality`,
		`lat` AS `lat`,
		`lon` AS `lon`,
		`image` AS `image`,
		`source` AS `source`,
		`changed` AS `changed`,
		`monument_article` AS `monument_article`,
		'' AS `registrant_url`
		FROM `monuments_ch_(en)`;
/* Switzerland in French */
REPLACE INTO `monuments_all`
SELECT 'ch' AS `country`,
       'fr' AS `lang`,
		`kgs-nr` AS `id`,
		'ch' AS `adm0`,
		`objet` AS `name`,
		`addresse` AS `address`,
		`commune` AS `municipality`,
		`lat` AS `lat`,
		`lon` AS `lon`,
		`photo` AS `image`,
		`source` AS `source`,
		`changed` AS `changed`,
		`monument_article` AS `monument_article`,
		'' AS `registrant_url`
		FROM `monuments_ch_(fr)`;
/* Switzerland in German */
REPLACE INTO `monuments_all`
SELECT 'ch' AS `country`,
       'de' AS `lang`,
		`kgs-nr` AS `id`,
		'ch' AS `adm0`,
		`name` AS `name`,
		`addresse` AS `address`,
		`gemeinde` AS `municipality`,
		`lat` AS `lat`,
		`lon` AS `lon`,
		`foto` AS `image`,
		`source` AS `source`,
		`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        '' AS `registrant_url`
		FROM `monuments_ch_(de)`;
/* Denmark bygninger */
REPLACE INTO `monuments_all`
SELECT 'dk-bygninger' AS `country`,
       'da' AS `lang`,
		CONCAT(`kommunenr`, '-', `ejendomsnr`, '-', `bygningsnr`) AS `id`,
		'dk' AS `adm0`,
		`sagsnavn` AS `name`,
		`adresse` AS `address`,
		`by` AS `municipality`,
		`lat` AS `lat`,
		`lon` AS `lon`,
		`billede` AS `image`,
		`source` AS `source`,
		`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
		FROM `monuments_dk-bygninger_(da)`;
/* Denmark fortidsminder */
REPLACE INTO `monuments_all`
SELECT 'dk-fortidsminder' AS `country`,
       'da' AS `lang`,
		`systemnummer` AS `id`,
		'dk' AS `adm0`,
		`stednavn` AS `name`,
		'' AS `address`,
		'' AS `municipality`,
		`lat` AS `lat`,
		`lon` AS `lon`,
		`billede` AS `image`,
		`source` AS `source`,
		`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
	FROM `monuments_dk-fortidsminder_(da)`;
/* Bergheim, NRW, Germany in German */
REPLACE INTO `monuments_all`
SELECT 'de-nrw-bm' AS `country`, 
    'de' AS `lang`,
	`nummer` AS `id`,
	'de' AS `adm0`,
	'de-nw' AS `adm1`,
    `bezeichnung` AS `name`,
    `adresse` AS `address`,
    `ortsteil` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    `bild` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        REPLACE( `artikel`,  ' ',  '_' ) AS `monument_article`,
        '' AS `registrant_url`
	FROM `monuments_de-nrw-bm_(de)`;
/* Bavaria, Germany in German */
REPLACE INTO `monuments_all`
SELECT 'de-by' AS `country`, 
    'de' AS `lang`,
	`nummer` AS `id`,
	'de' AS `adm0`,
	'de-by' AS `adm1`,
    `bezeichnung` AS `name`,
    `adresse` AS `address`,
    `stadt` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    `bild` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
    REPLACE( `artikel`,  ' ',  '_' ) AS `monument_article`,
    '' AS `registrant_url`
	FROM `monuments_de-by_(de)`;
/* Hessen, Germany in German */
REPLACE INTO `monuments_all`
SELECT 'de-he' AS `country`, 
    'de' AS `lang`,
	`nummer` AS `id`,
	'de' AS `adm0`,
	'de-he' AS `adm1`,
    `bezeichnung` AS `name`,
    `adresse` AS `address`,
    `stadt` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    `bild` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        REPLACE( `artikel`,  ' ',  '_' ) AS `monument_article`,
        `registrant_url` AS `registrant_url`
	FROM `monuments_de-he_(de)`;
/* Cologne, Germany in German */
REPLACE INTO `monuments_all`
SELECT 'de-nrw-k' AS `country`, 
    'de' AS `lang`,
	`nummer_denkmalliste` AS `id`,
	'de' AS `adm0`,
	'de-nw' AS `adm1`,
	'Köln' AS `adm2`,
    `bezeichnung` AS `name`,
    `adresse` AS `address`,
    `ortsteil` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    `bild` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        '' AS `registrant_url`
	FROM `monuments_de-nrw-k_(de)`;
/* Estonia */
REPLACE INTO `monuments_all`
SELECT 'ee' AS `country`,
       'et' AS `lang`,
		`number` AS `id`, 
		'ee' AS `adm0`,
	`nimi` AS `name`,
	`aadress` AS `address`,
	`omavalitsus` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	`pilt` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
	FROM `monuments_ee_(et)`;
/* Spain in Catalan */
REPLACE INTO `monuments_all`
SELECT 'es' AS `country`,
       'ca' AS `lang`,
        `bic` AS `id`,
		'es' AS `adm0`,
        `nomcoor` AS `name`,
        `lloc` AS `address`,
        `municipi` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `imatge` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        '' AS `registrant_url`
        FROM `monuments_es_(ca)`;
/* Spain in Spanish */
REPLACE INTO `monuments_all`
SELECT 'es' AS `country`,
       'es' AS `lang`,
		`bic` AS `id`,
		'es' AS `adm0`,
        `nombrecoor` AS `name`,
        `lugar` AS `address`,
        `municipio` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `imagen` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        '' AS `registrant_url`
        FROM `monuments_es_(es)`
        WHERE tipobic='M';
/* Catalunya in Catalan */
REPLACE INTO `monuments_all`
SELECT 'es-ct' AS `country`,
       'ca' AS `lang`,
        `bic` AS `id`,
		'es' AS `adm0`,
		'es-ct' AS `adm1`,
        `nomcoor` AS `name`,
        `lloc` AS `address`,
        `municipi` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `imatge` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
        FROM `monuments_es-ct_(ca)`;
/* Galicia province (Spain) in Galician */
REPLACE INTO `monuments_all`
SELECT 'es' AS `country`,
       'gl' AS `lang`,
        `bic` AS `id`,
		'es' AS `adm0`,
        `nomeoficial` AS `name`,
        `lugar` AS `address`,
        `concello` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `imaxe` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        '' AS `registrant_url`
        FROM `monuments_es-gl_(gl)`;
/* Valencia in Catalan */
REPLACE INTO `monuments_all`
SELECT 'es-vc' AS `country`,
       'ca' AS `lang`,
       `bic` AS `id`,
	   'es' AS `adm0`,
		'es-vc' AS `adm1`,
        `nomcoor` AS `name`,
        `lloc` AS `address`,
        `municipi` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `imatge` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        '' AS `registrant_url`
        FROM `monuments_es-vc_(ca)`;
/* France in Catalan */
REPLACE INTO `monuments_all`
SELECT 'fr' AS `country`,
       'ca' AS `lang`,
        `id` AS `id`,
		'fr' AS `adm0`,
        `nomcoor` AS `name`,
        `lloc` AS `address`,
        `municipi` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `imatge` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
        FROM `monuments_fr_(ca)`;
/* France in French */
REPLACE INTO `monuments_all`
SELECT 'fr' AS `country`,
       'fr' AS `lang`,
        `notice` AS `id`,
		'fr' AS `adm0`,
        `monument` AS `name`,
        `adresse` AS `address`,
        `commune` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `image` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
        FROM `monuments_fr_(fr)`;
/* Ireland in English */
REPLACE INTO `monuments_all`
SELECT 'ie' AS `country`,
       'en' AS `lang`,
        `number` AS `id`,
		'ie' AS `adm0`,
        `name` AS `name`,
	'' AS `address`,
	`townland` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	`image` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        '' AS `registrant_url`
	FROM `monuments_ie_(en)`;
/* Sardinia in Catalan */
REPLACE INTO `monuments_all`
SELECT 'it-88' AS `country`,
       'ca' AS `lang`,
        `id` AS `id`,
		'it' AS `adm0`,
		'it-88' AS `adm1`,
        `nomcoor` AS `name`,
        `lloc` AS `address`,
        `municipi` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `imatge` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
        FROM `monuments_it-88_(ca)`;
/* South Tyrol in German */
REPLACE INTO `monuments_all`
SELECT 'it-bz' AS `country`, 
       'de' AS `lang`,
        `objektid` AS `id`,
		'it' AS `adm0`,
		'it-32' AS `adm1`,
		'it-bz' AS `adm2`,
        `name` AS `name`,
        `adresse` AS `address`,
        `gemeinde` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `foto` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        REPLACE( `artikel`,  ' ',  '_' ) AS `monument_article`,
        `registrant_url` AS `registrant_url`
        FROM `monuments_it-bz_(de)`;
/* Luxemburg in Luxemburgish */
REPLACE INTO `monuments_all`
SELECT 'lu' AS `country`,
       'lb' AS `lang`,
		`id` AS `id`,
		'lu' AS `adm0`,
        `offiziellen_numm` AS `name`,
        `lag` AS `address`,
        `uertschaft` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `bild` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        '' AS `registrant_url`
        FROM `monuments_lu_(lb)`;
/* Malta in German */
REPLACE INTO `monuments_all`
SELECT 'mt' AS `country`, 
       'de' AS `lang`,
	   `inventarnummer` AS `id`,
	   'mt' AS `adm0`,
       `name-de` AS `name`,
       `adresse` AS `address`,
       `gemeinde` AS `municipality`,
       `lat` AS `lat`,
       `lon` AS `lon`,
       `foto` AS `image`,
       `source` AS `source`,
       `changed` AS `changed`,
        REPLACE( `artikel`,  ' ',  '_' ) AS `monument_article`,
        `registrant_url` AS `registrant_url`
        FROM `monuments_mt_(de)`;		
/* Netherlands */
REPLACE INTO `monuments_all`
SELECT 'nl' AS `country`,
       'nl' AS `lang`,
		`objrijksnr` AS `id`, 
		'nl' AS `adm0`,
		/* provincie AS `adm1`, */
		`woonplaats` AS `adm2`,
	`objectnaam` AS `name`,
	`adres` AS `address`,
	`woonplaats` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	`image` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
	FROM `monuments_nl_(nl)`;
/* Norway */
REPLACE INTO `monuments_all`
SELECT 'no' AS `country`,
       'no' AS `lang`,
		`id` AS `id`,
		'no' AS `adm0`,
	`navn` AS `name`,
	'' AS `address`,
	`kommune` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	`bilde` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
	FROM `monuments_no_(no)`;
/* Poland */
REPLACE INTO `monuments_all`
SELECT 'pl' AS `country`,
       'pl' AS `lang`,
		`numer` AS `id`, 
		'pl' AS `adm0`,
	`nazwa` AS `name`,
	`adres` AS `address`,
	`gmina` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	`zdjecie` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        '' AS `registrant_url`
	FROM `monuments_pl_(pl)`;
/* Portugal */
REPLACE INTO `monuments_all`
SELECT 'pt' AS `country`,
       'pt' AS `lang`,
		`id` AS `id`,
		'pt' AS `adm0`,
	`designacoes` AS `name`,
	'' AS `address`,
	`concelho` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	`imagem` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
	FROM `monuments_pt_(pt)`;
/* Romania */
REPLACE INTO `monuments_all`
SELECT 'ro' AS `country`,
       'ro' AS `lang`,
	`cod` AS `id`, 
	'ro' AS `adm0`,
	`denumire` AS `name`,
	`adresa` AS `address`,
	`localitate` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	`imagine` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        '' AS `registrant_url`
	FROM `monuments_ro_(ro)`;
/* Russia */
REPLACE INTO `monuments_all`
SELECT 'ru' AS `country`,
       'ru' AS `lang`,
	`id` AS `id`, 
	'ru' AS `adm0`,
	`name` AS `name`,
	`address` AS `address`,
	`region` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	`image` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        '' AS `registrant_url`
	FROM `monuments_ru_(ru)`;
/* Scotland */
REPLACE INTO `monuments_all`
SELECT 'sct' AS `country`,
       'en' AS `lang`,
	`hbnum` AS `id`, 
	'gb' AS `adm0`,
	'sct' AS `adm1`,
	`name` AS `name`,
	'' AS `address`,
	`parbur` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	`image` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
	FROM `monuments_sct_(en)`;
/* Sweden */
REPLACE INTO `monuments_all`
SELECT 'se' AS `country`,
       'sv' AS `lang`,
	`bbr` AS `id`,
	'se' AS `adm0`,
	`namn` AS `name`,
	`plats` AS `address`,
	`kommun` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	`bild` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `registrant_url` AS `registrant_url`
	FROM `monuments_se_(sv)`;
/* Slovakia in German */
REPLACE INTO `monuments_all`
SELECT 'sk' AS `country`,
       'de' AS `lang`,
       `objektid` AS `id`,
	   'sk' AS `adm0`,
       `name-de` AS `name`,
       `adresse` AS `address`,
       `obec` AS `municipality`,
       `lat` AS `lat`,
       `lon` AS `lon`,
       `foto` AS `image`,
       `source` AS `source`,
       `changed` AS `changed`,
       REPLACE( `artikel`,  ' ',  '_' ) AS `monument_article`,
       '' AS `registrant_url` /* FIXME: Add this field to source table */
       FROM `monuments_sk_(de)`;
/* Slovakia in Slovak */
REPLACE INTO `monuments_all`
SELECT 'sk' AS `country`,
       'sk' AS `lang`,
       `idobjektu` AS `id`,
	   'sk' AS `adm0`,
       `nazov-sk` AS `name`,
       `adresa` AS `address`,
       `obec` AS `municipality`,
       `lat` AS `lat`,
       `lon` AS `lon`,
       `fotka` AS `image`,
       `source` AS `source`,
       `changed` AS `changed`,
       REPLACE( `clanok`,  ' ',  '_' ) AS `monument_article`,
       '' AS `registrant_url` /* FIXME: Add this field to source table */
       FROM `monuments_sk_(sk)`;
/* United States */
REPLACE INTO `monuments_all`
SELECT 'us' AS `country`,
       'en' AS `lang`,
		`refnum` AS `id`, 
		'us' AS `adm0`,
		/* State  AS `adm1`, */
		`county` AS `adm2`,
	CONCAT('[[', `article`, '|', `name`, ']]') AS `name`,
	CONCAT(`address`, ' ', `city`) AS `address`,
	`county` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	`image` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`,
        REPLACE( `article`,  ' ',  '_' ) AS `monument_article`,
        '' AS `registrant_url`
	FROM `monuments_us_(en)`;
