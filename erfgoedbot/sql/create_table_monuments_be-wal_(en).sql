/* Create table statement for the protected heritage sites in Wallona in English */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_be-wal_(en)`;
CREATE TABLE IF NOT EXISTS `monuments_be-wal_(en)` (
  `niscode` int(8) NOT NULL DEFAULT  0,
  `objcode` varchar(15) NOT NULL DEFAULT '0',
  `descr_en` varchar(255) NOT NULL DEFAULT '',
  `descr_de` varchar(255) NOT NULL DEFAULT '',
  `descr_nl` varchar(255) NOT NULL DEFAULT '',
  `descr_fr` varchar(255) NOT NULL DEFAULT '',
  `section` varchar(255) NOT NULL DEFAULT '',
  `town` varchar(255) NOT NULL DEFAULT '',
  `address` varchar(255) NOT NULL DEFAULT '',
  `objtype` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT  0,
  `lon` double NOT NULL DEFAULT  0,
  `architect` varchar(255) NOT NULL DEFAULT '',
  `date` varchar(255) NOT NULL DEFAULT '',
  `image` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `monument_article` varchar(255) NOT NULL DEFAULT '',
  `registrant_url` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`niscode`,`objcode`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
