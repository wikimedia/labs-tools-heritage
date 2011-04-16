/* Create table statement for the Rijksmonumenten in the Poland in Polish */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_pl_(pl)`;
CREATE TABLE `monuments_pl_(pl)` (
  `numer` varchar(11) NOT NULL DEFAULT '0',
  `nazwa` varchar(255) NOT NULL DEFAULT '',
  `adres` varchar(255) NOT NULL DEFAULT '',
  `gmina` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT '0',
  `lon` double NOT NULL DEFAULT '0',
  `zdjecie` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`numer`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
