<?php

/**
 * Gpx output type. See http://www.topografix.com/gpx.asp for more information
 * @author Maarten Dammers (multichill), based on Platonides work
 */
class FormatGpx extends FormatBase {
	function getContentType() {
		return "application/xml";
	}
	
	function headers() {
		parent::headers();
		echo '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>';
		echo '<gpx';
		echo ' version="1.0"';
		echo ' creator="Monuments api - http://toolserver.org/~erfgoed/api/api.php"';
		echo ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"';
		echo ' xmlns="http://www.topografix.com/GPX/1/0"';
		echo ' xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd">';

		    
	}
	
	function outputBegin($selectedItems) {
		// FIXME: Check if time format is correct
		echo '<time>' . date('c') . '</time>';
		// FIXME: Add bounds
		// <bounds minlat="42.401051" minlon="-71.126602" maxlat="42.468655" maxlon="-71.102973"/>
	}
	function outputContinue($row, $continueKey, $primaryKey) {
		/* $continue = '';
		 * foreach ( $primaryKey as $key ) {
		 *	$continue .= "|" . rawurlencode( $row->$key );
		 * }
		 * $continue = substr( $continue, 1 );
		 * echo '<continue ' . $continueKey . '="' . htmlspecialchars( $continue ) . '" />';
		 */
	}
	
	function outputRow($row, $selectedItems) {
		// FIXME: Only include item if proper lat and lon are set
		echo '<wpt';
		echo ' lat="' . htmlspecialchars ( $row->lat ) . '"';
		echo ' lon="' . htmlspecialchars ( $row->lon ) . '"';
		echo '>';
		// FIXME: Check if the time format is correct.
		echo '<time>' .  htmlspecialchars ( date('c', strtotime($row->changed) ) ) . '</time>';
		// FIXME: Remove wikitext from name
		echo '<name>' . htmlspecialchars ( $row->id ) . '</name>';
		// cmt
		// FIXME: Clean up or remove
		echo '<desc>' . htmlspecialchars ( $row->name ) . '</desc>';
		// src
		echo '<src>' . htmlspecialchars ( $row->source ) . '</src>';
		// FIXME: Only include link if set
		echo '<link>' . 'http://'. $row->lang .'.wikipedia.org/wiki/'. htmlspecialchars( $row->monument_article ) . '</link>';
		// sym (icon)
		echo '</wpt>';
	}
	function outputEnd() {
		echo '</gpx>';
		// FIXME: Include some information about the rest
	}
}
