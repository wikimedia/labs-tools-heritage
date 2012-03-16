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
		header('Content-Disposition: attachment; filename="monuments.csv"');
	}
	
	function outputBegin($selectedItems) {
		$selectedItems = array_map( 'self::csvQuote', $selectedItems );
		echo implode( ',', $selectedItems );
	}
	
	function outputContinue($row, $continueKey, $primaryKey) {
		$continue = '';
		foreach ( $primaryKey as $key ) {
			$continue .= "|" . rawurlencode( $row->$key );
		}
		$continue = substr( $continue, 1 );
		
		echo '>> Continue at ' . $this->api->getFullUrl( array( $continueKey => $continue ) );
	}
	
	function outputRow($row, $selectedItems) {
		$needComma = false;
		foreach ( $row as $name => $value ) {
			if ( in_array( $name, $selectedItems ) ) {
				if ( $needComma ) echo ',';
				echo self::csvQuote( $value );
				$needComma = true;
			}
		}
		echo "\n";
	}
	
	function outputEnd() {

	}
	
	static function csvQuote($text) {
		return '"' . str_replace( '"', '""', $text ) . '"';
	}
}
