<?php
error_reporting(E_ALL);
ini_set('display_errors', true);
ini_set('html_errors', true);

/* Entry point for the monuments api */
require dirname( __FILE__ ) . '/autoloader.php';
require dirname( __FILE__ ) . '/includes/Defaults.php';

/**
 * Look for config overrides
 *
 * First look in p_erfgoed's parent dir, then in p_erfgoed root.
 * Otherwise, erfgoed will just use Defaults.php.
 */
$config_override = 'database.inc';
if ( file_exists( dirname( dirname( dirname( __FILE__ ) ) ) . "/{$config_override}" ) ) {
	require dirname( dirname( dirname( __FILE__ ) ) ) . "/{$config_override}";
} elseif ( file_exists( dirname( dirname( __FILE__ ) ) . "/{$config_override}" ) ) {
	require dirname( dirname( __FILE__ ) ) . "/{$config_override}";
}

/**
 * Loading libraries installed via Composer
 */
require_once __DIR__ . '/../vendor/autoload.php';

/**
 * Localization
 * Intuition was loaded via Composer
 */

$opts = array(
	'domain' => 'heritage', // name of your main text-domain here
	'globalfunctions' => false, // defines _(), _e() and _g() as shortcut for $I18N->msg( .. )
	'suppresserrors' => false, // Krinkle heeft het stukgemaakt
	);
$I18N = new Intuition( $opts );
$I18N->registerDomain( 'heritage', __DIR__ . '/../i18n' );

if ( !function_exists( '_i18n' ) and !function_exists( '_html' ) ) {
	// defines _i18n() as shortcut for $I18N->msg( .. )
	function _i18n( $key, $options = array() ) {
		global $I18N;
		return $I18N->msg( $key, $options );
	}
	// defines _html() as shortcut for _i18n() escaped as html
	function _html( $key, $options = array() ) {
		if ( is_string( $options ) ) {
			$options = array( 'domain' => $options );
		}
		$options = array_merge( $options, array( 'escape' => 'html' ) );
		return _i18n( $key, $options );
	}
}else{
	trigger_error( "_i18n() or _html() already defined", E_USER_WARNING);
}

/* Database */
$dbStatus = Database::define($dbServer, $dbDatabase, $dbUser,
	isset( $toolserver_password )? $toolserver_password : $dbPassword );
if (!$dbStatus) {
	die( "Coudn't connect to db! ". mysqli_error( $dbStatus ) );
}

header ('Content-type: text/html; charset=utf-8');

