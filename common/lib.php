<?php

header("Content-Type: text/html; charset=utf-8");

error_reporting( E_ALL | E_STRICT );
ini_set( 'display_errors', PHP_SAPI == 'cli' );

$MEDIAWIKI_TRUNK = "/home/platonides/subversion/mediawiki/"; 
$IP = "$MEDIAWIKI_TRUNK/phase3";
$families = array( 'wikipedia', 'wiktionary', 'wikibooks', 'wikimedia', 'wikinews', 'wikiquote', 'wikisource', 'wikispecies', 'wikiversity', 'wikimania' );

if ( defined( 'MEDIAWIKI' ) ) {
	/* We use MediaWiki Database and friends: DatabaseMySQL, ResultWrapper... */

	require_once( "$IP/includes/AutoLoader.php" );
	require_once( "$IP/includes/Defines.php" ); # Allow NS_* defines
	require_once( "$IP/includes/DefaultSettings.php" ); # Avoid all kind of undefined variables and register globals
	require_once( "$IP/includes/profiler/ProfilerStub.php" ); # Functions needed for working
	require_once( "$IP/includes/GlobalFunctions.php" );

	$wgDBmysql5 = false; // Legacy binary encoding (although it is utf-8 inside)
	$wgAutoloadClasses['SubcategoryLister'] = dirname( __FILE__ ) . "/../subcategories/SubcategoryLister.php";

/**
 * Returns a database object suitable for that cluster and that DB.
 */
function DBforCluster($number, $dbName = false) {
	static $dbCache = array();
	
	if ( $number == '*' ) {
		if ( count( $dbCache ) ) {
			$db = reset( $dbCache );
			$db->selectDB( $dbName );
			return $db;
		}
		$number = 2; /* Any cluster number in range would do... (using cluster 2 because its servers are not outdated, see TS-1067) */
	}
	
	if ( isset( $dbCache[$number] ) ) {
		if ( $dbName ) {
			$dbCache[$number]->selectDB( $dbName );
		}
		return $dbCache[$number];
	}
	
	
	if ($number == 'sql')
		$subdomain = 'sql';
	/* $number puede acabar en -rr o -user */
	elseif (strpos($number, '-') === false)
		$subdomain = "sql-s$number-rr";
	else
		$subdomain = "sql-s$number";
		
	$passwd = posix_getpwuid( posix_getuid() );
	$HOME = $passwd['dir'];
	$conf = parse_ini_file("$HOME/.my.cnf"); /* provides, user, password and host */
	$conf['host'] = "$subdomain.toolserver.org";
	$conf['dbname'] = $dbName;
	$conf['tableprefix'] = '';
	
	try {
		$dbCache[$number] = Database::factory( 'mysql', $conf );
	}
	catch (Exception $e) {
		if ( PHP_SAPI == 'cli' )
			echo $e->getMessage();
		
		/* We might have the password in the stack trace */
		die( "\nError trying to get a database\n" );
	}
	return $dbCache[$number];
}

/**
 * Returns a database object suitable for that DB.
 * @param $dbName String Name of the database
 * @param $strict Boolean If true, die if the db can't be found.
 */
function DBforName($dbName, $strict = true) {
	static $databaseClusters = array();
	if ( isset( $databaseClusters[$dbName] ) ) {
		return DBforCluster( $databaseClusters[$dbName], $dbName );
	}
	
	/* We need to figure out in which server is this db */
	$db = DBforCluster( '*', 'toolserver' );
	$server = $db->selectField( 'wiki', 'server', array( 'dbname'=> $dbName ) );
	if ( $server === false ) {
		if ( $strict ) {
			die( "Cluster for $dbName not found." );
		} else {
			return false;
		}
	}
	
	$databaseClusters[$dbName] = $server;
	return DBforCluster( $server, $dbName );
}

function DBforConds( $conds ) {
	$db = DBforCluster( '*', 'toolserver' );

	$res = $db->select( 'wiki', array( 'server', 'dbname' ), $conds, 'DBforConds', array( 'LIMIT' => 1 ) );
	if ( !$res || !$res->numRows() )
		return false;
	
	$row = $res->fetchObject();
	return DBforCluster( $row->server, $row->dbname );
}

}

/* Fetch the tool name from the folder of the script which is executed */
$toolName = basename( pathinfo( $_SERVER['SCRIPT_NAME'], PATHINFO_DIRNAME ) );

/**
 * Load internationalization i18n class
 * Documentation available at  https://wiki.toolserver.org/view/Toolserver_Intuition
 */
require "$MEDIAWIKI_TRUNK/tools/ToolserverI18N/ToolStart.php";

/* Load setting just the domain, and defining the helper funcions _(), _g()...
 * The global must be named $I18N for the functions to work.
 * The used language can be obtained with $I18N->getLang()
 */


$textdomain = ucfirst( strtolower( $toolName ) ); # text-domain should only contain lowercase alphabetical and numerical characters starting with a capital letter
$I18N = new TsIntuition( array( 'domain' => $textdomain, 'suppressfatal' => false, 'suppressnotice' => false ) );

// $I18N->loadTextdomain() is a no-op if it exists, as the constructor will have already called it
if ( !$I18N->loadTextdomain( $textdomain ) && file_exists( "$textdomain.i18n.php" ) ) {
	$I18N->loadTextdomainFromFile( "$textdomain.i18n.php", $textdomain );
}

/**
 * Creates the html for a select control
 * @param $name String Name of the control.
 * @param Array $values List of values for the drop-down list. If it has non-numeric keys, they are used as the items to send.
 * @param $default string Key to be selected initially.
 * @return String HTML to generate such control
 */
function dropdown( $name, $values, $default ) {
	$html = '<select name="' . htmlspecialchars( $name ) . '">';
	foreach( $values as $k => $v ) {
		if ( is_numeric( $k ) ) {
			$k = $v;
		}
		$html .= '<option';
		if ( $k != $v ) {
			$html .= ' value="' . htmlspecialchars( $k ) . '"';
		}
		if ( $k == $default ) {
			$html .= ' selected="selected"';
		}
		$html .= '>' . htmlspecialchars( $v ) . '</option>';
	}
	$html .= '</select>';
	
	return $html;
}
