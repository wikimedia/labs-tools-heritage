<?php

/**
 * JSON output type
 */
#error_reporting(E_ALL); 
#ini_set('display_errors', true);
#ini_set('html_errors', false);

class FormatJson extends FormatBase {

	private $returnJSONArray;

	function getContentType() {
		if ( $this->api->getParam('callback') ) {
			return 'text/javascript';
		}
		return 'application/json';
	}
	
	function outputBegin() {
		$this->returnJSONArray = array();
	}

	function outputContinue($row, $continueKey, $primaryKey) {
		$continue = '';
		foreach ( $primaryKey as $key ) {
			$continue .= "|" . rawurlencode( $row->$key );
		}
		$continue = substr( $continue, 1 );
		$this->returnJSONArray["continue"] = array($continueKey=>$continue);	
	}
	
	function outputRow($row, $selectedItems) {
	
		$monumentArr = array();
		foreach ( $row as $name => $value ) {
			if ( in_array( $name, $selectedItems ) ) {
				$monumentArr[$name] = $value;
			}
		}
		$this->returnJSONArray["monuments"][] = $monumentArr;	
		
	}

	function outputEnd() {
		$prefix = $suffix = '';
		$callback = $this->api->getParam('callback');
		if ( !is_null( $callback ) ) {
			$prefix = preg_replace( "/[^][.\\'\\\"_A-Za-z0-9]/", '', $callback ) . '(';
			$suffix = ')';
		}
		echo $prefix . json_encode($this->returnJSONArray) . $suffix;
	}
	
}
