<?php

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

/* Localization */
if ( $tsI18nDir ) {
	require_once( "$tsI18nDir/ToolStart.php" );
	$opts = array(
		'domain' => 'MonumentsAPI', // name of your main text-domain here
		'globalfunctions' => true, // defines _(), _e() and _g() as shortcut for $I18N->msg( .. )
	);
	$I18N = new TsIntuition( $opts );
}

Database::define($dbServer, $dbDatabase, $dbUser,
	isset( $toolserver_password )? $toolserver_password : $dbPassword );

ApiMain::dispatch();
