DROP TABLE IF EXISTS `commonscat`;
CREATE TABLE `commonscat` (
  `site` ENUM ('be-x-old', 'ca', 'da', 'de', 'en', 'es', 'et', 'fr', 'gl', 'lb', 'nl', 'no', 'pl', 'pt', 'ro', 'sv' ) NOT NULL, -- Wikipedia the title belongs to
  `title`  VARCHAR (255) NOT NULL DEFAULT '', -- Title at site
  `commonscat` VARCHAR (255), -- Commons category into which files listed at title should be categorised
  `changed` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (site, title)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

