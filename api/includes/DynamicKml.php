<?php

/**
 * KML network link generation
 */


class DynamicKml {

    function output($request_url) {
        header( "Content-Type: application/vnd.google-earth.kml+xml" );
        $replCount = 1;
        $kml_url = htmlspecialchars( str_replace('format=dynamickml', 'format=kml', $request_url, $replCount) );
        $desc = 'Cultural heritage monuments database for <a 
href="http://www.wikilovesmonuments.eu">www.wikilovesmonuments.eu</a>';
        $desc = htmlspecialchars( $desc );
        $folderName = 'Wiki Loves Monuments';
        $folderName = htmlspecialchars( $folderName );
        $linkName = 'Monuments';
        $linkName = htmlspecialchars( $linkName );
        echo '<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.1">
 <Folder>
  <name>'. $folderName .'</name>
  <open>1</open>
  <Snippet></Snippet>
  <description>'. $desc .'</description>
  <NetworkLink>
   <name>'. $linkName .'</name>
   <visibility>1</visibility>
   <open>0</open>
   <Link>
    <href>' . $kml_url .'</href>
    <viewRefreshMode>onStop</viewRefreshMode>
    <viewRefreshTime>1</viewRefreshTime>
    <viewFormat>bbox=[bboxWest],[bboxSouth],[bboxEast],[bboxNorth]</viewFormat>
    <viewBoundScale>0.9</viewBoundScale>
   </Link>
  </NetworkLink>
 </Folder>
</kml>
';
    } //func

	
} //class
