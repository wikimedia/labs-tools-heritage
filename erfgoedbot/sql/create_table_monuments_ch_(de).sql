/* Create table statement for the monuments in Switzerland in German */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_ch_(de)`; 
CREATE TABLE IF NOT EXISTS `monuments_ch_(de)` (
  `kgs-nr` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL DEFAULT '',
  `addresse` varchar(255) NOT NULL DEFAULT '',
  `gemeinde` varchar(255) NOT NULL DEFAULT '',
  `kanton` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT  0,
  `lon` double NOT NULL DEFAULT  0,
  `foto` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `monument_article` varchar(255) NOT NULL DEFAULT '',
  `typ` varchar(255) NOT NULL DEFAULT '',
  `region-iso` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`kgs-nr`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;
