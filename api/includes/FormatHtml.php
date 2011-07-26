<?php
error_reporting(E_ALL);
/**
 * HTML output type, based on XML
 * @author Joancreus (jcreus), based on Platonides work 
 */
class FormatHtml extends FormatBase {
	function getContentType() {
		return "text/html";
	}
	
	function headers() {
		parent::headers();
		echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">';
	}
	
	function linebreak() {
		echo "\n";
	}

	private $isTableOpen;
	
	function outputBegin() {
		echo '<html>';$this->linebreak();
		echo '<head>';$this->linebreak();
		echo '<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">';$this->linebreak();
		echo '<style type="text/css">';$this->linebreak();
		echo 'td, th,table { border: 1px solid gray; border-collapse: collapse; }';$this->linebreak();
		echo 'th { background:steelblue; }';$this->linebreak();
		echo 'tr{ background:lightsteelblue; opacity:0.8; }';$this->linebreak();
		echo 'tr:hover { opacity:0.99; }';$this->linebreak();
		echo 'tr#header { opacity:0.99; }';$this->linebreak();
		echo "</style>\n</head>\n<body>\n<table>\n";
		
		$this->isFirstRow = true;
	}
	
	function outputContinue($row, $continueKey, $primaryKey) {
		$continue = '';
		foreach ( $primaryKey as $key ) {
			$continue .= "|" . rawurlencode( $row->$key );
		}
		$continue = substr( $continue, 1 );
		
		echo '</table>';
		$this->isTableOpen = false;
		
		echo '<p style="text-align:right;"><a href="' .
			htmlspecialchars( $this->api->getUrl( array( $continueKey => $continue ) ) ) . '">next page</a></p>';
	}
	
	function outputRow($row, $selectedItems) {
		if (!$this->isTableOpen) {
			echo '<tr id="header">';
			
			foreach ( $row as $name => $value ) {
				if ( in_array( $name, $selectedItems ) ) {
					echo '<th>' . $name . '</th>'; $this->linebreak();
				}
			}
			echo '</tr>';
			$this->isTableOpen = true;
		}
		
		echo '<tr>';
		$this->linebreak();
		foreach ( $row as $name => $value ) {
			if ( in_array( $name, $selectedItems ) ) {
				echo '<td>' . self::prettifyUrls( $value ) . '</td>';$this->linebreak();
			}
		}
		echo '</tr>';$this->linebreak();
	}
	
	function outputEnd() {
		if ($this->isTableOpen)
			echo "</table>\n";

		echo "</body>\n</html>";
	}
	
	/**
	 * Make this a nice link if it is a url (source column)
	 */
	static function prettifyUrls($text) {
		if ( preg_match( '/(http:\/\/([^\.]*)\.wikipedia\.org/w/index.php?title=(.*))&redirect=no&useskin=monobook&oldid=(.*)', $name, $m ) ) {
			// Our current sources are: http://ca.wikipedia.org http://nl.wikipedia.org http://be-x-old.wikipedia.org http://en.wikipedia.org http://et.wikipedia.org http://es.wikipedia.org/ http://fr.wikipedia.org http://lb.wikipedia.org http://pl.wikipedia.org http://pt.wikipedia.org
			return '<a href="' . htmlspecialchars( $m[1] . '&oldid=' . $m[2] ) . '">' . htmlspecialchars( $m[1] . ': ' . $m[2] ) . '</a>';
		} else {
			// Normal text
			return htmlspecialchars( $value );
		}
	}
}
