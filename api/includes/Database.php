<?php

/**
 * Database wrapper
 * @author Platonides
 */
class Database {
	private static $singleton = null;
	private $db, $dbName;
	
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
	
	function select($fields, $where, $limit, $orderBy = false) {
		$sql = "SELECT " . $this->implodeIdentifier( $fields ) . " FROM " . 
			$this->escapeIdentifier( $this->dbName );
		if ( count( $where ) > 0 ) {
			$sql .= " WHERE " . implode( ' AND ', $where );
		}
		
		if ( $orderBy !== false )
			$sql .= " ORDER BY " . $this->implodeIdentifier( $orderBy );
		$sql .= " LIMIT $limit";
		
		return new ResultWrapper( $db, $this->query( $sql ) );
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
		return mysql_select_db( $database, self::$singleton->db );
	}
	
	function quote($str) {
		return "'" . mysql_real_escape_string( $str, $this->db ) . "'";
	}
	
	function escapeIdentifier($str) {
		return "`$str`";
	}
	
	function numRows($wrapper) {
		return mysql_num_rows( $wrapper->result );
	}
	
	function fetchObject($wrapper) {
		@$obj = mysql_fetch_object( $wrapper->result );
		if ($obj === false) throw new Exception('mysql_fetch_object');
		return $obj;
	}
	
	function fetchRow($wrapper) {
		@$obj = mysql_fetch_row( $wrapper->result );
		if ($obj === false) throw new Exception('mysql_fetch_object');
		return $obj;
	}
	
	function freeResult($wrapper) {
		/* No-op*/
	}
	
	function dataSeek($wrapper, $rowNumber) {
		return mysql_data_seek( $wrapper, $rowNumber );
	}
}
