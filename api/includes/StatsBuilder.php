<?php
/**
 * Statistics builder
 * @author Nuno Tavares <nuno.tavares@wikimedia.pt>
 *
 * Needs the DB table and adjustments described in INSTALL
 *
 * NOTE May be optimized by INSERTing in batches
 */


/*
*
* Needs table to store:
*  CREATE TABLE `statistics` (
  `day` date NOT NULL,
  `item` varchar(50) NOT NULL,
  `idx` varchar(100) NOT NULL,
  `value` varchar(16) NOT NULL DEFAULT '0',
  PRIMARY KEY (`day`,`item`,`idx`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


ALTER TABLE monuments_all ADD INDEX idx_ctry_municp(country,municipality);

ALTER TABLE statistics ADD INDEX idx_day_idx(day,idx);

*/

class StatsBuilder extends Statistics {
    var $aFields = null; // built on constructor, to allow Statistics::$fieldPrefix

    /** Indicates where report should be built in RAM
    * true - more RAM, but traceable;
    * false - much less RAM, no traceability, not necessarily faster?
    */
    static $bBuildInRAM = true;  

    function __construct($oDB = null) {
        parent::__construct($oDB);
        $this->aFields = array(
            'name' => array( 'type' => 'string', 'report_as' => Statistics::$fieldPrefix.'name' ),
            'address' => array( 'type' => 'string', 'report_as' => Statistics::$fieldPrefix.'address' ),
            'municipality' => array( 'type' => 'string', 'report_as' => Statistics::$fieldPrefix.'municipality' ),
            'image' => array( 'type' => 'string', 'report_as' => Statistics::$fieldPrefix.'image' ),
            'coordinates' => array( 'type' => 'latlon', 'report_as' => Statistics::$fieldPrefix.'coordinates' ),
        );
        ini_set('memory_limit', '256M');
    }

    function storeValue($item,$index,$value) {
	    //$this->debug($item."[$index] = ".$value);

        // NOTE http://dev.mysql.com/doc/refman/5.5/en/insert-delayed.html
        //   INSERT DELAYED should be used only for INSERT statements that specify value lists. 
        //   The server ignores DELAYED for INSERT ... SELECT or INSERT ... ON DUPLICATE KEY UPDATE statements.
        // Anyway, from the benchmarks, there was no actual gain.
	    $sql = 'INSERT INTO '.Statistics::$dbTable.' VALUES("'.$this->getLatestDay().'","'.$item.'","'.$index.'","'.$value.'") ON DUPLICATE KEY UPDATE value = "'.$value.'"';
        //$this->debug("  + SQL: $sql");
	    return $this->db->query($sql);
    }


    /**
     * Wipe "Latest Day" statistics (removing changing) 
     */
    private function clearLatestData() {
        $this->debug('Clearing latest stats: '.$this->getLatestDay());
        $sql = 'DELETE FROM '.Statistics::$dbTable.' WHERE day = "'.$this->getLatestDay().'"';
        $this->db->query($sql);
    }


    /** Helper to fix encoding
    */
    static function fixEncoding($sString, $bToUTF8=true) {
        /*
        if ( $bToUTF8 ) {
            return utf8_encode($sString);
        }
        */
        return $sString;
    }


    /** Calculate totals 
     * @return false on error, true otherwise
     */
    private function getTotals() {
        $this->debug('Determining Totals');
        $sql = 'SELECT country, municipality, COUNT(1) AS total
            FROM '.Monuments::$dbTable.'
            GROUP BY country, municipality';
        $wres = new ResultWrapper( $this->db, $this->db->query( $sql ) );
        if ( !$wres ) {
	        return false;
        } 
        
        while ($row = $wres->fetchRow()) {
            $idx = $this->db->sanitize($row[0].':'.StatsBuilder::fixEncoding($row[1], true));
            $this->setReportItem(Statistics::$fieldPrefix.'total', $idx, $row[2]);
        }
        return true;
    }

