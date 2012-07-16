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



<?php if(isset($this->results)) { ?>
		<div id="mapview_listview" class="results">
			<table class="results" cellpadding="4" cellspacing="0">
				<tr>
					<td style="vertical-align:middle; white-space: nowrap; overflow: hidden; padding: 0px;"  width="50%">
						<span id="location-area" class="small" style=" color: #555555; font-size:12px; ">
						<form id="location-input" onsubmit="geocodeAddress('<?php echo $this->geo_bias ?>'); return false;" >
							<input type="text" id="newaddress" class="address-input"  value="<?php echo $_REQUEST['address'] ?>">
							<input type="submit" value="Location" class="stndsmall" style="font-size: 11px">
						</form>
						<div id="did-you-mean" style="display:none;">
						</div>
						</span>
					</td>
					<td  valign="top" style="white-space: nowrap; overflow: hidden;">
						<p align="right"><span class="small" style="color: #555555">
						<?php if($this->view_type == MAP_VIEW) { ?>
							<a href="<?php echo $this->oar_browser_path ?>?url=<?php echo $this->url ?>&<?php echo $this->get_current_url('viewType', LIST_VIEW, 'pageKey',0, true, true); ?>">List&nbsp;View</a>
						<?php } else { ?>
							<b style="font-size: 90%">List&nbsp;View</b>
						<?php } ?>	
							&nbsp;|&nbsp; 
						<?php if($this->view_type == LIST_VIEW) { ?>
							<a href="<?php echo $this->oar_browser_path ?>?url=<?php echo $this->url ?>&<?php echo $this->get_current_url('viewType', MAP_VIEW, 'pageKey',0,true, true); ?>">Map&nbsp;View</a>
						<?php } else { ?>
							<b style="font-size: 90%">Map&nbsp;View</b>
						<?php } ?>	 
						</span></p>
					</td>
				</tr>
			</table>
		</div>
		<?php } ?>


<?php if($this->list_height) { ?>
<div class="results" style="width:<?php echo $this->list_width; ?>;height:<?php echo $this->list_height; ?>;overflow-y: scroll; overflow-x: hidden;">
<?php } ?>
<table class="results" cellpadding="4" cellspacing="0">
<?php
	
   if($error_msg != "") {
   
   	?>
   	<tr>
   		<td class="resultstext">
   			<span nowrap class="small" style="color: #550000"><?php echo $error_msg; ?></span>
   		</td>
   	</tr>
   	<?php
   }
 
   if(count($results['hotspots']) > 0) { 
	$cnt = 0;
	foreach($results['hotspots'] as $hotspot)
	{	
		if(strpos($hotspot['actions'][0]['uri'], "http") === false) {
			$first_hyperlink = false;		//Determine if we hyperlink from the first link
		} else {
			$first_hyperlink = true;
		}	
		
		//Special case conduit -- yerg
		if($this->link_target == '_conduit') { 
			$hotspot['actions'][0]['uri'] = $hotspot['actions'][0]['uri'] . "#_new";
		}		
	?>

		<tr>
			<td class="resultstext" <?php if($cnt%2 == 1) { ?>bgcolor="#F9F9F9"<?php } else { ?>bgcolor="#F1F1F1"<?php } ?>>
			
				<span class="regular">
					<?php if($first_hyperlink == true) {?>
						<a href="<?php echo $hotspot['actions'][0]['uri']; ?>" title="<?php echo $hotspot['title'] ?>" target="<?php echo $this->link_target ?>">
					<?php } else { ?>
						<b>
					<?php } ?>
							<?php if($hotspot['title']) {
								echo $this->limit_chars($hotspot['title'], 45, "..");
								} else {
								echo "[No Title]";
								} ?>
					<?php if($first_hyperlink == true) {?>
						</a>
					<?php } else { ?>
						</b>
					<?php } ?>
				</span>
				<?php if($hotspot['actions'][0]['layerURL'] == 1) { ?>
				 &nbsp;&nbsp;&nbsp;<span nowrap class="small" style="text-align: right; font-weight:bold;"><a href="<?php echo $oar_browser_path . '?url=' . $hotspot['actions'][0]['uri'] . '&lat=' . $this->latitude . '&lon=' . $this->longitude ?>">Layer</a> &raquo;</span>
		<?php } ?>
			<br/>
		
			<span class="small"><?php echo $this->limit_chars($hotspot['line2'],55,".."); ?></span><br/>
			<span class="small"><?php echo $this->limit_chars($hotspot['line3'],55,".."); ?></span><br/>
			<?php if(isset($hotspot['line4'])) { ?>
				<span class="small"><?php echo $this->limit_chars($hotspot['line4'],55,".."); ?></span>
			<?php } ?>
			
			
			<?php if(isset($hotspot['actions'][1]['uri'])) { ?>
				
				<span class="small"><a href="#" onclick="document.getElementById('more<?php echo $cnt ?>').style.display = 'block'; return false;">More..</a></span>
				<div  id="more<?php echo $cnt ?>" style="display: none; background-color:#AAAAAA; padding: 5px">
					<span class="regular">
					<?php if((isset($hotspot['actions'][0]['uri']))&&($first_hyperlink == false)) { ?>
						<a href="<?php echo $hotspot['actions'][0]['uri'] ?>"><?php echo $hotspot['actions'][0]['label'] ?></a><br/>
					<?php } ?>
					<?php if(isset($hotspot['actions'][1]['uri'])) { ?>
						<a href="<?php echo $hotspot['actions'][1]['uri'] ?>"><?php echo $hotspot['actions'][1]['label'] ?></a><br/>
					<?php } ?>
						
					<?php if(isset($hotspot['actions'][2]['uri'])) { ?>
						<a href="<?php echo $hotspot['actions'][2]['uri'] ?>"><?php echo $hotspot['actions'][2]['label'] ?></a><br/>
					<?php } ?>
					<?php if(isset($hotspot['actions'][3]['uri'])) { ?>
						<a href="<?php echo $hotspot['actions'][3]['uri'] ?>"><?php echo $hotspot['actions'][3]['label'] ?></a><br/>
					<?php } ?>
					</span>
				</div>
			<?php } ?>
	
			</td>

			<td class="distance" <?php if($cnt%2 == 0) { ?>bgcolor="#F9F9F9"<?php } else { ?>bgcolor="#F1F1F1"<?php } ?> align="center"><span class="regular"><?php if($hotspot['distance'] > 1000) {
						 echo sprintf("%.0f", $hotspot['distance']/1000) . "km";
					     } else {
						 echo sprintf("%.0f", $hotspot['distance']) . "m";
					     } ?>
					     <br/>
				<!--<a href="http://maps.google.com/maps?
saddr=42.35892,-71.05781&daddr=40.756054,-73.986951">Test link</a>-->
				 <a href="http://maps.google.com/maps?f=d&hl=en&doflg=ptk&q=<?php echo ($hotspot['lat']/1000000.0) ?>%2C<?php echo ($hotspot['lon']/1000000.0) ?>&ie=UTF8&om=1">Map</a> <?php /* Have changed it around so that you see the destination as your starting point &ll=<?php echo $this->latitude ?>%2C<?php echo $this->longitude ?> maps.google.co.uk     &daddr=<?php echo ($hotspot['lat']/1000000.0) ?>%2C<?php echo ($hotspot['lon']/1000000.0) ?>&saddr=<?php echo $this->latitude ?>%2C<?php echo $this->longitude ?>  */ ?></span>
			</td>

			<td class="pics" valign="center">
				
				<span>
				<?php if($hotspot['imageURL'] != '') { ?>
					<a href="<?php echo $hotspot['actions'][0]['uri'] ?>" target="<?php echo $this->link_target ?>"><img border="0" src="<?php echo $hotspot['imageURL'] ?>"></a>
				<?php } ?>
				</span>
				
			</td>				
		</tr>
	<?php 	$cnt++;		//Counts the screen id for the more link
		} ?>

<?php if(($results['morePages'] === true)&&($results['nextPageKey'] != null)) {
	//Show a more...  ?>
	<tr><td colspan="3">
	<br/>
	<p style="text-align:center;"><span class="small" style="font-weight:bold; "><a href="#" onclick="document.lpf.pageKey.value = '<?php echo $results['nextPageKey'] ?>'; document.lpf.submit();return false;">More results</a> &raquo;</span></p>			 	   	
	</td></tr>
				 	   
<?php 
     }
 } ?>

