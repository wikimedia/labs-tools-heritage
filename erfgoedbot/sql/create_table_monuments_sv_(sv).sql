/* Create table statement for monuments in Sweden in Swedish */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_sv_(sv)`;
CREATE TABLE `monuments_sv_(sv)` (
  `bbr` int(25) NOT NULL DEFAULT '0',
  `namn` varchar(255) NOT NULL DEFAULT '',
  `funktion` varchar(255) NOT NULL DEFAULT '',
  `byggar` varchar(255) NOT NULL DEFAULT '',
  `arkitekt`  varchar(255) NOT NULL DEFAULT '',
  `plats` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT '0',
  `lon` double NOT NULL DEFAULT '0',
  `bild` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`bbr`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
