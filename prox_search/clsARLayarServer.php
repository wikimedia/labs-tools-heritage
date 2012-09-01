<?php
/*
 cls.basic_geosearch.php

 Does a basic but scalable&fast non-keyword geo-search (or nearest item search) on a table.
 Includes Peano code generation.

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


Author: Peter Abrahamson  peter@atomjump.com  18 Feb 09. Document last update 4 July 09.	
*/

// functions

require_once('CommonFunctions.php');
require_once( 'clsBasicGeosearch.php' );


//class

class clsARLayarServer extends clsBasicGeosearch {
	
	public $layar_name;
	public $layar_attribution;
	public $layar_latitude;
	public $layar_longitude;
	public $layar_radius;
	public $layar_title;
	public $layar_imageURL;
	public $layar_actions_uri_1;
	public $layar_actions_uri_2;
	public $layar_actions_uri_3;
	public $layar_actions_uri_4;
	public $layar_actions_label_1;
	public $layar_actions_label_2;
	public $layar_actions_label_3;
	public $layar_actions_label_4;
	public $layar_layerURL;
	public $layar_line_2;
	public $layar_line_3;
	public $layar_line_4;
	public $layar_dimension;
	public $layar_rel;
	public $layar_angle;
	public $layar_scale;
	public $layar_baseURL;
	public $layar_full;
	public $layar_reduced;
	public $layar_icon;
	public $layar_size;
	public $layar_alt;
	public $layar_relative_alt;
	public $layar_autoTriggerRange;
	public $layar_autoTriggerOnly;
	public $layar_filters;
	public $layar_filter_1_text;
	public $layar_filter_1_param;
	public $layar_filter_2_text;
	public $layar_filter_2_param;
	public $layar_filter_3_text;
	public $layar_filter_3_param;
	public $layar_next_page_key;
	public $layar_more_pages;
	public $layar_type;
	public $max_records;
	private $debug;
	private $javascript_server;
	
