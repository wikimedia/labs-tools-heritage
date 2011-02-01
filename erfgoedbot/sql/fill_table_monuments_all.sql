/* Create view for all country tables */
connect p_erfgoed_p sql.toolserver.org;
TRUNCATE TABLE monuments_all;
REPLACE INTO `monuments_all`
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
        FROM `monuments_be-vlg`)
UNION ALL
/* Switzerland */
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
/* Portugal */
(SELECT 'pt' AS `country`,
	`id` AS `id`, 
	`designacoes` AS `name`,
	'' AS `address`,
	`concelho` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	`imagem` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`
	FROM `monuments_pt`);
