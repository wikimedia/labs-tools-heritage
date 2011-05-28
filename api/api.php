<?php

/* Entry point for the monuments api */
require dirname( __FILE__ ) . '/autoloader.php';
require dirname( dirname( dirname( __FILE__ ) ) ) . '/database.inc';

Database::define(Monuments::$dbServer, Monuments::$dbDatabase, 
	Monuments::$dbUser, $toolserver_password );

$api = new ApiMonuments();
$api->execute();
