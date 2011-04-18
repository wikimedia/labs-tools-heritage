/* Create table statement for the Rijksmonumenten in the Estonia in Estoian */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_ee_(et)`;
CREATE TABLE `monuments_ee_(et)` (
  `number` int(11) NOT NULL DEFAULT '0',
  `nimi` varchar(255) NOT NULL DEFAULT '',
  `liik` varchar(255) NOT NULL DEFAULT '',
  `aadress` varchar(255) NOT NULL DEFAULT '',
  `omavalitsus` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT '0',
  `lon` double NOT NULL DEFAULT '0',
  `pilt` varchar(255) NOT NULL DEFAULT '',
  `commons` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`number`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
