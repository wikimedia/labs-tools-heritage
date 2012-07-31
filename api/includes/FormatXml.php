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
	
	function outputBegin($selectedItems) {
		echo sprintf( '<%s>', $this->api->getTopLevelNodeName() );
	}
	function outputContinue($row, $continueKey, $primaryKey) {
		$continue = '';
		foreach ( $primaryKey as $key ) {
			$continue .= "|" . rawurlencode( $row->$key );
		}
		$continue = substr( $continue, 1 );
		echo '<continue ' . $continueKey . '="' . htmlspecialchars( $continue ) . '" />';
	}
	
	function outputRow($row, $selectedItems) {
		echo sprintf( '<%s', $this->api->getObjectNodeName() );
		foreach ( $row as $name => $value ) {
			if ( in_array( $name, $selectedItems ) ) {
				echo ' ' . htmlspecialchars( $name ) . '="' . htmlspecialchars( $value ) . '"';
			}
		}
		echo ' />';
	}
	function outputEnd() {
		echo sprintf( '</%s>', $this->api->getTopLevelNodeName() );
	}

	function outputErrors( $errors ) {
		echo "<errors>\n";
		foreach ( (array)$errors as $err ) {
			echo '<error>' . htmlspecialchars( $err ) . "</error>\n";
		}
		echo '</errors>';
	}
}
