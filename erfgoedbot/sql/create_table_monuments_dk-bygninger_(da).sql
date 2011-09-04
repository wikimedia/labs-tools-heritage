/* Create table statement for bygninger in Denmark in Danish */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_dk-bygninger_(da)`;
CREATE TABLE `monuments_dk-bygninger_(da)` (
  `systemnrbyg` int(11) NOT NULL DEFAULT '0',
  `sagsnavn` varchar(255) NOT NULL DEFAULT '',
  `komplekstype` varchar(255) NOT NULL DEFAULT '',
  `opforelsesar` varchar(255) NOT NULL DEFAULT '',
  `adresse` varchar(255) NOT NULL DEFAULT '',
  `postnr`  varchar(255) NOT NULL DEFAULT '',
  `by` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT '0',
  `lon` double NOT NULL DEFAULT '0',
  `kommunenr` int(11) NOT NULL DEFAULT '0',
  `ejendomsnr` int(11) NOT NULL DEFAULT '0',
  `bygningsnr` int(11) NOT NULL DEFAULT '0',
  `fredar` varchar(255) NOT NULL DEFAULT '',
  `sagsnr` int(11) NOT NULL DEFAULT '0',
  `billede` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`sagsnr`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
