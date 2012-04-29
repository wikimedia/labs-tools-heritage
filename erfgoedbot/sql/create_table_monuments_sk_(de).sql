/* Create table statement for the Monuments in Slovakia in German */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_sk_(de)`;
CREATE TABLE `monuments_sk_(de)` (
  `objektid` varchar(11) NOT NULL DEFAULT '0',
  `foto` varchar(255) NOT NULL DEFAULT '',
  `commonscat` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  `anzeige-name` varchar(255) NOT NULL DEFAULT '',
  `artikel` varchar(255) NOT NULL DEFAULT '',
  `adresse` varchar(255) NOT NULL DEFAULT '',
  `adresse-sort` varchar(255) NOT NULL DEFAULT '',
  `region-iso` varchar(255) NOT NULL DEFAULT '',
  `katastralgemeinde` varchar(255) NOT NULL DEFAULT '',
  `bearbeitungsdatum` varchar(255) NOT NULL DEFAULT '',
  `beschreibung` varchar(255) NOT NULL DEFAULT '',
  `offiziellebeschreibung` varchar(255) NOT NULL DEFAULT '',
  `anzeige-artikel` varchar(255) NOT NULL DEFAULT '',
  `konskriptionsnr` varchar(255) NOT NULL DEFAULT '',
  `obec` varchar(255) NOT NULL DEFAULT '',
  `kod_obce` int(11) NOT NULL DEFAULT '0',
  `okres` varchar(255) NOT NULL DEFAULT '',
  `kod_okresu` int(11) NOT NULL DEFAULT '0',
  `lat` double NOT NULL DEFAULT '0',
  `lon` double NOT NULL DEFAULT '0',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ObjektID`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;