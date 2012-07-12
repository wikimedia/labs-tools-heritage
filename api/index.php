<?php
error_reporting(E_ALL); 
ini_set('display_errors', true);
ini_set('html_errors', false);

/* Localization */
require_once( '/home/project/i/n/t/intuition/ToolserverI18N/ToolStart.php' );
require_once( 'searchPage.php');
require_once dirname( dirname( dirname( __FILE__ ) ) ) . '/database.inc';

require dirname( __FILE__ ) . '/autoloader.php';

$dbStatus = Database::define(Monuments::$dbServer, Monuments::$dbDatabase, 
	Monuments::$dbUser, $toolserver_password );
if (!$dbStatus) {
    die( "Coudn't connect to db! ". mysql_error() );
}
    
$opts = array(
    'domain' => 'MonumentsAPI', // name of your main text-domain here
    'globalfunctions' => true, // defines _(), _e() and _g() as shortcut for $I18N->msg( .. )
    'suppresserrors' => false, // Krinkle heeft het stukgemaakt
    );
$I18N = new TsIntuition( $opts );

header ('Content-type: text/html; charset=utf-8');

$searchPage = new SearchPage($I18N);
echo $searchPage->getSearchPage();
