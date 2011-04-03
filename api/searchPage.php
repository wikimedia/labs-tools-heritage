<?php
class SearchPage {
	private $fieldStyle = 'style="width:300px"';
    	public function getSearchPage() {
        	$result = array ();
        	$result[] = '<html>';
		$result[] = '<head>';
		/* FIXME search-title */
        	$result[] = '<title>Monuments search mockup</title>';
        	$result[] = '</head>';
		$result[] = '<body>';
		/* FIXME search-monuments-database */
        	$result[] = '<H1>Search the monuments database</H1>';
        	$result = array_merge($result, $this->getSearchForm());
        	$result[] = '</body>';
		$result[] = '</html>';
		return implode ("\n", $result);
    }

    	private function getSearchForm() {
		$result = array ();
		$result[] = '<form>';
		$result[] = '<table border="1">';
		$result[] = '<tr>';
		$result[] = '<th>' . _( 'search-table-th-field' ) . '</th>';
		$result[] = '<th>' . _( 'search-table-th-search' ) . '</th>';
		$result[] = '<th>' . _( 'search-table-th-filter' ) . '</th>';
		$result[] = '</tr>';
		$result[] = '<tr>';
		/* FIXME i18n countries */
		$result[] = '<td><label>Countries</label></td>';
		$result[] = '<td>&nbsp;<!-- Empty, no search for country --></td>';
		$result[] = '<td>';
		$result = array_merge($result, $this->getCountriesFilter());
		$result[] = '</td>';
		$result[] = '</tr>';
		$result[] = '<tr>';
		/* FIXME i18n languages */
		$result[] = '<td><label>Languages</label></td>';
		$result[] = '<td>&nbsp;<!-- Empty, no search for languages --></td>';
		$result[] = '<td>'; 
		$result = array_merge($result, $this->getLanguagesFilter());
		$result[] = '</td>';
		$result[] = '</tr>';
		$result[] = '<tr>';
		/* FIXME i18n name */
		$result[] = '<td><label>Name</label></td>';
		$result[] = '<td><input type="text" name="NameSearch" ' . $this->fieldStyle . '"></td>';
		$result[] = '<td>';
		$result = array_merge($result, $this->getNameSelect());
		$result[] = '</td>';
		$result[] = '</tr>';
		$result[] = '<tr>';
		/* FIXME i18n address */
		$result[] = '<td><label>Address</label></td>';
		$result[] = '<td><input type="text" name="AddressSearch" ' . $this->fieldStyle . '"></td>';
		$result[] = '<td>';
		$result = array_merge($result, $this->getAddressSelect());
		$result[] = '</td>';
		$result[] = '</tr>';
		$result[] = '<tr>';
		/* FIXME i18n municipality */
		$result[] = '<td><label>Municipality</label></td>';
		$result[] = '<td><input type="text" name="MunicipalitySearch" ' . $this->fieldStyle . '"></td>';
		$result[] = '<td>';
		$result = array_merge($result, $this->getMunicipalitySelect());
		$result[] = '</td>';
		$result[] = '</tr>';
		$result[] = '<tr>';
		/* FIXME coordinates */
		$result[] = '<td><label>Coordinates</label></td>';
		$result[] = '<td><!-- Lat/lon bounding box --><!-- Lat/lon distance --></td>';
		$result[] = '<td>';
		$result = array_merge($result, $this->getCoordinatesSelect());
		$result[] = '</td>';
		$result[] = '</tr>';
		$result[] = '<tr>';
		/* FIXME i18n images */
		$result[] = '<td><label>Images</label></td>';
		$result[] = '<td><!-- Not search images --></td>';
		$result[] = '<td>';
	        $result = array_merge($result, $this->getImagesSelect());
		$result[] = '</td>';
		$result[] = '</tr>';
		$result[] = '<tr>';
		/* FIXME i18n output */
		$result[] = '<th colspan="3">Output</th>';
		$result[] = '</tr>';
		$result[] = '<tr>';
		/* FIXME i18n output language */
		$result[] = '<td><label>Output language</label></td>';
		$result[] = '<td colspan="2">';
	        $result = array_merge($result, $this->getOutputLanguageSelect());
		$result[] = '</td>';
		$result[] = '</tr>';
		$result[] = '<tr>';
		/* FIXME i18n format */
		$result[] = '<td><label>Output format</label></td>';
		$result[] = '<td colspan="2">';
		$result = array_merge($result, $this->getOutputFormatSelect());
		$result[] = '</td>';
		$result[] = '</tr>';
		$result[] = '<tr>';
		/* FIXME i18n search */
		$result[] = '<td colspan="3" align="right"><input type="submit" value="Search"> </td>';
		$result[] = '</tr>';
		$result[] = '</table>';
		$result[] = '</form>';
		return $result;
	}
    
    	private function getCountriesFilter() {
		/*
	 	* Pull the countries from the database and build a nice select box
		 */
		$result = array ();
		$result[] = '<select multiple name="countries" size="5" ' . $this->fieldStyle . '">';
		/*  FIXME Pull from database and localize */
		$result[] = '<option value="fr" selected>France</option>';
		$result[] = '<option value="nl" selected>Netherlands</option>';
		$result[] = '<option value="pt" selected>Portugal</option>';
		$result[] = '</select>';
		return $result;
    	}
    	private function getLanguagesFilter() {
		/*
	 	 * Pull the languages from the database and build a nice select box
		 */
		$result = array ();
		$result[] = '<select multiple name="languages" size="5" ' .$this->fieldStyle . '">';
		/* FIXME Pull from database and localize */
		$result[] = '<option value="nl" selected>Dutch</option>';
		$result[] = '<option value="pt" selected>Portugese</option>';
		$result[] = '</select>';
		return $result;
	}

