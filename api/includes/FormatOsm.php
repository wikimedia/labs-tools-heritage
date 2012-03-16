<?php
error_reporting(E_ALL);
/**
 * OSM output type, the format just redirects you to an OpenStreetMap
 * based map containing the result of the search.
 * @author Maarten Dammers (multichill), based on Platonides work 
 */

class FormatOsm extends FormatBase {
	private $osmUrl = 'http://toolserver.org/~erfgoed/map/';

	function getContentType() {
		return "text/html";
	}
	
	function headers() {
		/*
		 * Take the current headers and redirect the client 
		 * to the OpenStreetMap with the same headers.
		 */
		parent::headers();
		$p = $this->api->getParams();
		// Remove the format
		unset($p['format']);
		if ( version_compare( PHP_VERSION, '5.4', '>=' ) ) {
			$query = http_build_query( $p, '', '&', PHP_QUERY_RFC3986 );
		} else {
			$query = http_build_query( $p, '', '&' );
		}
		$location = $this->osmUrl . "?$query";
		// FIXME: Should make a BBOX based on the result and send that to the map
		header('Location: ' . $location);
	}

	function outputBegin($selectedItems) {
	}
	
	function outputContinue($row, $continueKey, $primaryKey) {
	}
	
	function outputRow($row, $selectedItems) {
	}
	
	function outputEnd() {
	}
}
