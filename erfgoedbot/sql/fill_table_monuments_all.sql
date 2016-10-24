/* Create table for all country tables
 *
 * Please keep this list sorted by country code!
 *
 * If you change something please test it.
 */

-- Update PHP code when changing this
SET @granularity = 20;

SET NAMES UTF8;

DROP TABLE IF EXISTS `monuments_all_tmp`;

CREATE TABLE `monuments_all_tmp` (
  `country` varchar(10) binary NOT NULL DEFAULT '',
  `lang` varchar(10) binary NOT NULL DEFAULT '',
  `project` varchar(150) NOT NULL DEFAULT 'wikipedia',
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
  `wd_item` varchar(255) DEFAULT NULL,
  `commonscat` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(510) NOT NULL DEFAULT '',
  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `monument_article` varchar(255) NOT NULL DEFAULT '',
  `registrant_url` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`country`,`lang`,`id`),
  KEY `admin_levels0` (`adm0`, `lang`, `name`, `country`, `id`),
  KEY `admin_levels1` (`adm0`, `adm1`, `lang`, `name`, `country`, `id`),
  KEY `admin_levels2` (`adm2`(32), `lang`, `name`, `country`, `id`),
  KEY `admin_levels3` (`adm3`(32), `lang`, `name`, `country`, `id`),
  KEY `admin_levels4` (`adm4`(32), `lang`, `name`, `country`, `id`),
  KEY `name` (`name`),
  KEY `coord` (`lat_int`,`lon_int`,`lat`),
  FULLTEXT KEY `name_address_ft` (`name`, `address`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

TRUNCATE TABLE `monuments_all_tmp`;

/* Andorra in Catalan */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`, `wd_item`
  ) SELECT
    'ad' AS `country`,
    'ca' AS `lang`,
    `id` AS `id`,
    'ad' AS `adm0`,
    LOWER(`region`) AS `adm1`,
    NULL AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `nomcoor` AS `name`,
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
    `registrant_url` AS `registrant_url`,
    `wd_item` AS `wd_item`
    FROM `monuments_ad_(ca)`;

/* Albania in Albanian */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'al' AS `country`,
    'sq' AS `lang`,
    `idno` AS `id`,
    'al' AS `adm0`,
    NULL AS `adm1`,
    NULL AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
    `place` AS `address`,
    `municipality` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    '' AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_al_(sq)`;

/* Armenia in Armenian */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'am' AS `country`,
    'hy' AS `lang`,
    `id` AS `id`,
    'am' AS `adm0`,
    LOWER(`prov_iso`) AS `adm1`,
    `municipality` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `description` AS `name`,
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
    `registrant_url` AS `registrant_url`
    FROM `monuments_am_(hy)`;

/* Antarctica in English */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'aq' AS `country`,
    'en' AS `lang`,
    CONCAT(`type`, '-', `number`) AS `id`,
    'aq' AS `adm0`,
    NULL AS `adm1`,
    NULL AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
    `description` AS `address`,
    `proponent` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_aq_(en)`;

/* Argentina in Spanish */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'ar' AS `country`,
    'es' AS `lang`,
    `id` AS `id`,
    'ar' AS `adm0`,
    LOWER(`prov-iso`) AS `adm1`,
    NULL AS `adm2`,
    `municipio` AS `adm3`,
    `localidad` AS `adm4`,
    `monumento` AS `name`,
    `direccion` AS `address`,
    `municipio` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `imagen` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    CONCAT('http://www.monumentosysitios.gov.ar/ficha.php?idMonumento=', id) AS `registrant_url`
    FROM `monuments_ar_(es)`;

/* Austria in German */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'at' AS `country`,
    'de' AS `lang`,
    `objektid` AS `id`,
    'at' AS `adm0`,
    LOWER(`region-iso`) AS `adm1`,
    `bezirk` AS `adm2`,
    `gemeinde` AS `adm3`,
    `katastralgemeinde` AS `adm4`,
    `name` AS `name`,
    `adresse` AS `address`,
    `gemeinde` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `foto` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    REPLACE( `artikel`, ' ', '_' ) AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_at_(de)`;

/* Azerbaijan in Azerbaijani */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'az' AS `country`,
    'az' AS `lang`,
    `id` AS `id`,
    'az' AS `adm0`,
    LOWER(`ray-iso`) AS `adm1`,
    `municipality` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
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
    `registrant_url` AS `registrant_url`
    FROM `monuments_az_(az)`;

/* Brussels in Dutch */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'be-bru' AS `country`,
    'nl' AS `lang`,
    `code` AS `id`,
    'be' AS `adm0`,
    'be-bru' AS `adm1`,
    `plaats` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `omschrijving` AS `name`,
    `adres` AS `address`,
    `plaats` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_be-bru_(nl)`;

/* Vlaanderen in English */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'be-vlg' AS `country`,
    'en' AS `lang`,
    `id` AS `id`,
    'be' AS `adm0`,
    'be-vlg' AS `adm1`,
    LOWER(`prov-iso`) AS `adm2`,
    `commune` AS `adm3`,
    NULL AS `adm4`,
    `descr_en` AS `name`,
    `address` AS `address`,
    `town` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_be-vlg_(en)`;

/* Vlaanderen in French */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'be-vlg' AS `country`,
    'fr' AS `lang`,
    `id` AS `id`,
    'be' AS `adm0`,
    'be-vlg' AS `adm1`,
    LOWER(`prov-iso`) AS `adm2`,
    `commune` AS `adm3`,
    NULL AS `adm4`,
    `nom_objet` AS `name`,
    `adresse` AS `address`,
    `commune` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_be-vlg_(fr)`;

/* Vlaanderen in Dutch */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'be-vlg' AS `country`,
    'nl' AS `lang`,
    `id` AS `id`,
    'be' AS `adm0`,
    'be-vlg' AS `adm1`,
    LOWER(`prov-iso`) AS `adm2`,
    `gemeente` AS `adm3`,
    NULL AS `adm4`,
    `objectnaam` AS `name`,
    `adres` AS `address`,
    `gemeente` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_be-vlg_(nl)`;

/* Wallonia in English */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'be-wal' AS `country`,
    'en' AS `lang`,
    CONCAT(`niscode`, '-', `objcode`) AS `id`,
    'be' AS `adm0`,
    'be-wal' AS `adm1`,
    LOWER(`prov-iso`) AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `descr_en` AS `name`,
    `address` AS `address`,
    `section` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_be-wal_(en)`;

/* Wallonie in French */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'be-wal' AS `country`,
    'fr' AS `lang`,
    CONCAT(`id_commune`, '-', `clt-pex`, '-', `id_objet`) AS `id`,
    'be' AS `adm0`,
    'be-wal' AS `adm1`,
    LOWER(`prov-iso`) AS `adm2`,
    `commune` AS `adm3`,
    NULL AS `adm4`,
    `nom_objet` AS `name`,
    `adresse` AS `address`,
    `commune` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_be-wal_(fr)`;

/* Wallonie in Dutch */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'be-wal' AS `country`,
    'nl' AS `lang`,
    CONCAT(`niscode`, '-', `objcode`) AS `id`,
    'be' AS `adm0`,
    'be-wal' AS `adm1`,
    LOWER(`prov-iso`) AS `adm2`,
    `gemeente` AS `adm3`,
    NULL AS `adm4`,
    `descr_nl` AS `name`,
    `adres` AS `address`,
    `gemeente` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_be-wal_(nl)`;

/* Bolivia in Spanish */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'bo' AS `country`,
    'es' AS `lang`,
    `id` AS `id`,
    'bo' AS `adm0`,
    LOWER(`iso`) AS `adm1`,
    `municipio` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `monumento` AS `name`,
    `direccion` AS `address`,
    `municipio` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monumento_enlace` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_bo_(es)`;

/* Belarus in Belarusian */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'by' AS `country`,
    'be-tarask' AS `lang`,
    `id` AS `id`,
    'by' AS `adm0`,
    LOWER(`oblast-iso`) AS `adm1`,
    `rajon` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
    `address` AS `address`,
    `place` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_by_(be-tarask)`;

/*  Canada in English 3 times because of the 3 levels in one source table */
/*  Canada in English (Federal) */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`, `wd_item`
  ) SELECT
    'ca' AS `country`,
    'en' AS `lang`,
    `idf` AS `id`,
    'ca' AS `adm0`,
    LOWER(`prov_iso`) AS `adm1`,
    `municipality` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
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
    `registrant_url` AS `registrant_url`,
    `wd_item` AS `wd_item`
    FROM `monuments_ca_(en)`
    WHERE NOT (`idf` IS NULL OR `idf`=''); -- Federal

/*  Canada in English (Provincial) */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`, `wd_item`
  ) SELECT
    'ca' AS `country`,
    'en' AS `lang`,
    `idp` AS `id`,
    'ca' AS `adm0`,
    LOWER(`prov_iso`) AS `adm1`,
    `municipality` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
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
    `registrant_url` AS `registrant_url`,
    `wd_item` AS `wd_item`
    FROM `monuments_ca_(en)`
    WHERE (`idf` IS NULL OR `idf`='') AND NOT (`idp` IS NULL OR `idp`=''); -- Provincial

