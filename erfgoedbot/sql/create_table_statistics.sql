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

CREATE TABLE IF NOT EXISTS `statisticsct` (
  `img_name` varbinary(255) NOT NULL,
  `img_user_id` int(5) NOT NULL,
  `img_user_name` varchar(255) NOT NULL,
  `img_page_id` int(8) NOT NULL,
  `img_wlm_country` varchar(20) NOT NULL DEFAULT '',
  `img_wlm_id` varchar(25) NOT NULL DEFAULT '',
  `img_timestamp` varchar(14) NOT NULL,
  `img_has_changed` tinyint(1) NOT NULL,
  PRIMARY KEY (`img_name`),
  KEY `idx_wlm_id` (`img_wlm_id`),
  KEY `idx_ts` (`img_timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
