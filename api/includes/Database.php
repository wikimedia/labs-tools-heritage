<?php

/**
 * Database wrapper
 * @author Platonides
 */
class Database {
	private static $singleton = null;
	private $db;
	
	static function getDb() {
		if ( is_null( self::$singleton ) ) {
			throw new Exception( 'Database not available' );
		}
		return self::$singleton;
	}
	
	function implodeIdentifier($list) {
		$l = '';
		foreach( $list as $item ) {
			$l .= ', ' . $this->escapeIdentifier( $item );
		}
		return substr( $l, 1 );
	}
	
	function implodeConds($where, $glue) {
		$text = '';
		foreach ($where as $key => $value) {
			if ( is_int( $key ) )
				$text .= $value . $glue;
			else
				$text .= $this->escapeIdentifier( $key ) . '=' . $this->quote( $value ) . $glue;
		}
		return substr( $text, 0, -strlen( $glue ) );
	}
	
	function select($fields, $table, $where, $orderBy = false, $limit = false) {
		$sql = "SELECT " . $this->implodeIdentifier( $fields ) . " FROM " . 
			$this->escapeIdentifier( $table );
		if ( count( $where ) > 0 ) {
			$sql .= " WHERE (" . $this->implodeConds( $where, ') AND (' ) . ')';
		}
		
		if ( $orderBy )
			$sql .= " ORDER BY " . $this->implodeIdentifier( $orderBy );
		if ( $limit )
			$sql .= " LIMIT $limit";
		return new ResultWrapper( $this, $this->query( $sql ) );
	}
	
	/* Mysql specific */
	function query($sql) {
		return mysql_query( $sql, $this->db );
	}
	
	static function define($server, $database, $username, $password) {
		self::$singleton = new Database();
		self::$singleton->db = @mysql_connect( $server, $username, $password );
		if ( !self::$singleton->db ) {
			return false;
		}

		self::$singleton->query( 'SET NAMES utf8' );
		return mysql_select_db( $database, self::$singleton->db );
	}
	
	function quote($str) {
		return "'" . $this->sanitize( $str ) . "'";
	}
	
	function escapeIdentifier($str) {
		return "`$str`";
	}
	
	function numRows($wrapper) {
		return mysql_num_rows( $wrapper->result );
	}
	
	function fetchObject($wrapper) {
		@$obj = mysql_fetch_object( $wrapper->result );
		return $obj;
	}
	
	function fetchRow($wrapper) {
		@$obj = mysql_fetch_row( $wrapper->result );
		return $obj;
	}
	
	function fetchAssoc($wrapper) {
		@$obj = mysql_fetch_assoc( $wrapper->result );
		return $obj;
	}
	
	function freeResult($wrapper) {
		/* No-op*/
	}
	
	function dataSeek($wrapper, $rowNumber) {
		return mysql_data_seek( $wrapper->result, $rowNumber );
	}

    function sanitize($sSQL) {
        return mysql_real_escape_string( $sSQL, $this->db );
    }
}
