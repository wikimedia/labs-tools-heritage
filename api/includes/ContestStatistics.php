<?php
/**
 * Statistics wrapper
 * @author Nuno Tavares <nuno.tavares@wikimedia.pt>
 *
 * Depends on ContestStatsBuilder being run on a daily basis
 */

ini_set('display_errors', 1);
ini_set('error_reporting', E_ALL);


class ContestStatistics extends StatisticsBase {
    static $dbTable = 'statisticsct2';
    var $report = array();


    static $dbPrimaryKey = array( 'img_name' );

    /* Use the following to draw records in blocks
    * to minimize server load 
    */
    static $activeCountries = array(
        'Portugal' => 'Cultural_heritage_monuments_in_Portugal_with_known_IDs',
        'Romania' => 'Cultural_heritage_monuments_in_Romania_with_known_IDs',
        'Estonia' => 'Cultural_heritage_monuments_in_Estonia_(with_known_IDs)',
        'Austria' => 'Cultural_heritage_monuments_in_Austria_with_known_IDs',
        'Andorra' => 'Cultural_heritage_monuments_in_Andorra_with_known_IDs',
       // 'Denmark' => 'Cultural_heritage_monuments_in_Denmark_with_known_IDs',
        'France' => 'Cultural_heritage_monuments_in_France_with_known_IDs',
        'Poland' => 'Cultural_heritage_monuments_in_Poland_with_known_IDs',
        'Belgium' => 'Onroerend_erfgoed_with_known_IDs',
        'the_Netherlands' => 'Rijksmonumenten_with_known_IDs',
        'Russia' => 'Cultural_heritage_monuments_in_Russia_with_known_IDs',         //??
        'Luxembourg' => 'Cultural_heritage_monuments_in_Luxembourg_with_known_IDs', //??
        'Norway' => 'Cultural_heritage_monuments_in_Norway_with_known_IDs',
        'Sweden' => 'Cultural_heritage_monuments_in_Sweden_with_known_IDs',
        'Germany' => 'Images_from_Wiki_Loves_Monuments_2011_in_Germany',  //??
        'Spain' => 'Cultural_heritage_monuments_in_Spain_with_known_IDs',
        'Switzerland' => 'Images_from_Wiki_Loves_Monuments_2011_in_Switzerland',    //??
    );


    static $reportUserCols = array('user','n_images','images','n_images_accepted','n_countries' ,'countries', 'n_wlm_ids', 'wlm_ids', 'n_images_all', 'images_all', 'n_images_accepted_all', 'n_wlm_ids_all', 'wlm_ids_all', 'user_is_new');
    static $reportCountryCols = array('country','images','users','new_users' ,'new_users_ratio', 'from_new_users', 'from_new_users_ratio');
    static $reportDumpCols = array('name', 'user_id', 'user_name', 'page_id', 'wlm_country', 'wlm_id', 'timestamp', 'user_first_rev', 'is_valid');
    static $ctScopes = array( /*default(0)=>*/ 'user','country','image','dump');


    function getAxis($sAxis) {
        return $this->axis[$sAxis];
    }


    function retrieveReport($ctscope, $ctitems, $ctcountries, $ctfrom, $limit, $ctorderby = 'n_images') {
        switch($ctscope) {
        case 'country':
            $ctitems = array('country','images','users','new_users' ,'new_users_ratio');
            $report = $this->retrieveReportCountry($ctitems, 'images DESC');
            break;
        case 'user':
            //$ctitems = array('user','n_images','n_images_accepted','n_countries' ,'n_wlm_ids', 'n_images_all', 'n_wlm_ids_all', 'n_images_accepted_all');
            $report = $this->retrieveReportUser($ctcountries, $ctitems, $limit, $ctorderby.' DESC');
            break;
        case 'image': 
            $report = $this->retrieveReportImage($ctcountries);
            break;
        case 'dump': 
            $report = $this->retrieveReportDump($ctcountries,$ctitems,$ctfrom, $limit);
            break;
        default:
            $report = null;
        }
        return $report;
    }


