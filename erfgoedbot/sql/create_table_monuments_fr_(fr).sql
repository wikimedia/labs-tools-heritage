/* Create table statement for the monuments in France in French table */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_fr_(fr)`;
CREATE TABLE `monuments_fr_(fr)` (
  `tri` varchar(11) NOT NULL DEFAULT '0',
  `monument` varchar(255) NOT NULL DEFAULT '',
  `commune` varchar(255) NOT NULL DEFAULT '',
  `tri commune` varchar(255) NOT NULL DEFAULT '',
  `adresse` varchar(255) NOT NULL DEFAULT '',
  `tri adresse` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT '0',
  `lon` double NOT NULL DEFAULT '0',
  `titre_coordonnees` varchar(255) NOT NULL DEFAULT '',
  `notice` varchar(11) NOT NULL DEFAULT '0',
  `protection` varchar(255) NOT NULL DEFAULT '',
  `date` varchar(255) NOT NULL DEFAULT '',
  `image` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`notice`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
