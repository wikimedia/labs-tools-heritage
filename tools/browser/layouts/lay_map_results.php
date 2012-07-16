<?php  /*
    LightRod OAR Browser
    
    Copyright (C) 2001 - 2010  High Country Software Ltd.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see http://www.gnu.org/licenses/.



Usage:
	See http://www.lightrod.org/  'LightRod OAR Browser' section for the most up-to-date instructions.

*/ ?>



 <script type="text/javascript" src="<?php echo $this->oar_browser_dir ?>js/moving-map.js?version=2"></script>
 <!--<script type="text/javascript" src="js/dynamic-search.js"></script>-->
 
 <script type="text/javascript">

var linkTarget = '<?php echo $this->link_target ?>';
 
 // https://developer.mozilla.org/en/Core_JavaScript_1.5_Reference/Global_Functions/encodeURIComponent#Description
function urlEncode( s )
   {
      return encodeURIComponent( s ).replace( /\%20/g, '+' ).replace( /!/g, '%21' ).replace( /'/g, '%27' ).replace( /\(/g, '%28' ).replace( /\)/g, '%29' ).replace( /\*/g, '%2A' ).replace( /\~/g, '%7E' );
} 
 
function getResultsData(latitude, longitude, show)
{
    //alert('<?php echo $this->oar_server ?>');
    <?php 
    	$url = $this->oar_browser_dir . "dynamic-map.php?url=";
    	$url .= urlencode($this->oar_server);
    	 if(strpos($this->oar_server, "?") === false) { 
	 	$url .= urlencode("?");
	 	
	 } else {
	 	$url .= urlencode("&");
	 }
    	
    	
    	$url .= urlencode($this->get_current_url(null, null, null, null, false, false));
	
	/* if(strpos($url, "?") === false) { 
	 	$url .= urlencode("?");
	 	
	 } else {*/
	 	$url .= urlencode("&");
	 //}
    ?>


    getUrl = '<?php echo $url; ?>' + urlEncode('&lat=' + latitude + '&lon=' + longitude + '&show=' + show);  //&jsServer=1
    
    //alert(getUrl);	
   //The callback is ready for JSONP wrapping by dynamic-map     
   jQuery.getJSON(getUrl+"&callback=?", function(data) {
          searchComplete(data);
          
   });
   
   <?php if(isset($_REQUEST['rvolve'])) { ?>
   
   	   var getUrl = "http://rvolve.com/search.php?" + 
               "type=json&lat=" + latitude + "&lon=" + longitude + "&site=<?php echo $_REQUEST['rvolve'] ?>&units=km&num_results=5";
         
          
           jQuery.getJSON(getUrl+"&callback=?", function(data) { 
                advertsComplete(data);
          
   	   });	
   
   <?php } ?>


}



<?php //By default we show the favico and a little shadow, however if the site has defined a custom
	//map marker we get that
	if($this->oar_mapmarker !="") {
		list($width, $height, $type, $attr) = getimagesize($this->oar_mapmarker);
		
		?>
		var markerImage = new google.maps.MarkerImage('<?php echo $this->oar_mapmarker ?>',
      		new google.maps.Size(<?php echo $width?>, <?php echo $height ?>),	//99/115
      		new google.maps.Point(0,0),
     		new google.maps.Point(<?php echo $width/2; ?>,<?php echo $height ?>));
		
		var markerShadow = new google.maps.MarkerImage('<?php echo $this->oar_browser_dir ?>images/shadow-block.png',
      		new google.maps.Size(25, 16),	//99/115
      		new google.maps.Point(0,0),
     		new google.maps.Point(8, 16));
		
		<?php	
	} else {
		?>
	
		
var markerImage = new google.maps.MarkerImage('<?php echo $this->favicon ?>',
      		new google.maps.Size(16, 16),	//99/115
      		new google.maps.Point(0,0),
     		new google.maps.Point(16, 8));

var markerShadow = new google.maps.MarkerImage('<?php echo $this->oar_browser_dir ?>images/shadow-block.png',
      		new google.maps.Size(25, 16),	//99/115
      		new google.maps.Point(0,0),
     		new google.maps.Point(16, 8));
     	<?php } ?>
     		     
     	
     	
     	 <?php if(isset($_REQUEST['rvolve'])) { ?>
 var advertImage = new google.maps.MarkerImage('http://rvolve.com/images/mapicon.png',
      		new google.maps.Size(18, 18),	//99/115
      		new google.maps.Point(0,0),
     		new google.maps.Point(18, 9));

var advertShadow = new google.maps.MarkerImage('<?php echo $this->oar_browser_dir ?>images/shadow-block.png',
      		new google.maps.Size(25, 16),	//99/115
      		new google.maps.Point(0,0),
     		new google.maps.Point(18, 9));    	 
     	 
     	 
     	 
     	<?php } ?>
     		     		
     	/*	var icon = new GIcon();
    icon.image = "images/block.png";
    icon.shadow = "images/shadow-block.png";
    icon.iconSize = new GSize(16.0, 16.0);
    icon.shadowSize = new GSize(25.0, 16.0);
    icon.iconAnchor = new GPoint(8.0, 8.0);
    icon.infoWindowAnchor = new GPoint(8.0, 8.0);
*/
     		
/*var markerShadow = new google.maps.MarkerImage('images/beachflag_shadow.png',
	      new google.maps.Size(16, 16),
	      new google.maps.Point(0,0),
	      new google.maps.Point(8, 16));
*/

</script>

<?php if(isset($this->results)) { ?>
		<div id="mapview_listview" class="results">
			<table class="results" width="100%">
				<tr>
					<td style="vertical-align:middle; white-space: nowrap; overflow: hidden; padding: 0px;"  width="50%">
						<span id="location-area" class="small" style="color: #555555; font-size:12px;">
						<form id="location-input" onsubmit="geocodeAddress('<?php echo $this->geo_bias ?>'); return false;">
							<input type="text" id="newaddress" class="address-input" value="<?php echo $_REQUEST['address'] ?>">
							<input class="stndsmall" type="submit" value="Location" style="font-size: 11px; padding: 0px;">
						</form>
						<div id="did-you-mean" style="display:none;"></div>
						</span>
					</td>
					<td valign="top" style="white-space: nowrap; overflow: hidden;">
						<p align="right"><span class="small" style="color: #555555;">
						<?php if($this->view_type == MAP_VIEW) { ?>
							<a href="<?php echo $this->oar_browser_path ?>?url=<?php echo $this->url ?>&<?php echo $this->get_current_url('viewType', LIST_VIEW, 'pageKey',0,true, true); ?>">List&nbsp;View</a>
						<?php } else { ?>
							<b style="font-size: 90%">List&nbsp;View</b>
						<?php } ?>&nbsp;|&nbsp;<?php if($this->view_type == LIST_VIEW) { ?>
							<a href="<?php echo $this->oar_browser_path ?>?url=<?php echo $this->url ?>&<?php echo $this->get_current_url('viewType', MAP_VIEW, 'pageKey',0,true, true); ?>">Map&nbsp;View</a>
						<?php } else { ?>
							<b style="font-size: 90%">Map&nbsp;View<?php /* <i>Beta</i> */?></b>
						<?php } ?>	 
						</span></p>
					</td>
				</tr>
			</table>
		</div>
		<?php } ?>


<table class="results" cellpadding="4" cellspacing="0">
<div id="mapview" class="mapspecs" style="display: block;"></div>
	

</table>