/*  Canada in English (Municipal) */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`, `wd_item`
  ) SELECT
    'ca' AS `country`,
    'en' AS `lang`,
    `idm` AS `id`,
    'ca' AS `adm0`,
    LOWER(`prov_iso`) AS `adm1`,
    `municipality` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
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
    `registrant_url` AS `registrant_url`,
    `wd_item` AS `wd_item`
    FROM `monuments_ca_(en)`
    WHERE (`idf` IS NULL OR `idf`='') AND (`idp` IS NULL OR `idp`='') AND NOT (`idm` IS NULL OR `idm`=''); -- Municipal

/*  Canada in French */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'ca' AS `country`,
    'fr' AS `lang`,
    `numero` AS `id`,
    'ca' AS `adm0`,
    LOWER(`prov_iso`) AS `adm1`,
    `municipalite` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `lieu` AS `name`,
    `adresse` AS `address`,
    `municipalite` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_ca_(fr)`;

/* Switzerland in English */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'ch-old' AS `country`,
    'en' AS `lang`,
    `kgs_nr` AS `id`,
    'ch' AS `adm0`,
    LOWER(`region-iso`) AS `adm1`,
    NULL AS `adm2`,
    `municipality` AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
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
    '' AS `registrant_url`
    FROM `monuments-old_ch_(en)`;

