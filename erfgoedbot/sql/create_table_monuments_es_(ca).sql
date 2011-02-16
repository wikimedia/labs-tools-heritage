/* Create table statement for the monuments in Spain in Catalan table */
connect p_erfgoed_p sql.toolserver.org;
CREATE TABLE `monuments_es_(ca)` (
  `bic` int(11) NOT NULL DEFAULT '0',
  `nom` varchar(255) NOT NULL DEFAULT '',
  `lloc` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT '0',
  `lon` double NOT NULL DEFAULT '0',
  `imatge` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`bic`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;