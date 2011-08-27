<?php
error_reporting(E_ALL); 
ini_set('display_errors', true);
ini_set('html_errors', false);

require_once '/home/project/e/r/f/erfgoed/database.inc';
require '/home/project/e/r/f/erfgoed/public_html/api/autoloader.php';

$dbStatus = Database::define(Monuments::$dbServer, Monuments::$dbDatabase, 
	Monuments::$dbUser, $toolserver_password );
if (!$dbStatus) {
    die( "Coudn't connect to db! ". mysql_error() );
}
	$db = Database::getDb();
    
header ('Content-type: text/html; charset=utf-8');

if (isset($_GET["country"]) AND isset($_GET["lang"])) {
	$country = $_GET["country"];
	$lang = $_GET["lang"];

	$date = '';
	$sql = sprintf("SELECT changed FROM `id_dump` WHERE (`country` = '%s' AND `lang`='%s') LIMIT 1",
                 $country,
                 $lang);
	$qres = new ResultWrapper( $db, $db->query( $sql ) );
	foreach ( $qres as $row ) {
		$date = $row->changed;
	}

	print '<h1>Duplicate IDs in wikilists, as of '. $date .'</h1>';
	print '<table>';
	$sql = sprintf("SELECT count(*) AS count, id FROM `id_dump` WHERE (`country` = '%s' AND `lang`='%s') GROUP BY id HAVING count>1 ORDER BY `id_dump`.`id` ASC LIMIT 1000",
                 $country,
                 $lang);
	$qres = new ResultWrapper( $db, $db->query( $sql ) );

	foreach ( $qres as $row ) {
		print '<tr><td>' . $row->id . '</td><td></td></tr>';
		$dsql = sprintf("SELECT `source` FROM `id_dump` WHERE (`country` = '%s' AND `lang`='%s' AND `id`='%s')",
                 $country,
                 $lang,
                 $row->id);
		$dres = new ResultWrapper( $db, $db->query( $dsql ) );
		foreach ( $dres as $drow ) {
			print '<tr><td></td><td><a href="'. $drow->source .'">' . $drow->source . '</a></td></tr>';
		}
	}
	print '</table>';

} else {
	$sql = "SELECT DISTINCT `country`, `lang` FROM `id_dump`";
	$qres = new ResultWrapper( $db, $db->query( $sql ) );
	foreach ( $qres as $row ) {
		print '* <a href="' . $_SERVER['PHP_SELF'] . '?country=' . $row->country. '&lang=' . $row->lang .'">'. $row->country . ' ('. $row->lang . ')</a><br/>';
	}

}

?>