/* Switzerland in Italian */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'ch' AS `country`,
    'it' AS `lang`,
    `no_pbc` AS `id`,
    'ch' AS `adm0`,
    LOWER(`region-iso`) AS `adm1`,
    NULL AS `adm2`,
    `comune` AS `adm3`,
    NULL AS `adm4`,
    `oggetto` AS `name`,
    `indirizzo` AS `address`,
    `comune` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `foto` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_ch_(it)`;

/* Switzerland in French */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'ch' AS `country`,
    'fr' AS `lang`,
    `no pbc` AS `id`,
    'ch' AS `adm0`,
    LOWER(`region-iso`) AS `adm1`,
    NULL AS `adm2`,
    `commune` AS `adm3`,
    NULL AS `adm4`,
    `objet` AS `name`,
    `addresse` AS `address`,
    `commune` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `photo` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_ch_(fr)`;

/* Switzerland in German #1 */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'ch' AS `country`,
    'de' AS `lang`,
    `kgs-nr` AS `id`,
    'ch' AS `adm0`,
    LOWER(`region-iso`) AS `adm1`,
    NULL AS `adm2`,
    `gemeinde` AS `adm3`,
    NULL AS `adm4`,
    `objekt` AS `name`,
    `adresse` AS `address`,
    `gemeinde` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `foto` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_ch_(de)`;

/* Switzerland in German #2 */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'ch' AS `country`,
    'de' AS `lang`,
    `id` AS `id`,
    'ch' AS `adm0`,
    LOWER(`region-iso`) AS `adm1`,
    NULL AS `adm2`,
    `gemeinde` AS `adm3`,
    NULL AS `adm4`,
    `objekt` AS `name`,
    `adresse` AS `address`,
    `gemeinde` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `foto` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_ch2_(de)`;

/* Switzerland in German #3 */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'ch' AS `country`,
    'de' AS `lang`,
    `id` AS `id`,
    'ch' AS `adm0`,
    LOWER(`region-iso`) AS `adm1`,
    NULL AS `adm2`,
    `gemeinde` AS `adm3`,
    NULL AS `adm4`,
    `objekt` AS `name`,
    `adresse` AS `address`,
    `gemeinde` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `foto` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_ch3_(de)`;

/* Cameroun in French */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'cm' AS `country`,
    'fr' AS `lang`,
    `id` AS `id`,
    'cm' AS `adm0`,
    LOWER(`region_iso`) AS `adm1`,
    NULL AS `adm2`,
    NULL AS `adm3`,
    `ville` AS `adm4`,
    `nom` AS `name`,
    '' AS `address`,
    `ville` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_cm_(fr)`;

/* China in English */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'cn' AS `country`,
    'en' AS `lang`,
    `designation` AS `id`,
    'cn' AS `adm0`,
    LOWER(`prov_iso`) AS `adm1`,
    `location` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `site` AS `name`,
    `location` AS `address`,
    `province` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_cn_(en)`;

/* Czech Republic in Czech language */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'cz' AS `country`,
    'cs' AS `lang`,
    `id_objektu` AS `id`,
    'cz' AS `adm0`,
    LOWER(`kraj-iso`) AS `adm1`,
    LOWER(`okres-iso`) AS `adm2`,
    `municipality` AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
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
    CONCAT('http://monumnet.npu.cz/pamfond/list.php?hledani=1&CiRejst=',`id_objektu`) AS `registrant_url`
    FROM `monuments_cz_(cs)`;

/* Chile in Spanish */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'cl' AS `country`,
    'es' AS `lang`,
    `id` AS `id`,
    'cl' AS `adm0`,
    LOWER(`ISO`) AS `adm1`,
    `comuna` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `monumento` AS `name`,
    `direccion` AS `address`,
    `comuna` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `imagen` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monumento_enlace` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_cl_(es)`;

/* Colombia in Spanish */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'co' AS `country`,
    'es' AS `lang`,
    `id` AS `id`,
    'co' AS `adm0`,
    LOWER(`iso`) AS `adm1`,
    `municipio` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `monumento` AS `name`,
    `direccion` AS `address`,
    `municipio` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `imagen` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_co_(es)`;

/* Denmark (bygninger) in Danish */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'dk-bygninger' AS `country`,
    'da' AS `lang`,
    CONCAT(`kommunenr`, '-', `ejendomsnr`, '-', `bygningsnr`) AS `id`,
    'dk' AS `adm0`,
    LOWER(`region-iso`) AS `adm1`,
    `kommune` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `sagsnavn` AS `name`,
    `adresse` AS `address`,
    `by` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `billede` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_dk-bygninger_(da)`;

/* Denmark (fortidsminder) in Danish */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'dk-fortidsminder' AS `country`,
    'da' AS `lang`,
    `systemnummer` AS `id`,
    'dk' AS `adm0`,
    LOWER(`region-iso`) AS `adm1`,
    `kommune` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `stednavn` AS `name`,
    '' AS `address`,
    '' AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `billede` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_dk-fortidsminder_(da)`;

/* Bavaria, Germany in German */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'de-by' AS `country`,
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
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `bild` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    REPLACE( `artikel`, ' ', '_' ) AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_de-by_(de)`;

/* Hessen, Germany in German */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`, `wd_item`
  ) SELECT
    'de-he' AS `country`,
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
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `bild` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    REPLACE( `artikel`, ' ', '_' ) AS `monument_article`,
    `registrant_url` AS `registrant_url`,
     `wd_item` AS `wd_item`
    FROM `monuments_de-he_(de)`;

/* Bergheim, NRW, Germany in German */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'de-nrw-bm' AS `country`,
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
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `bild` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    REPLACE( `artikel`, ' ', '_' ) AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_de-nrw-bm_(de)`;

/* Cologne, NRW, Germany in German */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'de-nrw-k' AS `country`,
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
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `bild` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_de-nrw-k_(de)`;

