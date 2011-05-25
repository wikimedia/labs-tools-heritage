<?php

/**
 * Xml output type
 * @author Platonides
 */
class FormatXml extends FormatBase {
	function outputBegin($row) {
		echo '<monuments>';
	}
	function outputContinue($row, $continueKey, $primaryKey) {
		$continue = '';
		foreach ( $row as $name => $value ) {
			if ( in_array( $name, $primaryKey ) ) {
				$continue .= "|" . rawurlencode( $name );
			}
		}
		$continue = substr( $continue, 1 );
		echo '<continue ' . $continueKey . '="' . htmlspecialchars( $continue ) . '" />';
	}
	
	function outputRow($row) {
		echo '<monument ';
		foreach ( $row as $name => $value ) {
			echo htmlspecialchars( $name ) . '="' . htmlspecialchars( $value ) . '"';
		}
		echo ' />';
	}
	function outputEnd($row) {
		echo '</monuments>';
	}
}