    private function getFilterForField($field) {
        switch($this->aFields[$field]['type']) {
        case 'latlon': 
            $filter = 'lat <> 0 AND lon <> 0';
            break;
        default: /* 'string' */
            $filter = $field.' IS NOT NULL AND LENGTH(TRIM('.$field.')) > 0';
            break;
        }
        return $filter;
    }


    private function getFieldStats($field) {

        $filter = $this->getFilterForField($field);
        $report_as = $this->aFields[$field]['report_as'];

        $tmp_table = 'tmp_'.$field;

        $sql = 'CREATE TEMPORARY TABLE '.$tmp_table.'
            SELECT country, municipality, count(1) as non_blank
            FROM '.Monuments::$dbTable.'
            WHERE '.$filter.'
            GROUP BY country, municipality';
        $this->db->query($sql);

        $sql = 'ALTER TABLE '.$tmp_table.' ADD UNIQUE INDEX idx1(country,municipality)';
        $this->db->query($sql);

        $sql = 'SELECT m1.country, m1.municipality, IF(m2.non_blank IS NULL,0,m2.non_blank) AS non_blank
          FROM '.Monuments::$dbTable.' m1
          LEFT JOIN '.$tmp_table.' m2 ON m2.country = m1.country AND m2.municipality = m1.municipality
          GROUP BY m1.country, m1.municipality';
        $oRes = new ResultWrapper( $this->db, $this->db->query($sql) );
        if ( !$oRes ) {
	        $this->setErrorMsg("ERROR: failed to get total:".$field);
            return false;
        }

        while ( $row = $oRes->fetchRow() ) {
	        $idx = $row[0].':'.$this->db->sanitize(StatsBuilder::fixEncoding($row[1],true));
            $this->setReportItem($report_as, $idx, $row[2]);
            $value_pct = sprintf("%.2f", 100*$row[2]/$this->report[Statistics::$fieldPrefix.'total'][$idx]);
	        $this->setReportItem($report_as.'_pct', $idx, $value_pct);
        }
        return true;
    }


    /** Helper - to simplify direct database loading
     * NOTE: remember to keep a copy of 'totals' in $this->report;
     */
    public function setReportItem($item, $idx, $value) {
        //$this->debug('REPORT['.$item.']['.$idx.'] = '.$value);
        // we will need the totals in RAM anyway
        if ( ($item === Statistics::$fieldPrefix.'total') or StatsBuilder::$bBuildInRAM ) {
            $this->report[$item][$idx] = $value;
        }

        if ( !StatsBuilder::$bBuildInRAM ) {        
            $this->storeValue($item,$idx,$value);
        }
    }


    public function buildReport() {
        $nTimeStart = time();
        $this->debug('buildReport(): start');
        $this->clearLatestData();
        if ( !$this->getTotals() ) {
            $this->setErrorMsg("ERROR: failed to get totals");
            return false;
        }
        foreach ($this->aFields as $field => $fdata) {
            $this->debug(' + Building report for field: '.$field);
            $nTimeStart2 = time();
            $this->getFieldStats($field);
            $nTimeEnd2 = time();
            $this->debug('   - Time elapsed: '.($nTimeEnd2 - $nTimeStart2).' seconds.');
        }
        $nTimeEnd = time();
        $this->debug(' - Time elapsed: '.($nTimeEnd - $nTimeStart).' seconds.');
        return true;
    }


    /** 
     * Store report 
     */
    public function storeReport() {
        $nTimeStart = time();
        $this->debug('storeReport(): start');
        if ( StatsBuilder::$bBuildInRAM ) {
            foreach ($this->report as $item => $table) {
                $this->debug(' + Storing report for item: '.$item);
	            foreach ($table as $idx => $val) {
		            if ( !$this->storeValue($item,$idx,$val) ) {
                        return false;
                    }
                }
            }
        }
        $nTimeEnd = time();
        $this->debug(' - Time elapsed: '.($nTimeEnd - $nTimeStart).' seconds.');
    }

}

