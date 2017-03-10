-- UPDATE `{domain}_all_tmp` SET lat_int = ROUND(lat * @granularity), lon_int = ROUND(lon * @granularity);

/* when both lat and lon = 0 something went wrong */
UPDATE `{domain}_all_tmp`
SET `lat`=NULL, `lon`=NULL, `lat_int`=NULL, `lon_int`=NULL
WHERE `lat`=0 AND `lon`=0;

DROP TABLE IF EXISTS `{domain}_all`;

ALTER TABLE `{domain}_all_tmp` RENAME TO `{domain}_all`;
