/* Create table statement for the Onroerend Erfgoed in Vlaanderen in French */
connect p_erfgoed_p sql.toolserver.org;
DROP TABLE IF EXISTS `monuments_be-vlg_(fr)`;
CREATE TABLE IF NOT EXISTS `monuments_be-vlg_(fr)` (
  `id` int(11) NOT NULL DEFAULT  0,
  `classement` varchar(255) NOT NULL DEFAULT '',
  `commune` varchar(255) NOT NULL DEFAULT '',
  `section_communale` varchar(255) NOT NULL DEFAULT '',
  `section_communale_id` varchar(25) NOT NULL DEFAULT '',
  `adresse` varchar(255) NOT NULL DEFAULT '',
  `nom_objet` varchar(255) NOT NULL DEFAULT '',
  `annee_construction` varchar(255) NOT NULL DEFAULT '',
  `architecte` varchar(255) NOT NULL DEFAULT '',
  `lat` double NOT NULL DEFAULT  0,
  `lon` double NOT NULL DEFAULT  0,
  `image` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(255) NOT NULL DEFAULT '',
  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `monument_article` varchar(255) NOT NULL DEFAULT '',
  `registrant_url` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `latitude` (`lat`),
  KEY `longitude` (`lon`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
