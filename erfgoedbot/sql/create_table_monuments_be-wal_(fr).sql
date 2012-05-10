connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_be-wal_(fr)`;
CREATE TABLE IF NOT EXISTS `monuments_be-wal_(fr)` (
  `id_commune` int(8) NOT NULL DEFAULT  0,
  `clt-pex` varchar(6) NOT NULL DEFAULT '0',
  `id_objet` varchar(15) NOT NULL DEFAULT '0',
  `descr_de` varchar(255) NOT NULL DEFAULT '',
  `descr_nl` varchar(255) NOT NULL DEFAULT '',
  `nom_objet` varchar(255) NOT NULL DEFAULT '',
  `commune` varchar(255) NOT NULL DEFAULT '',
  `section_communale` varchar(255) NOT NULL DEFAULT '',
  `adresse` varchar(255) NOT NULL DEFAULT '',
  `objtype` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT  0,
  `lon` double NOT NULL DEFAULT  0,
  `architecte` varchar(255) NOT NULL DEFAULT '',
  `annee_construction` varchar(255) NOT NULL DEFAULT '',
  `image` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `monument_article` varchar(255) NOT NULL DEFAULT '',
  `registrant_url` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id_commune`,`clt-pex`,`id_objet`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
