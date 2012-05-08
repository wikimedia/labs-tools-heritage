/* Create table statement for the Baudenkmäler in Bayern in german */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_de-by_(de)`;
CREATE TABLE IF NOT EXISTS `monuments_de-by_(de)` (
  `nummer` varchar(15) NOT NULL DEFAULT '0',
  `stadt` varchar(255) NOT NULL DEFAULT '',
  `ortsteil` varchar(255) NOT NULL DEFAULT '',
  `adresse` varchar(255) NOT NULL DEFAULT '',
  `bezeichnung` varchar(255) NOT NULL DEFAULT '',
  `artikel` varchar(255) NOT NULL DEFAULT '',
  `beschreibung` varchar(255) NOT NULL DEFAULT '',
  `bild` varchar(255) NOT NULL DEFAULT '',
  `commonscat` varchar(255) NOT NULL DEFAULT '',
  `ns` double NOT NULL DEFAULT  0,
  `ew` double NOT NULL DEFAULT  0,
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`nummer`),
  KEY `latitude` (`ns`),
  KEY `longitude` (`ew`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
