/* Create view for all country tables */
connect p_erfgoed_p sql.toolserver.org;
TRUNCATE TABLE monuments_all;
/* Switzerland */
REPLACE INTO `monuments_all`
(SELECT 'ch' AS `country`,
	`kgs_nr` AS `id`, 
	`name` AS `name`,
	`address` AS `address`,
	`municipality` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	`image` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`
	FROM `monuments_ch`)
UNION ALL
/* Netherlands */
(SELECT 'nl' AS `country`,
	`objrijksnr` AS `id`, 
	`objectnaam` AS `name`,
	`adres` AS `address`,
	`woonplaats` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	`image` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`
	FROM `monuments_nl`)
UNION ALL
/* Vlaanderen */
(SELECT 'be-vlg' AS `country`,
	`id` AS `id`,
        `objectnaam` AS `name`,
        `adres` AS `address`,
        `gemeente` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `image` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`
        FROM `monuments_be-vlg`);