/* Algeria in Arabic */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'dz' AS `country`,
    'ar' AS `lang`,
    `id` AS `id`,
    'dz' AS `adm0`,
    `prov-iso` AS `adm1`,
    `city` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
    '' AS `address`,
    `prov-iso` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_dz_(ar)`;

/* Estonia in Estonian */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'ee' AS `country`,
    'et' AS `lang`,
    `number` AS `id`,
    'ee' AS `adm0`,
    LOWER(`region-iso`) AS `adm1`,
    `omavalitsus` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `nimi` AS `name`,
    `aadress` AS `address`,
    `omavalitsus` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `pilt` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_ee_(et)`;

/* Spain in Catalan */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`, `wd_item`
  ) SELECT
    'es' AS `country`,
    'ca' AS `lang`,
    `bic` AS `id`,
    'es' AS `adm0`,
    LOWER(`CCAA_iso`) AS `adm1`,
    LOWER(`provincia_iso`) AS `adm2`,
    `municipi` AS `adm3`,
    NULL AS `adm4`,
    `nomcoor` AS `name`,
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
    '' AS `registrant_url`,
    `wd_item` AS `wd_item`
    FROM `monuments_es_(ca)`;

/* Spain in Spanish */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'es' AS `country`,
    'es' AS `lang`,
    `bic` AS `id`,
    'es' AS `adm0`,
    LOWER(`CCAA_iso`) AS `adm1`,
    LOWER(`provincia_iso`) AS `adm2`,
    `municipio` AS `adm3`,
    NULL AS `adm4`,
    `nombrecoor` AS `name`,
    `lugar` AS `address`,
    `municipio` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `imagen` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_es_(es)`;

/* Catalunya in Catalan */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`, `wd_item`
  ) SELECT
    'es' AS `country`,
    'ca' AS `lang`,
    `bic` AS `id`,
    'es' AS `adm0`,
    LOWER(`CCAA_iso`) AS `adm1`,
    LOWER(`provincia_iso`) AS `adm2`,
    `municipi` AS `adm3`,
    NULL AS `adm4`,
    `nomcoor` AS `name`,
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
    `registrant_url` AS `registrant_url`,
    `wd_item` AS `wd_item`
    FROM `monuments_es-ct_(ca)`;

/* Galicia province (Spain) in Galician */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'es' AS `country`,
    'gl' AS `lang`,
    `bic` AS `id`,
    'es' AS `adm0`,
    'es-ga' AS `adm1`,
    `provincia_iso` AS `adm2`,
    `concello` AS `adm3`,
    NULL AS `adm4`,
    `nomeoficial` AS `name`,
    `lugar` AS `address`,
    `concello` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `imaxe` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_es-gl_(gl)`;

/* Valencia in Catalan */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`, `wd_item`
  ) SELECT
    'es' AS `country`,
    'ca' AS `lang`,
    `bic` AS `id`,
    'es' AS `adm0`,
    LOWER(`CCAA_iso`) AS `adm1`,
    LOWER(`provincia_iso`) AS `adm2`,
    `municipi` AS `adm3`,
    NULL AS `adm4`,
    `nomcoor` AS `name`,
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
    '' AS `registrant_url`,
     `wd_item` AS `wd_item`
    FROM `monuments_es-vc_(ca)`;

/* France in Catalan */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`, `wd_item`
  ) SELECT
    'fr' AS `country`,
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
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `imatge` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`,
    `wd_item` AS `wd_item`
    FROM `monuments_fr_(ca)`;

/* France in French */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'fr' AS `country`,
    'fr' AS `lang`,
    `notice` AS `id`,
    'fr' AS `adm0`,
    LOWER(`region_iso`) AS `adm1`,
    LOWER(`departement_iso`) AS `adm2`,
    `commune` AS `adm3`,
    NULL AS `adm4`,
    `monument` AS `name`,
    `adresse` AS `address`,
    `commune` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_fr_(fr)`;

/* France (object monuments) in French */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `registrant_url`
  ) SELECT
    'fr-object' AS `country`,
    'fr' AS `lang`,
    `palissy` AS `id`,
    'fr' AS `adm0`,
    LOWER(`region_iso`) AS `adm1`,
    LOWER(`departement_iso`) AS `adm2`,
    `commune` AS `adm3`,
    NULL AS `adm4`,
    `commune` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_fr-object_(fr)`;

/* United Kingdom: England in English */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`, `wd_item`
  ) SELECT
    'gb-eng' AS `country`,
    'en' AS `lang`,
    `uid` AS `id`,
    'gb' AS `adm0`,
    'eng' AS `adm1`,
    LOWER(`subdivision_iso`) AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
    `location` AS `address`,
    LOWER(`subdivision_iso`) AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`,
    `wd_item` AS `wd_item`
    FROM `monuments_gb-eng_(en)`;

/* United Kingdom: Northern Ireland in English */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'gb-nir' AS `country`,
    'en' AS `lang`,
    `hb` AS `id`,
    'gb' AS `adm0`,
    'nir' AS `adm1`,
    LOWER(`subdivision_iso`) AS `adm2`,
    `authority` AS `adm3`,
    NULL AS `adm4`,
    `address` AS `name`,
    `address` AS `address`,
    LOWER(`subdivision_iso`) AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_gb-nir_(en)`;

