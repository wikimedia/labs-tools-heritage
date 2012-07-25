<?php
error_reporting(E_ALL);
ini_set('display_errors', true);
ini_set('html_errors', false);

require dirname( __FILE__ ) . '/clsBasicGeosearch.php';

require_once dirname( dirname( __FILE__ ) ) . '/public_html/api/includes/Defaults.php';
require_once dirname( dirname( __FILE__ ) ) . '/database.inc';
require dirname( dirname( __FILE__ ) ) . '/public_html/api/autoloader.php';

$dbStatus = Database::define($dbServer, $dbDatabase, $dbUser, $dbPassword );
if (!$dbStatus) {
    die( "Coudn't connect to db! ". mysql_error() );
}


$db = Database::getDb();
$db->query( "SET NAMES 'utf8' COLLATE 'utf8_unicode_ci'" ); // Force utf8_unicode_ci collation


$bg = new clsBasicGeosearch();

$query = "SELECT `country`, `lang`, `id`, `lat`, `lon`
       FROM `monuments_all`
       WHERE `lat` IS NOT NULL
GROUP BY `country`, `id`";



$result = $db->query($query);
if (!$result) 
{
  die('Invalid query: ' . mysql_error());
}
$result = new ResultWrapper( $db, $result );

foreach ($result as $row) {

	if ( $row->lat >= -90 and $row->lat <= 90 and 
	     $row->lon >= -180 and $row->lon <= 180 ) {
		 
		$peano1 = $bg->generate_peano1($row->lat, $row->lon);	
		$peano2 = $bg->generate_peano2($row->lat, $row->lon);
		$peano1iv = $bg->generate_peano_iv($peano1);
		$peano2iv = $bg->generate_peano_iv($peano2);
		
		$r_result = $db->replace( 'prox_search', array(
										'mon_country' => $row->country,
										'mon_lang' => $row->lang,
										'mon_id' => $row->id,
										'lat' => $row->lat,
										'lon' => $row->lon,
										'int_peano1' => $peano1,
										'int_peano2' => $peano1,
										'int_peano1iv' => $peano1iv,
										'int_peano2iv' => $peano2iv
									) );

		if (!$r_result) {
			die('Invalid query: ' . mysql_error());
		}
	} else {
		echo('Location data out of range: ');
		print_r($row);
	}
}
