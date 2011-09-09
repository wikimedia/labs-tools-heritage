<?php
/**
 * Contest Statistics builder
 * @author Nuno Tavares <nuno.tavares@wikimedia.pt>
 *
 * Needs the DB table and adjustments described in INSTALL
 *
 * NOTE May be optimized by INSERTing in batches
 */


class ContestStatsBuilder extends ContestStatistics {

    var $stats_wlmid_failed = 0;
    var $stats_wlmid_updated = 0;
    var $stats_wlmid_total = 0;

    private $latest_timestamp = '20110901000000';

    private $__mutex = null;
    private $__mutex_file = '/tmp/wlm.contest.lock';
    private $uiFeedback = 15;

    function __construct($oDB = null) {
        parent::__construct($oDB);
    }

    function openExclusiveLock() {
        $this->debug('Opening ExclusiveLock');
        $this->__mutex = @fopen($this->__mutex_file, 'x');
        if ( !$this->__mutex ) {
            return false;
        }
        return true;
    }

    function closeExclusiveLock() {
        @fclose($this->__mutex);
        @unlink($this->__mutex_file);
        return true;
    }

    /**
     * Wipe  statistics table. 
     * TODO This is the lazy approach. We should update it in batches 
     * (eg, WHERE recent.timestamp >= MAX(table))
     * @return the MAX(img_timestamp) found (before being deleted)
     */
    private function clearLatestData_() {
        $this->debug('Clearing latest stats.');
        $sql = 'TRUNCATE TABLE '.ContestStatistics::$dbTable;
        $this->db->query($sql);
    }

    /*private*/ function clearLatestData() {
        $this->debug('Clearing latest stats.');
        $sql = 'SELECT MAX(img_timestamp) AS latest_ts FROM '.ContestStatistics::$dbTable;
        $oRes = new ResultWrapper( $this->db, $this->db->query($sql) );
        if ( !$oRes ) {
            $this->setErrorMsg("ERROR: Problems getting MAX(img_timestamp)");
            return false;
        }
        if ( $oRes->numRows()<=0 ) {
            // table empty?
            $this->latest_timestamp = '20110901000000';
            return '20110901000000';
        }
        $row = $oRes->fetchAssoc();
        $this->latest_timestamp = $row['latest_ts'];
        if ( empty($this->latest_timestamp) ) {
            $this->debug('Weird.. no rows with MAX(img_timestamp)?');
            $this->latest_timestamp = '20110901000000';
            return '20110901000000';
        }
        $this->debug('Clearing data from: '.$this->latest_timestamp);
        $sql = 'DELETE FROM '.ContestStatistics::$dbTable.' WHERE img_timestamp >= '.$this->latest_timestamp;
        $this->db->query($sql);
        if ( $this->db->getAffectedRows()<=0 ) {
            $this->debug('Weird.. no deleted rows >= '.$this->latest_timestamp.'?');
        }
    }

