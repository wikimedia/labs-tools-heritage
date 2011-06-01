<?php

/**
 * Kml output type
 */


error_reporting(E_ALL); 
ini_set('display_errors', true);
ini_set('html_errors', false);


class FormatKml extends FormatBase {
	function getContentType() {
		return "application/application/vnd.google-earth.kml+xml";
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
		echo '<Placemark';
        $placemarkId = $row->country . $row->lang . $row->id;
        echo ' id="'. htmlspecialchars( $placemarkId ) .'">';
        echo '<name>' . htmlspecialchars( $row->name ) . '</name>';
        echo '<description>';
        //echo '<![CDATA[';
		foreach ( $row as $name => $value ) {
			if ( in_array( $name, $selectedItems ) ) {
				echo ' ' . htmlspecialchars( $name ) . ' -- ' . htmlspecialchars( $value ) . '';
			}
		}
        //echo ']]>';
		echo '</description>';
        if ($row->image) {
            $styleUrl = '#monPicStyle';
        } else {
            $styleUrl = '#monumentStyle';
        }
        echo '<styleUrl>' . $styleUrl . '</styleUrl>';
        echo '<Point><coordinates>' . $row->lon . ','  . $row->lat . '</coordinates></Point>';
		echo '</Placemark>';
	}
	function outputEnd() {
		 echo '</Document>';
		echo '</kml>';
	}
}
