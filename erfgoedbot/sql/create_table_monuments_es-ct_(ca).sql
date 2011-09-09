/* Create table statement for the monuments in Catalunya in Catalan table */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_es-ct_(ca)`;
CREATE TABLE `monuments_es-ct_(ca)` (
  `bic` varchar(25) NOT NULL DEFAULT '0',
  `idurl` varchar(255) NOT NULL DEFAULT '',
  `bcin` varchar(255) NOT NULL DEFAULT '0',
  `nom` varchar(255) NOT NULL DEFAULT '',
  `estil` varchar(255) NOT NULL DEFAULT '',
  `epoca` varchar(255) NOT NULL DEFAULT '',
  `municipi` varchar(255) NOT NULL DEFAULT '',
  `lloc` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT '0',
  `lon` double NOT NULL DEFAULT '0',
  `nomcoor` varchar(255) NOT NULL DEFAULT '',
  `imatge` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `title`  varchar(255) NOT NULL DEFAULT '',
  `changed` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`bic`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
