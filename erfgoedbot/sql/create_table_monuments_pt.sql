/* Create table statement for the monuments in Portugal (IGESPAR) */
connect p_erfgoed_p sql.toolserver.org;
CREATE TABLE `monuments_pt` (
  `id` int(11) NOT NULL DEFAULT '0',
  `designacoes` varchar(255) NOT NULL DEFAULT '',
  `categoria` varchar(255) NOT NULL DEFAULT '',
  `tipologia` varchar(255) NOT NULL DEFAULT '',
  `concelho` varchar(255) NOT NULL DEFAULT '',
  `freguesia` varchar(255) NOT NULL DEFAULT '',
  `grau` varchar(255) NOT NULL DEFAULT '',
  `ano` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT '0',
  `lon` double NOT NULL DEFAULT '0',
  `imagem` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