/* United Kingdom: Scotland in English */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'gb-sct' AS `country`,
    'en' AS `lang`,
    `hb` AS `id`,
    'gb' AS `adm0`,
    'sct' AS `adm1`,
    LOWER(`council_iso`) AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
    `location` AS `address`,
    `council_area` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_gb-sct_(en)`;

/* United Kingdom: Wales in English */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'gb-wls' AS `country`,
    'en' AS `lang`,
    `hb` AS `id`,
    'gb' AS `adm0`,
    'wls' AS `adm1`,
    LOWER(`subdivision_iso`) AS `adm2`,
    `location` AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
    `notes` AS `address`,
    LOWER(`subdivision_iso`) AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_gb-wls_(en)`;

/* Georgia in Georgian */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'ge' AS `country`,
    'ka' AS `lang`,
    `id` AS `id`,
    'ge' AS `adm0`,
    LOWER(`region_iso`) AS `adm1`,
    `municipality` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
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
    '' AS `monument_article`, -- Not available
    `registrant_url` AS `registrant_url`
    FROM `monuments_ge_(ka)`;

/* Ghana in English */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'gh' AS `country`,
    'en' AS `lang`,
    `id` AS `id`,
    'gh' AS `adm0`,
    LOWER(`region_iso`) AS `adm1`,
    `location` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
    NULL AS `address`,
    `location` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url` -- Not available
    FROM `monuments_gh_(en)`;

/* Hong Kong (declared monuments) in English */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'hk' AS `country`,
    'en' AS `lang`,
    `id` AS `id`,
    'hk' AS `adm0`,
    NULL AS `adm1`,
    `region` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
    `location` AS `address`,
    'Hong Kong' AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    NULL AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url` -- Not available
    FROM `monuments_hk_(en)`;

/* Hungary in Hungarian */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'hu' AS `country`,
    'hu' AS `lang`,
    `id` AS `id`,
    'hu' AS `adm0`,
    `county_iso` AS `adm1`,
    `regio` AS `adm2`,
    `town` AS `adm3`,
    `district` AS `adm4`,
    `name` AS `name`,
    `address` AS `address`,
    `regio` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_hu_(hu)`;

/* India in English */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'in' AS `country`,
    'en' AS `lang`,
    `number` AS `id`,
    'in' AS `adm0`,
    LOWER(`state_iso`) AS `adm1`,
    `circle` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `description` AS `name`,
    `address` AS `address`,
    `location` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    NULL AS `monument_article`,
    NULL AS `registrant_url`
    FROM `monuments_in_(en)`;

/* Israel in Hebrew */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'il' AS `country`,
    'he' AS `lang`,
    `id` AS `id`,
    'il' AS `adm0`,
    LOWER(`district-iso`) AS `adm1`,
    `municipality` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
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
    `article` AS `monument_article`,
    NULL AS `registrant_url`
    FROM `monuments_il_(he)`;

/* Ireland in English */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'ie' AS `country`,
    'en' AS `lang`,
    `number` AS `id`,
    'ie' AS `adm0`,
    LOWER(`region-iso`) AS `adm1`,
    NULL AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
    '' AS `address`,
    `townland` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_ie_(en)`;

/* Iran in Farsi */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'ir' AS `country`,
    'fa' AS `lang`,
    `id` AS `id`,
    'ir' AS `adm0`,
    LOWER(`ISO`) AS `adm1`,
    NULL AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
    `address` AS `address`,
    `city` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_ir_(fa)`;

/* Italy in Italian */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'it' AS `country`,
    'it' AS `lang`,
    `id` AS `id`,
    'it' AS `adm0`,
    LOWER(`regione-iso`) AS `adm1`,
    LOWER(`prov-iso`) AS `adm2`,
    `comune` AS `adm3`,
    NULL AS `adm4`,
    `monumento` AS `name`,
    `indirizzo` AS `address`,
    `comune` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `immagine` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `wikivoce` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_it_(it)`;

/* Sardinia in Catalan */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'it-88' AS `country`,
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
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `imatge` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_it-88_(ca)`;

/* South Tyrol in German */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'it-bz' AS `country`,
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
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `foto` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    REPLACE( `artikel`, ' ', '_' ) AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_it-bz_(de)`;

/* Jordan in Arabic */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'jo' AS `country`,
    'ar' AS `lang`,
    `id` AS `id`,
    'jo' AS `adm0`,
    LOWER(`prov-iso`) AS `adm1`,
    NULL AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
    `position` AS `address`,
    LOWER(`prov-iso`) AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_jo_(ar)`;

/* Japan in English */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'jp-nhs' AS `country`,
    'en' AS `lang`,
    `id` AS `id`,
    'jp' AS `adm0`,
    LOWER(`prefecture_iso`) AS `adm1`,
    `municipality` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
    '' AS `address`,
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
    `registrant_url` AS `registrant_url`
    FROM `monuments_jp-nhs_(en)`;

/* Kenya in English */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'ke' AS `country`,
    'den' AS `lang`,
    `id` AS `id`,
    'ke' AS `adm0`,
    NULL AS `adm1`,
    NULL AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
    `address` AS `address`,
    `county` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_ke_(en)`;

/* Luxemburg in Luxemburgish */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'lu' AS `country`,
    'lb' AS `lang`,
    `id` AS `id`,
    'lu' AS `adm0`,
    LOWER(`region-iso`) AS `adm1`,
    NULL AS `adm2`,
    `uertschaft` AS `adm3`,
    NULL AS `adm4`,
    `offiziellen_numm` AS `name`,
    `lag` AS `address`,
    `uertschaft` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `bild` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_lu_(lb)`;

/* Malta in German */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'mt' AS `country`,
    'de' AS `lang`,
    `inventarnummer` AS `id`,
    'mt' AS `adm0`,
    LOWER(`region-iso`) AS `adm1`,
    `gemeinde` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `name-de` AS `name`,
    `adresse` AS `address`,
    `gemeinde` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `foto` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    REPLACE( `artikel`, ' ', '_' ) AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_mt_(de)`;

