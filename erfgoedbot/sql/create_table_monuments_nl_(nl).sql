/* Create table statement for the Rijksmonumenten in the Netherlands in Dutch */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_nl_(nl)`;
CREATE TABLE IF NOT EXISTS `monuments_nl_(nl)` (
  `objrijksnr` int(11) NOT NULL DEFAULT  0,
  `woonplaats` varchar(255) NOT NULL DEFAULT '',
  `adres` varchar(255) NOT NULL DEFAULT '',
  `objectnaam` varchar(255) NOT NULL DEFAULT '',
  `type_obj` enum('G','A') DEFAULT NULL,
  `oorspr_functie` varchar(128) NOT NULL DEFAULT '',
  `bouwjaar` varchar(255) NOT NULL DEFAULT '',
  `architect` varchar(255) NOT NULL DEFAULT '',
  `cbs_tekst` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT  0,
  `lon` double NOT NULL DEFAULT  0,
  `image` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `monument_article` varchar(255) NOT NULL DEFAULT '',
  `registrant_url` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`objrijksnr`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;