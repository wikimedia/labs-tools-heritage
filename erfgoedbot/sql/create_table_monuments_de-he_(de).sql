/* Create table statement for the Baudenkmaeler in Bergheim in german */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_de-nrw-bm_(de)`;
CREATE TABLE `monuments_de-nrw-bm_(de)` (
  `nummer` int(11) NOT NULL DEFAULT '0',
  `ortsteil` varchar(255) NOT NULL DEFAULT '',
  `adresse` varchar(255) NOT NULL DEFAULT '',
  `bezeichnung` varchar(255) NOT NULL DEFAULT '',
  `artikel` varchar(255) NOT NULL DEFAULT '',
  `beschreibung` varchar(255) NOT NULL DEFAULT '',
  `stadt` varchar(255) NOT NULL DEFAULT '',
  `bild` varchar(255) NOT NULL DEFAULT '',
  `commonscat` varchar(255) NOT NULL DEFAULT '',
  `ns` double NOT NULL DEFAULT '0',
  `ew` double NOT NULL DEFAULT '0',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`nummer`),
  KEY `latitude` (`ns`),
  KEY `longitude` (`ew`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
