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
require dirname(dirname( __FILE__ )) . '/api/includes/Defaults.php';
require_once( dirname( dirname( dirname( __FILE__ ) ) ) . '/database.inc' );

ini_set('display_errors', 1);
ini_set('error_reporting', E_ALL);

// This script is not intended to be run from an HTTP request
if (!defined('STDIN')) {
	print "This script is not intended to be run from an HTTP request.\n";
	die(0);
}

Database::define($dbServer, $dbDatabase, $dbUser,
	isset( $toolserver_password )? $toolserver_password : $dbPassword );



$stb = new StatsBuilder( Database::getDb() );
if ( !$stb->buildReport() ) {
    print $stb->getErrorMsg()."\n";
    die(0);
}
$stb->storeReport();
$stb->debug('Memory usage: '.memory_get_peak_usage());
$stb->debug('exiting...');

