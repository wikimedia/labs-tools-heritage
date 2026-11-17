CREATE TABLE IF NOT EXISTS `statistics` (
  `day` date NOT NULL,
  `item` varchar(50) NOT NULL,
  `country` varchar(100) NOT NULL,
  `muni` varchar(100) NOT NULL,
  `lang` varchar(100) NOT NULL,
  `project` varchar(100) NOT NULL,
  `value` varchar(16) NOT NULL DEFAULT '0',
  PRIMARY KEY (`day`,`item`, `country`, `muni`, `lang`, `project`),
  KEY `idx_day_idx` (`day`, `country`, `muni`, `lang`, `project`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
