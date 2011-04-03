<html>
<head>
<title>Monuments search mockup</title>
</head>
<body>
<H1>Search the monuments database</H1>
<form>
<table border="1">
<tr>
<th>Field</th>
<th>Search</th>
<th>Filter</th>
</tr>
<tr>
<td><label>Countries</label></td>
<td>&nbsp;<!-- Empty, no search for country --></td>
<td>
<select multiple name="countries" size="5" style="width:300px">
<!-- Pull from database and localize -->
<option value="fr" selected>France</option>
<option value="nl" selected>Netherlands</option>
<option value="pt" selected>Portugal</option>
</select>
</td>
</tr>

<tr>
<td><label>Languages</label></td>
<td>&nbsp;<!-- Empty, no search for languages --></td>
<td>
<select multiple name="languages" size="5" style="width:300px">
<!-- Pull from database and localize -->
<option value="nl" selected>Dutch</option>
<option value="pt" selected>Portugese</option>
</select>
</td>
</tr>

<tr>
<td><label>Name</label></td>
<td><input type="text" name="NameSearch" style="width:300px"></td>
<td><select name="NameFilter" style="width:300px">
<option value="all" selected>All</option>
<option value="set" >Only with name</option>
<option value="unset" >Only without name</option>
</select>
</td>
</tr>

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
