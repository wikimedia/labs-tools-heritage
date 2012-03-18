/* Create table statement for the Monuments in Austria in German */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_it-bz_(de)`;
CREATE TABLE IF NOT EXISTS `monuments_it-bz_(de)` (
  `objektid` varchar(11) NOT NULL DEFAULT '0',
  `foto` varchar(255) NOT NULL DEFAULT '',
  `fotobeschreibung` varchar(255) NOT NULL DEFAULT '',
  `commonscat` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  `artikel` varchar(255) NOT NULL DEFAULT '',
  `anzeige-Name` varchar(255) NOT NULL DEFAULT '',
  `adresse` varchar(255) NOT NULL DEFAULT '',
  `adresse-sort` varchar(255) NOT NULL DEFAULT '',
  `region-iso` varchar(255) NOT NULL DEFAULT '',
  `gemeinde` varchar(255) NOT NULL DEFAULT '',
  `gemeindekennzahl` int(15) NOT NULL DEFAULT '',
  `katastralgemeinde` varchar(255) NOT NULL DEFAULT '',
  `status` varchar(255) NOT NULL DEFAULT '',
  `beschreibung` varchar(255) NOT NULL DEFAULT '',
  `eintragung` varchar(255) NOT NULL DEFAULT '',
  `beschluss` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT '0',
  `lon` double NOT NULL DEFAULT '0',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `registrant_url` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`objektid`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;