    function getLatestTimestamp() {
        return $this->latest_timestamp;
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



    public function updateEntry($img_name, $wlm_id) {
        $sql = 'UPDATE '.ContestStatistics::$dbTable.'
            SET img_wlm_id = '.$wlm_id.'
            WHERE img_name = "'.$img_name.'"';
        //$this->debug($sql);
        $this->db->query($sql);
        if ( $this->db->getAffectedRows()<=0 ) {
            $this->stats_wlmid_failed++;
            $this->debug('WARNING: missed update for entry: '.$img_name);
        }
        $this->stats_wlmid_updated++;
    }

    public function updateWlmEmptyIds() {
        $this->debug('updateWlmEmptyIds(): start');
        $availcountries = implode('", "', array_keys(WlmIdHelper::$wlmids));
        $sql = 'SELECT img_name AS img_name,img_wlm_country
            FROM '.ContestStatistics::$dbTable.'
            WHERE img_wlm_id = ""
                AND img_wlm_country IN ("'.$availcountries.'")';
        $oRes = new ResultWrapper( $this->db, $this->db->query($sql) );
        if ( !$oRes ) {
            $this->setErrorMsg("ERROR: failed to load empty WLM IDs -- ".$sql);
            return false;
        }
        $wih = new WlmIdHelper();
        $count = 0;
        while ( $row = $oRes->fetchAssoc() ) {
            $this->stats_wlmid_total++;
            $wlm_id = $wih->parseWlmId($row['img_name'], $row['img_wlm_country']);
            if ( $wlm_id ) {
                $this->updateEntry($row['img_name'], $wlm_id);
            } else {
                $this->stats_wlmid_failed++;
                $this->debug('Failed to get ID for: '.$row['img_name']);
                print 'X';
            }
            if ( ++$count % $this->uiFeedback == 0 ) { print '.'; }
        }
        print "\n";
        return true;
    }


    public function buildReport() {
        $this->debug('buildReport(): start');
        $sql = 'SELECT i.img_name AS img_name
                , u.user_id AS img_user_id
                , u.user_name AS img_user_name
                , p.page_id AS img_page_id
                , SUBSTR(cl2.cl_to, 42) AS img_wlm_country
                , i.img_timestamp AS img_timestamp
                , INSTR(GROUP_CONCAT(DISTINCT ug.ug_group), "bot") AS found_bot
            FROM categorylinks cl 
            /* get country category - there can/must be only one */
            LEFT JOIN categorylinks cl2 ON cl2.cl_from = cl.cl_from
                AND cl2.cl_to LIKE "Images_from_Wiki_Loves_Monuments_2011_in_%"
            /* resolve mw info */
            JOIN page p ON cl.cl_from = p.page_id 
                AND p.page_namespace = 6 
                AND p.page_is_redirect = 0
            /* resolve img details */
            JOIN image i ON i.img_name = p.page_title 
                AND i.img_timestamp >= '.$this->latest_timestamp.'
            JOIN user u ON u.user_id = i.img_user
            /* exclude bots: they are probably the last uploaders on a WLM photo.. */
            LEFT JOIN user_groups ug ON ug.ug_user = u.user_id

            WHERE cl.cl_to = "Images_from_Wiki_Loves_Monuments_2011"
            GROUP BY i.img_name
            HAVING found_bot <= 0 OR found_bot IS NULL
            ORDER BY i.img_timestamp';

        $oRes = new ResultWrapper( $this->db, $this->db->query($sql) );
        if ( !$oRes ) {
	        $this->setErrorMsg("ERROR: failed to get bulk data: ".$this->db->getDBError());
            return false;
        }

        while ( $row = $oRes->fetchAssoc() ) {
                $this->report[] = $row;
        }
 
        return true;
    }


    public function printStats() {
        print 'Pending: '.$this->stats_wlmid_total."\n";
        print 'Failed: '.$this->stats_wlmid_failed."\n";
        print 'Updated: '.$this->stats_wlmid_updated."\n";
    }

    /** 
     * Store report 
     */
    public function storeReport() {
        $this->debug('storeReport(): start');

        for($i=0;$i<count($this->report);$i++) {
            $row = $this->report[$i];
            $sql = 'INSERT INTO '.ContestStatistics::$dbTable.'(img_name,img_user_id,img_user_name,img_page_id,img_wlm_country,img_timestamp)
            VALUES("'.$this->db->sanitize($row['img_name']).'"
                , "'.$row['img_user_id'].'"
                , "'.$this->db->sanitize($row['img_user_name']).'"
                , "'.$row['img_page_id'].'"
                , "'.$this->db->sanitize($row['img_wlm_country']).'"
                , "'.$row['img_timestamp'].'"
                /* found_bot='.$row['found_bot'].' */
                )';
            //$this->debug( "SQL $sql" );
            //$this->debug('ID: '.$row['img_page_id'].' -- IMG: '.$row['img_name']);
            $oRes = $this->db->query($sql);
            if ( !$oRes ) {
                $this->setErrorMsg('ERROR: failed to store bulk data at line: '.$i.' -- '.$sql.';; Database says: '.$this->db->getDBError());
                return false;
            }
            if ( $i % $this->uiFeedback == 0 ) { print '.'; }
        }
        print "\n";
        $this->debug('Records: '.$i);
        return true;
    }

}

