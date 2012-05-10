connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_lu_(lb)`;
CREATE TABLE IF NOT EXISTS `monuments_lu_(lb)` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lag` varchar(255) NOT NULL DEFAULT '',
  `uertschaft` varchar(255) NOT NULL DEFAULT '',
  `offiziellen_numm` varchar(255) NOT NULL DEFAULT '',
  `beschreiwung` varchar(255) NOT NULL DEFAULT '',
  `niveau` varchar(255) NOT NULL DEFAULT '',
  `klasseiert_zenter` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT  0,
  `lon` double NOT NULL DEFAULT  0,
  `bild` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `monument_article` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;
