DROP TABLE IF EXISTS `id_dump`;
CREATE TABLE `id_dump` (
  `source` varchar(510) NOT NULL DEFAULT '',
  `id` varchar(25) NOT NULL DEFAULT '0',
  `country` varchar(10) binary NOT NULL DEFAULT '',
  `lang` varchar(10) binary NOT NULL DEFAULT '',
  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
