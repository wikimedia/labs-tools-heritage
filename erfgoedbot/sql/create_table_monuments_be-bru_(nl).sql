connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_be-bru_(nl)`;
CREATE TABLE IF NOT EXISTS `monuments_be-bru_(nl)` (
  `code` varchar(25) NOT NULL DEFAULT '0',
  `omschrijving` varchar(255) NOT NULL DEFAULT '',
  `plaats` varchar(255) NOT NULL DEFAULT '',
  `adres` varchar(255) NOT NULL DEFAULT '',
  `bouwjaar` varchar(255) NOT NULL DEFAULT '',
  `bouwdoor` varchar(255) NOT NULL DEFAULT '',
  `bouwstijl` varchar(255) NOT NULL DEFAULT '',
  `objtype` varchar(255) NOT NULL DEFAULT '',
  `beschermd` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT  0,
  `lon` double NOT NULL DEFAULT  0,
  `image` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `monument_article` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`code`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
