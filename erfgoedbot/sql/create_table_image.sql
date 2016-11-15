/*
 * Create table for images with an identifier
 *
 * If you change something please test it.
 */

SET NAMES UTF8;

DROP TABLE IF EXISTS `image`;

CREATE TABLE `image` (
  `country` varchar(10) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT '',
  `id` varchar(25) NOT NULL DEFAULT '0',
  `img_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`country`,`id`, `img_name`),
  KEY `country_id` (`country`,`id`),
  KEY `img_name` (`img_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
