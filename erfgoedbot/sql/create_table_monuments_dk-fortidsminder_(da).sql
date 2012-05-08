/* Create table statement for fortidsminder in Denmark in Danish */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_dk-fortidsminder_(da)`;
CREATE TABLE IF NOT EXISTS `monuments_dk-fortidsminder_(da)` (
  `fredningsnummer` int(11) NOT NULL DEFAULT  0,
  `stednavn` varchar(255) NOT NULL DEFAULT '',
  `type` varchar(255) NOT NULL DEFAULT '',
  `datering` varchar(255) NOT NULL DEFAULT '',
  `sevaedighed` varchar(255) NOT NULL DEFAULT '',
  `systemnummer` int(11) NOT NULL DEFAULT  0,
  `anlnr` int(11) NOT NULL DEFAULT  0,
  `lat` double NOT NULL DEFAULT  0,
  `lon` double NOT NULL DEFAULT  0,
  `billede` varchar(255) NOT NULL DEFAULT '',
  `bemaerkning` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `monument_article` varchar(255) NOT NULL DEFAULT '',
  `registrant_url` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`systemnummer`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
