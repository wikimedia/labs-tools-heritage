<?php
/**
 * Gallery of images of a monument in Estonia
 *
 * @author  Platonides, Kentaur
 */

define( 'MEDIAWIKI', 1 );
require_once dirname( dirname( __DIR__ ) ) . "/common/lib.php";
require_once dirname( dirname( __DIR__ ) ) . "/common/skin.php";

$wgServer = 'http://commons.wikimedia.org';
$wgArticlePath = '/wiki/$1';
$wgUseImageResize = $wgUseImageMagick = true;

$wgLocalFileRepo = [
	'class' => 'LocalRepo',
	'name' => 'local',
	'directory' => __DIR__ . '/thumbs', // getScalerType() wants to make sure that the folders exist, even though we are resizing through a 404. Ok, I will have a bunch of empty folders there
	'scriptDirUrl' => $wgScriptPath,
	'scriptExtension' => '.php',
	'url' => 'http://upload.wikimedia.org/wikipedia/commons',
	'hashLevels' => 2,
	'thumbScriptUrl' => $wgThumbnailScriptPath,
	'transformVia404' => true,
	'deletedDir' => false,
	'deletedHashLevels' => 1
];

$wgMemc = wfGetCache( CACHE_NONE );
$wgUseDatabaseMessages = false;

$passwd = posix_getpwuid( posix_getuid() );
$HOME = $passwd['dir'];
$conf = parse_ini_file( "$HOME/.my.cnf" ); /* provides, user, password and host */
$conf['host'] = 'sql-s4-user.toolserver.org';
$conf['dbname'] = 'commonswiki_p';
$conf['type'] = 'mysql';
$conf['load'] = '';
$conf['flags'] = DBO_DEFAULT;
$wgDBservers = [ $conf ];
unset( $conf );

// conf for monument categories
$monumentCat = [
	'ad' => 'Cultural heritage monuments in Andorra with known IDs',
	'ar' => 'Monuments in Argentina with known IDs',
	'at' => 'Cultural heritage monuments in Austria with known IDs',
	'be-bru' => 'Cultural heritage monuments in Brussels with known IDs',
	'be-vlg' => 'Onroerend erfgoed with known IDs',
	'be-wal' => 'Cultural heritage monuments in Wallonia with known IDs',
	'by' => 'Cultural heritage monuments in Belarus with known IDs',
	'ca' => 'Heritage properties in Canada with known IDs',
	'ch' => 'Cultural properties of national significance in Switzerland with known IDs',
	'cz' => 'Cultural monuments in the Czech Republic with known IDs',
	'cl' => 'National monuments in Chile with known IDs',
	'co' => 'National monuments in Colombia with known IDs',
	'dk-bygning' => 'Listed buildings in Denmark with known IDs',
	'dk-fortids' => 'Archaeological monuments in Denmark with known IDs',
	'de-by' => 'Cultural heritage monuments in Bavaria with known IDs',
	'de-he' => 'Cultural heritage monuments in Hesse with known ID',
	'de-nrw-bm' => 'Cultural heritage monuments in Bergheim with known ID',
	'de-nrw-k' => 'Cultural heritage monuments in Cologne with known ID',
	'de-nrw' => 'Cultural heritage monuments in NRW with known ID',
	'ee' => 'Cultural_heritage_monuments_in_Estonia_(with_known_IDs)',
	'es' => 'Cultural heritage monuments in Spain with known IDs',
	'fr' => 'Cultural heritage monuments in France with known IDs',
	'gh' => 'Cultural heritage monuments in Ghana with known IDs',
	'in' => 'ASI Monuments with known IDs',
	'il' => 'Heritage sites in Israel with known IDs',
	'it' => 'Cultural heritage monuments in Italy with known IDs',
	'it-bz' => 'Cultural heritage monuments in South Tyrol with known IDs',
	'ke' => 'Kenya Monuments with known IDs',
	'nl' => 'Rijksmonumenten with known IDs',
	'mt' => 'Cultural heritage monuments in Malta with known IDs',
	'mx' => 'Monuments in Mexico with known IDs',
	'no' => 'Cultural heritage monuments in Norway with known IDs',
	'pa' => 'Cultural heritage monuments in Panama with known IDs',
	'ph' => 'Cultural heritage monuments in the Philippines with known IDs',
	'pt' => 'Cultural heritage monuments in Portugal with known IDs',
	'ro' => 'Cultural heritage monuments in Romania with known IDs',
	'rs' => 'Cultural heritage monuments in Serbia with known IDs',
	'ru' => 'Cultural heritage monuments in Russia with known IDs',
	'se-bbr' => 'Protected buildings in Sweden with known IDs',
	'se-fornmin' => 'Archaeological monuments in Sweden with known IDs',
	'sk' => 'Cultural heritage monuments in Slovakia with known IDs',
	'za' => 'South Africa Heritage Resources with known IDs',
	'ua' => 'Cultural heritage monuments in Ukraine with known IDs',
	'us' => 'National Register of Historic Places with known IDs',
	'us-ca' => 'California Historical Landmarks with known IDs'
];

