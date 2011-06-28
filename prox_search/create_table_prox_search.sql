DROP TABLE IF EXISTS `prox_search`; 
CREATE TABLE `prox_search` (
  `point_id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  `mon_country` varchar(10) NOT NULL DEFAULT '',
  `mon_lang` varchar(10) NOT NULL DEFAULT '',
  `mon_id` varchar(25) NOT NULL DEFAULT '0',  
  `lat` DECIMAL(14,10) NOT NULL,
  `lon` DECIMAL(15,10) NOT NULL,
  `int_peano1`  INTEGER UNSIGNED NOT NULL,
  `int_peano2` INTEGER UNSIGNED NOT NULL,
  `int_peano1iv` INTEGER UNSIGNED NOT NULL,
  `int_peano2iv` INTEGER UNSIGNED NOT NULL,
  
  PRIMARY KEY(point_id),
  UNIQUE INDEX (`mon_country`, `mon_lang`, `mon_id`),  
  INDEX peano1 (int_peano1, point_id),
  INDEX peano2 (int_peano2, point_id),
  INDEX peano1iv (int_peano1iv, point_id),
  INDEX peano2iv (int_peano2iv, point_id)

) ENGINE=MyISAM DEFAULT CHARSET=utf8;
