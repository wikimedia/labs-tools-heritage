<?php
/*
 * Layar server using modified classes from LightRod.org
 */


# error_reporting(E_ALL); 
# ini_set('display_errors', true);
# ini_set('html_errors', false);

require_once( dirname( dirname( __FILE__ ) ) . '/api/includes/Defaults.php' );
require_once( '/home/project/e/r/f/erfgoed/prox_search/clsARLayarServer.php' );
require dirname( dirname( __FILE__ ) ) . '/api/autoloader.php';
require dirname( dirname( dirname( __FILE__ ) ) ) . '/database.inc';

$dbStatus = Database::define($dbServer, $dbDatabase, 
	$dbUser, $dbPassword );
if (!$dbStatus) {
    die( "Coudn't connect to db! ". mysql_error() );
}	
	

$monTable = Monuments::$dbTable;
$proxTable = 'prox_search';
$layarName = 'wikilovesmonuments';
$layarAttribution = 'wikilovesmonuments.org';


$joinSql = "JOIN ". $monTable ." allm ON (m.mon_country = allm.country AND m.mon_lang = allm.lang AND m.mon_id = allm.id)";

	
$ly = new clsARLayarServer();
$ly_params = array('layar_name' => $layarName,
				'layar_attribution' => $layarAttribution,
//				'actions_label_1' => "actions_label_1",
				'actions_uri_1' => "actions_uri_1",
				'line_2' => "line_2",
				'line_3' => "line_3",
				'line_4' => "line_4",
				'title' => "title",
				'imageURL' => "imageURL",
				'morePages' => true,
//				'layerURL' => "layerURL",
				'type' => "type",
				'debug' => false);		//Switch to false when taking server live  TEMP to TRUE

$ly->layar_request($ly_params);		
$params = array('latitude' => $ly->layar_latitude,		//Latitude in decimal degrees of center of search
		'longitude' => $ly->layar_longitude,			//Longitude in decimal degrees of center of search 
		'table_name' => $proxTable,		//Main table name that is being searched on 
		'id_field' => "point_id",	//Unique reference to each point in the table
		'latitude_field' => "lat",	//Field in table that has the latitude in decimal
		'longitude_field' => "lon",	//Field in table that has the longitude in decimal
		'peano_field_header' => "int_peano",	//First letters of fields in table that hold peano
                                                        //integers E.g. 'int_peano', which gets appended
			 				//to create 'int_peano1, int_peano2, int_peano1iv,
			 				// int_peano2iv'
		'max_records' => $ly->max_records,	//10 by default
		'first_record' => $ly->layar_next_page_key,
		'radius' => $ly->layar_radius,
		'misc_fields' => "
				 allm.country AS country,
				 allm.lang AS lang,
				 allm.id AS id, 
				 allm.address AS address, 
				 allm.municipality AS municipality, 
				 allm.name AS name, 
				 allm.image AS image,
                 allm.monument_article AS monument_article,
				  0 AS type			
				  ",				//Type 0 is the default black circle, 1 = first entered type
		'custom_join' => $joinSql,
		'show_queries' => false,
		'provide_count' => true
);


list($results_array, $count) = $ly->proximity_finder($params);

		
$ly->layar_response($results_array, $count['show_next']);	
		


?>
