<?php

function autoloader($name) {
	if ( preg_match('^[A-Za-z0-9]+$') ) {
		$filename = dirname( __FILE__ ) . "/$name.php";
		require $filename;
	}
}

spl_autoload_register ( 'autoloader' );
