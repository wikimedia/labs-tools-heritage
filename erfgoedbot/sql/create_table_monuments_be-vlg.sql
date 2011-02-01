/* Create table statement for the Onroerend Erfgoed in Vlaanderen */
connect p_erfgoed_p sql.toolserver.org;
CREATE TABLE `monuments_be-vlg` (
  `id` int(11) NOT NULL DEFAULT '0',
  `gemeente` varchar(255) NOT NULL DEFAULT '',
  `deelgem` varchar(255) NOT NULL DEFAULT '',
  `adres` varchar(255) NOT NULL DEFAULT '',
  `objectnaam` varchar(255) NOT NULL DEFAULT '',
  `bouwjaar`  varchar(255) NOT NULL DEFAULT '',
  `architect` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT '0',
  `lon` double NOT NULL DEFAULT '0',
  `image` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;