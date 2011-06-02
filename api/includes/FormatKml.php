<?php

/**
 * Kml output type
 */


error_reporting(E_ALL); 
ini_set('display_errors', true);
ini_set('html_errors', false);


//functions


function getImageFromCommons($filename, $size) {
    $md5hash=md5($filename);
    $url = "http://upload.wikimedia.org/wikipedia/commons/thumb/" . $md5hash[0] . "/" . $md5hash[0] . $md5hash[1] . "/" . urlencode($filename) . "/" . $size . "px-" . urlencode($filename);
    return $url;
}

function processWikitext($wikilang, $text, $makelinks) {
    /* Process the wikitext.
     * If makelinks is true, make html links
     * If makelinks is false, remove wikitext to produce normal text without links
     */
    $result = $text;
    $differentLinkRegex="/\[\[([^\|]*)\|([^\]]*)\]\]/";
    $simpleLinkRegex="/\[\[([^\]]*)\\]\]/";
    $wikiUrl = 'http://' . $wikilang . '.wikipedia.org/wiki/';
    $differentLinkReplace = "'<a href=" . $wikiUrl ."' . rawurlencode('$1') . '>$2</a>'";
    $simpleLinkReplace = "'<a href=". $wikiUrl ."' . rawurlencode('$1') . '>$1</a>'";
    if ( $makelinks ) {
        $result = preg_replace($differentLinkRegex . "e", $differentLinkReplace, $result);
        $result = preg_replace($simpleLinkRegex . "e", $simpleLinkReplace, $result);
        $result = $result;
    } else {
        $result = preg_replace($differentLinkRegex, "$2", $result);
        $result = preg_replace($simpleLinkRegex, "$1", $result);
    }
    return $result;
}



//class

class FormatKml extends FormatBase {


	function getContentType() {
		return "application/vnd.google-earth.kml+xml";
	}
	
	function headers() {
		parent::headers();
		echo '<?xml version="1.0" encoding="UTF-8"?>';
	}
	
	function outputBegin() {
		echo '<kml xmlns="http://www.opengis.net/kml/2.2">';
        echo '<Document>
        <Style id="monumentStyle"><IconStyle id="monumentIcon"><Icon><href>http://maps.google.com/mapfiles/kml/paddle/red-blank.png</href></Icon></IconStyle></Style>
        <Style id="monPicStyle"><IconStyle id="monPicIcon"><Icon><href>http://maps.google.com/mapfiles/kml/paddle/red-circle.png</href></Icon></IconStyle></Style>';
	}

	function outputContinue($row, $continueKey, $primaryKey) {
	}
	
	function outputRow($row, $selectedItems) {
        if ( isset($row->lon) and isset($row->lat) ) {
            echo '<Placemark';
            $placemarkId = $row->country . $row->lang . $row->id;
            echo ' id="'. htmlspecialchars( $placemarkId ) .'">';
            if ( isset($row->name) ) {
                $makeLinks = false;
                echo '<name>' . htmlspecialchars( processWikitext($row->lang, $row->name, $makeLinks) ) . '</name>';
            }
            echo '<description>';
            $desc = '';
            if ( isset($row->image) and $row->image ) {
                $imgsize = 100;
                $desc .= '<a href="http://commons.wikimedia.org/wiki/File:' . rawurlencode($row->image) . '">';
                $desc .= '<img src="' . getImageFromCommons($row->image, $imgsize) . '" align="right" />';
                $desc .= '</a>';
            }
            $desc .= '<ul>';
            $hasWikitext = array('name', 'address', 'municipality');
            foreach ( $row as $name => $value ) {
                if ( in_array( $name, $selectedItems ) ) {
                    if ($name != 'image') {
                        $desc .= '<li> ' . $name . ' - ';
                        if ( in_array( $name, $hasWikitext ) ) {
                            $makeLinks = true;
                            $desc .= processWikitext($row->lang, $value, $makeLinks);
                        } else {
                            $desc .= $value;
                        }
                        $desc .= '</li>';
                    }
                }
            }
            $desc .= '</ul>';
            //echo '<![CDATA[';
            echo htmlspecialchars( $desc );
            //echo ']]>';
            echo '</description>';
            if ( isset($row->image) and $row->image ) {
                $styleUrl = '#monPicStyle';
            } else {
                $styleUrl = '#monumentStyle';
            }
            echo '<styleUrl>' . $styleUrl . '</styleUrl>';
            echo '<Point><coordinates>' . $row->lon . ','  . $row->lat . '</coordinates></Point>';
            echo '</Placemark>';
        }
	}
    
	function outputEnd() {
		 echo '</Document>';
		echo '</kml>';
	}
}
