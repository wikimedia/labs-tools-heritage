<?php

function autoloader( $name ) {
	if ( preg_match( '/^[A-Za-z0-9]+$/', $name ) ) {
		$filename = __DIR__ . "/includes/$name.php";
		require $filename;
	}
}

spl_autoload_register( 'autoloader' );

