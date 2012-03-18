<?php

/* Entry point for the monuments api */
require dirname( __FILE__ ) . '/autoloader.php';
require dirname( dirname( dirname( __FILE__ ) ) ) . '/database.inc';

/* Localization */
require_once( '/home/project/i/n/t/intuition/ToolserverI18N/ToolStart.php' );

Database::define(Monuments::$dbServer, Monuments::$dbDatabase, 
	Monuments::$dbUser, $toolserver_password );

$opts = array(
    'domain' => 'MonumentsAPI', // name of your main text-domain here
    'globalfunctions' => true, // defines _(), _e() and _g() as shortcut for $I18N->msg( .. )
);
$I18N = new TsIntuition( $opts );

$api = new ApiMonuments();
$api->execute();
