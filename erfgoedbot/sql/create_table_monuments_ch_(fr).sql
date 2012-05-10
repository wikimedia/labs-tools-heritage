connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_ch_(fr)`;
CREATE TABLE IF NOT EXISTS `monuments_ch_(fr)` (
  `kgs-nr` int(11) NOT NULL DEFAULT  0,
  `objet` varchar(255) NOT NULL DEFAULT '',
  `addresse` varchar(255) NOT NULL DEFAULT '',
  `commune` varchar(255) NOT NULL DEFAULT '',
  `canton` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT  0,
  `lon` double NOT NULL DEFAULT  0,
  `photo` varchar(255) NOT NULL DEFAULT '',
  `region-iso` varchar(255) NOT NULL DEFAULT '',
  `typ_a` varchar(255) NOT NULL DEFAULT '',
  `typ_arch` varchar(255) NOT NULL DEFAULT '',
  `typ_b` varchar(255) NOT NULL DEFAULT '',
  `typ_e` varchar(255) NOT NULL DEFAULT '',
  `typ_m` varchar(255) NOT NULL DEFAULT '',
  `typ_o` varchar(255) NOT NULL DEFAULT '',
  `typ_s` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `monument_article` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`kgs-nr`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
