<?php

/* Entry point for the monuments api */
require dirname( __FILE__ ) . '/autoloader.php';
require dirname( __FILE__ ) . '/includes/Defaults.php';
require dirname( dirname( dirname( __FILE__ ) ) ) . '/database.inc';

/* Localization */
require_once( "$tsI18nDir/ToolStart.php" );

Database::define($dbServer, $dbDatabase, $dbUser,
	isset( $toolserver_password )? $toolserver_password : $dbPassword );

$opts = array(
    'domain' => 'MonumentsAPI', // name of your main text-domain here
    'globalfunctions' => true, // defines _(), _e() and _g() as shortcut for $I18N->msg( .. )
);
$I18N = new TsIntuition( $opts );

ApiMain::dispatch();
