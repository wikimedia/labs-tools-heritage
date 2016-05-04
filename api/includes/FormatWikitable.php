<?php
error_reporting(E_ALL);
/**
 * Wikitable output type, based on HTML, which at its turn is based on XML
 * @author Joancreus (jcreus), based on Platonides work 
 */
//functions: matchWikiprojectLink
require_once('CommonFunctions.php');

class FormatWikitable extends FormatBase {
	function getContentType() {
		return "text/plain;charset=UTF-8";
	}
	
	function headers() {
		parent::headers();
	}
	
	function linebreak() {
		echo "\n";
	}

	private $isTableOpen;
	
	function outputBegin($selectedItems) {
	        echo '{|class="wikitable" style="width:100%;"';$this->linebreak();	
		$this->isFirstRow = true;
	}
	
	function outputContinue($row, $continueKey, $primaryKey) {
		$continue = '';
		foreach ( $primaryKey as $key ) {
			$continue .= "|" . rawurlencode( $row->$key );
		}
		$continue = substr( $continue, 1 );
		
		echo '|}';$this->linebreak();
		$this->isTableOpen = false;
		
		echo '<p style="text-align:right;">[http://toolserver.org' .
			 $this->api->getUrl( array( $continueKey => $continue ) ) . ' next page]</p>';
	}
	
	function outputRow($row, $selectedItems) {
		if (!$this->isTableOpen) {
			//echo '|-';$this->linebreak();
			
			foreach ( $row as $name => $value ) {
				if ( in_array( $name, $selectedItems ) ) {
					echo '!' . $name; $this->linebreak();
				}
			}
			$this->isTableOpen = true;
		}
		echo '|-';
		$this->linebreak();
		foreach ( $row as $name => $value ) {
			$cellData = '';
			if ( in_array( $name, $selectedItems ) ) {
				if ($name == "image") { 
					$cellData = self::genImage($value);
				} elseif ($name == "source") {
					$cellData = self::prettifyUrls( $value ); 
				} else {
					$cellData = htmlspecialchars( $value );
				}
				
				echo '|' . $cellData;$this->linebreak(); 
			}
		}
	}
	
	function outputEnd() {
		if ($this->isTableOpen)
			echo "|}\n";
        }	
	/**
	 * Make this a nice link if it is a url (source column)
	 */
	static function prettifyUrls($text) {
		try {
			$m = matchWikiprojectLink( $text );
			$encodedLinkText = str_replace( '_', ' ', $m[5] );
			$linkText = urldecode( $encodedLinkText );
			return '[//' . htmlspecialchars( $m[2]  ) .' '. htmlspecialchars( $m[3] . ': ' . $linkText ) . ']';
		} catch (Exception $e) {
			// Normal text
			return htmlspecialchars( $text );
		}
	}

	static function genImage($img) {
		if ($img != "") {
			return '[[File:'.$img.'|100px]]';
		}
	}
}
