<?php

/**
 * Csv output type
 * @author Platonides
 */
class FormatCsv extends FormatBase {
	function getContentType() {
		return "text/csv";
	}
	
	function headers() {
		parent::headers();
	}
	
	function outputBegin() {

	}
	
	function outputContinue($row, $continueKey, $primaryKey) {
		$continue = '';
		foreach ( $primaryKey as $key ) {
			$continue .= "|" . rawurlencode( $row->$key );
		}
		$continue = substr( $continue, 1 );
		
		echo '>> Continue at ' . $this->api->getUrl( array( $continueKey => $continue ) );
	}
	
	function outputRow($row, $selectedItems) {
		$needComma = false;
		foreach ( $row as $name => $value ) {
			if ( in_array( $name, $selectedItems ) ) {
				if ( $needComma ) echo ',';
				echo '"' . str_replace( '"', '""', $value ) . '"';
				$needComma = true;
			}
		}
	}
	
	function outputEnd() {

	}
}
