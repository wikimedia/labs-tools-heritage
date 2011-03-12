/* Create table statement for the monuments in Valencia in Catalan table */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_es-vc_(ca)`;
CREATE TABLE `monuments_es-vc_(ca)` (
  `idurl` int(11) NOT NULL DEFAULT '0',
  `bic` int(11) NOT NULL DEFAULT '0',
  `nom` varchar(255) NOT NULL DEFAULT '',
  `nomcoor` varchar(255) NOT NULL DEFAULT '',
  `estil` varchar(255) NOT NULL DEFAULT '',
  `municipi` varchar(255) NOT NULL DEFAULT '',
  `lloc` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT '0',
  `lon` double NOT NULL DEFAULT '0',
  `imatge` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`idurl`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
