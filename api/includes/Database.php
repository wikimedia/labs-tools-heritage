<?php

/**
 * Database wrapper
 * @author Platonides
 */
class Database {
	/**
	 * @var Database
	 */
	private static $singleton = null;
	private $db;

	/**
	 * @return Database
	 */
	static function getDb() {
		if ( is_null( self::$singleton ) ) {
			throw new Exception( 'Database not available' );
		}
		return self::$singleton;
	}

	/**
	 * @param $list
	 *
	 * @return string
	 */
	function implodeIdentifier($list) {
		$l = '';
		foreach( $list as $item ) {
			$l .= ', ' . $this->escapeIdentifier( $item );
		}
		return substr( $l, 1 );
	}

	/**
	 * @param $where
	 * @param $glue
	 *
	 * @return string
	 */
	function implodeConds($where, $glue) {
		$text = '';
		foreach ($where as $key => $value) {
			if ( is_int( $key ) ) {
				$text .= $value . $glue;
			} else {
				
				if ( is_array( $value ) ) {
					if ( count( $value ) > 1 ) {
						$text .= $this->escapeIdentifier( $key ) . ' IN (' . $this->quote( $value[0] );
						for ( $i = 1; $i < count( $value ); $i++ )
							$text .= ', ' . $this->quote( $value[$i] );
						$text .= ')' . $glue;
					} else {
						$value = $value[0];
					}
				}
				
				if ( !is_array( $value ) ) {
					$text .= $this->escapeIdentifier( $key ) . '=' . $this->quote( $value ) . $glue;
				}
			}
		}
		return substr( $text, 0, -strlen( $glue ) );
	}

	/**
	 * @param array $fields
	 * @param string $table
	 * @param array $where
	 * @param array|bool $orderBy
	 * @param int|bool $limit
	 * @param string|bool $forceIndex
	 *
	 * @return ResultWrapper
	 */
	function select($fields, $table, $where, $orderBy = false, $limit = false, $forceIndex = false) {
		$sql = "SELECT " . $this->implodeIdentifier( $fields ) . " FROM " . 
			$this->escapeIdentifier( $table );
		if ( $forceIndex !== false ) {
			$sql .= ' FORCE INDEX( ' . $this->escapeIdentifier( $forceIndex ) . ' ) ';
		}
		if ( count( $where ) > 0 ) {
			$sql .= " WHERE (" . $this->implodeConds( $where, ') AND (' ) . ')';
		}
		
		if ( $orderBy )
			$sql .= " ORDER BY " . $this->implodeIdentifier( $orderBy );
		if ( $limit )
			$sql .= " LIMIT $limit";
		return new ResultWrapper( $this, $this->query( $sql ) );
	}
	
	function insert($table, $fields) {
		return $this->insertion('INSERT', $table, $fields);
	}
	
	function replace($table, $fields) {
		return $this->insertion('REPLACE', $table, $fields);
	}
	
	protected function insertion($action, $table, $fields) {
		$sql = "$action INTO " . $this->escapeIdentifier( $table );
		$sql2 = ') VALUES ';
		
		$sep = '(';
		
		foreach ($fields as $name => $value) {
			$sql .= $sep . $this->escapeIdentifier( $name );
			$sql2 .= $sep . $this->quote( $value );
			$sep = ',';
		}
		
		return $this->query($sql . $sql2 . ')');
	}
	
	/* Mysql specific */
	function query($sql) {
		// don't log teh useless SET NAMES utf8
		if ( !preg_match( '/^SET\b/i', $sql ) ) {
			Debug::log( $sql );
		}
		$res = mysql_query( $sql, $this->db );
		if ( !$res ) {
			if ( mysql_errno() == 1146 ) { // someone's swapping tables? retry
				usleep( 500 * 1000 ); // wait half a second
				$res = mysql_query( $sql, $this->db );
			}
			if ( !$res ) {
				throw new DBException( mysql_error(), mysql_errno(), $sql );
			}
		}
		return $res;
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
