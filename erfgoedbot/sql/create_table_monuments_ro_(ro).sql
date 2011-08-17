/* Create table statement for monuments in Romania */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_ro_(ro)`;
CREATE TABLE `monuments_ro_(ro)` (
  `cod` varchar(25) NOT NULL DEFAULT '0',
  `denumire` varchar(255) NOT NULL DEFAULT '',
  `localitate` varchar(255) NOT NULL DEFAULT '',
  `adresa` varchar(255) NOT NULL DEFAULT '',
  `datare`  varchar(255) NOT NULL DEFAULT '',
  `arhitect` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT '0',
  `lon` double NOT NULL DEFAULT '0',
  `imagine` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`cod`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