	private function getNameSelect() {
		/*
		 *
		 */
		$selectName = 'NameFilter';
		$options = array (
			'all' => 'All',
			'set' => 'Only with name',
			'unset' => 'Only without name',
		);
		return $this->getSelect ( $selectName , $options );
	}

	private function getAddressSelect() {
		/*
		 *
		 */
		$selectName = 'AddressFilter';
		$options = array (
			'all' => 'All',
			'set' => 'Only with address',
			'unset' => 'Only without address',
		);
		return $this->getSelect ( $selectName , $options );
	}
	
	private function getMunicipalitySelect() {
		/*
		 *
		 */
		$selectName = 'MunicipalityFilter';
		$options = array (
			'all' => 'All',
			'set' => 'Only with municipality',
			'unset' => 'Only without municipality',
		);
		return $this->getSelect ( $selectName , $options );
	}

	private function getCoordinatesSelect() {
		/*
		 *
		 */
		$selectName = 'CoordinatesFilter';
		$options = array (
			'all' => 'All',
			'set' => 'Only with coordinates',
			'unset' => 'Only without coordinates',
		);
		return $this->getSelect ( $selectName , $options );
	}

	private function getImagesSelect() {
		/*
		 *
		 */
		$selectName = 'ImagesFilter';
		$options = array (
			'all' => 'All',
			'set' => 'Only with image',
			'unset' => 'Only without image',
		);
		return $this->getSelect ( $selectName , $options );
	}

	private function getOutputLanguageSelect() {
		/*
		 *
		 */
		$selectName = 'OutputLanguage';
		//FIXME $options = $I18N->getLangNames();
		$options = array (
			'en' => 'English',
			'fr' => 'French',
			'nl' => 'Dutch',
			'pt' => 'Portugese',
		);

		return $this->getSelect ( $selectName , $options );
	}

	private function getOutputFormatSelect() {
		/*
		 *
		 */
		$selectName = 'OutputFormat';
		/* FIXME pull from formats */
		// $options = $apiOutputFormats;
		$options = array (
			'dynamickml', 'Dynamic KML (Google Earth/Google Maps)',

		);

		return $this->getSelect ( $selectName , $options );
	}


	private function getSelect ( $selectName , $options ) {
		/*
		 * 
		 */
		$result = array();
		$result[] = '<select name="' . $selectName . '" ' . $this->fieldStyle . '">';
		/* FIXME selected */
		foreach ( $options as $value => $name ) {
			$result[] = '<option value="' . $value . '" >' . $name . '</option>';
		}
		$result[] = '</select>';
		return $result;
	}
}
/*
<tr>
<td><label>Address</label></td>
<td><input type="text" name="AddressSearch" style="width:300px"></td>
<td><select name="AddressFilter" style="width:300px">
<option value="all" selected>All</option>
<option value="set" >Only with address</option>
<option value="unset" >Only without address</option>
</select>
</td>
</tr>

<tr>
<td><label>Municipality</label></td>
<td><input type="text" name="MunicipalitySearch" style="width:300px"></td>
<td><select name="MunicipalityFilter" style="width:300px">
<option value="all" selected>All</option>
<option value="set" >Only with municipality</option>
<option value="unset" >Only without municipality</option>
</select>
</td>
</tr>

<tr>
<td><label>Coordinates</label></td>
<td><!-- Lat/lon bounding box -->
<!-- Lat/lon distance --></td>
<td><select name="CoordinatesFilter" style="width:300px">
<option value="all" selected>All</option>
<option value="set" >Only with coordinates</option>
<option value="unset" >Only without coordinates</option>
</select>
</td>
</tr>

<tr>
<td><label>Images</label></td>
<td><!-- Not search images --></td>
<td><select name="ImagesFilter" style="width:300px">
<option value="all" selected>All</option>
<option value="set" >Only with images</option>
<option value="unset" >Only without images</option>
</select>
</td>
</tr>
<tr>
<th colspan="3">Output</th>
</tr>
<tr>
<td><label>Output language</label></td>
<td colspan="2"><select name="OutputLanguage" style="width:300px">
<option value="en" selected>English</option>
<option value="fr">French</option>
<option value="nl">Dutch</option>
<option value="pt">Portugese</option>
</select>
</td>
</tr>
<tr>
<td><label>Output format</label></td>
<td colspan="2"><select name="OutputFormat" style="width:300px">
<option value="dynamickml">Dynamic KML (Google Earth/Google Maps)</option>
<option value="statickml">Static KML (Google Earth/Google Maps)</option>
<option value="gpx">Gpx (GPS format)</option>
<option value="poi">POI (TomTom format)</option>
<option value="layar">Layar (Augmented reality for your phone)</option>
<option value="printhtml">HTML to print</option>
<!-- http://www.mediawiki.org/wiki/API:Data_formats -->
<option value="json">JSON format</option>
<option value="php">serialized PHP format</option>
<option value="wddx">WDDX format</option>
<option value="xml">XML format</option>
<option value="yaml">YAML format</option>
<option value="rawfm">JSON format with the debugging elements (HTML)</option>
<option value="txt">PHP print_r() format</option>
<option value="dbg">PHP var_export() format</option>
<option value="dump">PHP var_dump() format</option>
</select>
</td>
<tr>
<td colspan="3" align="right"><input type="submit" value="Search"> </td>
</tr>

</table>
</form>
</body>
</html>
 */
?>
