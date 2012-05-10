connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_es-gl_(gl)`;
CREATE TABLE IF NOT EXISTS `monuments_es-gl_(gl)` (
  `bic` varchar(25) NOT NULL DEFAULT '',
  `idurl` int(3) NOT NULL DEFAULT  0,
  `nomeoficial` varchar(255) NOT NULL DEFAULT '',
  `outrosnomes` varchar(255) NOT NULL DEFAULT '',
  `paxina` varchar(255) NOT NULL DEFAULT '',
  `concello` varchar(255) NOT NULL DEFAULT '',
  `lugar` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT  0,
  `lon` double NOT NULL DEFAULT  0,
  `notas` varchar(255) NOT NULL DEFAULT '',
  `data_declaracion` varchar(255) NOT NULL DEFAULT '',
  `imaxe` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `title` varchar(255) NOT NULL DEFAULT '',
  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `monument_article` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`bic`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
