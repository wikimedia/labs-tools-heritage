/* Create table statement for the National Register of Historic Places listings in the United States in English */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_us_(en)`;
CREATE TABLE `monuments_us_(en)` (
  `refnum` int(11) NOT NULL DEFAULT '0',
  `pos` int(3) NOT NULL DEFAULT '0',
  `type` varchar(25) NOT NULL DEFAULT 'NRHP',
  `article` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  `address`  varchar(255) NOT NULL DEFAULT '',
  `city` varchar(255) NOT NULL DEFAULT '',
  `county` varchar(255) NOT NULL DEFAULT '',
  `state` varchar(255) NOT NULL DEFAULT '',
  `date` varchar(255) NOT NULL DEFAULT '',
  `image` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT '0',
  `lon` double NOT NULL DEFAULT '0',
  `description` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`refnum`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
