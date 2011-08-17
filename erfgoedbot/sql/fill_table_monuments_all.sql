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
/* Austria in German */
REPLACE INTO `monuments_all`
SELECT 'at' AS `country`, 
       'de' AS `lang`,
	`objektid` AS `id`,
        `name` AS `name`,
        `adresse` AS `address`,
        `katastralgemeinde` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `foto` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`
        FROM `monuments_at_(de)`;
/* Brussel */
REPLACE INTO `monuments_all`
SELECT 'be-bru' AS `country`,
       'nl' AS `lang`,
	`code` AS `id`,
        `omschrijving` AS `name`,
        `adres` AS `address`,
        `plaats` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `image` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`
        FROM `monuments_be-bru_(nl)`;
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
/* Wallonie */
REPLACE INTO `monuments_all`
SELECT 'be-wal' AS `country`,
       'nl' AS `lang`,
	CONCAT(`niscode`, '-', `objcode`) AS `id`,
        `descr_nl` AS `name`,
        `adres` AS `address`,
        `gemeente` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `image` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`
        FROM `monuments_be-wal_(nl)`;
/* Belarus */
REPLACE INTO `monuments_all`
SELECT 'by' AS `country`,
       'be-x-old' AS `lang`,
        `id` AS `id`,
        `name` AS `name`,
        `address` AS `address`,
        `place` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `image` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`
        FROM `monuments_by_(be-x-old)`;
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
/* Estonia */
REPLACE INTO `monuments_all`
SELECT 'ee' AS `country`,
       'et' AS `lang`,
	`number` AS `id`, 
	`nimi` AS `name`,
	`aadress` AS `address`,
	`omavalitsus` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	`pilt` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`
	FROM `monuments_ee_(et)`;
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
/* Spain in Spanish */
REPLACE INTO `monuments_all`
SELECT 'es' AS `country`,
       'es' AS `lang`,
	`bic` AS `id`,
        `nombrecoor` AS `name`,
        `lugar` AS `address`,
        `municipio` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `imagen` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`
        FROM `monuments_es_(es)`
        WHERE tipobic='M';
/* Catalunya in Catalan */
REPLACE INTO `monuments_all`
SELECT 'es-ct' AS `country`,
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
        FROM `monuments_es-ct_(ca)`;
/* Valencia in Catalan */
REPLACE INTO `monuments_all`
SELECT 'es-vc' AS `country`,
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
        FROM `monuments_es-vc_(ca)`;
/* France in Catalan */
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
/* France in French */
REPLACE INTO `monuments_all`
SELECT 'fr' AS `country`,
       'fr' AS `lang`,
	`notice` AS `id`,
        `monument` AS `name`,
        `adresse` AS `address`,
        `commune` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `image` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`
        FROM `monuments_fr_(fr)`;
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
/* Luxemburg in Luxemburgish */
REPLACE INTO `monuments_all`
SELECT 'lu' AS `country`,
       'lb' AS `lang`,
	`id` AS `id`,
        `offiziellen_numm` AS `name`,
        `lag` AS `address`,
        `uertschaft` AS `municipality`,
        `lat` AS `lat`,
        `lon` AS `lon`,
        `bild` AS `image`,
        `source` AS `source`,
        `changed` AS `changed`
        FROM `monuments_lu_(lb)`;
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
/* Poland */
REPLACE INTO `monuments_all`
SELECT 'pl' AS `country`,
       'pl' AS `lang`,
	`numer` AS `id`, 
	`nazwa` AS `name`,
	`adres` AS `address`,
	`gmina` AS `municipality`,
	`lat` AS `lat`,
	`lon` AS `lon`,
	`zdjecie` AS `image`,
	`source` AS `source`,
	`changed` AS `changed`
	FROM `monuments_pl_(pl)`;
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
