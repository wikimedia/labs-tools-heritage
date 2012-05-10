connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_es_(ca)`;
CREATE TABLE IF NOT EXISTS `monuments_es_(ca)` (
  `bic` varchar(25) NOT NULL DEFAULT '0',
  `nom` varchar(255) NOT NULL DEFAULT '',
  `tipus` varchar(255) NOT NULL DEFAULT '',
  `municipi` varchar(255) NOT NULL DEFAULT '',
  `lloc` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT  0,
  `lon` double NOT NULL DEFAULT  0,
  `nomcoor` varchar(255) NOT NULL DEFAULT '',
  `imatge` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `title` varchar(255) NOT NULL,
  `idurl` varchar(255) NOT NULL DEFAULT '',
  `monument_article` varchar(255) NOT NULL DEFAULT '',
  `registrant_url` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`bic`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
