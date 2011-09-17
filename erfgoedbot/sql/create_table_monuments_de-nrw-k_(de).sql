/* Create table statement for the Baudenkmäler in Cologne in german */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_de-nrw-k_(de)`;
CREATE TABLE `monuments_de-nrw-k_(de)` (
  `nummer_denkmalliste` int(11) NOT NULL DEFAULT '0',
  `ortsteil` varchar(255) NOT NULL DEFAULT '',
  `adresse` varchar(255) NOT NULL DEFAULT '',
  `bezeichnung` varchar(255) NOT NULL DEFAULT '',
  `bauzeit` varchar(255) NOT NULL DEFAULT '',
  `beschreibung` varchar(255) NOT NULL DEFAULT '',
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
