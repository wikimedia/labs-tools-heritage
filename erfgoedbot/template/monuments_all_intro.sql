/*
 * Create table for all country tables.
 *
 * Do not update this file manually.
 */

-- Update PHP code when changing this
SET @granularity = 20;

SET sql_mode = "ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION";

SET NAMES UTF8;

DROP TABLE IF EXISTS `{domain}_all_tmp`;

CREATE TABLE `{domain}_all_tmp` (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

TRUNCATE TABLE `{domain}_all_tmp`;
