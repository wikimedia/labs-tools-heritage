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
    static $dbTable = 'statisticsct';
    var $report = array();


    function retrieveReport() {
    }



}
