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

	private $isfirstrow = 0;
	
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
	}
	
	function outputContinue($row, $continueKey, $primaryKey) {
		$continue = '';
		foreach ( $primaryKey as $key ) {
			$continue .= "|" . rawurlencode( $row->$key );
		}
		$continue = substr( $continue, 1 );
		echo '<td colspan="'.$this->selectedCount.'" style="text-align:right;"><a href="'.$_SERVER['REQUEST_URI'].'&' . $continueKey . '=' . htmlspecialchars( $continue ) . '">next page</a></td>';
	}
	
	function outputRow($row, $selectedItems) {
		$this->selectedCount = count($selectedItems);
		if (($this->isfirstrow)>=count($selectedItems)) { echo '<tr>'; }
		else { echo '<tr id="header">'; }
		$this->linebreak();
		foreach ( $row as $name => $value ) {
			if (($this->isfirstrow)>=count($selectedItems)) {
				if ( in_array( $name, $selectedItems ) ) {
					echo '<td>' . htmlspecialchars( $value ) . '</td>';$this->linebreak();
				}
		     } else {
				$this->isfirstrow += 1;
				echo '<th>' . $name . '</th>';$this->linebreak();
		     }
		}
		echo '</tr>';$this->linebreak();
	}
	
	function outputEnd() {
		echo "</table>\n</body>\n</html>";
	}
}

