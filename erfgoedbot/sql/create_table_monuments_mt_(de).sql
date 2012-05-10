connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_mt_(de)`;
CREATE TABLE IF NOT EXISTS `monuments_mt_(de)` (
  `inventarnummer` varchar(11) NOT NULL DEFAULT '0',
  `foto` varchar(255) NOT NULL DEFAULT '',
  `artikel` varchar(255) NOT NULL DEFAULT '',
  `name-de` varchar(255) NOT NULL DEFAULT '',
  `name-en` varchar(255) NOT NULL DEFAULT '',
  `name-mt` varchar(255) NOT NULL DEFAULT '',
  `gemeinde` varchar(255) NOT NULL DEFAULT '',
  `adresse` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT  0,
  `lon` double NOT NULL DEFAULT  0,
  `region-iso` varchar(255) NOT NULL DEFAULT '',
  `beschreibung` varchar(255) NOT NULL DEFAULT '',
  `registrant_url` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`inventarnummer`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
