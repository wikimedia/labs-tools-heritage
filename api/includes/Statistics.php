<?php
/**
 * Statistics wrapper
 * @author Nuno Tavares <nuno.tavares@wikimedia.pt>
 *
 * Depends on StatsBuilder being run on a daily basis
 */

ini_set('display_errors', 1);
ini_set('error_reporting', E_ALL);


class Statistics extends StatisticsBase {
    static $dbTable = 'statistics';
    var $report = array();
    var $axis = array();
    static $fieldPrefix = 'st_';

    var $lastDay = '';
    static $aItems = array('address', 'address_pct', 'coordinates', 'coordinates_pct', 'image', 'image_pct', 'municipality', 'municipality_pct', 'name', 'name_pct', 'total' );


    function getLatestDay() {
        if ( empty($this->lastDay) ) {
            $sql = 'SELECT MAX(day) FROM '.Statistics::$dbTable;
            $res = $this->db->query( $sql );
            $oRes = new ResultWrapper( $this->db, $res );
            $row = $oRes->fetchRow();
            $this->lastDay = $row[0];
        }
        // fallback to today, if none found (set initial/first timestamp)
        if ( empty($this->lastDay) ) {
            $this->lastDay = date('Y-m-d');
        }
        return $this->lastDay;
    }


    function retrieveReport($aItems, $aFilters, $sLimit, $groupby = 'item') {
        //$this->debug('retrieveReport() started.');

        // sanitize inputs
        $items = array();
        for($i=0; $i<count($aItems); $i++) {
            $items[] = $this->db->sanitize($aItems[$i]);
        }
        $filters = array();
        for($i=0; $i<count($aFilters); $i++) {
            $filters[] = $this->db->sanitize($aFilters[$i]);
        }
        $sLimit = $this->db->sanitize($sLimit);

        // determine proper axis - TODO recover groupby='country'
        $gc = 'item';
        $gi = 'idx';

        // determine SQL filters
        $fields = array( 'day', 'item', 'idx', 'value' );
        $where = array();

        $items_in = '"'. Statistics::$fieldPrefix . implode('","'.Statistics::$fieldPrefix, $items) . '"';
        $where[] = 'item IN ('.$items_in.')';
        $where[] = '`day` = "'.$this->getLatestDay().'"';

        $filters_in = array();
        for($i=0; $i<count($filters); $i++) {
            $filters_in[] = 'idx LIKE "'.$filters[$i].':%"';
        }
        $where[] = implode(' OR ', $filters_in);

    	$oRes = $this->db->select($fields, Statistics::$dbTable, $where, false, $sLimit);
	    if ( !$oRes ) {
            $this->setErrorMsg('ERROR: Error running query');
            return false;
        }
        $group = array();
        $idxs = array();
		while ($row = $oRes->fetchAssoc()) {
            //var_dump($row);
            $group[$row[$gc]] = 1;
            $idxs[$row[$gi]] = 1;
            list($country,$municipality) = explode(':', $row[$gi], 2);
            $this->report[$row[$gi]]['country'] = $country;
            $this->report[$row[$gi]]['lang'] = $country == 'us' ? 'en' : $country;
            $this->report[$row[$gi]]['municipality'] = $municipality;
            $this->report[$row[$gi]][$row[$gc]] = $row['value'];
	    }
        //var_dump($this->report);
        $this->axis['columns'] = array_keys($group);
        sort($this->axis['columns']);
        $this->axis['rows'] = array_keys($idxs);

	    $this->db->freeResult($oRes);

        return $this->report;
    }


    function getAxis($sAxis) {
        return $this->axis[$sAxis];
    }

}
