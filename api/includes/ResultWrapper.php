<?php
/* Copied from MediaWiki */

/**
 * Result wrapper for grabbing data queried by someone else
 * @ingroup Database
 */
class ResultWrapper implements Iterator {
	var $db, $result, $pos = 0, $currentRow = null;

	/**
	 * Create a new result object from a result resource and a Database object
	 *
	 * @param Database $database
	 * @param resource $result
	 */
	function __construct( $database, $result ) {
		$this->db = $database;

		if ( $result instanceof ResultWrapper ) {
			$this->result = $result->result;
		} else {
			$this->result = $result;
		}
	}

	/**
	 * Get the number of rows in a result object
	 *
	 * @return integer
	 */
	function numRows() {
		return $this->db->numRows( $this );
	}

	/**
	 * Fetch the next row from the given result object, in object form.
	 * Fields can be retrieved with $row->fieldname, with fields acting like
	 * member variables.
	 *
	 * @return object
	 * @throws DBUnexpectedError Thrown if the database returns an error
	 */
	function fetchObject() {
		return $this->db->fetchObject( $this );
	}

	/**
	 * Fetch the next row from the given result object, in associative array
	 * form.  Fields are retrieved with $row['fieldname'].
	 *
	 * @return Array
	 * @throws DBUnexpectedError Thrown if the database returns an error
	 */
	function fetchRow() {
		return $this->db->fetchRow( $this );
	}

	/**
	 * Fetch the next row from the given result object, in associative array
	 * form.  Fields are retrieved with $row['fieldname'].
	 *
	 * @return Array
	 * @throws DBUnexpectedError Thrown if the database returns an error
	 */
	function fetchAssoc() {
		return $this->db->fetchAssoc( $this );
	}

	/**
	 * Free a result object
	 */
	function free() {
		$this->db->freeResult( $this );
		unset( $this->result );
		unset( $this->db );
	}

	/**
	 * Change the position of the cursor in a result object.
	 * See mysql_data_seek()
	 *
	 * @param $row integer
	 */
	function seek( $row ) {
		$this->db->dataSeek( $this, $row );
	}

	/*********************
	 * Iterator functions
	 * Note that using these in combination with the non-iterator functions
	 * above may cause rows to be skipped or repeated.
	 */

	function rewind() {
		if ( $this->numRows() ) {
			$this->db->dataSeek( $this, 0 );
		}
		$this->pos = 0;
		$this->currentRow = null;
	}

	function current() {
		if ( is_null( $this->currentRow ) ) {
			$this->next();
		}
		return $this->currentRow;
	}

	function key() {
		return $this->pos;
	}

	function next() {
		$this->pos++;
		$this->currentRow = $this->fetchObject();
		return $this->currentRow;
	}

	function valid() {
		return $this->current() !== false;
	}

    function isError() {
        return (is_null($this->result) or ($this->result === false));
    }
}