    function retrieveReportUser($selcountries,$selcolumns, $limit=50,$orderby = false) {
        $countries = '"'.implode('", "', $selcountries).'"';
        $selcolumns = array_intersect(ContestStatistics::$reportUserCols, $selcolumns);
        sort($selcolumns);
        $sql = 'SELECT 
                    st1.img_user_name AS user
                    , COUNT(DISTINCT st1.img_name) AS n_images
                    , SUM(img_is_valid) AS n_images_accepted
                    , GROUP_CONCAT(DISTINCT st1.img_name SEPARATOR "[,]") AS images
                    , COUNT(DISTINCT st1.img_wlm_id) AS n_wlm_ids
                    , GROUP_CONCAT(DISTINCT st1.img_wlm_id SEPARATOR "[,]") AS wlm_ids
                    , st2.n_countries AS n_countries
                    , st2.countries AS countries
                    , st2.n_images_all AS n_images_all
                    , st2.images_all AS images_all
                    , st2.n_wlm_ids_all AS n_wlm_ids_all
                    , st2.wlm_ids_all AS wlm_ids_all
                    , st2.n_images_accepted_all
                    , IF(st1.user_first_rev<20110831230000,0,1) AS user_is_new
                FROM statisticsct2 st1
                JOIN ( 
                    SELECT img_user_name
                        , COUNT(DISTINCT img_wlm_country) AS n_countries
                        , GROUP_CONCAT(DISTINCT img_wlm_country SEPARATOR "[,]") AS countries
                        , COUNT(DISTINCT img_name) AS n_images_all
                        , GROUP_CONCAT(DISTINCT img_name SEPARATOR "[,]") AS images_all
                        , COUNT(DISTINCT img_wlm_id) AS n_wlm_ids_all
                        , GROUP_CONCAT(DISTINCT img_wlm_id SEPARATOR "[,]") AS wlm_ids_all
                        , SUM(img_is_valid) AS n_images_accepted_all
                    FROM statisticsct2 
                    GROUP BY img_user_name) st2 
                        ON st1.img_user_name = st2.img_user_name
                WHERE st1.img_wlm_country IN ( '.$countries.' )
                GROUP BY st1.img_user_name';
        if ( $orderby ) {
            $sql .= ' ORDER BY '.$this->db->sanitize($orderby);
        }
        if ( $limit ) {
            $sql .= ' LIMIT '.$this->db->sanitize($limit);
        }
        //print "SQL: $sql";
        $oRes = new ResultWrapper( $this->db, $this->db->query($sql) );
        if ( !$oRes ) {
	        $this->setErrorMsg("ERROR: failed to get reportCountry data: ".$this->db->getDBError());
            return false;
        }
        $users = array();
        while ($row = $oRes->fetchAssoc()) {
            $users[$row['user']] = 1;
            for($i=0;$i<count($selcolumns);$i++) {
                $this->report[$row['user']][$selcolumns[$i]] = $row[$selcolumns[$i]];
            }
            $this->report[$row['user']]['lang'] = 'pt';
 	    }
        $this->axis['columns'] = $selcolumns;
        $users = array_keys($users);
        sort($users);
        $this->axis['rows'] = $users;

	    $this->db->freeResult($oRes);

        return $this->report;
    }


    function retrieveReportCountry($selcolumns, $orderby = false) {
        $selcolumns = array('country','images','users','new_users' ,'new_users_ratio', 'from_new_users', 'from_new_users_ratio');
        $selcolumns = array_intersect(ContestStatistics::$reportCountryCols, $selcolumns);
        sort($selcolumns);
        $queries = array();
        foreach (ContestStatistics::$activeCountries as $country => $category) {
            $sql = 'SELECT img_wlm_country AS country
                    , COUNT(1) AS images
                    , COUNT(DISTINCT st1.img_user_id) AS users
                    , (SELECT COUNT(DISTINCT img_user_name) 
                        FROM statisticsct2 st2
                        WHERE img_wlm_country = "'.$country.'" 
                            AND st2.user_first_rev >= 20110831230000) AS new_users
                    , ((SELECT COUNT(DISTINCT img_user_name) 
                        FROM statisticsct2 st2
                        WHERE img_wlm_country = "'.$country.'" 
                            AND st2.user_first_rev >= 20110831230000) / COUNT(DISTINCT st1.img_user_id))*100 AS new_users_ratio
                    , (SELECT COUNT(1)
                        FROM statisticsct2 st2
                        WHERE user_first_rev>=20110831230000
                            AND img_wlm_country = "'.$country.'") AS from_new_users
                    , ((SELECT COUNT(1)
                        FROM statisticsct2 st2
                        WHERE user_first_rev>=20110831230000
                            AND img_wlm_country = "'.$country.'") / COUNT(1))*100 AS from_new_users_ratio
                FROM statisticsct2 st1 
                WHERE img_wlm_country = "'.$country.'"
                ';
            $queries[] = $sql;
        }
        $sql = implode(' UNION ', $queries);
        if ( $orderby ) {
            $sql .= ' ORDER BY '.$orderby;
        }
        //print "SQL: $sql";
        $oRes = new ResultWrapper( $this->db, $this->db->query($sql) );
        if ( !$oRes ) {
	        $this->setErrorMsg("ERROR: failed to get reportCountry data: ".$this->db->getDBError());
            return false;
        }
        $countries = array();
        while ($row = $oRes->fetchAssoc()) {
            // TEMP: skip empty countries
            if ( strlen($row['country'])<=0 ) {
                continue;
            }
            $countries[$row['country']] = 1;
            for($i=0;$i<count($selcolumns);$i++) {
                $this->report[$row['country']][$selcolumns[$i]] = $row[$selcolumns[$i]];
            }
/*
            $this->report[$row['country']]['country'] = $row['country'];
            $this->report[$row['country']]['images'] = $row['images'];
            $this->report[$row['country']]['users'] = $row['users'];
            $this->report[$row['country']]['new_users'] = $row['new_users'];
            $this->report[$row['country']]['new_users_ratio'] = $row['new_users_ratio'];
*/
            $this->report[$row['country']]['lang'] = 'pt';
 	    }
        $this->axis['columns'] = $selcolumns;
        $countries = array_keys($countries);
        sort($countries);
        $this->axis['rows'] = $countries;

	    $this->db->freeResult($oRes);

        return $this->report;
    }


