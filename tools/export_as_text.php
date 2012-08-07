<?php
if ( php_sapi_name() != 'cli' ) {
	die( 'This is a command-line script' );
}

error_reporting( E_ALL | E_STRICT );
ini_set( 'display_errors', 1 );

ini_set( 'memory_limit', '200M' );

$t0 = microtime( true );
require_once( dirname( dirname( __FILE__ ) ) . '/api/includes/Defaults.php' );
require_once( dirname( dirname( dirname( __FILE__ ) ) ) . '/database.inc' );

// make the db connection, check for errors
$db = new mysqli( $dbServer, $dbUser, $dbPassword, $dbDatabase );
$db->query( 'SET NAMES UTF8' );
if ( $db->connect_errno ) {
	error( "db connection failed: {$db->connect_error}" );
}

if ( count( $argv ) < 2 ) {
	error( 'Usage: php export_as_text.php <table name>' );
}

$table = $argv[1];

$query = "SELECT * FROM `$table`";
$res = $db->query( $query );
handleDbError( $query );
while ( $row = $res->fetch_assoc() ) {
	$columns = 0;
	foreach( $row as $value ) {
		if ( $columns++ ) {
			echo "\t";
		}
		$value = strtr( $value, "\r\n\t", "   " );
		echo $value;
	}
	echo "\n";
}

mysqli_close( $db );


/**
 * Helper function for handling MySQL errors
 */
function handleDbError( $query ) {
	global $db;

	if ( $db->errno ) {
		error( "MySQL error: {$db->error}\nQuery: {$query}" );
	}
}

function error( $message ) {
	fwrite( STDERR, "$message\n" );
	die( 1 );
}
