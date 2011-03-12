/* Create view for all country tables */
connect p_erfgoed_p sql.toolserver.org;
TRUNCATE TABLE monuments_all;
/* Andorra in Catalan */
REPLACE INTO `monuments_all`
SELECT 'ad' AS `country`, 
       'ca' AS `lang`,
	`id` AS `id`,
        `nomcoor` AS `name`,
        `lloc` AS `address`,
        `municipi` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `imatge` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`
        FROM `monuments_ad_(ca)`;
/* Vlaanderen */
REPLACE INTO `monuments_all`
SELECT 'be-vlg' AS `country`,
       'nl' AS `lang`,
	`id` AS `id`,
        `objectnaam` AS `name`,
        `adres` AS `address`,
        `gemeente` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `image` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`
        FROM `monuments_be-vlg_(nl)`;
/* Switzerland */
REPLACE INTO `monuments_all`
SELECT 'ch' AS `country`,
       'en' AS `lang`,
	`kgs_nr` AS `id`, 
	`name` AS `name`,
	`address` AS `address`,
	`municipality` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	`image` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`
	FROM `monuments_ch_(en)`;
/* Spain in Catalan */
REPLACE INTO `monuments_all`
SELECT 'es' AS `country`,
       'ca' AS `lang`,
	`bic` AS `id`,
        `nomcoor` AS `name`,
        `lloc` AS `address`,
        `municipi` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `imatge` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`
        FROM `monuments_es_(ca)`;
/* Catalunya in Catalan */
REPLACE INTO `monuments_all`
SELECT 'es-ct' AS `country`,
       'ca' AS `lang`,
	`id` AS `id`,
        `nomcoor` AS `name`,
        `lloc` AS `address`,
        `municipi` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `imatge` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`
        FROM `monuments_es-ct_(ca)`;
/* Valencia in Catalan */
REPLACE INTO `monuments_all`
SELECT 'es-vc' AS `country`,
       'ca' AS `lang`,
	`idurl` AS `id`,
        `nomcoor` AS `name`,
        `lloc` AS `address`,
        `municipi` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `imatge` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`
        FROM `monuments_es-vc_(ca)`;
/* French in Catalan */
REPLACE INTO `monuments_all`
SELECT 'fr' AS `country`,
       'ca' AS `lang`,
	`id` AS `id`,
        `nomcoor` AS `name`,
        `lloc` AS `address`,
        `municipi` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `imatge` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`
        FROM `monuments_fr_(ca)`;
/* Ireland in English */
REPLACE INTO `monuments_all`
SELECT 'ie' AS `country`,
       'en' AS `lang`,
        `number` AS `id`,
        `name` AS `name`,
	'' AS `address`,
	`townland` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	`image` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`
	FROM `monuments_ie_(en)`;
/* Sardinia in Catalan */
REPLACE INTO `monuments_all`
SELECT 'it-88' AS `country`,
       'ca' AS `lang`,
	`id` AS `id`,
        `nomcoor` AS `name`,
        `lloc` AS `address`,
        `municipi` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `imatge` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`
        FROM `monuments_it-88_(ca)`;
/* Netherlands */
REPLACE INTO `monuments_all`
SELECT 'nl' AS `country`,
       'nl' AS `lang`,
	`objrijksnr` AS `id`, 
	`objectnaam` AS `name`,
	`adres` AS `address`,
	`woonplaats` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	`image` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`
	FROM `monuments_nl_(nl)`;
/* Portugal */
REPLACE INTO `monuments_all`
SELECT 'pt' AS `country`,
       'pt' AS `lang`,
	`id` AS `id`, 
	`designacoes` AS `name`,
	'' AS `address`,
	`concelho` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	`imagem` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`
	FROM `monuments_pt_(pt)`;
