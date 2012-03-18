<?php
error_reporting(E_ALL);
/**
 * Googlemap output type, the format just redirects you to Google Maps
 * based map containing the result of the search.
 * @author Maarten Dammers (multichill), based on Platonides work 
 */

class FormatGooglemaps extends FormatBase {
	private $gmUrl = 'http://maps.google.com/';

	function getContentType() {
		return "text/html";
	}
	
	function headers() {
		/*
		 * Take the current headers and redirect the client 
		 * to Google Maps with the same headers except the format.
		 */
		parent::headers();
		$apiurl = $this->api->getFullUrl(array( 'format' => 'kml' ) ) ;

		$location = $this->gmUrl . '?q=' . urlencode($apiurl);
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