/* Mexico in Spanish */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'mx' AS `country`,
    'es' AS `lang`,
    `id` AS `id`,
    'mx' AS `adm0`,
    LOWER(`iso`) AS `adm1`,
    `municipio` AS `adm2`,
    `localidad` AS `adm3`,
    NULL AS `adm4`,
    `monumento` AS `name`,
    `direccion` AS `address`,
    `municipio` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `imagen` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_mx_(es)`;

/* Nigeria in English */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`, `wd_item`
  ) SELECT
    'ng' AS `country`,
    'en' AS `lang`,
    `wd_item` AS `id`,
    'ng' AS `adm0`,
    NULL AS `adm1`,
    NULL AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
    `place` AS `address`,
    `state` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url`,
    `wd_item` AS `wd_item`
    FROM `monuments_ng_(en)`;

/* Netherlands in Dutch */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`, `wd_item`
  ) SELECT
    'nl' AS `country`,
    'nl' AS `lang`,
    `objrijksnr` AS `id`,
    'nl' AS `adm0`,
    LOWER(`prov-iso`) AS `adm1`,
    `woonplaats` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `objectnaam` AS `name`,
    `adres` AS `address`,
    `woonplaats` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`,
    `wd_item` AS `wd_item`
    FROM `monuments_nl_(nl)`;

/* Aruba in English */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'nl-aw' AS `country`,
    'en' AS `lang`,
    `objcode` AS `id`,
    'nl' AS `adm0`,
    'nl-aw' AS `adm1`,
    `town` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `descr_en` AS `name`,
    `address` AS `address`,
    `town` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_nl-aw_(en)`;

/* Aruba in Dutch */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`, `wd_item`
  ) SELECT
    'nl-aw' AS `country`,
    'nl' AS `lang`,
    `objectnr` AS `id`,
    'nl' AS `adm0`,
    'nl-aw' AS `adm1`,
    `plaats` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `omschrijving` AS `name`,
    `adres` AS `address`,
    `plaats` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`,
    `wd_item` AS `wd_item`
    FROM `monuments_nl-aw_(nl)`;

/* Netherlands (gemeentelijke monumenten) in Dutch */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`, `wd_item`
  ) SELECT
    'nl-gem' AS `country`,
    'nl' AS `lang`,
    CONCAT(`gemcode`, '/', `objnr`) AS `id`,
    'nl' AS `adm0`,
    LOWER(`prov-iso`) AS `adm1`,
    `gemeente` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `object` AS `name`,
    `adres` AS `address`,
    `gemeente` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url`,
    `wd_item` AS `wd_item`
    FROM `monuments_nl-gem_(nl)`;

/* Netherlands (provinciale monumenten) in Dutch */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`, `wd_item`
  ) SELECT
    'nl-prov' AS `country`,
    'nl' AS `lang`,
    `objnr` AS `id`,
    'nl' AS `adm0`,
    LOWER(`prov-iso`) AS `adm1`,
    `gemeente` AS `adm2`,
    `plaats` AS `adm3`,
    NULL AS `adm4`,
    `object` AS `name`,
    `adres` AS `address`,
    `gemeente` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`,
    `wd_item` AS `wd_item`
    FROM `monuments_nl-prov_(nl)`;

/* Norway in Norwegian */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'no' AS `country`,
    'no' AS `lang`,
    `id` AS `id`,
    'no' AS `adm0`,
    LOWER(`county_iso`) AS `adm1`,
    `kommune` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `navn` AS `name`,
    '' AS `address`,
    `kommune` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `bilde` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_no_(no)`;

/* Nepal in English */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'np' AS `country`,
    'en' AS `lang`,
    `number` AS `id`,
    'np' AS `adm0`,
    LOWER(`region_iso`) AS `adm1`,
    LOWER(`zone_iso`) AS `adm2`,
    `district` AS `adm3`,
    NULL AS `adm4`,
    `description` AS `name`,
    `address` AS `address`,
    `district` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_np_(en)`;

/* Panamá in Spanish */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'pa' AS `country`,
    'es' AS `lang`,
    `id` AS `id`,
    'pa' AS `adm0`,
    LOWER(`prov-iso`) AS `adm1`,
    NULL AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `nombre` AS `name`,
    `direccion` AS `address`,
    `provincia` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `imagen` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `articulo` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_pa_(es)`;

/* Philippines in English */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'ph' AS `country`,
    'en' AS `lang`,
    `cp-wmph-id` AS `id`,
    'ph' AS `adm0`,
    LOWER(`region-iso`) AS `adm1`,
    `province` AS `adm2`, /* province-iso is still empty, could be used later */
    `location` AS `adm3`,
    NULL AS `adm4`,
    `site_name` AS `name`,
    `address` AS `address`,
    `location` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    NULL AS `monument_article`,
    NULL AS `registrant_url`
    FROM `monuments_ph_(en)`;

/* Pakistan in English */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'pk' AS `country`,
    'en' AS `lang`,
    `number` AS `id`,
    'pk' AS `adm0`,
    LOWER(`prov_iso`) AS `adm1`,
    `district` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `description` AS `name`,
    `address` AS `address`,
    `district` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_pk_(en)`;

