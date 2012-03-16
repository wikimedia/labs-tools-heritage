/* Create table statement for the Rijksmonumenten in Spain in Spanish */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_es_(es)`;
CREATE TABLE IF NOT EXISTS `monuments_es_(es)` (
  `bic` varchar(25) NOT NULL DEFAULT '0',
  `nombre` varchar(255) NOT NULL DEFAULT '',
  `nombrecoor` varchar(255) NOT NULL DEFAULT '',
  `tipobic` varchar(255) NOT NULL DEFAULT '',
  `tipo` varchar(255) NOT NULL DEFAULT '',
  `municipio` varchar(255) NOT NULL DEFAULT '',
  `lugar` varchar(400) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT '0',
  `lon` double NOT NULL DEFAULT '0',
  `fecha` varchar(255) NOT NULL DEFAULT '',
  `imagen` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `title` varchar(255) NOT NULL,
  `id_aut` varchar(21) NOT NULL DEFAULT '',
  `monument_article` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`bic`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;