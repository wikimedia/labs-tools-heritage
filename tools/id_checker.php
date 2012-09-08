<?php
error_reporting(E_ALL); 
ini_set('display_errors', true);
ini_set('html_errors', false);

require_once '/home/project/e/r/f/erfgoed/public_html/api/includes/Defaults.php';
require_once '/home/project/e/r/f/erfgoed/database.inc';
require '/home/project/e/r/f/erfgoed/public_html/api/autoloader.php';

$dbStatus = Database::define($dbServer, $dbDatabase, 
	$dbUser, $dbPassword );
if (!$dbStatus) {
    die( "Coudn't connect to db! ". mysql_error() );
}
	$db = Database::getDb();
    
header ('Content-type: text/html; charset=utf-8');
$dupe_limit = 1000;

if (isset($_GET["country"]) AND isset($_GET["lang"])) {
	$country = $_GET["country"];
	$lang = $_GET["lang"];

	$date = '';
	$qres = $db->select( array( 'changed' ), 'id_dump', array( 'country' => $country, 'lang' => $lang ), false, 1);
	foreach ( $qres as $row ) {
		$date = $row->changed;
	}

	print '<h1>Duplicate IDs in wikilists, as of '. $date .', with limit '. $dupe_limit .'</h1>';
	print '<table>';
	$sql = sprintf("SELECT count(*) AS count, id FROM `id_dump` WHERE (`country` = %s AND `lang`=%s) GROUP BY id HAVING count>1 ORDER BY `id_dump`.`id` ASC LIMIT %s",
                 $db->quote( $country ),
                 $db->quote( $lang ),
				 $dupe_limit);
	$qres = new ResultWrapper( $db, $db->query( $sql ) );

	foreach ( $qres as $row ) {
		print '<tr><td>' . htmlspecialchars( $row->id ) . '</td><td></td></tr>';

		$dres = $db->select( array( 'source' ), 'id_dump', array( 'country' => $country, 'lang' => $lang, 'id' => $row->id ) );
		foreach ( $dres as $drow ) {
			print '<tr><td></td><td><a href="'. htmlspecialchars( $drow->source ) .'">' . htmlspecialchars( $drow->source ) . '</a></td></tr>';
		}
	}
	print '</table>';

} else {
	$sql = "SELECT DISTINCT `country`, `lang` FROM `id_dump`";
	$qres = new ResultWrapper( $db, $db->query( $sql ) );
	foreach ( $qres as $row ) {
		print '* <a href="id_checker.php?country=' . htmlspecialchars( $row->country ) . '&lang=' . htmlspecialchars( $row->lang ) .'">'. htmlspecialchars( $row->country ) . ' ('. htmlspecialchars( $row->lang ) . ')</a><br/>';
	}

}


