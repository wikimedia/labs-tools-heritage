-- UPDATE `{domain}_all_tmp` SET lat_int = ROUND(lat * @granularity), lon_int = ROUND(lon * @granularity);

/* when both lat and lon = 0 something went wrong */
UPDATE `{domain}_all_tmp`
SET `lat`=NULL, `lon`=NULL, `lat_int`=NULL, `lon_int`=NULL
WHERE `lat`=0 AND `lon`=0;

-- Safety net: first-ever run has no {domain}_all yet.
CREATE TABLE IF NOT EXISTS `{domain}_all` LIKE `{domain}_all_tmp`;

-- Clear any leftover from a previously timed-out drop.
DROP TABLE IF EXISTS `{domain}_all_old`;

-- Atomic multi-rename: the API never observes a missing table.
RENAME TABLE `{domain}_all` TO `{domain}_all_old`,
             `{domain}_all_tmp` TO `{domain}_all`;

-- The expensive part. If this times out the fresh {domain}_all is
-- already live; the leftover is cleaned up by the next run.
DROP TABLE IF EXISTS `{domain}_all_old`;