/* Poland in Polish */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'pl' AS `country`,
    'pl' AS `lang`,
    `id` AS `id`,
    'pl' AS `adm0`,
    LOWER(`prov-iso`) AS `adm1`,
    `powiat` AS `adm2`,
    `gmina` AS `adm3`,
    `miejscowosc` AS `adm4`,
    `nazwa` AS `name`,
    `adres` AS `address`,
    `gmina` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `zdjecie` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_pl_(pl)`;

/* Portugal in Portuguese */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'pt' AS `country`,
    'pt' AS `lang`,
    `id` AS `id`,
    'pt' AS `adm0`,
    LOWER(`region-iso`) AS `adm1`,
    `concelho` AS `adm2`,
    `freguesia` AS `adm3`,
    NULL AS `adm4`,
    `designacoes` AS `name`,
    '' AS `address`,
    `concelho` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `imagem` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_pt_(pt)`;

/* Romania in Romanian */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'ro' AS `country`,
    'ro' AS `lang`,
    `cod` AS `id`,
    'ro' AS `adm0`,
    LOWER(`judetul-iso`) AS `adm1`,
    `localitate` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `denumire` AS `name`,
    `adresa` AS `address`,
    `localitate` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `imagine` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_ro_(ro)`;

/* Serbia in Serbian */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'rs' AS `country`,
    'sr' AS `lang`,
    `id` AS `id`,
    'rs' AS `adm0`,
    LOWER(`iso_okrug`) AS `adm1`,
    `district` AS `adm2`,
    `city` AS `adm3`,
    `city_district` AS `adm4`,
    `name` AS `name`,
    `address` AS `address`,
    `city` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_rs_(sr)`;

/* Russia in Russian */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `project`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`, `wd_item`
  ) SELECT
    'ru' AS `country`,
    'ru' AS `lang`,
    'wikivoyage' AS `project`,
    `id` AS `id`,
    'ru' AS `adm0`,
    LOWER(`region_iso`) AS `adm1`,
    `district` AS `adm2`,
    `city` AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
    `address` AS `address`,
    `city` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`,
    `wd_item` AS `wd_item`
    FROM `monuments_ru_(ru)`;

/* Sweden (BBR Monuments) in Swedish */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'se-bbr' AS `country`,
    'sv' AS `lang`,
    `bbr` AS `id`,
    'se' AS `adm0`,
    LOWER(`region-iso`) AS `adm1`,
    `kommun` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `namn` AS `name`,
    `plats` AS `address`,
    `kommun` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `bild` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_se-bbr_(sv)`;

/* Sweden (Fornminne Monuments) in Swedish */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'se-fornmin' AS `country`,
    'sv' AS `lang`,
    `id` AS `id`,
    'se' AS `adm0`,
    LOWER(`region-iso`) AS `adm1`,
    `kommun` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    CONCAT(`namn`, ' (', `raa-nr`, ', ', `typ`, ')' ) AS `name`,
    `plats` AS `address`,
    `kommun` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `bild` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `artikel` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_se-fornmin_(sv)`;

/* Sweden (Listed historical ships) in Swedish */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'se-ship' AS `country`,
    'sv' AS `lang`,
    `signal` AS `id`,
    'se' AS `adm0`,
    NULL AS `adm1`,
    NULL AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `namn` AS `name`,
    `hemmahamn` AS `address`,
    '' AS `municipality`,
    NULL AS `lat`,
    NULL AS `lon`,
    NULL AS `lat_int`,
    NULL AS `lon_int`,
    `bild` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `artikel` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_se-ship_(sv)`;

/* Sweden (Working Life Museums) in Swedish */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'se-arbetsl' AS `country`,
    'sv' AS `lang`,
    `id` AS `id`,
    'se' AS `adm0`,
    LOWER(`region-iso`) AS `adm1`,
    `kommun` AS `adm2`,
    `ort` AS `adm3`,
    NULL AS `adm4`,
    `namn` AS `name`,
    `adress` AS `address`,
    `kommun` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `bild` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url` /* FIXME: Add this field to source table */
    FROM `monuments_se-arbetsl_(sv)`;

/* Slovakia in German */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'sk' AS `country`,
    'de' AS `lang`,
    `objektid` AS `id`,
    'sk' AS `adm0`,
    LOWER(`region-iso`) AS `adm1`,
    `okres` AS `adm2`,
    `obec` AS `adm3`,
    `katastralgemeinde` AS `adm4`,
    `name-de` AS `name`,
    `adresse` AS `address`,
    `obec` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `foto` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    REPLACE( `artikel`, ' ', '_' ) AS `monument_article`,
    '' AS `registrant_url` /* FIXME: Add this field to source table */
    FROM `monuments_sk_(de)`;

/* Slovakia in Slovak */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'sk' AS `country`,
    'sk' AS `lang`,
    `idobjektu` AS `id`,
    'sk' AS `adm0`,
    LOWER(`iso-regionu`) AS `adm1`,
    `okres` AS `adm2`,
    `obec` AS `adm3`,
    `katastralne_uzemie` AS `adm4`,
    `nazov-sk` AS `name`,
    `adresa` AS `address`,
    `obec` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `fotka` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    REPLACE( `clanok`, ' ', '_' ) AS `monument_article`,
    '' AS `registrant_url` /* FIXME: Add this field to source table */
    FROM `monuments_sk_(sk)`;

