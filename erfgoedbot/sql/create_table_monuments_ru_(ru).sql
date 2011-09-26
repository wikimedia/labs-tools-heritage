/* Create table statement for the monuments in Russia in Russian. Field names are English already */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_ru_(ru)`;
CREATE TABLE `monuments_ru_(ru)` (
  `id` varchar(25) NOT NULL DEFAULT '0',
  `name` varchar(255) NOT NULL DEFAULT '',
  `complex` varchar(255) NOT NULL DEFAULT '',
  `address` varchar(255) NOT NULL DEFAULT '',
  `description`  varchar(255) NOT NULL DEFAULT '',
  `region` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT '0',
  `lon` double NOT NULL DEFAULT '0',
  `image` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
