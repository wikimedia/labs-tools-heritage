<?php
error_reporting(E_ALL);
/**
 * Wikitable output type, based on HTML, which at its turn is based on XML
 * @author Joancreus (jcreus), based on Platonides work 
 */
//functions: processWikitext
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
		if ( preg_match( '/(http:\/\/([^\.]*)\.wikipedia\.org\/w\/index.php\?title=(.*))&redirect=no&useskin=monobook&oldid=(.*)/', $text, $m ) ) {
			/* Our current sources are: http://ca.wikipedia.org http://nl.wikipedia.org http://be-x-old.wikipedia.org http://en.wikipedia.org http://et.wikipedia.org http://es.wikipedia.org/ http://fr.wikipedia.org http://lb.wikipedia.org http://pl.wikipedia.org http://pt.wikipedia.org */
			return '[' . htmlspecialchars( $m[1] . '&oldid=' . $m[4] ) .' '. htmlspecialchars( $m[2] . ': ' . str_replace( '_', ' ', $m[3] ) ) . ']';
		} else {
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
