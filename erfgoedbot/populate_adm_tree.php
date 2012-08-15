<?php
/**
 * A script to populate the admin_tree table
 *
 * This is a helluva lot faster than attempting to insert all the data using
 * complex MySQL queries. With VERBOSE == false, this inserts all the data
 * on my test instance in about 10s as opposed to... a lot more.
 *
 * @author Arthur Richards <arichards@wikimedia.org>
 */

if ( php_sapi_name() != 'cli' ) {
	die( 'This is a command-line script' );
}

error_reporting( E_ALL | E_STRICT );
ini_set( 'display_errors', 1 );

ini_set( 'memory_limit', '200M' );

// set to true for verbose output
define( 'VERBOSE', false );

$t0 = microtime( true );
require_once( dirname( dirname( __FILE__ ) ) . '/api/includes/Defaults.php' );
require_once( dirname( dirname( dirname( __FILE__ ) ) ) . '/database.inc' );

// make the db connection, check for errors
$db = new mysqli( $dbServer, $dbUser, $dbPassword, $dbDatabase );
if ( $db->connect_errno ) {
	die( "db connection failed: {$db->connect_error}\n" );
}

echo "Deleting previous data...\n";
$query = 'DELETE FROM `admin_tree`';
$db->query( $query );
handleDbError( $query );

echo "Rebuilding table...\n";
// build a data structure of unique admin values and their parents. store them as keys for easy retrieval.
$admin_levels = array();
$monuments_query = "SELECT `lang`, `adm0`, `adm1`, `adm2`, `adm3`, `adm4` FROM `monuments_all`";
if ( $result = $db->query( $monuments_query ) ) {
	while ( $row = $result->fetch_object() ) {
		$adm0 = trim( $row->adm0 );
		$lang = $row->lang;
		if ( !isset( $admin_levels[$lang] ) ) {
			$admin_levels[$lang] = array();
		}
		if ( !isset( $admin_levels[$lang][$adm0] ) ) {
			$admin_levels[$lang][$adm0] = array();
		}
		if ( $row->adm1 ) {
			$adm1 = trim( $row->adm1 );
			if ( !isset( $admin_levels[$lang][$adm0][$adm1] ) ) {
				$admin_levels[$lang][$adm0][$adm1] = array();
			}
			if ( $row->adm2 ) {
				$adm2 = trim( $row->adm2 );
				if ( !isset( $admin_levels[$lang][$adm0][$adm1][$adm2] ) ) {
					$admin_levels[$lang][$adm0][$adm1][$adm2] = array();
				}
				if ( $row->adm3 ) {
					$adm3 = trim( $row->adm3 );
					if ( !isset( $admin_levels[$lang][$adm0][$adm1][$adm2][$adm3] ) ) {
						$admin_levels[$lang][$adm0][$adm1][$adm2][$adm3] = array();
					}
					if ( $row->adm4 ) {
						$adm4 = trim( $row->adm4 );
						if ( !isset( $admin_levels[$lang][$adm0][$adm1][$adm2][$adm3][$adm4] ) && $adm4 ) {
							$admin_levels[$lang][$adm0][$adm1][$adm2][$adm3][$adm4] = array();
						}
					}
				}
			}
		}
	}
	$result->close();
} else {
	handleDbError( $monuments_query );
}

// loop through each admin level, and store it in the db with appropriate parents
$counter = 0;
$db->query( 'BEGIN' );
foreach ( $admin_levels as $lang => $levels ) {
	foreach ( $levels as $adm0 => $v0 ) {
		$query = "INSERT INTO admin_tree ( `lang`, `level`, `name`, `parent` ) VALUES ( '{$db->real_escape_string( $lang )}',"
			. " 0, '{$db->real_escape_string( $adm0 )}', NULL )";
		out( $query );
		$db->query( $query );
		handleDbError( $query );
		$id0 = $db->insert_id;
		newRow();
		foreach ( $v0 as $adm1 => $v1 ) {
			$id1 = insert_sub_adm( $lang, 1, $adm1, $id0 );
			newRow();

			foreach ( $v1 as $adm2 => $v2 ) {
				$id2 = insert_sub_adm( $lang, 2, $adm2, $id1 );
				newRow();

				foreach ( $v2 as $adm3 => $v3 ) {
					$id3 = insert_sub_adm( $lang, 3, $adm3, $id2 );
					newRow();

					foreach ( $v3 as $adm4 => $v4 ) {
						insert_sub_adm( $lang, 4, $adm4, $id3 );
						newRow();
					}
				}
			}
		}
	}
}
$db->query( 'COMMIT' );
mysqli_close( $db );
$t1 = microtime( true );
$t = $t1 - $t0;
echo "Inserted $counter admin zones in $t seconds.\n";

/**
 * Insert an admin level > 0 to the db
 *
 * @param $lang string Language code
 * @param $level int
 * @param $adm string The name of the admin level
 * @param $parentId int The row id of the admin level's parent
 *
 * @return int The row id of the inserted admin level
 */
function insert_sub_adm( $lang, $level, $adm, $parentId ) {
	global $db;
	$query = "INSERT INTO admin_tree ( `lang`, `level`, `name`, `parent` ) VALUES ( '{$db->real_escape_string( $lang )}',"
		. " {$level}, '{$db->real_escape_string( $adm )}', {$parentId} )";
	out( $query );
	$db->query( $query );
	handleDbError( $query );
	return $db->insert_id;
}

/**
 * Helper function for verbose output.
 */
function out( $str ) {
	if ( VERBOSE ) echo $str . "\n";
}

/**
 * Helper function for handling MySQL errors
 */
function handleDbError( $query ) {
	global $db;
	if ( $db->errno ) {
		die( "MySQL error: {$db->error}\nQuery: {$query}\n" );
	}
}

function newRow() {
	global $counter, $db;

	if ( ++$counter % 500 == 0 ) {
		$db->query( 'COMMIT' );
		$db->query( 'BEGIN' );
	}
}
