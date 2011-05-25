<?php

/* Entry point for the monuments api */
require dirname( __FILE__ ) . '/autoloader.php';
require dirname( dirname( __FILE__ ) ) . '/database.inc';

Database::define(Monuments::$dbServer, Monuments::$dbTable, 
	Monuments::$dbUser, $toolserver_password );

$api = new ApiMonuments();
$api->execute();
