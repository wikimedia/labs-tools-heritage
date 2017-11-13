<?php
/**
 * Statistics wrapper
 * @author Nuno Tavares <nuno.tavares@wikimedia.pt>
 *
 * Depends on StatsBuilder being run on a daily basis
 */

ini_set( 'display_errors', 1 );
ini_set( 'error_reporting', E_ALL );

class Statistics extends StatisticsBase {
	static $dbTable = 'statistics';
	var $report = [];
	var $axis = [];
	static $fieldPrefix = 'st_';
	static $maxMuniLength = 100;  # length of muni db field

	var $lastDay = '';
	static $aItems = [
		'address', 'address_pct', 'coordinates', 'coordinates_pct', 'image',
		'image_pct', 'municipality', 'municipality_pct', 'name', 'name_pct', 'total' ];

	function getLatestDay() {
		if ( empty( $this->lastDay ) ) {
			$sql = 'SELECT MAX(day) FROM '.Statistics::$dbTable;
			$res = $this->db->query( $sql );
			$oRes = new ResultWrapper( $this->db, $res );
			$row = $oRes->fetchRow();
			$this->lastDay = $row[0];
		}
		// fallback to today, if none found (set initial/first timestamp)
		if ( empty( $this->lastDay ) ) {
			$this->lastDay = date( 'Y-m-d' );
		}
		return $this->lastDay;
	}

	function retrieveReport( $aItems, $aFilters, $sLimit, $groupby = 'item' ) {
		// $this->debug('retrieveReport() started.');

		// sanitize inputs
		$items = [];
		for ( $i=0; $i<count( $aItems ); $i++ ) {
			$items[] = $this->db->sanitize( $aItems[$i] );
		}
		$filters = [];
		for ( $i=0; $i<count( $aFilters ); $i++ ) {
			$filters[] = $this->db->sanitize( $aFilters[$i] );
		}
		$sLimit = $this->db->sanitize( $sLimit );

		// determine proper axis - TODO recover groupby='country'
		$gc = 'item';

		// determine SQL filters
		$fields = [ 'country', 'muni', 'lang', 'project', 'day', 'item', 'value' ];
		$where = [];

		$items_in = '"'. Statistics::$fieldPrefix . implode( '","'.Statistics::$fieldPrefix, $items ) . '"';
		$where[] = 'item IN ('.$items_in.')';
		$where[] = '`day` = "'.$this->getLatestDay().'"';

		$filters_in = [];
		for ( $i=0; $i<count( $filters ); $i++ ) {
			$filters_in[] = 'country LIKE "'.$filters[$i].'%"';
		}
		$where[] = implode( ' OR ', $filters_in );

		$oRes = $this->db->select( $fields, Statistics::$dbTable, $where, false, $sLimit );
		if ( !$oRes ) {
			$this->setErrorMsg( 'ERROR: Error running query' );
			return false;
		}
		$group = [];
		$idxs = [];
		while ( $row = $oRes->fetchAssoc() ) {
			# var_dump($row);
			$idx = Statistics::packIdxFromLabel( $row );
			# var_dump($idx);
			$idxString = Statistics::makeIdxString( $idx );
			$group[$row[$gc]] = 1;
			$idxs[$idxString] = 1;
			list( $country,$municipality,$lang,$project ) = $idx;
			$this->report[$idxString]['country'] = $country;
			$this->report[$idxString]['municipality'] = $municipality;
			$this->report[$idxString]['lang'] = $lang;
			$this->report[$idxString]['project'] = $project;
			$this->report[$idxString][$row[$gc]] = $row['value'];
		}
		// var_dump($this->report);
		$this->axis['columns'] = array_keys( $group );
		sort( $this->axis['columns'] );
		$this->axis['rows'] = array_keys( $idxs );

		$this->db->freeResult( $oRes );

		return $this->report;
	}

	/**
	 * Pack idx identifier as an array given a labeled row
	 */
	static function packIdxFromLabel( $row ) {
		$country = $row['country'];
		$municipality = $row['muni'];
		$lang = $row['lang'];
		$project = $row['project'];
		return [ $country, $municipality, $lang, $project ];
	}

	/**
	 * Pack idx identifier as an array given an indexed row
	 */
	static function packIdxFromIndex( $row, $db ) {
		$country = $db->sanitize( $row[0] );
		$muni = $row[1];
		if ( strlen( $muni ) >= Statistics::$maxMuniLength ) {
			$muni = substr( $muni, 0, Statistics::$maxMuniLength - 1 ) . '…';
		}
		$municipality = $db->sanitize( $muni );
		$lang = $db->sanitize( $row[2] );
		$project = $db->sanitize( $row[3] );
		return [ $country, $municipality, $lang, $project ];
	}

	/**
	 * Helper to convert idx identifier to string
	 */
	static function makeIdxString( $idx ) {
		// Need to replace any naturally occuring ':' in row[1]
		list( $country, $muni, $lang, $project ) = $idx;
		$muni = str_replace( ':', '&#58;', $muni );
		return $country . ':' . $muni . ':' . $lang . ':' . $project;
	}

	/**
	 * Helper to invert idx identifier string to array
	 */
	static function invertIdxString( $idxString ) {
		list( $country, $municipality, $lang, $project ) = explode( ':', $idxString, 4 );
		$municipality = str_replace( '&#58;', ':', $municipality );
		return [ $country, $municipality, $lang, $project ];
	}

	function getAxis( $sAxis ) {
		return $this->axis[$sAxis];
	}

}
