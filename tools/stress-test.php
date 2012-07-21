<?php

if ( php_sapi_name() != 'cli' ) {
	die( 'This is a command-line script.' );
}

ini_set( 'user_agent', 'WLM stress test by MaxSem' );

$countries = array(
	'ad',
	'at',
	'be-bru',
	'be-vlg',
	'be-wal',
	'ch',
	'dk-bygning',
	'dk-fortids',
	'ee',
	'es',
	'es-ct',
	'es-vc',
	'fr',
	'ie',
	'it-88',
	'it-bz',
	'lu',
	'mt',
	'nl',
	'no',
	'pl',
	'pt',
	'sct',
	'se',
	'sk',
	'us',
);

$searchTerms = array(
	'house',
	'casa',
	'city',
);

$site = 'http://toolserver.org/~erfgoed/api/';
$site = 'http://mobile-wlm.wmflabs.org/api/';
//$site = 'http://localhost/wlm/api/';
$site .= 'api.php?action=search&format=json';

echo "Started stress test, press Ctrl + Break to stop\n";
$timings = array();
$averagingFactor = 10;

while ( true ) {
	switch ( mt_rand( 0, 2 ) ) {
		case 0:
			$i = array_rand( $countries );
			$url = "{$site}&srcountry={$countries[$i]}";
			break;
		case 1:
			$i = array_rand( $searchTerms );
			// add a random search term to prevent query caching
			$url = "{$site}&srname=~+{$searchTerms[$i]}%20" . mt_rand( 0, 1000000 );
			break;
		case 2:
			// generate a coordinate 2 degrees around London
			$lat = 51.5 + mt_rand( -1000, 1000 ) / 1000;
			$lon = mt_rand( -1000, 1000 ) / 1000;
			$url = "{$site}&bbox=" . ( $lon - 0.099 ) . ',' . ( $lat - 0.099 ) . ',' . ( $lon + 0.099 ) . ',' . ( $lat + 0.099 );
			break;
	}

	echo "$url\n";
	$time = microtime( true );
	$result = file_get_contents( $url );
	$time = microtime( true ) - $time;
	array_push( $timings, $time );
	if ( count( $timings ) > $averagingFactor ) {
		array_shift( $timings );
	}
	$average = round( array_sum( $timings ) / count( $timings ), 1 );
	$time = round( $time, 1 );
	$result = json_decode( $result );
	$count = isset( $result->monuments ) ? count( $result->monuments ) : 0;
	$error = isset( $result->errors ) ? ', errors: ' . implode( "; ", $result->errors ) : '';
	echo "$time s (avearge = $average), monuments returned = {$count}{$error}\n";
}
