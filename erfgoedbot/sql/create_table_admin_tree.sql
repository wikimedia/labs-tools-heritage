CREATE TABLE IF NOT EXISTS `admin_tree` (
	`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`lang` VARCHAR(10) NOT NULL,
	`level` INT NOT NULL,
	`name` VARCHAR(255) NOT NULL,
	`parent` INT,
	KEY `parent` (`parent`),
	KEY `level_name_lang` (`level`, `name`, `lang`)
) ENGINE=INNODB DEFAULT CHARSET=utf8;
