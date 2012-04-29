<?php
/*
 cls.basic_geosearch.php

 Does a basic but scalable&fast non-keyword geo-search (or nearest item search) on a table.
 Includes Peano code generation.
 
 MY: modified the proximity field in sql, 19-06-2011
 
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
	See http://www.lightrod.org/  'Getting Started' section for the most up-to-date instructions.
	See http://www.lightrod.org/mediawiki/index.php/Layar_API  to create a Layar.


	Create a table with your points, and latitude, longitude, e.g. tbl_points (int_point_id, dec_latitude, dec_longitude).
			Note: You can use any field/table names
	Add four 32-bit integer columns called e.g. int_peano1, int_peano2, int_peano1iv, int_peano2iv. (or any alternative names)
	Add multi-column indexes to your table on (int_peano1, int_point_id)
							(int_peano2, int_point_id)
							(int_peano1iv, int_point_id)
							(int_peano2iv, int_point_id)

	Generate the peano codes before searching against the table (this can be done each time a new entry is added, or once at the beginning):

	require("cls.basic_geosearch.php");
	$bg = new clsBasicGeosearch();
	$peano1 = $bg->generate_peano1($latitude, $longitude);		//Lat/lon of point in table
	$peano2 = $bg->generate_peano2($latitude, $longitude);
	$peano1iv = $bg->generate_peano_iv($peano1);
	$peano2iv = $bg->generate_peano_iv($peano2);

	(and then write values back into the table).



	Then carry out a search using the following example:

** Most basic use **


	$params = array('latitude' => 50.00,			//Latitude in decimal degrees of center of search eg. 50.554345 (-90.0 to 90.0)
			'longitude' => 120.00,			//Longitude in decimal degrees of center of search eg. 20.554345 (-180.0 to 180.0)
			'table_name' => "tbl_points",		//Main table name that is being searched on e.g. 'tbl_my_points'
			'id_field' => "int_point_id",		//Unique reference to each point in the table e.g. 'int_point_id'
			'latitude_field' => "dec_latitude",	//Field in table that has the latitude in decimal for each point e.g. 50.554345
			'longitude_field' => "dec_longitude",	//Field in table that has the longitude in decimal for each point e.g. 20.554345
			'peano_field_header' => "int_peano"	//First letters of fields in table that hold peano integers
				 				//E.g. 'int_peano', which gets appended to create 'int_peano1,
				 				//int_peano2, int_peano1iv, int_peano2iv'
			);


	$results_array = $bg->proximity_finder($params);


	Returned values
	--------------

	$results_array[]			- the list of results and the included fields

	foreach($results_array as $result) {
		echo $result['int_point_id'] . ", Dist: " . $result['dist'] .  ", Lat: " . $result['latitude'] . ", Lon: " . $result['longitude'] . "<br>";
	}




	Additional Return Fields
	------------------------  (Optional, if 'provide_count' => true)

	For a search such as:

	$params = array( [...fields here...]
			'provide_count' => true
			);

	list($results_array, $count) = $bg->proximity_finder($params);

	Returns:

	$count['next_record_group']		- value to give $first_record on a 'More results' link
	$count['previous_record_group']		- value to give $first_record on a 'Previous results' link

	$count['coarse_matches']		- if $provide_count = true, total number of matches, approximation
						- uses $whole_data_dist and $max_total_results
	$count['show_next']			- true or false, for showing a 'More Results' link
	$count['show_previous']			- true or false, for showing a 'Previous Results' link


** See more complex usage below **


Notes:

Generates "peano-codes" from latitude and longitude coordinates.  Peano codes are points on a space filling curve.
  For technical information try a map text book such as "Elements of Cartography".
  The Mobilemaps nearby-engine uses peano-codes to perform a highly scalable proximity sort.
  Because one space filling curve can be very inaccurate by itself, Mobilemaps makes use of two separate curves,
  these are accessed by generate_peano1, and generate_peano2, which is a similar curve with a somewhat arbitrary x/y offset.


Note: this differs because PHP doesn't support 32-bit unsigned integers, so a string is returned if the value is negative.
  The returned values can still be inserted into an unsigned int database table, or used in a SQL string for comparisons, as if
  they were an integer.  32-bit is the prefered format to give enough accuracy to be useful.

Original code:
Geo-Mobilemaps-GeoparserLite




** More complex usage - here are all the fields.  Include them as addition params in the $params array **

	//REQUIRED
	//>>>>>>
	latitude			//Latitude in decimal degrees of center of search eg. 50.554345 (-90.0 to 90.0)
	longitude 			//Longitude in decimal degrees of center of search eg. 20.554345 (-180.0 to 180.0)
	table_name 			//Main table name that is being searched on e.g. 'tbl_my_points'
	id_field 			//Unique reference to each point in the table e.g. 'int_point_id'
	latitude_field			//Field in table that has the latitude in decimal for each point e.g. 50.554345
	longitude_field			//Field in table that has the longitude in decimal for each point e.g. 20.554345
	peano_field_header		//First letters of fields in table that hold peano integers
	 				//E.g. 'int_peano', which gets appended to create 'int_peano1,
	 				//int_peano2, int_peano1iv, int_peano2iv'

	 //OPTIONAL
	 //>>>>>>>  (default values give after '=' below)
	misc_fields = ""		//Miscellaneous fields to be selected and put into the results e.g.
	 				// "var_point_title, var_point_description, j.var_my_join_field"
	 				//This is usually from the same table, but can be from different tables
	 				//that are joined with $custom_join below
	first_record = 0		//First record to search from.  After clicking 'more' would set this to say 10
	max_records = 10		//Maximum number of results to display
	provide_count = false		//Provide an approximate count of the results found
	 				//The accuracy varies because it is doesn't count the results, see also
	 				//The count is returned in a second array
	start_record_group = 0		//This functionality is not yet working - once reached the end of the sample of
	 				//results we can look into the next bunch - usually incremented about 200 at a time

	custom_where = ""		//Limit the results to this set e.g. "int_code = 5"
	custom_join = ""		//Include a SQL join to other tables, (after the results have been found),
	 				//and a SQL WHERE clause or GROUP BY clause.  e.g.
	 				//"JOIN tbl_point_details pd ON m.int_point_details_id = pd.int_point_details_id
	 				//	WHERE pd.int_param > 10"
	show_queries = false		//Switch to 'true' to print queries in search to screen for debugging


	units = "km"			//'mi' or 'km' for search results units
	radius = 0			//=0 means no radius applied, otherwise limit results within this many km or miles
	 				//See $radius_units
	radius_units = "km"		//'mi' or 'km' of the radius to search within
	decimal_places = 1		//Precision of results displayed 2 would give 50.32
	get_dist_bearing = true		//5 mi _NE_, shows the bearing towards the result e.g. 'NE'. false switches this off
	relevancy_field = ""		//Field in table that corresponds to a relevancy, that is combined
	 				//with proximity to sort the results e.g. "int_value"
	relevancy_scaler = ""		//A max value that scales the results.  Can include a '-' to be inverted relevancy
	sort_order = 0.0		//Proportion of result ordering devoted to the relevancy field i.e.
	 				//   0.0 = no relevancy field influence, all geo-proximity influence
	 				//   1.0 = all relevancy field influence, no geo-proximity influence
	index_and = ""			//These fields are a part of the main peano database index, and reduce the
	 				//result set grabbed initally before the results are restricted
	 				//e.g. "int_country_id = 5"
	 				//Most useful if you want every result to have this characteristic.
	final_sort_field = ""		//Sort the last set of 10 results, right at the end of the process by this field
	 				//Useful for sorting by e.g. price.  Note: on clicking the 'Next', the results
	 				//will be sorted within the next 10, so the flow of results won't be perfect.
	 				//Note 2: can include ' DESC' to sort descending e.g. 'int_my_sort DESC'
	whole_data_dist = 20		//Distance in degrees around the planet that the whole dataset covers.  Used
	 				//to help approximate the count of results.  If you have global coverage, use
	 				//(full world lat+lon would be = 90+180 = 270)
	max_total_results = 1000000	//Maximum total results, used to prevent total results becoming so large
	 				//with the approximation that it is non-sensical.  Usually set to the
	 				//number of records in the search table.
	peano1_field = ""		//Optional flexible peano field names e.g. "int_peano1"
	peano2_field = ""		//  e.g. "int_peano2"
	peano1iv_field = ""		//  e.g. "int_peano1iv"
	peano2iv_field = ""		//  e.g. "int_peano2iv"





Author: Peter Abrahamson  peter@atomjump.com  18 Feb 09. Document last update 4 July 09.
*/

