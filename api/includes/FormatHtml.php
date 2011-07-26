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
                echo '<!DOCTYPE HTML
    PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
     "http://www.w3.org/TR/html4/loose.dtd">';
	}

        private $isfirstrow = true;
	
	function outputBegin() {
		echo '<html>';
                echo '<head><style type="text/css">\n';
                echo 'td, th,table { border: 1px solid gray; border-collapse: collapse; }\n'
                echo 'th { background:steelblue; }\n';
                echo 'td { background:lightsteelblue; opacity:0.8; }\n';
                echo 'td:hover { opacity:0.99; }\n';
                echo '</style></head><body>
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
		echo '<tr>';
		foreach ( $row as $name => $value ) {
                     if (!$this->isfirstrow) {
			if ( in_array( $name, $selectedItems ) ) {
				echo '<td>' . htmlspecialchars( $value ) . '</td>';
			}
                     } else {
                        $this->isfirstrow = false;
                        echo '<th>' . $name . '</th>';
                     }
		}
		echo '</tr>';
	}
	function outputEnd() {
		echo '</body>\n</html>';
	}
}

