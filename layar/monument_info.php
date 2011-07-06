<?php
/*
 * Summary info for a monument, referenced from Layar app
 * monument_info?country=&lang=&id=
 */


error_reporting(E_ALL); 
ini_set('display_errors', true);
ini_set('html_errors', false);

require dirname( dirname( __FILE__ ) ) . '/api/autoloader.php';
require dirname( dirname( dirname( __FILE__ ) ) ) . '/database.inc';
require_once( dirname( dirname( __FILE__ ) ) . '/api/includes/CommonFunctions.php' );

//uses id field from monuments_all table
function getRegistrantUrl($lang, $monumentId) {
	$registrant_url = array(
	"et" => "http://register.muinas.ee/?menuID=monument&action=view&id=", 
	"fr" => "http://www.culture.gouv.fr/public/mistral/merimee_fr?ACTION=CHERCHER&FIELD_1=REF&VALUE_1=",
	"nl" => "http://www.kich.nl/kich2010/rapport.jsp?id_qualifier=ODB:Rijksmonumentnr&id="
	);
	$outUrl = '';
	
	if ( isset($registrant_url[$lang] ) ) {
		$outUrl = $registrant_url[$lang] . $monumentId;
		return $outUrl;
	}
	
	return $outUrl;
}

//main

if (isset($_GET["country"]) AND isset($_GET["lang"]) AND isset($_GET["id"]) ) {

	$country = $_GET["country"];
	$lang = $_GET["lang"];
	$id = $_GET["id"];

	header ('Content-type: text/html; charset=utf-8');
	
	$dbStatus = Database::define(Monuments::$dbServer, Monuments::$dbDatabase, 
	Monuments::$dbUser, $toolserver_password );
	if (!$dbStatus) {
		die( "Coudn't connect to db! ". mysql_error() );
	}	


    $db = Database::getDb();
    $sql = "SELECT * FROM " . $db->escapeIdentifier( Monuments::$dbTable ) . 
	    " WHERE country=" . $db->quote( $country ) . " AND lang=". $db->quote( $lang ) . " AND id=". $db->quote( $id );
    $qres = new ResultWrapper( $db, $db->query( $sql ) );
    $desc = '';
    foreach ( $qres as $row ) {
	
			$title = '';
			if ( isset($row->name) and $row->name ) {
				$title = processWikitext('', $row->name, false);
			}
			
			$desc .= '<html>
<head>
	<title>'. $title .'</title>
</head>
<body>';
            if ( isset($row->image) and $row->image ) {
                $imgsize = 100;
                $desc .= '<a href="http://commons.wikimedia.org/wiki/File:' . rawurlencode($row->image) . '">';
                $desc .= '<img src="' . getImageFromCommons($row->image, $imgsize) . '" align="right" />';
                $desc .= '</a>';
            }

            $makeLinks = true;
			$desc .= '<h2>'. processWikitext($row->lang, $row->name, $makeLinks) . '</h2>';
            $desc .= '<ul>';
			if ($row->address) {
				$desc .= '<li>address: ' . processWikitext($row->lang, $row->address, $makeLinks). '</li>';
			}
			if ($row->municipality) {
				$desc .= '<li>municipality: ' . processWikitext($row->lang, $row->municipality, $makeLinks). '</li>';
			}
			if ($row->lat and $row->lon) {
				$desc .= '<li>location: ' . $row->lat . ', ' . $row->lon . '</li>';
			}
			$registrantUrl = getRegistrantUrl($row->lang, $row->id);
			if ($registrantUrl) {
				$desc .= '<li>id: <a href="' . $registrantUrl . '">' . $row->id . '</a></li>';
			} else {
				$desc .= '<li>id: ' . $row->id . '</li>';
			}
			$desc .= '<li>country: ' . strtoupper($row->country). '</li>';
			if (preg_match("/^(.+?)&/", $row->source, $matches) ) { 
				$wikiListUrl = $matches[1];
				$desc .= '<li><a href="' . $wikiListUrl. '">Source monuments list in Wikipedia</a></li>';
			} 			
            $desc .= '</ul>';
    }
	
	$desc .= '</body></html>';
	print $desc;

} //if
?>