/* Create view for all country tables */
DROP VIEW IF EXISTS monuments_all;
CREATE VIEW monuments_all AS 
/* Switzerland */
(SELECT `kgs_nr` AS `id`, 
	'ch' AS country,
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
(SELECT `objrijksnr` AS `id`, 
	'nl' AS country,
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
(SELECT `id` AS `id`,
        'be-vlg' AS country,
        `objectnaam` AS `name`,
        `adres` AS `address`,
        `gemeente` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `image` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`
        FROM `monuments_be-vlg`);