//error_reporting(E_ERROR | E_PARSE);			//Needed for Windows compatiblity


//This overriding class-exists should prevent class being called up twice
if(!class_exists("clsBasicGeosearch")) {

DEFINE("PI_OVER_180", 0.0174533); //used to convert degrees to radians



class clsBasicGeosearch
{

	public $top_left_latitude;			//Limits search radius (at the end of the search)
	public $top_left_longitude;
	public $bottom_right_longitude;
	public $bottom_right_latitude;

	public $multiplier_weight_prox;
	public $multiplier_weight_rel;
	public $id_field;
	
	public function __construct()	
	{
		//Set default as global search
		$this->top_left_latitude = 90.0;
		$this->top_left_longitude = -180.0;
		$this->bottom_right_longitude = 180.0;
		$this->bottom_right_latitude = -90.0;

		$this->multiplier_weight_prox = 1000;		//Multiplier for proximity
		$this->multiplier_weight_rel = 10;		//Opposite multiplier for relevance
	}


	public function generate_peano1($lat, $lon)
	{
		//Returns two peano codes  Peano1 and Peano2, offset from each other
		//Create a peano from a floating point latitude/longitude
		//value on the earth's surface. Assume a square(?) projection
		//where 1.0 latitude = 1.0 longitude.
		//The 16-bit value generated is centered on the equator (ie. 32768=Equator)
		//and the 0 = -180deg, 65536 = +180deg

		$lat = (($lat + 90.0)/180.0 * 32767) + 16384;
		$lon = ($lon + 180.0)/360.0 * 65535;

		$lat_16 = $lat&0x0000FFFF;
		$lon_16 = $lon&0x0000FFFF;

		$peano = self::derive_peano_32($lat_16, $lon_16);
		return $peano;

	}




	public function generate_peano2($lat, $lon)
	{

		//Same function as peano_latlon, but offset by a particular
		//distance in lat and lon. This will ensure two approximations
		//to the nearest points can be joined together to form
		//one good approximation, removing the chance of being near the
		//edge of a larger quad-tree boundary.
		//The worst cases are the UK W/E at Greenwich, and the US N/S of
		//Minneapolis (45 deg). We'll hence shift to the W by 30 deg which
		//is over the Azores in the Atlantic Ocean, and to the North by 20deg
		//which is at the S of Alaska.
		//Note: to ensure the grids don't naturally re-align nearby, it is
		//useful to have some random noise added.

		$OFFSET_LAT = -23.7432;
		$OFFSET_LON = 29.3456;
		$lat_16;
		$lon_16;

		//Shift according to realignment
		$lat = $lat + $OFFSET_LAT;
		$lon = $lon + $OFFSET_LON;

		//Wrap to the other side of the world horizontally
		//(not needed vertically because still inside the peano's square
		//which extends to 360*360 degs)
		if($lon < -180.0) {
			$lon = $lon + 360.0;
		}
		if($lon > 180.0) {
			$lon = $lon - 360.0;
		}

		$lat = (($lat + 90.0)/180.0 * 32767) + 16384;
		$lon = ($lon + 180.0)/360.0 * 65535;

		$lat_16 = $lat&0x0000FFFF;
		$lon_16 = $lon&0x0000FFFF;

		$peano = self::derive_peano_32($lat_16, $lon_16);

		return $peano;
	}



	private function derive_peano_32($lat_16, $lon_16)
	{
		//Interleave the bits from a latitude value with the bits
		//from a longitude value. Function assumes the latitude and
		//longitude have already been pre-sized to a 16-bit value.
		$peano = 0;
		$mask_in = 1;
		$mask_out = 2;

		for($cnt=0; $cnt<16; $cnt++) {

			if(($lat_16 & $mask_in)!=0) {
				$peano += $mask_out;
			}

			$mask_in = $mask_in << 1;
			$mask_out = $mask_out << 2;

		}

		$mask_in = 1;
		$mask_out = 1;
		for($cnt=0; $cnt<16; $cnt++) {

			if(($lon_16 & $mask_in)!=0) {
				$peano += $mask_out;
			}

			$mask_in = $mask_in << 1;
			$mask_out = $mask_out << 2;

		}

		//PHP doesn't support 32-bit unsigned integers so we need to force it to be a string
		if($peano < 0) {
			$peano = sprintf('%u', $peano);
		}


		return $peano;
	}



	public function generate_peano_iv($peano)
	{
		//Accept a string or integer and get the 32-bit inverse 2^32 = 4294967296  (think 8-bit, 2^8=256, 255 - x = inverse)
		return 4294967295 - $peano;
	}



	public function proximity_finder($params)
	{

		$latitude = $params['latitude'];		//Latitude in decimal degrees of center of search eg. 50.554345 (-90.0 to 90.0)
		$longitude = $params['longitude'];		//Longitude in decimal degrees of center of search eg. 20.554345 (-180.0 to 180.0)
		$table_name = $params['table_name'];		//Main table name that is being searched on e.g. 'tbl_my_points'
		$id_field = $params['id_field'];		//Unique reference to each point in the table e.g. 'int_point_id'
		$this->id_field = $id_field;
		$latitude_field = $params['latitude_field'];	//Field in table that has the latitude in decimal for each point e.g. 50.554345
		$longitude_field = $params['longitude_field'];	//Field in table that has the longitude in decimal for each point e.g. 20.554345
		$peano_field_header = $params['peano_field_header'];  //First letters of fields in table that hold peano integers
					 				//E.g. 'int_peano', which gets appended to create 'int_peano1,
					 				//int_peano2, int_peano1iv, int_peano2iv'

		//Options - set to defaults
		 				//OPTIONAL
		 				//>>>>>>>
		 $first_record = 0;		//First record to search from.  After clicking 'more' would set this to say 10
		 $max_records = 10;		//Maximum number of results to display
		 $provide_count = false;	//Provide an approximate count of the results found
		 				//The accuracy varies because it is doesn't count the results; see also
		 				//The count is returned in a second array
		 $start_record_group = 0;	//This functionality is not yet working - once reached the end of the sample of
		 				//results we can look into the next bunch - usually incremented about 200 at a time

		 $misc_fields = "";		//Miscellaneous fields to be selected and put into the results e.g.
		 				// "var_point_title; var_point_description, j.var_my_join_field"
		 				//This is usually from the same table, but can be from different tables
		 				//that are joined with $custom_join below
		 $custom_where = "";		//Limit the results to this set e.g. "int_code = 5"
		 $custom_join = "";		//Include a SQL join to other tables, (after the results have been found),
		 				//and a SQL WHERE clause or GROUP BY clause.  e.g.
		 				//"JOIN tbl_point_details pd ON m.int_point_details_id = pd.int_point_details_id
		 				//	WHERE pd.int_param > 10"
		 $show_queries = false;		//Switch to 'true' to print queries in search to screen for debugging
		 $units = "km";			//'mi' or 'km' for search results units
		 $radius = 0;			//=0 means no radius applied, otherwise limit results within this many km or miles
		 				//See $radius_units
		 $radius_units = "km";		//'mi' or 'km' of the radius to search within
		 $decimal_places = 1;		//Precision of results displayed 2 would give 50.32
		 $get_dist_bearing = true;	//5 mi _NE_, shows the bearing towards the result e.g. 'NE'. false switches this off
		 $relevancy_field = "";		//Field in table that corresponds to a relevancy, that is combined
		 				//with proximity to sort the results e.g. "int_value"
		 $relevancy_scaler = "";	//A max value that scales the results.  Can include a '-' to be inverted relevancy
		 $sort_order = 0.0;		//Proportion of result ordering devoted to the relevancy field i.e.
		 				//   0.0 = no relevancy field influence, all geo-proximity influence
		 				//   1.0 = all relevancy field influence, no geo-proximity influence
		 $index_and = "";		//These fields are a part of the main peano database index, and reduce the
		 				//result set grabbed initally before the results are restricted
		 				//e.g. "int_country_id = 5"
		 				//Most useful if you want every result to have this characteristic.
		 $final_sort_field = "";	//Sort the last set of 10 results, right at the end of the process by this field
		 				//Useful for sorting by e.g. price.  Note: on clicking the 'Next', the results
		 				//will be sorted within the next 10, so the flow of results won't be perfect.
		 				//Note 2: can include ' DESC' to sort descending e.g. 'int_my_sort DESC'
		 $whole_data_dist = 20;		//Distance in degrees around the planet that the whole dataset covers.  Used
		 				//to help approximate the count of results.  If you have global coverage, use
		 				//(full world lat+lon would be = 90+180 = 270)
		 $max_total_results = 1000000;	//Maximum total results, used to prevent total results becoming so large
		 				//with the approximation that it is non-sensical.  Usually set to the
		 				//number of records in the search table.
		 $peano1_field = "";		//Optional flexible peano field names e.g. "int_peano1"
		 $peano2_field = "";		//  e.g. "int_peano2"
		 $peano1iv_field = "";		//  e.g. "int_peano1iv"
		 $peano2iv_field = "";		//  e.g. "int_peano2iv"
		 $custom_having = "";		//Having instead of where clause
		 $keep_results_table = false;	//Keeps results in temporary table 'final_results'.  User must 'drop table final_results' after use.
		 $sample_data_callback = "";	//Can be used to process the results in all_data which have come from the sample 400 odd results
		 				//before selecting the final 10.
		 $sample_data_callback_params = null; 	//Params as an array into the callback function above
		 $pure_proximity = false;		//Set to not blank to refer to the pure proximity value (without the relevance, as pure_proximity)
		 $units_in_full = false;			//Mile units in full as 'miles' when true
		 $show_bearing = true;				//Show bearing e.g. 'NE'


		if(isset($params['first_record'])) $first_record = $params['first_record'];
		if(isset($params['max_records'])) $max_records = $params['max_records'];
		if(isset($params['provide_count'])) $provide_count = $params['provide_count'];
		if(isset($params['start_record_group'])) $start_record_group = $params['start_record_group'];
		if(isset($params['misc_fields'])) $misc_fields = $params['misc_fields'];
		if(isset($params['custom_where'])) $custom_where = $params['custom_where'];
		if(isset($params['custom_join'])) $custom_join = $params['custom_join'];
		if(isset($params['show_queries'])) $show_queries = $params['show_queries'];
		if(isset($params['units'])) $units = $params['units'];
		if(isset($params['radius'])) $radius = $params['radius'];
		if(isset($params['radius_units'])) $radius_units = $params['radius_units'];
		if(isset($params['decimal_places'])) $decimal_places = $params['decimal_places'];
		if(isset($params['get_dist_bearing'])) $get_dist_bearing = $params['get_dist_bearing'];
		if(isset($params['relevancy_field'])) $relevancy_field = $params['relevancy_field'];
		if(isset($params['relevancy_scaler'])) $relevancy_scaler = $params['relevancy_scaler'];
		if(isset($params['sort_order'])) $sort_order = $params['sort_order'];
		if(isset($params['index_and'])) $index_and = $params['index_and'];
		if(isset($params['final_sort_field'])) $final_sort_field = $params['final_sort_field'];
		if(isset($params['whole_data_dist'])) $whole_data_dist = $params['whole_data_dist'];
		if(isset($params['max_total_results'])) $max_total_results = $params['max_total_results'];
		if(isset($params['peano1_field'])) $peano1_field = $params['peano1_field'];
		if(isset($params['peano2_field'])) $peano2_field = $params['peano2_field'];
		if(isset($params['peano1iv_field'])) $peano1iv_field = $params['peano1iv_field'];
		if(isset($params['peano2iv_field'])) $peano2iv_field = $params['peano2iv_field'];


		if($peano1_field == "") {
			$peano1_field = $peano_field_header . "1";
		}
		if($peano2_field == "") {
			$peano2_field = $peano_field_header . "2";
		}
		if($peano1iv_field == "") {
			$peano1iv_field = $peano_field_header . "1iv";
		}
		if($peano2iv_field == "") {
			$peano2iv_field = $peano_field_header . "2iv";
		}


		if(isset($params['custom_having'])) $custom_having = $params['custom_having'];
		if(isset($params['keep_results_table'])) $keep_results_table = $params['keep_results_table'];
		if(isset($params['sample_data_callback'])) $sample_data_callback = $params['sample_data_callback'];
		if(isset($params['sample_data_callback_params'])) $sample_data_callback_params = $params['sample_data_callback_params'];
		if(isset($params['pure_proximity'])) $pure_proximity = $params['pure_proximity'];
		if(isset($params['units_in_full'])) $units_in_full = $params['units_in_full'];
		if(isset($params['show_bearing'])) $show_bearing = $params['show_bearing'];


		return self::proximity_search($latitude, $longitude, $radius, $radius_units, $table_name,
					$id_field, $latitude_field, $longitude_field, $peano1_field, $peano2_field,
					$peano1iv_field, $peano2iv_field, $misc_fields, $relevancy_field, $relevancy_scaler,
					$sort_order,$show_queries, $custom_where, $get_dist_bearing, $units, $decimal_places,
					$first_record, $max_records, $start_record_group, $custom_join, $index_and,
					$provide_count, $whole_data_dist, $max_total_results, $final_sort_field, $custom_having, $keep_results_table,
					$sample_data_callback, $sample_data_callback_params, $pure_proximity,$units_in_full,$show_bearing);

	}








	public function proximity_search($latitude, $longitude, $radius, $radius_units, $table_name,
						$id_field, $latitude_field, $longitude_field, $peano1_field, $peano2_field,
						$peano1iv_field, $peano2iv_field, $misc_fields, $relevancy_field, $relevancy_scaler,
						$sort_order,$show_queries, $custom_where, $get_dist_bearing, $units, $decimal_places,
						$first_record, $max_records, $start_record_group, $custom_join, $index_and,
						$provide_count, $whole_data_dist, $max_total_results, $final_sort_field = "", $custom_having="", $keep_results_table = false,
						$sample_data_callback = false, $sample_data_callback_params = null, $pure_proximity = false, $units_in_full = true, $show_bearing = true)
	{
		//Searches a list of records geographically close to the input latitude/longitude,
		// in a table which has been geographically indexed with two Peano codes (using generate_peano()).

		//Clip to the right number of dp - otherwise the sql query subtraction in the abs()
		//comes up with slightly wrong sort order
		$latitude = (float)sprintf("%.7f", $latitude);
		$longitude = (float)sprintf("%.7f", $longitude);

		//Convert input latitude/longitude into a peano and peanoiv
		$my_peano1 = self::generate_peano1($latitude, $longitude);
		$my_peano2 = self::generate_peano2($latitude, $longitude);
		$my_peano1iv = self::generate_peano_iv($my_peano1);
		$my_peano2iv = self::generate_peano_iv($my_peano2);

		//$first_record = 0;
		//$max_records = 20;

	  	$buff_empty = 200;		//Record number in an empty word query. Usage is a 4X multiplier
	  					//with a certain number of duplicates eg. 268 records/400 might be typical
	  					//for $buff_empty = 100.
		//$start_record_group = 0;
		$next_group = $buff_empty;
	  	$previous_group = 0;
	  	$more_group = 1;		//Assume there will be a more link, unless told otherwise
	  	$less_group = 1;


		//Constant proportions. When relevance = -5,  proximity = 100 it gives a
		  //								pretty good city level search balanced between relevance
		  //                        and proximity sort.  These are magic numbers based on
		  //                        a 'feeling'.  Therefore, X2 these values, because that is
		  //                        when $sort_order is at 0.5/0.5 on the seesaw.
		  $weight_rel = -$this->multiplier_weight_rel*($sort_order); //multiplier weight for relevance when used to order results
		  $weight_prox = $this->multiplier_weight_prox*(1.0-$sort_order); //multiplier weight for proximity when used to order results



	 	 //Weight the proximity calculation so that latitude and longitude are proportional
	 	 //To do this we need to multiple all longitude deltas by cosine of the search-longitude
	 	 $cosine_search_latitude = cos($latitude * PI_OVER_180); //degrees converted to radians for cosine
	  	 $cosine_search_latitude = sprintf("%.6f", $cosine_search_latitude);	//limit the number of decimal places for the SQL query

		//Set the radius as a square if we're setting a radius at all
		if(($radius)&&($radius != 0.0)) {
			$restrict_dist = self::get_limits_from_radius($radius, $radius_units, $latitude, $longitude);
		}


		//Ensure custom where is correct for sql
		if($custom_where != "") {
			$custom_where = " AND " . $custom_where;
		}

		if($custom_having != "") {
			$custom_where = " HAVING " . $custom_having;		//Goes instead of custom_where and overwrites it
		}

		if($index_and != "") {
			$index_and = " AND " . $index_and;
		}

		if($misc_fields != "") {
			//Replace field names with m.[field name]
			$token = strtok($misc_fields, ",");
			$full_string = "";

			while ($token != false)
			{
			  //If we haven't specified the table (and it isn't a number field), make it from markers table
			  if((stripos($token, ".") == false)
			  	&&(stripos($token, "(") == false)
			  	&&(stripos($token, "AS") == false)) {
			  	$full_string .= ", m." . trim($token);
			  } else {
			  	$full_string .= ", " . trim($token);
			  }
			  $token = strtok(",");
			}

			$misc_fields = $full_string;
			//echo "MISC
		}



 		//Find the limit of records that we want eg. 0-15
		  if ($first_record) {
			if(!isset($max_records)) {echo "Max_records must also be specified if first_record is specified!\n"; die;};
		  } else {
			$first_record = 0; //if first record is "", then set it to 0
		  };
		  if ($max_records) {
			$select_limit = "$first_record, " . ($max_records +1);  //+1 because we 										//want to know if there are any more results
		  };


		  //Final sort
		  if(($final_sort_field != "")||($keep_results_table == true)) {
		  	$final_sort_create = "create temporary table final_results engine=heap ";
		  }

		 //If we need to refer to the true proximity in degrees (incl cos), set here
		 if($pure_proximity == true) {		//This is only here because PADZ needed to refer to the pure proximity calculation
			$pure_proximity_incl = " , (ABS(latitude - $latitude) + ABS(longitude - $longitude)*$cosine_search_latitude) AS pure_proximity ";
		 } else {
			$pure_proximity_incl = "";
		 }



		$sql = "create temporary table nearest_matches engine=heap select $id_field from $table_name where $peano1_field>=$my_peano1 $index_and limit $start_record_group,$buff_empty";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql) or die("Unable to execute query $sql " . mysql_error());

		$sql = "insert into nearest_matches select $id_field from $table_name where $peano1iv_field>$my_peano1iv $index_and limit $start_record_group,$buff_empty";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql);

		$sql = "insert into nearest_matches select $id_field from $table_name where $peano2_field>$my_peano2 $index_and limit $start_record_group,$buff_empty";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql);

		$sql = "insert into nearest_matches select $id_field from $table_name where $peano2iv_field>$my_peano2iv $index_and limit $start_record_group,$buff_empty";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql);

		$sql = "create temporary table grouped_matches($id_field INT NOT NULL, INDEX USING BTREE ($id_field)) engine=heap";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql);

		$sql = "insert into grouped_matches select $id_field from nearest_matches group by $id_field";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql);




		$sql = "create temporary table all_data type=heap SELECT g.$id_field, m.$latitude_field AS latitude, m.$longitude_field AS longitude ";
		if($relevancy_field != "") {
			//$sql .= ", m.$relevancy_field ";  //Instead - put in misc_fields
		}
		$sql .= " $misc_fields FROM grouped_matches g JOIN $table_name m ON g.$id_field = m.$id_field $custom_join";
		//push($drop_tables, 'all_data');
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql) or die("Unable to execute query $sql " . mysql_error());


		//Get a count of the coarse number of results - doesn't take into account lat/lon limits below
		if($provide_count == true) {
			$count['coarse_matches'] = self::get_coarse_matches($latitude, $longitude, $whole_data_dist, $restrict_dist, $max_total_results, ($first_record+$max_records), $show_queries);

		}

		//See if we want to process the all_data table before selecting the final results - this could be use to generate a different
		//sort order by dynamically generating values in the relevance_field.  Uses a call-back to a user function.
		if($sample_data_callback != "") {
			if($sample_data_callback_params != null) {
				call_user_func($sample_data_callback, $sample_data_callback_params);
			} else {
				call_user_func($sample_data_callback);
			}
		}


		//If we have a relevancy field that includes a number that increases indefinitely e.g. a number of times clicked
		//we can do an aggregate query to get a max, so that the relevancy can be scaled in proportion to the location
		$relevancy_max = 255;
		if($relevancy_scaler != "") {
			$sql = "select " . $relevancy_scaler . " as max_relevancy from all_data";
			if($show_queries == true) { echo $sql . ";<br/>"; };
			$result = mysql_query($sql)  or die("Unable to execute query $sql " . mysql_error());
			if($row = mysql_fetch_array($result))
			{
				if($row['max_relevancy']) {
					$relevancy_max = $row['max_relevancy'];
				} else {
					//No records - allow to flow through with a 1 value - there will simply be no results below
					$relevancy_max = 1;
				}

			} else {
				//No records - allow to flow through with a 1 value - there will simply be no results below
				$relevancy_max = 1;
			}

		}



		$sql = "$final_sort_create select all_data.*, (((POWER(ABS(latitude - $latitude),2) + POWER(ABS(longitude - $longitude)*$cosine_search_latitude,2))*$weight_prox)";
		if($relevancy_field != "" ) {
			$sql .= "+ (($relevancy_field/$relevancy_max)*255 * $weight_rel)";
		}
		$sql .= ") AS proximity $pure_proximity_incl from all_data WHERE (latitude BETWEEN $this->bottom_right_latitude AND $this->top_left_latitude) AND (longitude BETWEEN $this->top_left_longitude AND $this->bottom_right_longitude) $custom_where ORDER BY proximity limit " . $select_limit;
		if($show_queries == true) { echo $sql . ";<br/>"; };
		$result = mysql_query($sql) or die("Unable to execute query $sql " . mysql_error());;



		if($final_sort_field == "") {
			if($keep_results_table == false) {
				//This is the results set
				$results = array();
				$rows_cnt = 0;
				while($row = mysql_fetch_array($result))
				{
					$results[] = $row;
					$rows_cnt++;
				}
			} else {
				//This was a create table, that we simply want to write out
				$sql = "SELECT * FROM final_results";
				if($show_queries == true) { echo $sql . ";<br/>"; };
				$result = mysql_query($sql) or die("Unable to execute query $sql " . mysql_error());;

				$results = array();
				$rows_cnt = 0;
				while($row = mysql_fetch_array($result))
				{
					$results[] = $row;
					$rows_cnt++;
				}
			}
		} else {
			//This was a create table, that we want to sort on now for the final sort
			$sql = "SELECT * FROM final_results ORDER BY $final_sort_field";
			if($show_queries == true) { echo $sql . ";<br/>"; };
			$result = mysql_query($sql) or die("Unable to execute query $sql " . mysql_error());;

			$results = array();
			$rows_cnt = 0;
			while($row = mysql_fetch_array($result))
			{
				$results[] = $row;
				$rows_cnt++;
			}
		}

		//Determine whether to show a next or previous
		//Figure out what the next group address should be
		$next_group = $start_record_group + $buff_empty;
		$previous_group = $start_record_group - $buff_empty;

		if($more_group == 0) {
		 	$next_group = 0;
		}
	  	$count['next_record_group'] = $next_group;


		//Stop going backwards past the beginning of the search results
		if($previous_group < 0) {
		 	$previous_group = 0;
		}
		$count['previous_record_group'] = $previous_group;


		//Calculate a count
		if($provide_count == true) {


			if($rows_cnt > $max_records) {	//1 more record than displaying
				//We don't know exactly how many, so use 'about'
				$count['coarse_matches'] = "about " . $count['coarse_matches'];
				$count['show_next'] = true;
				$count['next_first_record'] = $first_record + $max_records;
			} else {
				//We know we're less than the display
				$count['coarse_matches'] = $first_record + $rows_cnt;
				$count['show_next'] = false;

			}

			if($first_record >= $max_records) {
				$count['show_previous'] = true;
				$count['previous_first_record'] = $first_record - $max_records;		//TODO: handle case of previous record group

			} else {
				$count['show_previous'] = false;
			}

			//The last record is not needed for display purposes
			if($rows_cnt > $max_records) {
				array_pop($results);
				$rows_cnt --;
			}

			//Get the number of records to display range
			$count['precise_in_display'] = $rows_cnt;
			if($rows_cnt > $max_records) {
				$count['precise_in_display'] = $max_records;
			}
			$count['start_record'] = $first_record + 1;
			$count['end_record'] = $first_record + $rows_cnt;
		}




		//Optional post processing
		if($get_dist_bearing == true) {


			//Loop through to calculate with distance and bearing
			foreach($results as &$result) {
				list($direction, $distance) = self::calculate_direction_and_distance($latitude, $longitude, $result['latitude'], $result['longitude'], $units);
				$result['raw_dist'] = $distance;
				$result['dist'] = self::abbreviate_distance($distance, $units, $decimal_places, $units_in_full);
				if($show_bearing == true) {
					$result['dist'] = $result['dist'] . " " .
							self::abbreviate_bearing($direction);
				}
			}

		}

		if($keep_results_table == false) {
			$sql = "drop table grouped_matches";
			if($show_queries == true) { echo $sql . ";<br/>"; };
			mysql_query($sql);

			$sql = "drop table nearest_matches";
			if($show_queries == true) { echo $sql . ";<br/>"; };
			mysql_query($sql);

			$sql = "drop table all_data";
			if($show_queries == true) { echo $sql . ";<br/>"; };
			mysql_query($sql);

			if($final_sort_field != "") {
				$sql = "drop table final_results";
				if($show_queries == true) { echo $sql . ";<br/>"; };
				mysql_query($sql);
			}
		}


		//Return data
		if($provide_count == true) {
			$return_collection[] = $results;
			$return_collection[] = $count;
		} else {
			$return_collection = $results;
		}

		return $return_collection;

	}






	private function get_coarse_matches($latitude, $longitude, $whole_data_dist, $restrict_dist, $max_total_results, $min_results, $show_queries)
	{
		//Get a fast approximation of number of results based on distance to the furtherest result
		//in the 1000 old result set sample, versus distance in the whole result set.

		//Can't get the count from the select above because it is creating a table at the same time
		//I think this is the fastest method which uses the MySQL structure itself (not mysql_num_rows())
		$sql = "select count(*) as coarse_count from all_data";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		$result_c = mysql_query($sql) or die("Unable to execute query $sql " . mysql_error());
		if($row = mysql_fetch_array($result_c))
		{
			$rough_results = $row['coarse_count'];

			//echo "Rough results = $rough_results";

			if($rough_results > 1) {

				$random_sample = (int)($rough_results-1)/2;		//A random location, but fixed so that number remains the same
				$random_sample = (int)$random_sample;

				//TODO: get the average distance to several random samples to get a better idea

				//Now scale according to the size of the whole set - get the lat/lon of the last result
				$sql = "SELECT latitude, longitude FROM all_data LIMIT " . $random_sample . ",1";
				if($show_queries == true) { echo $sql . ";<br/>"; };
				$result_l = mysql_query($sql) or die("Unable to execute query $sql " . mysql_error());
				if($row = mysql_fetch_array($result_l))
				{
					//Furtherest point distance
					$f_lat = (float)$row['latitude'];
					$f_lon = (float)$row['longitude'];

					$f_dist = abs((float)$f_lat - $latitude) + abs((float)$f_lon - $longitude);		//Get a rough approximate distance

					//echo $f_dist;

					if($f_dist == 0.0) {
						$f_dist = 0.0000001;		//Handle a 0 value
					}

					if(($restrict_dist)&&($restrict_dist!=0)) {
						$course_results = $rough_results * ($restrict_dist/$f_dist);
					} else {
						$course_results = $rough_results * ($whole_data_dist/$f_dist);
					}

					if($course_results > $max_total_results) {
						$course_results = $max_total_results;	//Don't want a huge number more than actually exist
					}

					if($course_results < $min_results) {
						$course_results = $min_results+1;
					}

					//echo "Course results = $course_results";

					return (int)$course_results;

				}
			}



		}

		return 0;

	}


	public function get_bounds_of_results($results_array, $longitude, $latitude, $limit_at, $mirror_from_center)
	{
		//Takes a list of latitudes and longitudes (returned from a proximity_search call),
		//and return a bounding box after a certain number that encompasses all of them.
		//This is most useful to zoom out to include a certain number of results.
		//The longitude/latitude input is that of the viewer's location, and that becomes
		//a part of the list too.


		//Default to the current location
		$max_latitude = $latitude;
		$min_latitude = $latitude;
		$max_longitude = $longitude;
		$min_longitude = $longitude;




		for($cnt=0; (($cnt<$limit_at)&&($results_array[$cnt])); $cnt++) {

			if($results_array[$cnt]['latitude'] > $max_latitude) {
				$max_latitude = $results_array[$cnt]['latitude'];
			}

			if($results_array[$cnt]['latitude'] < $min_latitude) {
				$min_latitude = $results_array[$cnt]['latitude'];
			}

			if($results_array[$cnt]['longitude'] > $max_longitude) {
				$max_longitude = $results_array[$cnt]['longitude'];
			}

			if($results_array[$cnt]['longitude'] < $min_longitude) {
				$min_longitude = $results_array[$cnt]['longitude'];
			}
		}

		if($mirror_from_center == true) {
			//This option means we put the box around the map to equal
			//lengths on both sides mirrored, as opposed to skewed off in one direction

			$d_west = $longitude - $min_longitude;
			$d_east = $max_longitude - $longitude;
			//echo "Dwest = " . $d_west . " Deast=" . $d_east;
			if($d_west > $d_east) {
				$bounding_box['e'] = $longitude + $d_west;
				$bounding_box['w'] = $longitude - $d_west;
				$bounding_box['dist'] = $d_west;		//Get an approx dist
				//echo "<br> First half = " . $d_west;
			} else {
				$bounding_box['e'] = $longitude + $d_east;
				$bounding_box['w'] = $longitude - $d_east;
				$bounding_box['dist'] = $d_east;		//Get an approx dist
				//echo "<br> First half = " . $d_east;
			}



			$d_south = $latitude - $min_latitude;
			$d_north = $max_latitude - $latitude;
			//echo "Dnorth = " . $d_north . " Dsouth=" . $d_south;
			if($d_south > $d_north) {
				$bounding_box['n'] = $latitude + $d_south;
				$bounding_box['s'] = $latitude - $d_south;
				$bounding_box['dist'] += $d_south;		//Get an approx dist
				//echo "<br> 2nd half = " . $d_south;
			} else {
				$bounding_box['n'] = $latitude + $d_north;
				$bounding_box['s'] = $latitude - $d_north;
				$bounding_box['dist'] += $d_north;		//Get an approx dist
				//echo "<br> 2nd half = " . $d_north;
			}



		} else {
			//Use the bounds directly

			$bounding_box['w'] = $min_longitude;
			$bounding_box['e'] = $max_longitude;
			$bounding_box['s'] = $min_latitude;
			$bounding_box['n'] = $max_latitude;
			$bounding_box['dist'] = ($max_latitude - $latitude) + ($max_longitude - $longitude); //Get an approx dist
		}

		return $bounding_box;
	}


	public function count_results_in_box($results, $north, $south, $west, $east)
	{
		//Loops through a result set, and count how many results are inside a bounding box
		$cnt = 0;

		foreach($results as $result)
		{
			if(($result['latitude'] <= $north)&&
			 	($result['latitude'] >= $south)&&
			 	($result['longitude'] <= $east)&&
			 	($result['longitude'] >= $west)) {

			 	$cnt ++;
			 }
		}

		return $cnt;
	}



	public function super_proximity_search($latitude, $longitude, $radius, $radius_units, $table_name,
						$id_field, $latitude_field, $longitude_field, $peano1_field, $peano2_field,
						$peano1iv_field, $peano2iv_field, $misc_fields, $relevancy_field, $relevancy_scaler,
						$sort_order,$show_queries, $custom_where, $super_field, $super_on, $super_off)
	{
		//Searches a list of records geographically close to the input latitude/longitude,
		// in a table which has been geographically indexed with two Peano codes (using generate_peano()).
		//This is very similar to proximity_search, but is built for the special case of a double
		//search, where the results are broken by an on/off category (which is less complex than a word).
		//Application: trying to find the most popular results within a given radius, but the single search
		//hits it's limit, and popular entries from further away are not considered.
		//Therefore, a second search is carries out on a special index that
		//only has the most popular entries included, and the results are combined from all of them.

		//Convert input latitude/longitude into a peano and peanoiv
		$my_peano1 = self::generate_peano1($latitude, $longitude);
		$my_peano2 = self::generate_peano2($latitude, $longitude);
		$my_peano1iv = self::generate_peano_iv($my_peano1);
		$my_peano2iv = self::generate_peano_iv($my_peano2);

		$first_record = 0;
		$max_records = 20;		//Tempin TODO - make these input params

	  	$buff_empty = 200;		//Record number in an empty word query. Usage is a 4X multiplier
	  					//with a certain number of duplicates eg. 268 records/400 might be typical
	  					//for $buff_empty = 100.
		$start_record_group = 0;



		//Constant proportions. When relevance = -5,  proximity = 100 it gives a
		  //								pretty good city level search balanced between relevance
		  //                        and proximity sort.  These are magic numbers based on
		  //                        a 'feeling'.  Therefore, X2 these values, because that is
		  //                        when $sort_order is at 0.5/0.5 on the seesaw.
		  $weight_rel = -10*($sort_order); //multiplier weight for relevance when used to order results
		  $weight_prox = 1000*(1.0-$sort_order); //multiplier weight for proximity when used to order results


	 	 //Weight the proximity calculation so that latitude and longitude are proportional
	 	 //To do this we need to multiple all longitude deltas by cosine of the search-longitude
	 	 $cosine_search_latitude = cos($latitude * PI_OVER_180); //degrees converted to radians for cosine
	  	 $cosine_search_latitude = sprintf("%.6f", $cosine_search_latitude);	//limit the number of decimal places for the SQL query


		//Ensure custom where is correct for sql
		if($custom_where != "") {
			$custom_where = " AND " . $custom_where;
		}

		if($misc_fields != "") {
			//Replace field names with m.[field name]
			$token = strtok($misc_fields, ",");
			$full_string = "";

			while ($token != false)
			{
			  $full_string .= ", m." . trim($token);
			  $token = strtok(",");
			}

			$misc_fields = $full_string;
			//echo "MISC
		}



 		//Find the limit of records that we want eg. 0-15
		  if ($first_record) {
			if(!isset($max_records)) {echo "Max_records must also be specified if first_record is specified!\n"; die;};
		  } else {
			$first_record = 0; //if first record is "", then set it to 0
		  };
		  if ($max_records) {
			$select_limit = "$first_record, $max_records";
		  };


		//Super off
		$sql = "create temporary table nearest_matches engine=heap select $id_field from $table_name where $peano1_field>=$my_peano1 and $super_field = $super_off limit $start_record_group,$buff_empty";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql) or die("Unable to execute query $sql " . mysql_error());

		$sql = "insert into nearest_matches select $id_field from $table_name where $peano1iv_field>$my_peano1iv and $super_field = $super_off limit $start_record_group,$buff_empty";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql) or die("Unable to execute query $sql " . mysql_error());

		$sql = "insert into nearest_matches select $id_field from $table_name where $peano2_field>$my_peano2 and $super_field = $super_off limit $start_record_group,$buff_empty";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql) or die("Unable to execute query $sql " . mysql_error());

		$sql = "insert into nearest_matches select $id_field from $table_name where $peano2iv_field>$my_peano2iv and $super_field = $super_off limit $start_record_group,$buff_empty";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql) or die("Unable to execute query $sql " . mysql_error());


		//Super on search
		$sql = "insert into nearest_matches select $id_field from $table_name where $peano1_field>=$my_peano1 and $super_field = $super_on limit $start_record_group,$buff_empty";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql) or die("Unable to execute query $sql " . mysql_error());

		$sql = "insert into nearest_matches select $id_field from $table_name where $peano1iv_field>$my_peano1iv and $super_field = $super_on limit $start_record_group,$buff_empty";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql)or die("Unable to execute query $sql " . mysql_error());

		$sql = "insert into nearest_matches select $id_field from $table_name where $peano2_field>$my_peano2 and $super_field = $super_on limit $start_record_group,$buff_empty";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql) or die("Unable to execute query $sql " . mysql_error());

		$sql = "insert into nearest_matches select $id_field from $table_name where $peano2iv_field>$my_peano2iv and $super_field = $super_on limit $start_record_group,$buff_empty";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql) or die("Unable to execute query $sql " . mysql_error());



		$sql = "create temporary table grouped_matches($id_field INT NOT NULL, INDEX USING BTREE ($id_field)) engine=heap";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql) or die("Unable to execute query $sql " . mysql_error());

		$sql = "insert into grouped_matches select $id_field from nearest_matches group by $id_field";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql) or die("Unable to execute query $sql " . mysql_error());




		$sql = "create temporary table all_data type=heap SELECT g.$id_field, m.$latitude_field AS latitude, m.$longitude_field AS longitude ";
		if($relevancy_field != "") {
			$sql .= ", m.$relevancy_field ";
		}
		$sql .= " $misc_fields FROM grouped_matches g JOIN $table_name m ON g.$id_field = m.$id_field";
		//push($drop_tables, 'all_data');
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql) or die("Unable to execute query $sql " . mysql_error());


		//If we have a relevancy field that includes a number that increases indefinitely e.g. a number of times clicked
		//we can do an aggregate query to get a max, so that the relevancy can be scaled in proportion to the location
		$relevancy_max = 255;


		if($relevancy_scaler != "") {
			$sql = "select " . $relevancy_scaler . " as max_relevancy from all_data";
			if($show_queries == true) { echo $sql . ";<br/>"; };
			$result = mysql_query($sql)  or die("Unable to execute query $sql " . mysql_error());
			if($row = mysql_fetch_array($result))
			{
				if($row['max_relevancy']) {
					$relevancy_max = $row['max_relevancy'];
				} else {
					//No records - allow to flow through with a 1 value - there will simply be no results below
					$relevancy_max = 1;
				}

			} else {
				//No records - allow to flow through with a 1 value - there will simply be no results below
				$relevancy_max = 1;
			}

		}

		$sql = "select all_data.*, (((ABS(latitude - $latitude) + ABS(longitude - $longitude)*$cosine_search_latitude)*$weight_prox) ";
		if($relevancy_field != "" ) {
			$sql .= "+ (($relevancy_field/$relevancy_max)*255 * $weight_rel)";
		}
		$sql .= ") AS proximity from all_data WHERE (latitude BETWEEN $this->bottom_right_latitude AND $this->top_left_latitude) AND (longitude BETWEEN $this->top_left_longitude AND $this->bottom_right_longitude) $custom_where ORDER BY proximity limit $select_limit";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		$result = mysql_query($sql) or die("Unable to execute query $sql " . mysql_error());
		while($row = mysql_fetch_array($result))
		{
			$results[] = $row;
		}

		$sql = "drop table grouped_matches";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql);

		$sql = "drop table nearest_matches";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql);

		$sql = "drop table all_data";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql);


		return $results;

	}



	private function get_limits_from_radius($radius, $units, $latitude, $longitude)
	{
		//Function sets $this->top_left_latitude = 90.0;
		//		$this->top_left_longitude = -180.0;
		//		$this->bottom_right_longitude = 180.0;
		//		$this->bottom_right_latitude = -90.0;
		//with a square around latitude/longitude based on the radius
		//Radius = 6371 km (≈3,959 mi).


		$pi = 3.1415927;
		$two_pi_r_by_360 = 0;
		if ($units == 'mi') { //imperial miles
			$c360_by_two_pi_r = 0.014472286; // = 360/(2*3.1415927*3959)
		} else { //default to km metric
			$c360_by_two_pi_r = 0.008993216; //= 360/(2*3.1415927*6371)
		};								//used for km distance between points

		$pi_over_180 = 0.0174533; //pi/180 is the degree to radian converter


		//get the latitude of the current position in radians so
		//it can be used in cos(lat) to calculate how much to scale x
		$lat_radians = $latitude * $pi_over_180;

		//y deg = dist * 360 / 2 PI R
		//x deg = dist * cos (latitude) * 360 / 2 PI R
		$dx = ($c360_by_two_pi_r * cos($lat_radians)) * $radius; //in km units
		$dy = $c360_by_two_pi_r * $radius; //in km units

		//echo "Dx= $dx  Dy=$dy";
		$this->bottom_right_longitude = (float)$longitude + $dx;
		$this->top_left_longitude = (float)$longitude - $dx;
		$this->top_left_latitude = (float)$latitude + $dy;
		$this->bottom_right_latitude = (float)$latitude - $dy;

		return $dx;
	}




	private function calculate_direction_and_distance($lat_first, $long_first, $first_marker_latitude, $first_marker_longitude, $units)
	{

		//calculates the direction (bearing) in radians of the first search result marker
		//from the user's location.

		//use: list($direction, $distance) = calculate_direction_and_distance($lat_first,
		//										$long_first,
		//										$first_marker_latitude,
		//										$first_marker_longitude,
		//										$units);

		//echo "lat_first: $lat_first  lon_first: $long_first  first_marker_latitude:$first_marker_latitude, first_marker_longitude: $first_marker_longitude<br>";

		$direction = 0;
		$distance = 0; //outputs

		$pi = 3.1415927;
		$two_pi_r_by_360 = 0;
		if ($units == 'mi') { //imperial miles
			$two_pi_r_by_360 = 69.094; //178.951;
		} else { //default to km metric
			$two_pi_r_by_360 = 111.195; //two * pi * radius of earth / 360
		};								//used for km distance between points

		$pi_over_180 = 0.0174533; //pi/180 is the degree to radian converter

		//1. handle case of closest marker being ON the user's location (divide by zero problem)
		if (($lat_first == $first_marker_latitude) and
			($long_first == $first_marker_longitude)) {
				$direction = 0; //default to due north in this case
		} else {

			//get the latitude of the current position in radians so
			//it can be used in cos(lat) to calculate how much to scale x
			$lat_radians = $lat_first * $pi_over_180;

			//2. find x,y differences
			$x = (float)$first_marker_longitude - $long_first;
			$x = $x * $two_pi_r_by_360 * cos($lat_radians); //in km units
			$y = (float)$first_marker_latitude - $lat_first;
			$y = $y * $two_pi_r_by_360; //in km units
			//$distance = sqrt(($x * $x) + ($y * $y));
			$three_eighths = 0.375;
			$absy = $y;
			if($y < 0) {
				$absy = -$y;
			}
			$absx = $x;
			if($x < 0) {
				$absx = -$x;
			}
			if ($absy > $absx) {
				$distance = $absy + ($absx * $three_eighths);
			} else {
				$distance = $absx + ($absy * $three_eighths);
			};
			//3. use atan2 to find bearing
			//Switch x and y around for bearing(clockwise) rather than mathematical angle(counter-c)
			$direction = atan2($x,$y);

			//4. ensure the result is between 0 and 2pi radians, and not negative
			if ($direction < 0) {
				$direction += ($pi * 2);
			}
		}

		$bearing[] = $direction;
		$bearing[] = $distance;

		return $bearing;
	}

	private function abbreviate_bearing($bearing)
	{
		//$abbreviation; //output

		if(!isset($bearing)) {
			$bearing = 0; //default to north if there is no bearing
		}

		if (($bearing > 5.89) || ($bearing <= 0.39)) {
			$abbreviation = "N";
		} elseif (($bearing > 0.39) and ($bearing <= 1.18)) {
			$abbreviation = "NE";
		} elseif (($bearing > 1.18) and ($bearing <= 1.96)) {
			$abbreviation = "E";
		} elseif (($bearing > 1.96) and ($bearing <= 2.75)) {
			$abbreviation = "SE";
		} elseif (($bearing > 2.75) and ($bearing <= 3.53)) {
			$abbreviation = "S";
		} elseif (($bearing > 3.53) and ($bearing <= 4.32)) {
			$abbreviation = "SW";
		} elseif (($bearing > 4.32) and ($bearing <= 5.11)) {
			$abbreviation = "W";
		} elseif (($bearing > 5.11) and ($bearing <= 5.89)) {
			$abbreviation = "NW";
		}

		return ($abbreviation);
	}

	private function abbreviate_distance($distance, $units, $decimal_places, $units_in_full)
	{

		//$distance   input in km units
		//units   units 'km' or 'mi'
		if(!isset($decimal_places)) {
			$decimal_places = 0;
		}	 //default to 0

		$abbreviation; //output
		$YOUR_LOCATION = "this location"; //if changing this variable, also update it in Markers_html.pm
		$very_small_distance = 0.0001; //about 10 metres

		if ($units != 'mi') {
			$units = 'km'; //default to S.I. km
		};

		if($units_in_full == true) {
			switch($units) {
				case "mi":
					$units = "miles";
				break;

				case "km":
					$units = "km";
				break;

				default:
					$units = "km";
				break;
			}
		}

		$small_value = pow(10,(-$decimal_places)); //1=default e.g. 10 to power of -0 = 1, 10**-1=0.1

		if ($distance <= $very_small_distance) {
			$abbreviation = $YOUR_LOCATION;
		} elseif ($distance < $small_value) { //1 is default
			if(($small_value == 1)&&($units_in_full == true)&&($units == "miles")) {
				$units = "mile";
			}
			$abbreviation = "under $small_value $units";
		} else {
			$distance += ($small_value/2); //0.5 is default for rounding
			$distance *= pow(10,$decimal_places); //for rounding first multiply before taking int
			$distance = (int)$distance;
			$distance /= pow(10,$decimal_places); //finally divide following int
			$format = '%.' . $decimal_places . 'f';
			$distance = sprintf ($format,$distance);
			if(($distance == 1)&&($units_in_full == true)&&($units == "miles")) {
				$units = "mile";
			}
			$abbreviation = "$distance $units";
		}

		return ($abbreviation);
	}


	public function proximity_bounds($north, $south, $west, $east)
	{
		//Sets the proximity bounds that the result set is limited to at the last step.
		$this->top_left_latitude = $north;
		$this->bottom_right_latitude = $south;
		$this->top_left_longitude = $west;
		$this->bottom_right_longitude = $east;
	}


	public function remove_results_tables($show_queries = false)
	{
		//Call after keep_results_table => true, to clear the database memory
		$sql = "drop table grouped_matches";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql);

		$sql = "drop table nearest_matches";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql);

		$sql = "drop table all_data";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql);


		$sql = "drop table final_results";
		if($show_queries == true) { echo $sql . ";<br/>"; };
		mysql_query($sql);

	}
	
	public function insert_adverts($type, $number, $ads_id, $params)
	{
	
		switch($type) {
		
			case 'rvolve':
			
				$url = "http://rvolve.com/search.php?type=xml&lat=" . $params['latitude']. "&lon=" . $params['longitude'] . "&site=" . $ads_id . "&units=" . $params['units'] . "&num_results=" . $number;
				$xml = simplexml_load_file($url);
				
				$count = $xml['num_results'];
					
				$cnt = 0;	
					
				//print_r($xml);
				
				//echo "Full text:" . $xml->results->advert[0]->fullText[0];
				
				
				foreach($xml->results->advert as $advert) {
					
					//print_r($advert);
					
					//echo "Full text 2=" . $advert->fullText[0];
					
					$marker_lat = sprintf("%s", $advert->lat[0]);
					$marker_lon = sprintf("%s", $advert->lon[0]);
					
					list($direction, $distance) = $this->calculate_direction_and_distance($params['latitude'], $params['longitude'], $marker_lat, $marker_lon, $params['units']);
					
					
					//Include all the Layar options, if this is to be seen in Layar
					$results[$cnt]['int_point_id'] = sprintf("%s",(-($cnt + 1)));
					$results[$cnt]['var_actions_label_1'] = "More information";
					$results[$cnt]['var_title'] = sprintf("%s", $advert->fullText[0]);
					$results[$cnt]['var_actions_uri_1'] = sprintf("%s", $advert->url[0]);
					$results[$cnt]['var_line_2'] = "Rvolve.com ads";
					$results[$cnt]['imageURL'] = "http://www.rvolve.com/images/layar_marker.png";
					$results[$cnt]['latitude'] = $marker_lat;
					$results[$cnt]['longitude'] = $marker_lon;
					$results[$cnt]['raw_dist'] = $distance;//$advert['dist'];
					$results[$cnt]['dimension'] = 2;
					$results[$cnt]['rel'] = 'true';
					$results[$cnt]['angle'] = 0;
					$results[$cnt]['scale'] = 1.0;
					$results[$cnt]['baseURL'] = '';
					$results[$cnt]['full'] = 'http://www.rvolve.com/images/layar_marker.png';
					$results[$cnt]['reduced'] = 'http://www.rvolve.com/images/layar_marker.png';
					$results[$cnt]['icon'] = 'http://www.rvolve.com/images/layar_marker.png';
					$results[$cnt]['size'] = 20;
					$results[$cnt]['layerURL'] = "0";
					$results[$cnt]['type'] = 1;
					
					$cnt ++;
					
				}
				
				//print_r($results);
				
				$return_collection[] = $results;
				$return_collection[] = $count;
			break;
	
		}
	
		
	
		return $return_collection;
	}

}



} //if

?>
