/* Create table statement for Belarus in Belarussian */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_by_(be-x-old)`;
CREATE TABLE `monuments_by_(be-x-old)` (
  `шыфр` int(8) NOT NULL DEFAULT '0',
  `назва` varchar(255) NOT NULL DEFAULT '',
  `датаваньне` varchar(255) NOT NULL DEFAULT '',
  `населены_пункт` varchar(255) NOT NULL DEFAULT '',
  `адрэса` varchar(255) NOT NULL DEFAULT '',
  `катэгорыя ` varchar(255) NOT NULL DEFAULT '',
  `шырата` double NOT NULL DEFAULT '0',
  `даўгата` double NOT NULL DEFAULT '0',
  `каардынаты` varchar(255) NOT NULL DEFAULT '',
  `выява` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`шыфр`),
  KEY `latitude` (`шырата`),
  KEY `longitude` (`даўгата`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
