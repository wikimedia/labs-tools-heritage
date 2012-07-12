<?php
error_reporting(E_ALL); 
ini_set('display_errors', true);
ini_set('html_errors', false);

/* Entry point for the monuments api */
require dirname( __FILE__ ) . '/autoloader.php';
require dirname( __FILE__ ) . '/includes/Defaults.php';
require dirname( dirname( dirname( __FILE__ ) ) ) . '/database.inc';

/* Localization */
require_once( "$tsI18nDir/ToolStart.php" );

$dbStatus = Database::define($dbServer, $dbDatabase, $dbUser,
	isset( $toolserver_password )? $toolserver_password : $dbPassword );
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
