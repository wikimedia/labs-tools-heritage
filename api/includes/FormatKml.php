<?php

/**
 * Kml output type
 */


//functions
require_once('CommonFunctions.php');


//class

class FormatKml extends FormatBase {


	function getContentType() {
		return "application/vnd.google-earth.kml+xml";
	}
	
	function headers() {
		parent::headers();
		echo '<?xml version="1.0" encoding="UTF-8"?>';
	}
	
	function outputBegin($selectedItems) {
		echo '<kml xmlns="http://www.opengis.net/kml/2.2">';
        echo '<Document>
        <Style id="monumentStyle"><IconStyle id="monumentIcon"><Icon><href>http://maps.google.com/mapfiles/kml/paddle/ylw-blank.png</href></Icon></IconStyle></Style>
        <Style id="monPicStyle"><IconStyle id="monPicIcon"><Icon><href>http://maps.google.com/mapfiles/kml/paddle/blu-circle.png</href></Icon></IconStyle></Style>';
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
            $listFields = array('id', 'name', 'address', 'municipality');
            foreach ( $row as $name => $value ) {
                if ( in_array( $name, $selectedItems ) ) {
                    if ( in_array( $name, $listFields ) ) {
                        $desc .= '<li> ' . _('db-field-' . $name ) . ' - ';
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
