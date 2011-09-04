<?php
/**
 * Statistics wrapper
 * @author Nuno Tavares <nuno.tavares@wikimedia.pt>
 *
 * Depends on StatsBuilder being run on a daily basis
 */

ini_set('display_errors', 1);
ini_set('error_reporting', E_ALL);


class Statistics {
    static $dbTable = 'statistics';
    var $db = null;
    var $report = array();
    var $axis = array();
    static $fieldPrefix = 'st_';

    var $lastDay = '';
    var $_errorMsg = '';

    var $__bDebug = true;

    static $aItems = array('address', 'address_pct', 'coordinates', 'coordinates_pct', 'image', 'image_pct', 'municipality', 'municipality_pct', 'name', 'name_pct', 'total' );

    function __construct($oDB = null) {
        $this->db = $oDB;
    }


    function debug($msg) {
        if ( $this->__bDebug ) {
            print "[d] ".$msg."\n";
        }
    }

    function getLatestDay() {
        if ( empty($this->lastDay) ) {
            $sql = 'SELECT MAX(day) FROM '.Statistics::$dbTable;
            $res = $this->db->query( $sql );
            $oRes = new ResultWrapper( $this->db, $res );
            $row = $oRes->fetchRow();
            $this->lastDay = $row[0];
        }
        return $this->lastDay;
    }


    // TODO
    function getSanitizedParam($sParam) {
        return isset($_GET[$sParam])?$_GET[$sParam]:false;
    }

    private function setErrorMsg($msg) {
        $this->_errorMsg = $msg;
    }

    public function getErrorMsg() {
        return $this->_errorMsg;
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
            $this->report[$row[$gi]]['lang'] = $country;
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


    function lazyOutput() {
        echo '<table id="chart_'.md5(implode($this->getSanitizedParam('item'))).'">';
        // get columns
        if ( $this->getSanitizedParam('groupby')==='item' ) {
            echo '<tr><th>country</th><th>municipality</th>';
        } else {
            echo '<tr><th>item</th>';
        }
        foreach ($this->axis['columns'] as $col) {
            if ( $this->getSanitizedParam('groupby')==='item' ) {
                $col = substr($col, strlen(Statistics::fieldPrefix));
            }
            echo '<th>'.$col.'</th>';
        }
        echo '</tr>';
        // get rows
        $cl = 'odd';
        foreach ($this->report as $rowitem => $rowdata) {
            if ( $cl == 'odd' ) { 
                $cl = 'even';
            } else {
                $cl = 'odd';
            }
            
            echo '<tr class="'.$cl.'">';
            if ( $this->getSanitizedParam('groupby')==='item' ) {
                list($country,$rowitem) = explode(':', $rowitem, 2);
                echo '<td class="idx">'.$country.'</td>';
            } else {
                $rowitem = substr($rowitem, strlen(Statistics::$fieldPrefix));
            }
            echo '<td class="idx">'.$rowitem.'</td>';
            foreach ($this->axis['columns'] as $i) { // automatic sort
                $suffix = '';
                $tdclass = '';
                if ( (($this->getSanitizedParam('groupby')==='item') and strrpos($i, '_pct'))
                    or (($this->getSanitizedParam('groupby')==='country') and strrpos($rowitem, '_pct')) ) {
                    $suffix = ' %';
                    if ( $this->getSanitizedParam('color') === 'heatpct' ) {
                        $tdclass = ' class="ht'.(intval($rowdata[$i]/10)).'"';
                    }
                }
                echo '<td'.$tdclass.'>'.$rowdata[$i].$suffix.'</td>';
            }
            echo '</tr>';
        }
        print '</table>';
    }

    function getAxis($sAxis) {
        return $this->axis[$sAxis];
    }

    function output() {
        $this->retrieveReport();
        $this->lazyOutput();
    }

}
