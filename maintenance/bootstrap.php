<?php
/**
 * Shared setup for the maintenance scripts: refuses HTTP requests, shows all
 * errors (so they reach the job logs), loads the configuration and connects
 * to the monuments database.
 *
 * Include it at the top level of a script, so that the configuration
 * variables end up as globals.
 */

if ( !defined( 'STDIN' ) ) {
	print "This script is not intended to be run from an HTTP request.\n";
	die( 0 );
}

ini_set( 'display_errors', 1 );
ini_set( 'error_reporting', E_ALL );

require_once dirname( __DIR__ ) . '/api/autoloader.php';
require dirname( __DIR__ ) . '/api/includes/Defaults.php';
require_once dirname( dirname( __DIR__ ) ) . '/database.inc';

Database::define( $dbServer, $dbDatabase, $dbUser, $toolserver_password ?? $dbPassword );
