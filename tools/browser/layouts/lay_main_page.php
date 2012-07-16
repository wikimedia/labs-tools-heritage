<?php

/*
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

For assistance:
	peter AT lightrod.org
	or the LightRod forums
*/




?>
<?php if(!$oar->template_url) { ?>
<html>
<head>
	<title>Open Web Location Browzer - owlz.org</title>
	
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<meta name="viewport" content="width=device-width, user-scalable=no" />
	
	<?php 

		//Inlcude the header
		echo $oar->get_oar_header_as_var();
	} ?>
	
	
<?php if(!$oar->template_url) { ?>
</head>
	<body onunload="GUnload();" onload="<?php echo $oar->body_onload ?>">
<?php } ?>




	
	

	
	
	<div class="whole-page">
	
		<?php if(!$oar->template_url) { ?>
		<a href="<?php echo $oar_browser_path ?>" title="LightRod.org OAR Browser"><img src="images/lightrod_logo_fav.png" width="16" height="16" border="0"></a> <span class="small"><a href="<?php echo $oar_browser_path ?>" title="Go to Home">Home</a><!-- onclick="initialize_home(); document.lpf.submit();" -->&nbsp;&nbsp;&nbsp;<a href="#" onclick="set_home_cookie(document.lpf.url.value);" title="Save as your favourite page">Bookmark</a></span>&nbsp;&nbsp;&nbsp;<span class="small"><a href="#" onclick="initialize_home(); document.lpf.submit();" title="Go to your favourite page">Go-bookmark</a></span>&nbsp;&nbsp;&nbsp;<span class="small" style=""><a href="#" onclick="document.getElementById('advanced').style.display = 'inline'; return false;" title="Other options">...</a>&nbsp;&nbsp;&nbsp;</span><span id="advanced" class="small" style="display:none;"><a href="#" onclick="set_default_search_cookie(document.lpf.url.value);" title="Advanced: Include [SEARCH] in a URL that you search off. E.g. http://key.nakdreality.com/nakdreality/[SEARCH]/lr/locations/">Set-engine-pref</a></span>
		<?php } ?> 
		<form action="<?php echo $oar_browser_path ?>" name="lpf">
			
			<?php if(!$oar->template_url) { ?>
				<?php if(isset($oar->url)) {  ?>
					<span bgcolor="red">	
						<a href="<?php echo $oar->url_with_http; ?>"><img style="vertical-align: middle;" src="<?php echo $oar->favicon ?>" width="16" height="16" border="0"></a>
					</span>
				<?php } ?>
				<span>
			
					<input type="text" name="url" class="urlinput" value="<?php if(isset($oar->url)) 
											{ 
												echo $oar->url;
											 } else {
											 	echo 'http://';
											 } ?>" onclick="if(document.lpf.url.value == 'http://') { document.lpf.url.value = ''; }">
			<?php } else { //With a template instead of an input box - put a hidden field with value?>
					<input type="hidden" name="url" class="urlinput" value="<?php if(isset($oar->url)) 
											{ 
												echo $oar->url;
											 } else {
											 	echo 'http://';
											 } ?>" >
			<?php } ?>
				<input type="hidden" name="lat" value="<?php echo $oar->latitude ?>">
				<input type="hidden" name="lon" value="<?php echo $oar->longitude ?>">
				<input type="hidden" name="viewType" value="<?php echo $oar->view_type ?>">
				<input type="hidden" name="address" value="<?php echo $_REQUEST['address'] ?>">
				<input type="hidden" name="acc" value="0">
				<input type="hidden" name="template" value="<?php echo $oar->template_url ?>">
				<input type="hidden" name="geoBias" value="<?php echo $oar->geo_bias ?>">
				<input type="hidden" name="linkTarget" value="<?php echo $oar->link_target ?>">
				<input type="hidden" name="listHeight" value="<?php echo $oar->list_width . ',' . $oar->list_height ?>">
				
				<?php if($oar->rvolve_user_id) { ?>
					<input type="hidden" name="rvolve" value="<?php echo $oar->rvolve_user_id ?>">
				<?php }?>
				
				<?php if(($oar->filters_now == true)&&($oar->search_now == 1)) { 
					//Get any extra fields that we need from the search terms - note the output is post=true
					echo $oar->get_current_url(null, null, null, null, true, false, true);
				 } ?>
				<?php if(($results['morePages'] === true)&&($results['nextPageKey'] != "")) {
					//Next page of results  ?>
					<input type="hidden" name="pageKey" value="0">
				<?php } ?>
				<?php if(!$oar->template_url) { ?>
					<input type="submit" value="Show">
				<?php } ?>
			</span><?php if(!$oar->template_url) { ?><br/><?php } ?>
			
			<?php if(!isset($oar->results)) { ?>
				<span class="small" style="color: #555555;">Enter a location-activated webpage</span>
			<?php } ?>
		</form>
		
		<?php //Show a back if we are in a results page from a search filters input
			if(($oar->filters_now == true)&&($oar->search_now == 1)) {
				?>
				<span class="small">&laquo; <a style="border:10;" href="<?php echo $oar_browser_path ?>?url=<?php echo $oar->url ?>&lat=<?php echo $oar->latitude ?>&lon=<?php echo $oar->longitude ?>" title="Go Back">Search again</a></span><?php if(!$oar->template_url) { ?><br/><?php } ?>
				<?php
			}
		?>
		
		<noscript>
		<span class="small">Warning: You need Javascript enabled to be able to determine your location</span>
		</noscript>
		
		<?php if($oar->error_message != "") { ?>
			<span class="small">
			<?php echo $oar->error_message ?>
			</span>
		<?php } ?>
		
		<div id="location_message" class="locationmessagespecs"></div>
		<div id="map_canvas" class="mapspecs"></div>
		
		
		
		<?php if((($oar->oar_description != "")||($oar->oar_logo != ""))&&
			($oar->template_url == "")) { ?>
			<hr align="left" class="results">
			<table class="results">
				<tr>
					<?php if($oar->oar_logo != "") { ?>
					<td align="left" width="70">
						
						<a href="<?php echo $oar->url_with_http; //Old:onclick='document.lpf.submit();' ?>"><img src="<?php echo $oar->oar_logo ?>" border="0"></a>
						
					</td>
					<?php } else {
						echo "<td> </td>";
					}?>
					<td valign="top" style="padding-left:10px;">
						<span class="small" style="color: #555555"><?php echo $oar->oar_description ?></span>
					</td>
					
				</tr>
				
			</table>
			
			<hr align="left" class="results">
		<?php } ?>
		
		
		<?php if(isset($oar->results)) {
			//Output results - display 10 results, with map code.  Or output search engine text box which repeats the request.
			$oar->display_layer($results);
			
		} else { ?>
			
			<div class="homepage rounded">

			<table class="homepage"  cellpadding="7">
				<tr>
					<td colspan="2">
						<span class="small">Example websites</span>
					</td>
					
				</tr>
				<tr>
					<td width="110">
						<span class="small">
							<a href="#"  onclick="document.lpf.url.value='http://www.thundre.com'; document.lpf.submit();" >THUNDRE</a>
						</span>
					</td>
					<td>
						<span class="small" style="color: #555555;">Local Shopping</span>
					</td>
				</tr>
				<tr>
					<td>
						<span class="small"><a href="#" onclick="document.lpf.url.value='http://www.padz.com';document.lpf.submit()" >PADZ</a></span>
					</td>
					<td>
						<span class="small" style="color: #555555;">Rental Properties</span>
					</td>
				</tr>
				<tr>
					<td>
						<span class="small"><a href="#" onclick="document.lpf.url.value='http://www.gstart.org';document.lpf.submit()" >Gstart</a></span>
					</td>
					<td>
						<span class="small" style="color: #555555;">Library of location-activated websites</span>
					</td>
				</tr>
				<tr>
					<td colspan="2">
						<span class="small"> </span>
					</td>
				</tr>
				<tr>
					<td colspan="2">
						<span class="small">To location-activate your website, include a meta tag on your homepage that points at your location server, which could be a

</span>
					</td>
				</tr>
				<tr>
					<td width="110" colspan="1" valign="top">
						<span class="small" ><a href="http://www.lightrod.org/mediawiki/index.php/LightRod_Open_Augmented_Reality_Browser">Layar AR layer</a></span>
					</td>
					<td>
						<small class="small" style="color: #555555;">A compatible 3D information overlay</span>
					</td>
					
				</tr>
				<tr>
					<td width="110" colspan="1" valign="top">
						<span class="small" ><a href="http://www.nakdreality.com">NakdReality account</a></span>
					</td>
					<td>
						<small class="small" style="color: #555555;">Free ready made location server host</span>
					</td>
					
				</tr>
				<tr>
					<td width="110" colspan="1" valign="top">
						<span class="small" ><a href="http://www.lightrod.org">LightRod server</a></span>
					</td>
					<td>
						<small class="small" style="color: #555555;">Installable open source location server</span>
					</td>
					
				</tr>
				
				<tr>
					<td colspan="2" valign="top" >
						<span class="small">then <a href="http://www.gstart.org">add your site</a> to the Gstart library </span>
					</td>
					
				</tr>
				<tr>
					<td colspan="2">
						<span class="small"> </span>
					</td>
				</tr>
				<tr>
					<td colspan="2">
						<span class="small">What is this?</span>
					</td>
				</tr>
				<tr>
					<td  colspan="2">
						<span class="small" style="color: #555555;">A location browser.  See real-world information around you from websites that have been "location-activated".</span>
					</td>
				</tr>
					
			</table>
			
			</div>
			
			<table cellpadding="7" class="homepage">
				<tr>
					<td width="100%" align="right">
						<a href="http://www.lightrod.org"><img src="images/lightrod_powered_by.png" border="0"></a>
					</td>
					
				</tr>
			</table>
			
		<?php } ?>
		
	
	</div>

<?php if(!$oar->template_url) { ?>
	</body>
</html>
<?php } ?>
