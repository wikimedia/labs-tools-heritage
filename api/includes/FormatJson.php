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
	
	function outputBegin($selectedItems) {
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
				if ( $name == "lat" || $name == "lon" ) {
					$monumentArr[$name] = is_null( $value ) ? $value : (float)$value;
				} else {
					$monumentArr[$name] = $value;
				}
			}
		}
		$toplevel_node_name = $this->api->getTopLevelNodeName();
		$this->returnJSONArray[ $toplevel_node_name ][] = $monumentArr;	
		
	}

	function outputEnd() {
		$prefix = $suffix = '';
		$callback = $this->api->getParam('callback');
		if ( !is_null( $callback ) and $callback ) {
			$prefix = preg_replace( "/[^][.\\'\\\"_A-Za-z0-9]/", '', $callback ) . '(';
			$suffix = ')';
		}
		echo $prefix . json_encode($this->returnJSONArray) . $suffix;
	}

	function outputErrors( $errors ) {
		$this->outputBegin( false );
		foreach ( (array)$errors as $err ) {
			$this->returnJSONArray['errors'][] = $err;
		}
		$this->outputEnd();
	}
}
