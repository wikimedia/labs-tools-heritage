<?php

/**
 * Database wrapper
 * @author Nuno Tavares
 */
class DatabaseExt {
	private static $singleton = null;
	private $db = [ 0=> '', 1=>'' ];
	private static $_last_slot = 0;
	private static $_cur_slot = 0;

	private static $__bDebug = true;

	function debug( $msg ) {
		if ( DatabaseExt::$__bDebug ) {
			print "[d] ".$msg."\n";
		}
	}

	function getDb( $slot = 0 ) {
		if ( is_null( self::$singleton ) ) {
			throw new Exception( 'Database not available' );
		}
		return self::$singleton;
	}

	function setCurSlot( $slot = 0 ) {
		if ( isset( self::$singleton->db[$slot] ) ) {
			self::$_cur_slot = $slot;
		}
		DatabaseExt::debug( ' + Switched to server: '.mysqli_get_host_info( self::$singleton->db[self::$_cur_slot] ) );
			return self::$singleton->db[self::$_cur_slot];
	}

	/* Mysql specific */
	function query( $sql ) {
		return mysqli_query( self::$singleton->db[self::$_cur_slot], $sql );
	}

	static function initialize( $server, $database, $username, $password, $characterset = 'utf8' ) {
		if ( is_null( self::$singleton ) ) {
			self::$singleton = new DatabaseExt();
		}
		self::$singleton->db[self::$_last_slot] = @mysqli_connect( $server, $username, $password );
		if ( !isset( self::$singleton->db[self::$_last_slot] ) ) {
			return false;
		}
		self::setCurSlot( self::$_last_slot );
		self::$_last_slot++;
		self::$singleton->query( 'SET NAMES '.$characterset );
		return mysqli_select_db( self::$singleton->db[self::$_cur_slot], $database );
	}

	function getDBError() {
		return mysqli_error( self::$singleton->db[self::$_cur_slot] );
	}

	function quote( $str ) {
		return "'" . $this->sanitize( $str ) . "'";
	}

	function escapeIdentifier( $str ) {
		return "`$str`";
	}

	function numRows( $wrapper ) {
		return mysqli_num_rows( $wrapper->result );
	}

	function fetchObject( $wrapper ) {
		@$obj = mysqli_fetch_object( $wrapper->result );
		return $obj;
	}

	function fetchRow( $wrapper ) {
		@$obj = mysqli_fetch_row( $wrapper->result );
		return $obj;
	}

	function fetchAssoc( $wrapper ) {
		@$obj = mysqli_fetch_assoc( $wrapper->result );
		return $obj;
	}

	function freeResult( $wrapper ) {
		/* No-op*/
	}

	function dataSeek( $wrapper, $rowNumber ) {
		return mysqli_data_seek( $wrapper->result, $rowNumber );
	}

	function sanitize( $sSQL ) {
		return mysqli_real_escape_string( self::$singleton->db[self::$_cur_slot], $sSQL );
	}

	function getAffectedRows() {
		return mysqli_affected_rows( self::$singleton->db[self::$_cur_slot] );
	}
}