/* El Salvador in Spanish */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'sv' AS `country`,
    'es' AS `lang`,
    `id` AS `id`,
    'sv' AS `adm0`,
    LOWER(`departamento_iso`) AS `adm1`,
    `municipio` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `monumento` AS `name`,
    `direccion` AS `address`,
    `municipio` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monumento_enlace` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_sv_(es)`;

/* Thailand in Thai */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'th' AS `country`,
    'th' AS `lang`,
    `register` AS `id`,
    'th' AS `adm0`,
    LOWER(`prov_iso`) AS `adm1`,
    `district` AS `adm2`,
    `tambon` AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
    `location` AS `address`,
    `district` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_th_(th)`;

/* Tunisia in French */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'tn' AS `country`,
    'fr' AS `lang`,
    `id` AS `id`,
    'tn' AS `adm0`,
    LOWER(`gouvernorat_iso`) AS `adm1`,
    `site` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `monument` AS `name`,
    `adresse` AS `address`,
    `site` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    `registrant_url` AS `registrant_url`
    FROM `monuments_tn_(fr)`;

/* Ukraine in Ukrainian */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'ua' AS `country`,
    'uk' AS `lang`,
    `id` AS `id`,
    'ua' AS `adm0`,
    LOWER(`iso_oblast`) AS `adm1`,
    `rayon` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
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
    '' AS `registrant_url`
    FROM `monuments_ua_(uk)`;

/* United States in English */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'us' AS `country`,
    'en' AS `lang`,
    `refnum` AS `id`,
    'us' AS `adm0`,
    LOWER(`state_iso`) AS `adm1`,
    `county` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    CONCAT('[[', `article`, '|', `name`, ']]') AS `name`,
    CONCAT(`address`, ' ', `city`) AS `address`,
    `county` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    REPLACE( `article`, ' ', '_' ) AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_us_(en)`
    WHERE NOT `type`='NRHP-delisted';

/* United States: California in English */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'us-ca' AS `country`,
    'en' AS `lang`,
    `refnum` AS `id`,
    'us' AS `adm0`,
    'us-ca' AS `adm1`,
    `county` AS `adm2`,
    `city` AS `adm3`,
    NULL AS `adm4`,
    CONCAT('[[', `article`, '|', `name`, ']]') AS `name`,
    CONCAT(`address`, ' ', `city`) AS `address`,
    `county` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    REPLACE( `article`, ' ', '_' ) AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_us-ca_(en)`;

/* Uruguay in Spanish */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'uy' AS `country`,
    'es' AS `lang`,
    `id` AS `id`,
    'uy' AS `adm0`,
    LOWER(`dep_iso`) AS `adm1`,
    `localidad` AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `monumento` AS `name`,
    `direccion` AS `address`,
    `localidad` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monumento_enlace` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_uy_(es)`;

/* Venezuela in Spanish */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    've' AS `country`,
    'es' AS `lang`,
    `id` AS `id`,
    've' AS `adm0`,
    LOWER(`estado_iso`) AS `adm1`,
    `municipio` AS `adm2`,
    `ciudad` AS `adm3`,
    NULL AS `adm4`,
    `monumento` AS `name`,
    `direccion` AS `address`,
    `municipio` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monumento_enlace` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_ve_(es)`;

/* Kosovo in Albanian */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'xk' AS `country`,
    'sq' AS `lang`,
    `idno` AS `id`,
    'xk' AS `adm0`,
    NULL AS `adm1`,
    NULL AS `adm2`,
    NULL AS `adm3`,
    NULL AS `adm4`,
    `name` AS `name`,
    `place` AS `address`,
    `municipality` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    '' AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    `monument_article` AS `monument_article`,
    '' AS `registrant_url`
    FROM `monuments_xk_(sq)`;

/* South Africa in English */
REPLACE INTO
  `monuments_all_tmp` (
    `country`, `lang`, `id`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4`, `name`, `address`, `municipality`, `lat`, `lon`, `lat_int`, `lon_int`, `image`, `commonscat`, `source`, `changed`, `monument_article`, `registrant_url`
  ) SELECT
    'za' AS `country`,
    'en' AS `lang`,
    `sitereference` AS `id`,
    'za' AS `adm0`,
    LOWER(`province_iso`) AS `adm1`,
    `magisterial_district` AS `adm2`,
    `town` AS `adm3`,
    NULL AS `adm4`,
    `site_name` AS `name`,
    `site_name` AS `address`,
    `town` AS `municipality`,
    `lat` AS `lat`,
    `lon` AS `lon`,
    ROUND(`lat` * @granularity) AS `lat_int`,
    ROUND(`lon` * @granularity) AS `lon_int`,
    `image` AS `image`,
    `commonscat` AS `commonscat`,
    `source` AS `source`,
    `changed` AS `changed`,
    '' AS `monument_article`,
    '' AS `registrant_url` /* FIXME: Add this field to source table */
    FROM `monuments_za_(en)`;
-- UPDATE `monuments_all_tmp` SET lat_int = ROUND(lat * @granularity), lon_int = ROUND(lon * @granularity);

/* when both lat and lon = 0 something went wrong */
UPDATE `monuments_all_tmp`
SET `lat`=NULL, `lon`=NULL, `lat_int`=NULL, `lon_int`=NULL
WHERE `lat`=0 AND `lon`=0;

DROP TABLE IF EXISTS `monuments_all`;

ALTER TABLE `monuments_all_tmp` RENAME TO `monuments_all`;
