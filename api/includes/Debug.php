<?php

class Debug {
	private static $debugLog = null;

	/**
	 * @param string $msg
	 */
	public static function log( $msg ) {
		self::init();
		if ( self::$debugLog ) {
			fputs( self::$debugLog, "\t$msg\n" );
		}
	}

	public static function init() {
		if ( !defined( 'DEBUG_FILE' ) ) {
			return;
		}
		if ( !self::$debugLog ) {
			self::$debugLog = fopen( DEBUG_FILE, 'at' );
			if ( isset( $_SERVER['REQUEST_URI'] ) ) {
				$time = gmdate( DATE_ISO8601 );
				fputs( self::$debugLog, "$time\t{$_SERVER['REQUEST_URI']}\n" );
			}
		}
	}
}