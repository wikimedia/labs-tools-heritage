<?php
/* Localization */
require_once( '/home/krinkle/TsIntuition/ToolStart.php' );
require_once( 'searchPage.php');
require_once('/home/project/e/r/f/erfgoed/database.inc');

$opts = array(
    'domain' => 'MonumentsAPI', // name of your main text-domain here
    'globalfunctions' => true, // defines _(), _e() and _g() as shortcut for $I18N->msg( .. )
    'suppresserrors' => false, // Krinkle heeft het stukgemaakt
    );
$I18N = new TsIntuition( $opts );

$searchPage = new SearchPage();
echo $searchPage->getSearchPage();

?>
