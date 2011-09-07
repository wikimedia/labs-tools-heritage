<?php
/**
 * Statistics base class
 * @author Nuno Tavares <nuno.tavares@wikimedia.pt>
 *
 * Wraps commons functions shared by statistics builders
 */

ini_set('display_errors', 1);
ini_set('error_reporting', E_ALL);


class StatisticsBase {
    var $db = null;

    var $_errorMsg = '';

    var $__bDebug = true;


    function __construct($oDB = null) {
        $this->db = $oDB;
    }


    function debug($msg) {
        if ( $this->__bDebug ) {
            print "[d] ".$msg."\n";
        }
    }



    // TODO
    function getSanitizedParam($sParam) {
        return isset($_GET[$sParam])?$_GET[$sParam]:false;
    }

    protected function setErrorMsg($msg) {
        $this->_errorMsg = $msg;
    }

    public function getErrorMsg() {
        return $this->_errorMsg;
    }


}