	//With thanks to the basis for this code from
	//http://teknograd.wordpress.com/2009/10/19/augmented-reality-create-your-own-layar-layer/
	
	
	public function layar_request($params)	
	{
		//Get optional paramters
		$this->layar_name = isset($params['layar_name']) ? $params['layar_name'] : "LightRod.org";
		$this->layar_attribution = isset($params['layar_attribution']) ? $params['layar_attribution'] : "LightRod.org";
		$this->layar_title = isset($params['title']) ? $params['title'] : null;
		$this->layar_imageURL = isset($params['imageURL']) ? $params['imageURL'] : null;
		$this->layar_actions_uri_1 = isset($params['actions_uri_1']) ? $params['actions_uri_1'] : null;
		$this->layar_actions_uri_2 = isset($params['actions_uri_2']) ? $params['actions_uri_2'] : null;
		$this->layar_actions_uri_3 = isset($params['actions_uri_3']) ? $params['actions_uri_3'] : null;
		$this->layar_actions_uri_4 = isset($params['actions_uri_4']) ? $params['actions_uri_4'] : null;
		$this->layar_actions_label_1 = isset($params['actions_label_1']) ? $params['actions_label_1'] : null;
		$this->layar_actions_label_2 = isset($params['actions_label_2']) ? $params['actions_label_2'] : null;
		$this->layar_actions_label_3 = isset($params['actions_label_3']) ? $params['actions_label_3'] : null;
		$this->layar_actions_label_4 = isset($params['actions_label_4']) ? $params['actions_label_4'] : null;
		$this->layar_layerURL = isset($params['layerURL']) ? $params['layerURL'] : null;
		$this->layar_line_2 = isset($params['line_2']) ? $params['line_2'] : null;
		$this->layar_line_3 = isset($params['line_3']) ? $params['line_3'] : null;
		$this->layar_line_4 = isset($params['line_4']) ? $params['line_4'] : null;
		$this->layar_dimension = isset($params['dimension']) ? $params['dimension'] : null;
		$this->layar_rel = isset($params['rel']) ? $params['rel'] : null;
		$this->layar_angle = isset($params['angle']) ? $params['angle'] : null;
		$this->layar_scale = isset($params['scale']) ? $params['scale'] : null;
		$this->layar_baseURL = isset($params['baseURL']) ? $params['baseURL'] : null;
		$this->layar_full = isset($params['full']) ? $params['full'] : null;
		$this->layar_reduced = isset($params['reduced']) ? $params['reduced'] : null;
		$this->layar_icon = isset($params['icon']) ? $params['icon'] : null;
		$this->layar_size = isset($params['size']) ? $params['size'] : null;
		$this->layar_alt = isset($params['alt']) ? $params['alt'] : null;
		$this->layar_relative_alt = isset($params['relative_alt']) ? $params['relative_alt'] : null;
		$this->layar_autoTriggerRange = isset($params['autoTriggerRange']) ? $params['autoTriggerRange'] : null;
		$this->layar_autoTriggerOnly = isset($params['autoTriggerOnly']) ? $params['autoTriggerOnly'] : null;
		$this->layar_filters = isset($params['searchFilters']) ? $params['searchFilters'] : null;
		$this->layar_filter_1_text = isset($params['filter1Text']) ? $params['filter1Text'] : null;
		$this->layar_filter_1_param = isset($params['filter1Param']) ? $params['filter1Param'] : null;
		$this->layar_filter_2_text = isset($params['filter2Text']) ? $params['filter2Text'] : null;
		$this->layar_filter_2_param = isset($params['filter2Param']) ? $params['filter2Param'] : null;
		$this->layar_filter_3_text = isset($params['filter3Text']) ? $params['filter3Text'] : null;
		$this->layar_filter_3_param = isset($params['filter3Param']) ? $params['filter3Param'] : null;
		$this->layar_more_pages = isset($params['morePages']) ? $params['morePages'] : false;
		$this->layar_type = isset($params['type']) ? $params['type'] : null;
		$this->debug = isset($params['debug']) ? $params['debug'] : false;
		
		
	
		//Set the header to respond to the request as a JSON array 
		if($this->debug == false) {
			header('Content-type: application/json');
		}
	
		//Get request params from Layar client
		$this->layar_latitude = $_GET["lat"];
		$this->layar_longitude = $_GET["lon"];
		$this->layar_radius = ($_GET["radius"]/1000); // From m down to km as this is what we use for our SQL call.
		$this->layar_timestamp = $_GET["timestamp"];
		$this->layar_developerId = $_GET["developerId"];
		$this->layar_developerHash = $_GET["developerHash"];
		if($this->layar_more_pages == true) {
			$this->layar_next_page_key = isset($_GET["pageKey"]) ? $_GET["pageKey"] : null;
		}
		$this->javascript_server = isset($_REQUEST['jsServer']) ? $_REQUEST['jsServer'] : null;		//This is unique for a javascript variable return, useful for google maps client apps
		$this->max_records = isset($_REQUEST['show']) ? $_REQUEST['show'] : 10;	//10 by default
	
	}
	
	
	public function layar_response($results, $show_more = false)
	{
	
		// If we don’t get any hits lets send back error/nothing.
		if (count($results) == 0)
		{
			$arr = array("hotspots"=> array(), 
					"layer"=>$this->layar_name,
					"errorString"=>"Sorry, there are no results close to you.",
					"morePages"=>false, 
					"errorCode"=>21,
					"nextPageKey"=>null,
					"searchFilters"=>$this->layar_filters,		//Custom to lightrod
					 "filter1Text"=>$this->layar_filter_1_text,		//Custom to lightrod
					 "filter1Param"=>$this->layar_filter_1_param,		//Custom to lightrod
					 "filter2Text"=>$this->layar_filter_2_text,		//Custom to lightrod
					 "filter2Param"=>$this->layar_filter_2_param,		//Custom to lightrod
					 "filter3Text"=>$this->layar_filter_3_text,		//Custom to lightrod
					 "filter3Param"=>$this->layar_filter_3_param		//Custom to lightrod
				);
			echo json_encode($arr);
			exit(0); // Exit as we don’t want to run code below this if error/nothing.
		}
		
		
		

		// Lets start building valid return.
		$returnJSONArray = array("layer"=>$this->layar_name,
					 "errorString"=>"ok",
					 "morePages"=>$show_more,
					 "errorCode"=>0, 
					 "nextPageKey"=>$this->layar_next_page_key + count($results), //+1	//The more page
					 						//is the existing number and
					 						//the number of results
					 "searchFilters"=>$this->layar_filters,		//Custom to lightrod
					 "filter1Text"=>$this->layar_filter_1_text,		//Custom to lightrod
					 "filter1Param"=>$this->layar_filter_1_param,		//Custom to lightrod
					 "filter2Text"=>$this->layar_filter_2_text,		//Custom to lightrod
					 "filter2Param"=>$this->layar_filter_2_param,		//Custom to lightrod
					 "filter3Text"=>$this->layar_filter_3_text,		//Custom to lightrod
					 "filter3Param"=>$this->layar_filter_3_param		//Custom to lightrod
					 );
					 
		
		//Loop through each result and display each line
		foreach($results as $row)
		{
			//Create the actions array
			$actions = array();
			//if(isset($row[$this->layar_actions_uri_1])) {
				$autoTriggerOnly = null;
				if($row[$this->layar_autoTriggerOnly] == "true") {
					$autoTriggerOnly = true;
				} 
				if($row[$this->layar_autoTriggerOnly] == "false") {
					$autoTriggerOnly = false;
				} 	 
			
                $main_uri = 'http://toolserver.org/~erfgoed/api/api.php?action=search&format=htmllist&srcountry='. htmlspecialchars($row['country']) . '&srlang=' . htmlspecialchars($row['lang']) . '&srid='. htmlspecialchars($row['id']) .'&props=image|name|address|municipality|lat|lon|id|country|source|monument_article|registrant_url';
				$main_label = 'info';
				$actions[] = array("uri" => $main_uri,
						   "label" =>  $main_label,
						   "autoTriggerRange" => is_null($this->layar_autoTriggerRange) ? null : (int)$row[$this->layar_autoTriggerRange],
						   "autoTriggerOnly" => $autoTriggerOnly,
						   "layerURL" => $row[$this->layar_layerURL]);  //This is a lightrod addition
			//}
			if ( $row['monument_article'] ) { 
				$wikiUrl = 'http://'. $row['lang'] .'.wikipedia.org/wiki/';
				$articleUrl = $wikiUrl . htmlspecialchars( $row['monument_article'] );
				$wikiLabel = 'wikipedia';
				$actions[] = array("uri" => $articleUrl,
						   "label" => $wikiLabel);
			}

			$uploadUrl = 'http://commons.wikimedia.org/w/index.php?title=Special:UploadWizard&campaign=wlm-' . htmlspecialchars($row['country']) . '&id='. htmlspecialchars($row['id']) .'&descriptionlang={{{descriptionlang|'. htmlspecialchars($row['lang']) .'}}}&description='. htmlspecialchars($row['name']) .'&lat='. htmlspecialchars($row['lat']) .'&lon='. htmlspecialchars($row['lon']);
			$actions[] = array("uri" => $uploadUrl,
	                      "label" => 'upload image');
	
			
			$object = array( "baseURL" => $row[$this->layar_baseURL],
				"full" => $row[$this->layar_full],
				"reduced" => $row[$this->layar_reduced],
				"icon" => $row[$this->layar_icon],
				"size" => is_null($this->layar_size) ? null : (float)$row[$this->layar_size] );
				
			$rel = null;
			if($row[$this->layar_rel] == "true") {
				$rel = true;
			}
			if($row[$this->layar_rel] == "false") {
				$rel = false;
			}
			$transform = array("rel" => $rel,
				"angle" => (float)$row[$this->layar_angle],
				"scale" => (float)$row[$this->layar_scale]);	
			
			//MY 
			$imageURL = '';
			if ($row['image']) {
				$thumbSize = 100;
				$imageURL = getImageFromCommons($row['image'], $thumbSize);
			}
			$wikilang = '';
			$makelinks = false;
			$title = processWikitext($wikilang, $row['name'], $makelinks);
			$line2 = processWikitext($wikilang, $row['address'], $makelinks);
			$line3 = processWikitext($wikilang, $row['municipality'], $makelinks);
			$line4 = strtoupper($row['country']) . ', id: '. $row['id'];
			
			$returnJSONArray["hotspots"][] = array(
			
				"actions" => $actions,
				"attribution" => $this->layar_attribution,
				"distance" => $row['raw_dist']*1000, // km back to meter!
				"id" => $row[$this->id_field],
				"imageURL" => $imageURL,
				"lat" => (int) ($row['latitude']*1000000), // API wants clean INT we store in FLOAT.
				"lon" => (int) ($row['longitude']*1000000), // API wants clean INT we store in FLOAT.
				"line2" => $line2,
				"line3" => $line3,
				"line4" => $line4,
				"title" => $title,
				"dimension" => is_null($this->layar_dimension) ? null : (int)$row[$this->layar_dimension],
				"transform" => $transform,
				"object" => $object,
				"alt" => is_null($this->layar_alt) ? null : (int)$row[$this->layar_alt],
				"relative_alt" => is_null($this->layar_relative_alt) ? null : (int)$row[$this->layar_relative_alt],
				"type" => is_null($this->layar_type) ? 0 : (int)$row[$this->layar_type]);
		
		}
		
		if($this->javascript_server == 1) {
			//A call back using this library http://www.sergeychernyshev.com/javascript/remoteloader/
			//echo "SERGEYCHE.remoteloader.callback(" . json_encode($returnJSONArray) . ")";
			
			//Ie. was caching this response so that adding new markers weren't being found
			header("Cache-Control: no-cache, must-revalidate"); // HTTP/1.1
			header("Expires: Sat, 26 Jul 1997 05:00:00 GMT"); // Date in the past

			echo "SERGEYCHE.remoteloader.callback('" . addslashes(json_encode($returnJSONArray)) . "', 'good info');";
		} else {
			//A normal Layar response
			echo json_encode($returnJSONArray);
		}
	}

}


?>