// does monument template use leading zeros in category sortkey
$leadingZeros = [
	'ee' => 8,
	'es' => 8,
	'nl' => 8
];

// Dumb wrappers for function calls
class SillyLanguage {
	function needsGenderDistinction() {
		return false;
	}

	function getNsText( $namespace ) {
		if ( $namespace != NS_FILE ) {
			throw new Exception( "getNsText($namespace)" );
		}
		return "File";
	}

	function getVal( $name ) {
		return 'render';
	}

	function formatNum( $number, $nocommafy = false ) {
		return $number;
	}

	function truncate( $text, $length ) {
		return $text;
	}

	function getCode() {
		global $I18N;
		return $I18N->getLang();
	}

	function getMessage( $name ) {
		if ( $name == 'nbytes' ) {
			return '$1 bytes'; // It's the same in most languages
		}
		throw new Exception( "Requested message $name" );
	}
}

$wgContLang = new SillyLanguage;
$wgRequest = $wgContLang; // getVal('action')
$wgLang = $wgContLang; // formatNum(size), truncate(), getCode()

echo '<style type="text/css">#bodyContent li a { text-decoration: none } #bodyContent .author { float: right; text-align: right; text-decoration: underline }</style>';

$db = DBforCluster( '4-user', 'commonswiki_p' );

// FIXME: author_text should be author of first image revision
$query = "SELECT cl_from, img_user_text AS author_text, page_namespace, page_title FROM image
JOIN page ON img_name=page_title
JOIN categorylinks AS clB ON page_id=clB.cl_from
WHERE page_namespace=6
AND page_is_redirect=0";

if ( isset( $_GET['country'] ) ) {
	if ( isset( $monumentCat[$_GET['country']] ) ) {
		$monIdCat = str_replace( " ", "_", $monumentCat[$_GET['country']] );
		$query .= " AND clB.cl_to=" . $db->addQuotes( $monIdCat );
	} else {
		die( 'No conf for country!' );
	}
} else {
	die( 'Parameter country not set!' );
}

if ( isset( $_GET['id'] ) ) {
	if ( isset( $leadingZeros[$_GET['country']] ) ) {
		$id_insortkey = ' ' . str_pad( $_GET['id'], $leadingZeros[$_GET['country']], "0", STR_PAD_LEFT ) . "\n%";
	} else {
		$id_insortkey = ' ' . $_GET['id'] . "\n%";
	}
	$query .= " AND clB.cl_sortkey LIKE '" . $db->strencode( $id_insortkey ) . "'";

	echo "<p>", _html( 'gallery-header', [ 'raw-variables' => true, 'variables' => [
		"<a href=\"http://toolserver.org/~erfgoed/api/api.php?action=search&format=htmllist&srcountry=" . htmlspecialchars( $_GET['country'] ) . "&srlang=&srid=" . htmlspecialchars( $_GET['id'] ) . '">' . htmlspecialchars( $_GET['id'] ) . '</a>' ] ] ), " (Username shown is the last uploader.)</p>";

} else {
	exit( 0 );
}

$gallery = new ImageGallery();
$gallery->mShowBytes = false;

$res = $db->query( $query );
foreach ( $res as $row ) {
	$author_url = $wgServer . '/wiki/User:' . $row->author_text;
	$gallery->add( Title::newFromRow( $row ), Html::element( 'a', [ 'class' => 'author', 'href' => $author_url ], $row->author_text ) );
}

echo $gallery->toHTML();
