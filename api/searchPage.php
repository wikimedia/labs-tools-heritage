<?php

class SearchPage {
	private $fieldStyle = 'style="width:300px"';
	private $apiUrl = 'api.php';
	private $I18N = NULL;
    
	function __construct($I18N) {
		$this->I18N = $I18N;
	}
    
	public function getSearchPage() {
		$result = array ();
		$result[] = '<html>';
		$result[] = '<head>';
		$result[] = '<title>'. _( 'search-title' ) .'</title>';
		$result[] = '</head>';
		$result[] = '<body>';
		$result[] = '<H1>'. _( 'search-monuments-database' ) .'</H1>';
		$result = array_merge($result, $this->getSearchForm());
		$result[] = '<br/><hr/>';
		$result[] = $this->I18N->getPromoBox();
		$result[] = '</body>';
		$result[] = '</html>';

		return implode ("\n", $result);
	}

   	private function getSearchForm() {
		$result = array ();
		$result[] = '<form action="'. $this->apiUrl .'">';
		$result[] = '<input type="hidden" name="action" value="search">';
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
		$result[] = '<td><input type="text" name="srname" ' . $this->fieldStyle . '></td>';
		$result[] = '<td>';
	//$result = array_merge($result, $this->getNameSelect());
		$result[] = '</td>';
		$result[] = '</tr>';
		$result[] = '<tr>';
		/* FIXME i18n address */
		$result[] = '<td><label>Address</label></td>';
		$result[] = '<td><input type="text" name="sraddress" ' . $this->fieldStyle . '></td>';
		$result[] = '<td>';
	//$result = array_merge($result, $this->getAddressSelect());
		$result[] = '</td>';
		$result[] = '</tr>';
		$result[] = '<tr>';
		/* FIXME i18n municipality */
		$result[] = '<td><label>Municipality</label></td>';
		$result[] = '<td><input type="text" name="srmunicipality" ' . $this->fieldStyle . '></td>';
		$result[] = '<td>';
	//$result = array_merge($result, $this->getMunicipalitySelect());
		$result[] = '</td>';
		$result[] = '</tr>';
		$result[] = '<tr>';
		/* FIXME coordinates */
		$result[] = '<td><label>Coordinates</label></td>';
		$result[] = '<td><!-- Lat/lon bounding box --><!-- Lat/lon distance --></td>';
		$result[] = '<td>';
	//$result = array_merge($result, $this->getCoordinatesSelect());
		$result[] = '</td>';
		$result[] = '</tr>';
		$result[] = '<tr>';
		/* FIXME i18n images */
		$result[] = '<td><label>Images</label></td>';
		$result[] = '<td><!-- Not search images --></td>';
		$result[] = '<td>';
		$result[] = '<input type="checkbox" name="srwithoutimages" id="srwithoutimages" value="1"><label for="srwithoutimages">Only monuments without images</label>'; // FIXME: i18n
	//$result = array_merge($result, $this->getImagesSelect());
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
	        $result = array_merge( $result, $this->getOutputLanguageSelect() );
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
		$result[] = '<select name="srcountry" ' . $this->fieldStyle . '>';
		$result[] = '<option value="">' . _html('filter-all-countries') . '</option>';

		$db = Database::getDb();
		$sql = "SELECT DISTINCT country FROM " . $db->escapeIdentifier( Monuments::$dbTable ) . " ORDER BY country";
		$qres = new ResultWrapper( $db, $db->query( $sql ) );
		/*  FIXME localize */
		foreach ( $qres as $row ) {
			$option = '<option value="'. htmlspecialchars($row->country) . '"';
			if (@$_GET['country'] == $row->country) $option .= ' selected="selected"';
			$option .= '>'. htmlspecialchars($row->country) .'</option>';
			$result[] = $option;
		}
		$result[] = '</select>';

		return $result;
	}
        
	private function getLanguagesFilter() {
		/*
	 	 * Pull the languages from the database and build a nice select box
		 */
		$result = array ();
		$result[] = '<select name="srlang" ' .$this->fieldStyle . '>';
		/* FIXME Pull from database and localize */
		$result[] = '<option value="">' . _html('filter-all-languages') . '</option>';

		$db = Database::getDb();
		$sql = "SELECT DISTINCT lang FROM " . $db->escapeIdentifier( Monuments::$dbTable ) . " ORDER BY lang";
		$qres = new ResultWrapper( $db, $db->query( $sql ) );
		/*  FIXME localize */
		foreach ( $qres as $row ) {
			$option = '<option value="'. htmlspecialchars($row->lang) .'"';
			if (@$_GET['lang'] == $row->lang) $option .= ' selected="selected"';
			$option .= '>'. htmlspecialchars($row->lang) .'</option>';
			$result[] = $option;
		}
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
		$selectName = 'userlang';
		$options = $this->I18N->getAvailableLangs();

		/*
		$options = array (
			'en' => 'English',
			'fr' => 'French',
			'nl' => 'Dutch',
			'pt' => 'Portugese',
		);
		 */

		return $this->getSelect ( $selectName , $options, $this->I18N->getLang() );
	}

	private function getOutputFormatSelect() {
		/*
		 *
		 */
		$selectName = 'format';
		/* FIXME pull from formats */
		// $options = $apiOutputFormats;
		$options = array (
			'xml' => 'XML',
			'dynamickml' => 'Dynamic KML (Google Earth/Google Maps)',
			'kml' => 'Static KML (Google Earth/Google Maps)',
                        'html' => 'HTML table',
                        'wikitable' => 'Wiki table'
		);

		return $this->getSelect ( $selectName , $options );
	}


	private function getSelect ( $selectName, $options, $selected = false ) {
		/*
		 * 
		 */
		$result = array();
		$result[] = '<select name="' . htmlspecialchars( $selectName ) . '" ' . $this->fieldStyle . '>';
		foreach ( $options as $value => $name ) {
			$result[] = '<option value="' . htmlspecialchars( $value ) . '"' .
				( $value === $selected ? ' selected="selected"' : '' ) .	'>' . htmlspecialchars( $name ) . '</option>';
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
