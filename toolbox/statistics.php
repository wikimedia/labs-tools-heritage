<?php
require_once ( 'toolbox.php' );

$toolboxPage = new ToolboxPage( $I18N );
echo $toolboxPage->getPageIntro();
?>

<div id="content">


<h2><?php echo _i18n( 'toolbox-title-statistics' ) ?></h2>
<form method="get" action="https://tools.wmflabs.org/heritage/api/api.php">
			<input type="hidden" name="action" value="statistics" />
			<input type="hidden" name="format" value="html" />
			<input type="hidden" name="limit" value="0" />

<table id="mainform">

	<!--tr>
		<td colspan="2" class="subtitle">
			This is a text line
		</td>
	</tr>
	<tr-->
		<th><label for="#">
<?php echo _i18n( 'db-field-country' ) ?>		</label>
		</th>
		<td>
		<select id="stcountry" name="stcountry" multiple="multiple" size="5">
			<option value="">All</option>
			<option value="AD">AD</option>
			<option value="AT">AT</option>
			<option value="BE-BRU">BE-BRU</option>
			<option value="BE-VLG">BE-VLG</option>
			<option value="BE-WAL">BE-WAL</option>
			<option value="BY">BY</option>
			<option value="CH">CH</option>
			<option value="DE-HE">DE-HE</option>
			<option value="DE-NRW-BM">DE-NRW-BM</option>
			<option value="DE-NRW-K">DE-NRW-K</option>
			<option value="DK-BYGNING">DK-BYGNING</option>
			<option value="DK-FORTIDS">DK-FORTIDS</option>
			<option value="EE">EE</option>
			<option value="ES">ES</option>
			<option value="ES-CT">ES-CT</option>
			<option value="ES-VC">ES-VC</option>
			<option value="FR">FR</option>
			<option value="IE">IE</option>
			<option value="IT-88">IT-88</option>
			<option value="IT-BZ">IT-BZ</option>
			<option value="LU">LU</option>
			<option value="NL">NL</option>
			<option value="NO">NO</option>
			<option value="PL">PL</option>
			<option value="PT">PT</option>
			<option value="RO">RO</option>
			<option value="RU">RU</option>
			<option value="SE">SE</option>
			<option value="UA">UA</option>
			<option value="US">US</option>
		</select>
		</td>
	</tr>
	<tr>
		<th><label for="stitems">
Items		</label>
		</th>
		<td>
		<select id="stitem" name="stitem" multiple="multiple" size="5">
			<option value="total" selected="selected">Total number</option>
			<option value="name_pct" selected="selected">name pct</option>
			<option value="address"><?php echo _i18n( 'db-field-address' ) ?></option>
			<option value="address_pct" selected="selected">address_pct</option>
			<option value="municipality"><?php echo _i18n( 'db-field-municipality' ) ?></option>
			<option value="municipality_pct" selected="selected">municipality_pct</option>
			<option value="image"><?php echo _i18n( 'db-field-image' ) ?></option>
			<option value="image_pct" selected="selected">image_pct</option>
			<option value="coordinates"> coordinates </option>
			<option value="coordinates_pct" selected="selected">coordinates_pct</option>
		</select>
		</td>
	</tr>
		</td>
	</tr>
	<tr>
		<th>
			<label for="#">
			</label>
		</th>
		<td>
		<input type="submit" id="submit-statistic" value="Submit" />
		</td>
	</tr>
</table>

</form>

</div><!-- end content -->

<?php
echo $toolboxPage->getPageOutro();
