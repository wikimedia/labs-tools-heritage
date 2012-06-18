<?php

class DBException extends Exception {
	public function __construct( $message, $code = 0 ) {
		parent::__construct( "SQL error $code: $message" );
	}
}
