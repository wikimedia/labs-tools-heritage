/* Create table statement for monuments in Sweden in Swedish */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_se_(sv)`;
CREATE TABLE IF NOT EXISTS `monuments_se_(sv)` (
  `bbr` varchar(25) NOT NULL DEFAULT '0',
  `namn` varchar(255) NOT NULL DEFAULT '',
  `funktion` varchar(255) NOT NULL DEFAULT '',
  `byggar` varchar(255) NOT NULL DEFAULT '',
  `arkitekt` varchar(255) NOT NULL DEFAULT '',
  `plats` varchar(255) NOT NULL DEFAULT '',
  `kommun` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT  0,
  `lon` double NOT NULL DEFAULT  0,
  `bild` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `monument_article` varchar(255) NOT NULL DEFAULT '',
  `registrant_url` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`bbr`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
