connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_pl_(pl)`;
CREATE TABLE IF NOT EXISTS `monuments_pl_(pl)` (
  `numer` varchar(255) NOT NULL DEFAULT '0',
  `nazwa` varchar(255) NOT NULL DEFAULT '',
  `adres` varchar(255) NOT NULL DEFAULT '',
  `gmina` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT  0,
  `lon` double NOT NULL DEFAULT  0,
  `koordynaty` varchar(255) NOT NULL DEFAULT '',
  `zdjecie` varchar(255) NOT NULL DEFAULT '',
  `commons` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `monument_article` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`numer`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
