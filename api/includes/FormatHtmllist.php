<?php
error_reporting(E_ALL);
/**
 * HTML list output type, based on XML
 * 
 */
//functions: processWikitext
require_once('CommonFunctions.php');

class FormatHtmllist extends FormatBase {
	function getContentType() {
		return "text/html";
	}
	
	function headers() {
		parent::headers();
		echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">';
	}
	
	function outputBegin($selectedItems) {
		echo '<html>';
		echo '<head>';
		echo '<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">';
        echo "</head>\n<body>\n";
		
	}
	
	function outputContinue($row, $continueKey, $primaryKey) {
		$continue = '';
		foreach ( $primaryKey as $key ) {
			$continue .= "|" . rawurlencode( $row->$key );
		}
		$continue = substr( $continue, 1 );
		
		echo '<p style="text-align:right;"><a href="' .
			htmlspecialchars( $this->api->getUrl( array( $continueKey => $continue ) ) ) . '">next page</a></p>';
	}
	
	function outputRow($row, $selectedItems) {
        $desc = '';
        if ( isset($row->image) and $row->image ) {
            $imgsize = 100;
            $desc .= '<a href="http://commons.wikimedia.org/wiki/File:' . rawurlencode($row->image) . '">';
            $desc .= '<img src="' . getImageFromCommons($row->image, $imgsize) . '" align="right" />';
            $desc .= '</a>';
        }

        $desc .= '<ul>';
        $hasWikitext = array('name', 'address', 'municipality');
        //FIXME only use $listFields, if all fields are selected by default
        $listFields = array('id', 'name', 'address', 'municipality');
        foreach ( $row as $name => $value ) {
            if ( in_array( $name, $selectedItems ) ) {
                if ( in_array( $name, $listFields ) ) {
                    $desc .= '<li> ' . htmlspecialchars($name) . ': ';
                    if ( in_array( $name, $hasWikitext ) ) {
                        $makeLinks = true;
                        $desc .= htmlspecialchars( processWikitext($row->lang, $value, $makeLinks) );
                    } else {
                        $desc .= htmlspecialchars( $value );
                    }
                    $desc .= '</li>';
                }
             }
        }
		if ( isset($row->lat) and $row->lat ) {
			$desc .= '<li>location: ' . $row->lat . ', ' . $row->lon . '</li>';
		}

		if ( isset($row->source) and $row->source ) {
			if (preg_match("/^(.+?)&/", $row->source, $matches) ) { 
				$wikiListUrl = $matches[1];
				$desc .= '<li><a href="' . $wikiListUrl. '">Source monuments list in Wikipedia</a></li>';
			} 
		}
        
        $desc .= '</ul>';
        echo $desc;
	}
	
	function outputEnd() {
		echo "</body>\n</html>";
	}
	
	function output($result, $limit, $continueKey, $selectedItems, $primaryKey) {
		$this->headers();
		
		$this->outputBegin( $selectedItems );
        $count = 0;
		foreach ( $result as $row ) {
			if ( ++$count > $limit ) {
				$this->outputContinue( $row, $continueKey, $primaryKey );
			} else {
				$this->outputRow( $row, $selectedItems );
			}
		}
		$this->outputEnd();
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

}
