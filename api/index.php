<?php
require __DIR__ . '/common.php';
require __DIR__ . '/searchPage.php';

$searchPage = new SearchPage( $I18N );
echo $searchPage->getSearchPage();
