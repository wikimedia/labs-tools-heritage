<?php
error_reporting(E_ALL);
/**
 * HTML output type, based on XML
 * @author Joancreus (jcreus), based on Platonides work 
 */
//functions: processWikitext
require_once('CommonFunctions.php');

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
	
	function outputBegin($selectedItems) {
		echo '<html>';$this->linebreak();
		echo '<head>';$this->linebreak();
		echo '<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">';$this->linebreak();
		echo '<style type="text/css">';$this->linebreak();
		echo 'td, th,table { border: 1px solid gray; border-collapse: collapse; }';$this->linebreak();
		echo 'th { background:steelblue; }';$this->linebreak();
		echo 'tr{ background:lightsteelblue; opacity:0.8; }';$this->linebreak();
		echo 'tr:hover { opacity:0.99; }';$this->linebreak();
		echo 'tr#header { opacity:0.99; }';$this->linebreak();
        echo 'td.ht0 { background-color: #f00; }';$this->linebreak();
        echo 'td.ht1 { background-color: #f30; }';$this->linebreak();
        echo 'td.ht2 { background-color: #f60; }';$this->linebreak();
        echo 'td.ht3 { background-color: #f90; }';$this->linebreak();
        echo 'td.ht4 { background-color: #fc0; }';$this->linebreak();
        echo 'td.ht5 { background-color: #ff0; }';$this->linebreak();
        echo 'td.ht6 { background-color: #cf0; }';$this->linebreak();
        echo 'td.ht7 { background-color: #9f0; }';$this->linebreak();
        echo 'td.ht8 { background-color: #6f0; }';$this->linebreak();
        echo 'td.ht9 { background-color: #3f0; }';$this->linebreak();
        echo 'td.ht10 { background-color: #0f0; }';$this->linebreak();
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
		
		$hasWikitext = array('name', 'address', 'municipality');
		
		echo '<tr>';
		$this->linebreak();
		foreach ( $row as $name => $value ) {
            $tdattrs = '';
			$cellData = '';
			if ( in_array( $name, $selectedItems ) ) {
				if ($name == "image") { 
					$cellData = self::genImage($value);
				} elseif ($name == "source") {
					$cellData = self::prettifyUrls( $value ); 
				} elseif ( in_array( $name, $hasWikitext ) ) {
					$makeLinks = true;
                    // not all datasets are ResultWrapper
                    if ( is_object($row) && isset($row->lang) ) {
                        $lang = $row->lang;
                    } else { // assume $row is array
                        $lang = $row['lang'];
                    }
                    $cellData = processWikitext($lang, $value, $makeLinks);
				} elseif (strpos(strrev($name),'tcp_') === 0) { // capture Statistics _pct fields
                    $tdattrs = ' class="ht'.(intval($value/10)).'"';
                    $cellData = $value.' %';
				} else {
					$cellData = htmlspecialchars( $value );
				}
				
				echo '<td'.$tdattrs.'>' . $cellData . '</td>';$this->linebreak(); 
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
		if ( preg_match( '/(http:\/\/([^\.]*)\.wikipedia\.org\/w\/index.php\?title=(.*))&redirect=no&useskin=monobook&oldid=(.*)/', $text, $m ) ) {
			/* Our current sources are: http://ca.wikipedia.org http://nl.wikipedia.org http://be-x-old.wikipedia.org http://en.wikipedia.org http://et.wikipedia.org http://es.wikipedia.org/ http://fr.wikipedia.org http://lb.wikipedia.org http://pl.wikipedia.org http://pt.wikipedia.org */
			return '<a href="' . htmlspecialchars( $m[1] . '&oldid=' . $m[4] ) . '">' . htmlspecialchars( $m[2] . ': ' . str_replace( '_', ' ', $m[3] ) ) . '</a>';
		} else {
			// Normal text
			return htmlspecialchars( $text );
		}
	}

        static function genImage($img) {
         if ($img != "") {
          $img = str_replace(" ","_",$img);
          $md5 = md5($img);

          $url = 'http://upload.wikimedia.org/wikipedia/commons/thumb/'.substr($md5,0,1).'/'.substr($md5,0,2).'/'.$img.'/100px-'.$img;
          return '<a href="http://commons.wikimedia.org/wiki/File:'.$img.'"><img src="'.$url.'"></a>';
         }
        }
}
