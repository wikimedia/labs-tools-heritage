<?php
error_reporting( E_ALL );
ini_set( 'display_errors', true );
ini_set( 'html_errors', false );

require_once dirname( __DIR__ ) . '/api/common.php';
require_once ( '/api/includes/CommonFunctions.php' );

$db = Database::getDb();
print '<html>';
print '<head>
<title>Monuments database ID checker</title>
<style>
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
th, td {
    padding: 5px;
    text-align: left;
}
</style>
</head>';
print '<body>';
$dupe_limit = 1000;

if ( isset( $_GET["country"] ) and isset( $_GET["lang"] ) ) {
	$country = $_GET["country"];
	$lang = $_GET["lang"];

	$date = '';
	$qres = $db->select( [ 'changed' ], 'id_dump', [ 'country' => $country, 'lang' => $lang ], false, 1 );
	foreach ( $qres as $row ) {
		$date = $row->changed;
	}

	print '<h1>Duplicate IDs in wikilists, as of '. $date .', with limit '. $dupe_limit .'</h1>';
	print '<table>';
	print '<tr id="header">
	<th>' . _i18n( 'db-field-id' ) . '</th>
	<th>' . _i18n( 'db-field-source' ) . '</th>
	</tr>';
	$sql = sprintf( "SELECT count(*) AS count, id FROM `id_dump` WHERE (`country` = %s AND `lang`=%s) GROUP BY id HAVING count>1 ORDER BY `id_dump`.`id` ASC LIMIT %s",
				 $db->quote( $country ),
				 $db->quote( $lang ),
				 $dupe_limit );
	$qres = new ResultWrapper( $db, $db->query( $sql ) );

	foreach ( $qres as $row ) {
		$dres = $db->select( [ 'source' ], 'id_dump', [ 'country' => $country, 'lang' => $lang, 'id' => $row->id ] );
		$count = $dres->numRows();
		print '<tr>
			<td rowspan="' . ( $count + 1 ) . '">' . htmlspecialchars( $row->id ) . '</td>
			<td></td>
		</tr>';
		foreach ( $dres as $drow ) {
			$m = matchWikiprojectLink( $drow->source );
			$linkText = str_replace( '_', ' ', $m[5] );
			$encodedLink = urlencodeWikiprojectLink( $m );
			print '<tr>
				<td><a href="'. htmlspecialchars( $encodedLink ) .'">' . htmlspecialchars( $linkText ) . '</a></td>
			</tr>';
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
print '</body>';
print '</html>';
