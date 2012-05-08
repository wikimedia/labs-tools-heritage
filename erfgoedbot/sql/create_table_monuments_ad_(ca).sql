/* Create table statement for the monuments in Andorra in Catalan table */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_ad_(ca)`;
CREATE TABLE `monuments_ad_(ca)` (
  `id` int(11) NOT NULL DEFAULT  0,
  `nom` varchar(255) NOT NULL DEFAULT '',
  `estil` varchar(255) NOT NULL DEFAULT '',
  `epoca` varchar(255) NOT NULL DEFAULT '',
  `municipi` varchar(255) NOT NULL DEFAULT '',
  `lloc` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT  0,
  `lon` double NOT NULL DEFAULT  0,
  `nomcoor` varchar(255) NOT NULL DEFAULT '',
  `imatge` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `monument_article` varchar(255) NOT NULL DEFAULT '',
  `registrant_url` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
