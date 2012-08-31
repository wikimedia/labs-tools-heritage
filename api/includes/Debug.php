<?php

class Debug {
	private static $debugLog = false;

	/**
	 * @param string $msg
	 */
	public static function log( $msg ) {
		self::init();
		if ( self::$debugLog ) {
			self::$debugLog .= "\t$msg\n";
		}
	}

	public static function init() {
		if ( !defined( 'DEBUG_FILE' ) ) {
			return;
		}
		if ( !self::$debugLog ) {
			if ( isset( $_SERVER['REQUEST_URI'] ) ) {
				$time = gmdate( DATE_ISO8601 );
				self::$debugLog = "$time\t{$_SERVER['REQUEST_URI']}";
				if ( isset( $_SERVER['HTTP_USER_AGENT'] ) ) {
					self::$debugLog .= "\t" . $_SERVER['HTTP_USER_AGENT'];
				}
				self::$debugLog .= "\n";
			}
		}
	}

	public static function saveLog() {
		if ( self::$debugLog ) {
			file_put_contents( DEBUG_FILE, self::$debugLog );
		}
	}
}