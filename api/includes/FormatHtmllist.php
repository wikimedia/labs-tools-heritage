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
	
	function outputBegin( $selectedItems ) {
		echo '<html>';
		echo '<head>';
		echo '<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">';
		
	}
    
    function outputTitle( $result, $numRows ) {
        
        $title = '';
        if ($numRows == 1) {
            foreach ( $result as $row ) {
                if ( isset($row->name) and $row->name ) {
                    $title = htmlspecialchars(  processWikitext('', $row->name, false) );
                }
                break;
            }
        } else {
            $title = 'Monuments list';
        }
        echo '<title>'. $title .'</title>';
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

        if ( isset($row->name) and $row->name ) {
            if ( isset($row->monument_article) and $row->monument_article ) {
                $makeLinks = false;
                $article_url = 'http://'. $row->lang .'.wikipedia.org/wiki/'. htmlspecialchars( $row->monument_article );
                $desc .= '<h2><a href="'. $article_url .'">'. processWikitext($row->lang, $row->name, $makeLinks) . '</a></h2>';
            } else {
                $makeLinks = true;
                $desc .= '<h2>'. processWikitext($row->lang, $row->name, $makeLinks) . '</h2>';
            }
        }
        $desc .= '<ul>';
        $hasWikitext = array('address', 'municipality');
        $sepListedFields = array('name', 'image', 'lat', 'lon', 'source', 'monument_article');
        foreach ( $row as $name => $value ) {
            if ( in_array( $name, $selectedItems ) ) {
                if ( !in_array( $name, $sepListedFields ) ) {
                    $desc .= '<li> ' . htmlspecialchars($name) . ': ';
                    if ( in_array( $name, $hasWikitext ) ) {
                        $makeLinks = true;
                        $desc .= processWikitext($row->lang, $value, $makeLinks);
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
		
        $numRows = $result->numRows();
		$this->outputBegin( $selectedItems );
        $this->outputTitle( $result, $numRows );
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


}