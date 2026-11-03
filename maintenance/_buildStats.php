<?php
/**
 * Statistics wrapper
 * @author Nuno Tavares <nuno.tavares@wikimedia.pt>
 *
 * Needs the DB table and adjustments described in INSTALL
 *
 * May be optimized by INSERTing in batches
 */

require __DIR__ . '/bootstrap.php';

$stb = new StatsBuilder( Database::getDb() );
if ( !$stb->buildReport() ) {
	print $stb->getErrorMsg() . "\n";
	die( 0 );
}
$stb->storeReport();
$stb->debug( 'Memory usage: ' . memory_get_peak_usage() );
$stb->debug( 'exiting...' );
