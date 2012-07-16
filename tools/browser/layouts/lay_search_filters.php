<?php /*
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

<form action="<?php echo $oar_browser_path ?>" name="srch">
	<span class="small"><a href="<?php echo $this->url ?>"><img src="<?php echo $this->favicon ?>" width="16" height="16" border="0"></a> <?php echo $results['filter1Text'] ?></span><br/><input type="text" name="query1_<?php echo $results['filter1Param'] ?>" style="width:200px;">
	<?php if($results['filter2Param']) { ?>
		<br/><a href="<?php echo $this->url ?>"><img src="<?php echo $this->favicon ?>" width="16" height="16" border="0"></a> <span class="small"><?php echo $results['filter2Text'] ?></span><br/> <input type="text" name="query2_<?php echo $results['filter2Param'] ?>" style="width:200px;">
	<?php } ?>
	<?php if($results['filter3Param']) { ?>
		<br/><a href="<?php echo $this->url ?>"><img src="<?php echo $this->favicon ?>" width="16" height="16" border="0"></a> <span class="small"><?php echo $results['filter3Text'] ?></span><br/> <input type="text" name="query3_<?php echo $results['filter3Param'] ?>" style="width:200px;">
	<?php } ?>
	<input type="hidden" name="url"  value="<?php if(isset($this->url)) 
							{ 
								echo $this->url;
							 } else {
							 	echo 'http://';
							 } ?>">
	<input type="hidden" name="lat" value="<?php echo $this->latitude ?>">
	<input type="hidden" name="lon" value="<?php echo $this->longitude ?>">
	<input type="hidden" name="acc" value="0">
	<input type="hidden" name="srch" value="1">
	
	<br/><input type="submit" value="Search">
</form>
