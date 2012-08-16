<?php
require dirname( __FILE__ ) . '/common.php';
require dirname( __FILE__ ) . '/searchPage.php';

$searchPage = new SearchPage($I18N);
echo $searchPage->getSearchPage();
