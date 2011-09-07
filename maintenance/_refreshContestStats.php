<?php
/**
 * Statistics wrapper
 * @author Nuno Tavares <nuno.tavares@wikimedia.pt>
 *
 * Needs the DB table and adjustments described in INSTALL
 *
 * May be optimized by INSERTing in batches
 */

require_once( dirname(dirname( __FILE__ )) . '/api/autoloader.php' );
require_once( dirname( dirname( dirname( __FILE__ ) ) ) . '/database.inc' );

ini_set('display_errors', 1);
ini_set('error_reporting', E_ALL);

// This script is not intended to be run from an HTTP request
if (!defined('STDIN')) {
	print "This script is not intended to be run from an HTTP request.\n";
	die(0);
}



DatabaseExt::initialize(Monuments::$dbServer, Monuments::$dbDatabase, 
	Monuments::$dbUser, $toolserver_password, 'latin1' );

$stb = new ContestStatsBuilder( DatabaseExt::getDb() );
if ( !$stb->openExclusiveLock() ) {
    print "Exclusive Lock active: it seems there is one instance running already\n";
    die(0);
}
$stb->clearLatestData();
$stb->debug('Resuming update from: '.$stb->getLatestTimestamp());

DatabaseExt::initialize(CommonsDB::$dbServer, CommonsDB::$dbDatabase, 
	CommonsDB::$dbUser, $toolserver_password, 'latin1' );

if ( !$stb->buildReport() ) {
    print $stb->getErrorMsg()."\n";
    die(0);
}

DatabaseExt::getDb()->setCurSlot(0);

if ( !$stb->storeReport() ) {
    print $stb->getErrorMsg()."\n";
    die(0);
}

$stb->debug('Memory usage: '.memory_get_peak_usage());

if ( !$stb->updateWlmEmptyIds() ) {
    print $stb->getErrorMsg()."\n";
    die(0);
}
$stb->printStats();
$stb->closeExclusiveLock();

