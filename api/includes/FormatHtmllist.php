<?php
error_reporting(E_ALL);
/**
 * HTML list output type, based on XML
 * This output is for users (and not automated tools) so internationalization will be used.
 * 
 */
//functions: processWikitext
require_once('CommonFunctions.php');

class FormatHtmllist extends FormatBase {

    private $rowNumberIsOdd = 0;

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
        echo '<style type="text/css">';
        echo '.main { max-width:540px; }
              .row { padding:8px; }
              .oddRow { background-color:#F1F1F1; }
              .evenRow { background-color:#F9F9F9; }';
        echo '</style>';

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
        echo '<div class="main">';
    }
	
	function outputContinue($row, $continueKey, $primaryKey) {
		$continue = '';
		foreach ( $primaryKey as $key ) {
			$continue .= "|" . rawurlencode( $row->$key );
		}
		$continue = substr( $continue, 1 );
		
		echo '<p style="text-align:right;"><a href="' .
			htmlspecialchars( $this->api->getUrl( array( $continueKey => $continue ) ) ) . '">' . _('next-page') . '</a></p>';
	}
	
	function outputRow($row, $selectedItems) {
        $desc = '';
        $this->rowNumberIsOdd = 1 - $this->rowNumberIsOdd;
        
        if ( $this->rowNumberIsOdd ) {
            $desc .= '<div class="row oddRow">';
        } else {
            $desc .= '<div class="row evenRow">';
        }
        
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
        $sepListedFields = array('name', 'image', 'lat', 'lon', 'source', 'monument_article', 'registrant_url');
        foreach ( $row as $name => $value ) {
            if ( in_array( $name, $selectedItems ) ) {
                if ( !in_array( $name, $sepListedFields ) ) {
                    $desc .= '<li> ' . htmlspecialchars(_('db-field-' . $name ) ) . ': ';
                    if ( in_array( $name, $hasWikitext ) ) {
                        $makeLinks = true;
			$desc .= processWikitext($row->lang, $value, $makeLinks);
                    } else {
                        if ( strcmp($name, 'id') == 0 and 
                               isset($row->registrant_url) and $row->registrant_url) {
                            $desc .= '<a href="' . htmlspecialchars( $row->registrant_url ) . '">';
                            $desc .= htmlspecialchars( $value );
                            $desc .= '</a>';
                        } else {
                            $desc .= htmlspecialchars( $value );
                        }
                    }
                    $desc .= '</li>';
                }
             }
        }
		if ( isset($row->lat) and $row->lat ) {
			$desc .= '<li>' . _('location') . ': ' . $row->lat . ', ' . $row->lon . '</li>';
		}

		if ( isset($row->source) and $row->source ) {
			if (preg_match("/^(.+?)&/", $row->source, $matches) ) { 
				$wikiListUrl = $matches[1];
				$desc .= '<li><a href="' . $wikiListUrl. '">' . _('source-monuments-list-on-wikipedia') . '</a></li>';
			} 
		}
        
        $desc .= '</ul>';
        $desc .= '</div>';
        
        echo $desc;
	}
	
    function outputEnd() {
        echo '</div>';
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
