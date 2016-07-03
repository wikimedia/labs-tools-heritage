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

/* Localization
 * We are loading Intuition as a library via Composer
 */
require_once __DIR__ . '/../vendor/autoload.php';

$opts = array(
	'domain' => 'heritage', // name of your main text-domain here
	'globalfunctions' => true, // defines _(), _e() and _g() as shortcut for $I18N->msg( .. )
	'suppresserrors' => false, // Krinkle heeft het stukgemaakt
	);
$I18N = new Intuition( $opts );
$I18N->registerDomain( 'heritage', __DIR__ . '/../i18n' );

/* Database */
$dbStatus = Database::define($dbServer, $dbDatabase, $dbUser,
	isset( $toolserver_password )? $toolserver_password : $dbPassword );
if (!$dbStatus) {
	die( "Coudn't connect to db! ". mysql_error() );
}

header ('Content-type: text/html; charset=utf-8');