</table>
<?php if($this->rvolve_user_id != 0) { 
	//Include rvolve ads
	?>
	
	<p class="small">Local Noticeboard</p>
	<p><div id="rvolve-ads" class="small"></div></p>

	<script type="text/javascript">
	var rvolveLat = <?php echo $this->latitude ?>; //Optional: Replace with your latitude
	var rvolveLon = <?php echo $this->longitude ?>; //Optional: Replace with your longitude
	var rvolveUserId =  <?php echo $this->rvolve_user_id ?>; //Optional: Replace with your user id
	var rvolveSpan = "rvolve-ads"; //Optional: change for multiple adblocks
	var rvolveHead= document.getElementsByTagName('head')[0]; 
	<?php if($this->template_url == "") { //put the doc write outside in the template 
		?>
		var rvolveScript= document.createElement('script');
		rvolveScript.type= 'text/javascript'; rvolveScript.src = unescape("http://rvolve.com/search.php?type=js%26lat=" + rvolveLat + "%26lon=" + rvolveLon + "%26site="+ rvolveUserId + "%26span=" + rvolveSpan); rvolveHead.appendChild(rvolveScript);
	<?php } ?>
	</script> 
	<?php /*
	<script type="text/javascript">
		var rvolveLat = <?php echo $this->latitude ?>; //Optional: Replace with your latitude
		var rvolveLon = <?php echo $this->longitude ?>; //Optional: Replace with your longitude
		var rvolveUserId = <?php echo $_REQUEST['rvolve'] ?>; //Optional: Replace with your user id
		<?php if(!isset($this->template_url)) { //put the doc write outside in the template ?>
			document.write(unescape("%3Cscript src='http://rvolve.com/search.php?type=js&lat=" + rvolveLat + "&lon=" + rvolveLon + "&site="+ rvolveUserId +"' type='text/javascript'%3E%3C/script%3E"));
		<?php } ?>
	</script>
	<?php */ ?>
<?php } ?>

<?php if($this->list_height) { ?>
</div>
<?php } ?>
