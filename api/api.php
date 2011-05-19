<?php

/* Entry point for the monuments api */
require dirname( __FILE__ ) . '/autoloader.php';

Database::define(Monuments::$dbServer, Monuments::$dbTable, 
	Monuments::$dbUser, file_get_contents( 'secretPassword' ) );

$api = new ApiMonuments();
$api->execute();