    function retrieveReportImage($countries) {
        //$this->debug('retrieveReport() started.');

        $countries = array_intersect($countries, array_keys(ContestStatistics::$activeCountries));
        $countries_in = '"'.implode('", "', $countries).'"';
        $sql = 'SELECT SUBSTR(img_timestamp,1,10) AS timeslot
                , img_wlm_country as country
                , COUNT(1) as n_images
            FROM '.ContestStatistics::$dbTable.'
            WHERE img_wlm_country IN ( '.$countries_in.' )
            GROUP BY img_wlm_country,SUBSTR(img_timestamp,1,10)
            ORDER BY img_timestamp;
            ';
        //print "SQL: $sql";
        $oRes = new ResultWrapper( $this->db, $this->db->query($sql) );
        if ( !$oRes ) {
	        $this->setErrorMsg("ERROR: failed to get reportImage data: ".$this->db->getDBError());
            return false;
        }
        $timeslots = array();
        $countries = array();
		while ($row = $oRes->fetchAssoc()) {
            $timeslots[$row['timeslot']] = 1;
            $countries[$row['country']] = 1;
            $tmp = array();
            $tmp['country'] = $row['country'];
            $tmp['n_images'] = $row['n_images'];
            $tmp['timeslot'] = $row['timeslot'];
            $tmp['lang'] = 'pt';
            $this->report[] = $tmp;
 	    }
        $countries = array_keys($countries);
        sort($countries);
        $this->axis['columns'] = $countries;
        $this->axis['columns'] = array('timeslot', 'country', 'n_images');
        $timeslots = array_keys($timeslots);
        $this->axis['rows'] = $timeslots;

	    $this->db->freeResult($oRes);

        return $this->report;
    }


    function retrieveReportDump($selcountries, $selcolumns, $ctfrom, $limit = 0) {
        $countries_in = '"'.implode('", "', $selcountries).'"';
        $selcolumns = array_intersect(ContestStatistics::$reportDumpCols, $selcolumns);
        sort($selcolumns);
        $ctfrom = $this->db->sanitize($ctfrom);
        for($i=0;$i<count($selcolumns);$i++) {
            if ( $selcolumns[$i] != 'user_first_rev' ) {
                $selcolumns[$i] = 'img_'.$selcolumns[$i];
            }
        }
        $qcolumns = $selcolumns;
        if (!isset($qcolumns['img_name'])) {
            $qcolumns[] = 'img_name';
        }

        $sql = 'SELECT '.implode(',', $qcolumns).'
            FROM '.ContestStatistics::$dbTable.'
            WHERE img_wlm_country IN ( '.$countries_in.' )
                AND img_timestamp >= '.$ctfrom.'
            ORDER BY img_timestamp
            ';
        if ( $limit ) {
            $sql .= 'LIMIT '.$limit;
        }
        //print "SQL: $sql";
        $oRes = new ResultWrapper( $this->db, $this->db->query($sql) );
        if ( !$oRes ) {
	        $this->setErrorMsg("ERROR: failed to get reportImage data: ".$this->db->getDBError());
            return false;
        }
        $timeslots = array();
        $countries = array();
		while ($row = $oRes->fetchAssoc()) {
            for($i=0;$i<count($selcolumns);$i++) {
                $this->report[$row['img_name']][$selcolumns[$i]] = $row[$selcolumns[$i]];
            }
            $this->report[$row['img_name']]['lang'] = 'pt';
 	    }

        $this->axis['columns'] = $selcolumns;
        $this->axis['rows'] = array();
        return $this->report;
    }


}
