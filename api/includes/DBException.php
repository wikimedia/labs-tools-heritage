<?php

class DBException extends Exception {
	public function __construct( $message, $code = 0, $query = '' ) {
		$msg = "SQL error $code: $message";
		if ( $query ) {
			$msg .= "\nLast query was: $query";
		}
		parent::__construct( $msg );
	}
}
