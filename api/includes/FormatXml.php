<?php

/**
 * Xml output type
 * @author Platonides
 */
class FormatXml extends FormatBase {
	function getContentType() {
		return "application/xml";
	}
	
	function headers() {
		parent::headers();
		echo '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>';
	}
	
	function outputBegin() {
		echo '<monuments>';
	}
	function outputContinue($row, $continueKey, $primaryKey) {
		$continue = '';
		foreach ( $row as $name => $value ) {
			if ( in_array( $name, $primaryKey ) ) {
				$continue .= "|" . rawurlencode( $value );
			}
		}
		$continue = substr( $continue, 1 );
		echo '<continue ' . $continueKey . '="' . htmlspecialchars( $continue ) . '" />';
	}
	
	function outputRow($row) {
		echo '<monument';
		foreach ( $row as $name => $value ) {
			echo ' ' . htmlspecialchars( $name ) . '="' . htmlspecialchars( $value ) . '"';
		}
		echo ' />';
	}
	function outputEnd() {
		echo '</monuments>';
	}
}
