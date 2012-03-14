<?php
/**
 * Gallery of images of a monument in Estonia
 *
 * @author  Platonides
 */
 
define( 'MEDIAWIKI', 1 );
require_once dirname( dirname( dirname( __FILE__ ) ) ) . "/common/lib.php";
require_once dirname( dirname( dirname( __FILE__ ) ) ) . "/common/skin.php";

$wgServer = 'http://commons.wikimedia.org';
$wgArticlePath = '/wiki/$1';
$wgUseImageResize = $wgUseImageMagick = true;

$wgLocalFileRepo = array(
	'class' => 'LocalRepo',
	'name' => 'local',
	'directory' => dirname( __FILE__ ) . '/thumbs', // getScalerType() wants to make sure that the folders exist, even though we are resizing through a 404. Ok, I will have a bunch of empty folders there
	'scriptDirUrl' => $wgScriptPath,
	'scriptExtension' => '.php',
	'url' => 'http://upload.wikimedia.org/wikipedia/commons',
	'hashLevels' => 2,
	'thumbScriptUrl' => $wgThumbnailScriptPath,
	'transformVia404' => true,
	'deletedDir' => false,
	'deletedHashLevels' => 1
);

$wgMemc = wfGetCache( CACHE_NONE );
$wgUseDatabaseMessages = false;

$passwd = posix_getpwuid( posix_getuid() );
$HOME = $passwd['dir'];
$conf = parse_ini_file("$HOME/.my.cnf"); /* provides, user, password and host */
$conf['host'] = 'sql-s4-user.toolserver.org';
$conf['dbname'] = 'commonswiki_p';
$conf['type'] = 'mysql';
$conf['load'] = '';
$conf['flags'] = DBO_DEFAULT;
$wgDBservers = array( $conf );
unset( $conf );

// Dumb wrappers for function calls
class SillyLanguage {
	function needsGenderDistinction()  {
		return false;
	}
	function getNsText($namespace) {
		if ($namespace != NS_FILE) {
			throw new Exception( "getNsText($namespace)" );
		}
		return "File";
	}
	
	function getVal($name) {
		return 'render';
	}
	
	function formatNum( $number, $nocommafy = false ) {
		return $number;
	}
	
	function truncate($text, $length) {
		return $text;
	}
	
	function getCode() {
		global $I18N;
		return $I18N->getLang();
	}
	
	function getMessage($name) {
		if ($name == 'nbytes')
			return '$1 bytes'; // It's the same in most languages
		
		throw new Exception("Requested message $name");
	}
}

$wgContLang = new SillyLanguage;
$wgRequest = $wgContLang; // getVal('action')
$wgLang = $wgContLang; // formatNum(size), truncate(), getCode()

echo '<style type="text/css">#bodyContent li a { text-decoration: none } #bodyContent .author { float: right; text-align: right; text-decoration: underline }</style>';

$db = DBforCluster( '4-user', 'commonswiki_p');
//FIXME: author_text should be author of first image revision
$query = "SELECT cl_from, img_user_text AS author_text, page_namespace, page_title FROM image
JOIN page ON img_name=page_title
JOIN categorylinks AS clB ON page_id=clB.cl_from
WHERE page_namespace=6
AND page_is_redirect=0
AND clB.cl_to='Cultural_heritage_monuments_in_Estonia_(with_known_IDs)'";

//TRIM(LEADING '0' FROM TRIM(SUBSTR(clB.cl_sortkey, 1, INSTR(clB.cl_sortkey, \"\n\")-1))) AS img_wlm_id

if (isset($_GET['mon_id'])) {
    //Estonian id template specific
    $id_insortkey = ' ' . str_pad( $_GET['mon_id'], 8, "0", STR_PAD_LEFT ) . "\n%";
    $query .= " AND clB.cl_sortkey LIKE '" . $db->strencode( $id_insortkey ) . "'";

	echo "<p>", _html('gallery-header', array(  'raw-variables' => true, 'variables' => array( 
		"<a href=\"http://toolserver.org/~erfgoed/api/api.php?action=search&format=htmllist&srcountry=ee&srlang=et&srid=" . htmlspecialchars( $_GET['mon_id'] ) . '">' . htmlspecialchars( $_GET['mon_id'] ) . '</a>' ) ) ), "</p>";

} else {
	exit( 0 );
}

$gallery = new ImageGallery();
$gallery->mShowBytes = false; // Son números grandes y queda feo

$res = $db->query( $query );
foreach ($res as $row) {
    $author_url = $wgServer . '/wiki/User:'. $row->author_text;
	$gallery->add( Title::newFromRow( $row ), Html::element('a', array( 'class' => 'author', 'href' => $author_url ), $row->author_text ) );
}

echo $gallery->toHTML();

