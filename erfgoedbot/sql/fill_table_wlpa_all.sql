/* Create table for all country tables
 * 
 * Please keep this list sorted by country code!
 *
 * If you change something please test it. 
 *
 * FoP: ''=no info, 'pd'=Public domain or otherwise free (e.g. suitable CC license), 'FoP'=Copyrighted, FoP applies, 'noFoP'=Copyrighted, FoP does not apply
 */

-- Update PHP code when changing this
SET @granularity = 20;

SET NAMES UTF8;

DROP TABLE IF EXISTS `wlpa_all_tmp`;

CREATE TABLE `wlpa_all_tmp` (
  `country` varchar(10) binary NOT NULL DEFAULT '',
  `lang` varchar(10) binary NOT NULL DEFAULT '',
  `id` varchar(25) NOT NULL DEFAULT '0',
  `adm0` varchar(3) binary NOT NULL DEFAULT '',
  `adm1` varchar(7) binary DEFAULT NULL,
  `adm2` varchar(100) DEFAULT NULL,
  `adm3` varchar(150) DEFAULT NULL,
  `adm4` varchar(200) DEFAULT NULL,
  `name` varchar(255) NOT NULL DEFAULT '',
  `address` varchar(255) NOT NULL DEFAULT '',
  `municipality` varchar(255) NOT NULL DEFAULT '',
  `lat` double DEFAULT NULL,
  `lon` double DEFAULT NULL,
  `lat_int` smallint(6) DEFAULT NULL,
  `lon_int` smallint(6) DEFAULT NULL,
  `image` varchar(255) NOT NULL DEFAULT '',
  `commonscat` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `monument_article` varchar(255) NOT NULL DEFAULT '',
  `creator` varchar(255) NOT NULL DEFAULT '',
  `fop` enum('', 'pd', 'FoP', 'noFoP') not null,
  `registrant_url` varchar(255) NOT NULL DEFAULT '',
  `monument_random` mediumint(8) unsigned DEFAULT NULL, 
  PRIMARY KEY (`country`,`lang`,`id`),
  KEY `admin_levels0` (`adm0`, `lang`, `name`, `country`, `id`),
  KEY `admin_levels1` (`adm0`, `adm1`, `lang`, `name`, `country`, `id`),
  KEY `admin_levels2` (`adm2`(32), `lang`, `name`, `country`, `id`),
  KEY `admin_levels3` (`adm3`(32), `lang`, `name`, `country`, `id`),
  KEY `admin_levels4` (`adm4`(32), `lang`, `name`, `country`, `id`),
  KEY `name` (`name`),
  KEY `creator` (`creator`),
  KEY `coord` (`lat_int`,`lon_int`,`lat`),
  KEY `monument_random` (`monument_random`),
  FULLTEXT KEY `name_address_ft` (`name`, `address`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

TRUNCATE TABLE `wlpa_all_tmp`;

/* Catalonia in Catalan */
REPLACE INTO `wlpa_all_tmp` (`country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `creator`, `fop`, `registrant_url` )
SELECT 'es-ct' AS `country`,
       'ca' AS `lang`, 
       `codi` AS `id`,
		'es' AS `adm0`,
		'es-ct' AS `adm1`,
		NULL AS `adm2`,
		'municipi' AS `adm3`,
		NULL AS `adm4`,
        `titol` AS `name`,
        `lloc` AS `address`,
        `municipi` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
		ROUND(`lat` * @granularity) AS `lat_int`,
		ROUND(`lon` * @granularity) AS `lon_int`,
        `imatge` AS `image`,
		`commonscat` AS `commonscat`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `autor` AS `creator`,
        `fop` AS `fop`,
        `registrant_url` AS `registrant_url`
        FROM `wlpa_es-ct_(ca)`;
/* Austria in German */
REPLACE INTO `wlpa_all_tmp` (`country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `creator`, `fop`, `registrant_url` )
SELECT 'at' AS `country`,
       'de' AS `lang`, 
       CONCAT(`Region`, '-', `ID`) AS `id`,
		'at' AS `adm0`,
		NULL AS `adm1`,
		NULL AS `adm2`,
		`Region` AS `adm3`,
		NULL AS `adm4`,
        `Name` AS `name`,
        `Adresse` AS `address`,
        `municipality` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
		ROUND(`lat` * @granularity) AS `lat_int`,
		ROUND(`lon` * @granularity) AS `lon_int`,
        `Foto` AS `image`,
		`Commonscat` AS `commonscat`,
        `source` AS `source`,
        `changed` AS `changed`,
        `Artikel` AS `monument_article`,
        `Kunstler` AS `creator`,
        `fop` AS `fop`,
        `registrant_url` AS `registrant_url`
        FROM `wlpa_at_(de)`;
/* Israel in English */
REPLACE INTO `wlpa_all_tmp` (`country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `creator`, `fop`, `registrant_url` )
SELECT 'il' AS `country`,
       'en' AS `lang`, 
       `id` AS `id`,
		'il' AS `adm0`,
		LOWER(`district`) AS `adm1`,
		`municipality` AS `adm2`,
		NULL AS `adm3`,
		NULL AS `adm4`,
        `title` AS `name`,
        `address` AS `address`,
        `municipality` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
		ROUND(`lat` * @granularity) AS `lat_int`,
		ROUND(`lon` * @granularity) AS `lon_int`,
        `image` AS `image`,
		`commonscat` AS `commonscat`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `artist` AS `creator`,
        `fop` AS `fop`,
        `registrant_url` AS `registrant_url`
        FROM `wlpa_il_(en)`;
/* Finland in Finnish */
REPLACE INTO `wlpa_all_tmp` (`country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `creator`, `fop`, `registrant_url` )
SELECT 'fi' AS `country`,
       'fi' AS `lang`, 
       `id` AS `id`,
		'fi' AS `adm0`,
		LOWER(`maakunta`) AS `adm1`,
		`kunta` AS `adm2`,
		NULL AS `adm3`,
		NULL AS `adm4`,
        `nimi` AS `name`,
        `sijainti` AS `address`,
        `kunta` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
		ROUND(`lat` * @granularity) AS `lat_int`,
		ROUND(`lon` * @granularity) AS `lon_int`,
        `kuva` AS `image`,
		`commonscat` AS `commonscat`,
        `source` AS `source`,
        `changed` AS `changed`,
        `monument_article` AS `monument_article`,
        `tekija` AS `creator`,
        `fop` AS `fop`,
        `url` AS `registrant_url`
        FROM `wlpa_fi_(fi)`;
/* Add next here */

-- UPDATE `wlpa_all_tmp` SET lat_int = ROUND(lat * @granularity), lon_int = ROUND(lon * @granularity);

--  generate random values
UPDATE `wlpa_all_tmp` SET `monument_random`=ROUND(1000000 * RAND() );

DROP TABLE IF EXISTS `wlpa_all`;

ALTER TABLE `wlpa_all_tmp` RENAME TO `wlpa_all`;
