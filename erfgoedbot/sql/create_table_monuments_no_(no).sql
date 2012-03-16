/* Create table statement for the monuments in Norway in No */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_no_(no)`;
CREATE TABLE IF NOT EXISTS `monuments_no_(no)` (
  `id` int(11) NOT NULL DEFAULT '0',
  `navn` varchar(255) NOT NULL DEFAULT '',
  `artikkel` varchar(255) NOT NULL DEFAULT '',
  `kategori` varchar(255) NOT NULL DEFAULT '',
  `datering` varchar(128) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT '0',
  `lon` double NOT NULL DEFAULT '0',
  `kommunenr` int(10) NOT NULL DEFAULT '0',
  `kommune` varchar(255) NOT NULL DEFAULT '',
  `vernetype` varchar(255) NOT NULL DEFAULT '',
  `kat` varchar(255) NOT NULL DEFAULT '',
  `tilrettel` varchar(255) NOT NULL DEFAULT '',
  `verdensarv` varchar(255) NOT NULL DEFAULT '',
  `bilde` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `monument_article` varchar(255) NOT NULL DEFAULT '',
  `registrant_url` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
