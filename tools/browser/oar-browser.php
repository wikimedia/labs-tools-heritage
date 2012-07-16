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

//set the error level of the website - don't include warnings
error_reporting(E_ERROR | E_PARSE);				//Needed for Windows compatability



//Used by the layout pages - needed to be absolute given templates
if($_SERVER['HTTP_X_FORWARDED_HOST']) {
	//If on a load balancer
	$host = $_SERVER['HTTP_X_FORWARDED_HOST'];
	if(($host == 'owlz.org')||($host == 'www.owlz.org')) {
		$oar_browser_dir = 'http://' . $host . "/";
	} else {
		$oar_browser_dir = 'http://' . $host . dirname($_SERVER['SCRIPT_NAME']) . "/";
	}
} else {
	//A regular machine
	$host = $_SERVER['HTTP_HOST'];
	$oar_browser_dir = 'http://' . $host . dirname($_SERVER['SCRIPT_NAME']) . "/";
}






if($_SERVER["SERVER_NAME"] == "127.0.0.1") { 
	define("GOOGLE_MAPS_KEY", 'ABQIAAAAK9scMBruVrJb9OaY1EFbeRQmM3h9L3BgTlGR6dGXr_-vPADENhSNYAiWEUEANdtJWw0vzj9A-uEurQ');
} else {
	
	//if( strstr('internal',$_SERVER["SERVER_NAME"] != false)) {
	//	$oar_browser_dir = 'http://owlz.org/';
	//}
		


	//Atomjump - or put your own key in here	
	//define("GOOGLE_MAPS_KEY", 'ABQIAAAAqZq5joilTRJEerD58NWIiBTJvMA1VJ3LRQ4VO6FcYp9qeXpADxQgij2d-hn-oLcc_kMwQb9PI9BvIg');

	//Lightrod.org
	//define("GOOGLE_MAPS_KEY", "ABQIAAAAqZq5joilTRJEerD58NWIiBQ9HUNJ69cB_yBrpo2qKRgj0mhLyRSOUW2EqO_rW29i0RYWJLGgNWROhw");
	
	//Get any config from the user's own server
	if(file_exists("./.browser_conf.php")) {
		require_once("./.browser_conf.php");
	} else {
	
		//oar.lightrod.org
		//define("GOOGLE_MAPS_KEY", "ABQIAAAAqZq5joilTRJEerD58NWIiBRlOYGdwPi-gcmsssDy8Wj8iMd7lBTCQx2LEqqO3WVU2F15opgzbQAt8A");
	
		//owlz.org
		define("GOOGLE_MAPS_KEY", "ABQIAAAAqZq5joilTRJEerD58NWIiBTs2-HNR4z63Cui3xThNlGOwd6zfhSvl4VD-Y9iWFaRGHTGHm1uBDpD_A");
	}
}

//Used by the layout pages - needed to be absolute given templates
$oar_browser_path = $oar_browser_dir . "oar-browser.php";


//print_r($_SERVER);

//Some definitions
define('LIST_VIEW', 1);
define('MAP_VIEW', 2);


//Input URL
$url = 'http://toolserver.org/~erfgoed/layar/location.html';
$oar = new oarBrowser($url, 
			$_REQUEST['lat'], 
			$_REQUEST['lon'], 
			$_REQUEST['srch'], 
			$_REQUEST['pageKey'],
			$_REQUEST['viewType'],
			$_REQUEST['template'],
			$_REQUEST['linkTarget'],
			$_REQUEST['geoBias'],
			$_REQUEST['zoom'],
			$_REQUEST['address'],
			$_REQUEST['listHeight'],
			$_REQUEST['rvolve'],
			$oar_browser_path,
			$oar_browser_dir);

//Read any filters that exist for e.g. a text search
$oar->parse_filters();

//Read robots.txt file from URL, or read meta tag from homepage to find layer query string
if(isset($url)) {
	if($query_string = $oar->get_layer_query_str()) {
		
		//Optionally prepare the filters for user input
		//echo "Filtersnow=" . $oar->filters_now . " Search now=" . $oar->search_now;
		
		if(($oar->filters_now == true)&&($oar->search_now != 1)) {
			$results = $oar->parse_options_to_filters($oar->oar_filters);
		} else {
		
			//Read layer
			$results = $oar->read_layer($_REQUEST['lat'], $_REQUEST['lon']);
		
			//print_r($results);
		}
		//echo $query_string;
	} else {
		$oar->error_message = "Sorry, there is no layer from that URL or the website is not responding.<br/>";
	}
	
	
}


 



class oarBrowser
{
	public $url;
	public $url_with_http;
	public $favicon;
	public $oar_server;
	public $oar_filters;
	public $oar_description;
	public $oar_logo;
	public $results;
	public $latitude;
	public $longitude;
	public $search_now;
	
	public $query_1_param;
	public $query_1_val;	
	public $query_2_param;
	public $query_2_val;
	public $query_3_param;
	public $query_3_val;
	
	public $page_key;
	
	public $filters_now;
	public $error_message;
	
	public $default_search_engine;
	
	public $view_type;
	public $template_url;
	public $body_onload;
	
	public $oar_browser_path;
	public $oar_browser_dir;
	
	public $oar_mapmarker;
	public $link_target;
	
	public $geo_bias;
	public $init_map_zoom;
	public $address;
	
	public $list_height;
	public $list_width;
	
	public $rvolve_user_id;
	
		
	public function __construct($url, $lat, $lon, $search, $page_key = null, $view_type = LIST_VIEW, $template_url = null, $my_link_target = "_parent", $my_geo_bias, $my_init_map_zoom, $my_address = null, $my_list_height = null, $my_rvolve = null, $oar_browser_path, $oar_browser_dir)	
	{
		
		$this->url = $url;
		
		//Custom Nakdreality shortcut
		if(substr($url, 0,1) == '%') {
			$layer = substr($url, 1);
			$this->url = "http://poi.nakdreality.com/clients/" . $layer . "/";
		}
		
		
		if((isset($lat))&&($lat!='undefined')) {
			$this->latitude = $lat;
		} else {
			$this->latitude = 51.4726158;		//Grenwich
		}
		if((isset($lon))&&($lon!='undefined')) {
			$this->longitude = $lon;
		} else {
			$this->longitude = 0.0;			//Grenwich
		}
		
		if((isset($search))&&($search!='undefined')) {
			$this->search_now = $search;
		} else {
			$this->search_now = 0;
		}
		
		$this->filters_now = false;		//Display filters
		
		if((isset($page_key))&&($page_key!='undefined')) {
			$this->page_key = $page_key;
		} else {
			$this->page_key = 0;			//Assume no page key
		}
		
		if(isset($_COOKIE['default_search_engine'])) {
			$this->default_search_engine = $_COOKIE['default_search_engine'];
			
			
		} else {
			//Use our hosting providers as an example	
			//POI engine
			$this->default_search_engine = "http://key.nakdreality.com/nakdreality/[SEARCH]/lr/locations/";
		}
		
		/*
		if(substr($url, 0,1) == '.') {
			//NakdReality Keyword engine
			$this->default_search_engine = "http://www.nakdreality.com/search?userId=0&layerName=[SEARCH]";
		}*/
		
		
		if(isset($view_type)) {
			$this->view_type = $view_type;
		} else {
			$this->view_type = LIST_VIEW;
		} 
		
		if(isset($template_url)) {
			$this->template_url = $template_url;
		}
		
		$this->oar_browser_path = $oar_browser_path;
		$this->oar_browser_dir = $oar_browser_dir;
		$this->oar_mapmarker = "";
		
		if($my_link_target == "") {
			//Default to a whole new page from within a frame
			$this->link_target="_parent";
		} else {
			$this->link_target = $my_link_target;
		}
		
		if(isset($my_geo_bias)) {
			//Default to a whole new page from within a frame
			$this->geo_bias = $my_geo_bias;
		} else {
			$this->geo_bias = "";
		}
		
		if(isset($my_init_map_zoom)) {
			$this->init_map_zoom = $my_init_map_zoom;
		} else {
			$this->init_map_zoom = "false";		//This is a javsacript false so needs to be text
		}
		
		$this->address = $my_address;
		
		
		if(isset($my_list_height)) {
			list($this->list_width, $this->list_height) = explode(",",$my_list_height);
		}
		
		if(isset($my_rvolve)) {
			$this->rvolve_user_id = $my_rvolve;
		} else {
			$this->rvolve_user_id = false;
		}
	}
	

	public function parse_filters()
	{
		//These are input filters to the main search that we are calling
		foreach($_REQUEST as $name => $value)
		{
			//echo $name . " = " . $value ."<br>";
			if(strpos($name, "query1_") !== false) {
				$this->query_1_param = substr($name, 7);
				$this->query_1_val = $value;
			}

			if(strpos($name, "query2_") !== false) {
				$this->query_2_param = substr($name, 7);
				$this->query_2_val = $value;
			}

			if(strpos($name, "query3_") !== false) {
				$this->query_3_param = substr($name, 7);
				$this->query_3_val = $value;
			}
		
		}
	
	}
	
	public function parse_options_to_filters($options_text)
	{
		//Input
		//"text_box|query|Enter your search term,
			// option_box|myopt{'Option 1'=1;'Option 2'=2}|Select your option,
			// text_box|radius|Radius"
		$return_array = array();
		
		$filters = explode(",", $options_text);
		
		
		
		$cnt = 1;
		foreach($filters as $filter)
		{
			
			//OK we have text like "text_box:'Enter your search terms'=query"
			if($cnt < 4) {		//Only currently support 3 option filters
				$command_terms = explode("|" , trim($filter));
				if($command_terms[0] == 'text_box') {
					//echo $command_terms[1];
					//print_r($terms);
					$return_array['filter' . $cnt . 'Param'] = $command_terms[1];
					$return_array['filter' . $cnt . 'Text'] = str_ireplace("'", "", $command_terms[2]);
					
					//echo $return_array['filter' . $cnt . 'Text'];
				}
			}
			$cnt++;
		}
		
		$this->results = $return_array;
		return $return_array;
	}

	private function get_meta_data($html) {
		//Function doesn't currently work - but I'm told it is faster
		if(preg_match('/<meta[^>]+name=\"oar-server\"[^>]+content=\"([^\"]*)\"[^>]+>/i', $line, $match)) {
			$meta['oar-server'] = $match[1];
		} 
		return $meta;   
	}


	public function get_layer_query_str()
	{
		ini_set('user_agent', 'oar-lightrod-browser (http://www.lightrod.org)');
		$a_match = false;
		
		//echo $this->url;	//TEMPIN
		//exit(0);
		
		$url_with_http = $this->url;
		if(stristr($this->url,"http://") == false) {
			$url_with_http = "http://" . $this->url;
		} 
		$this->url_with_http = $url_with_http;			//Save for later
		
		
		$parsed = @parse_url($url_with_http); 
		if($parsed != false) {
		
			$parsed_host = "http://{$parsed['host']}/";
			$this->favicon = $parsed_host . "favicon.ico";		//Default favicon 
			
			if(@file_get_contents($this->favicon) == false) {
				//No such file, then set to lightrod icon
				$this->favicon = "lrod_favicon.ico";
			}
			
			
			$html = @file_get_contents($url_with_http);
			if($html == false) {
				//Try searching off the default search engine - this is a plain text search or layar
				//name most likely
				$url_with_http = str_ireplace("[SEARCH]", $this->url, $this->default_search_engine);
				$html = @file_get_contents($url_with_http);	
				
				//Get the favicon from the search engine
				$parsed = @parse_url($url_with_http);
				if($parsed != false) {
					$parsed_host = "http://{$parsed['host']}/";
					$this->favicon = $parsed_host . "favicon.ico";		//Default favicon 
				}
				
			}
			
			if ($html != false) {
				//Faster but not currently working $meta_tag_array = $this->get_meta_data($html);	    
			
				$meta_tag_array = get_meta_tags($url_with_http);   //TODO: we're extracting the file twice, make above work
		
				if(isset($meta_tag_array['oar-server'])) {
					//Found in the meta tags
					$this->oar_server = $meta_tag_array['oar-server'];
					$a_match = $this->oar_server;
					
					//Use for testing:
					 //$meta_tag_array['oar-options'] = "text_box|query|Enter your search terms";	//TEMPIN!!
					
					//Now check for options meta tags
					if(isset($meta_tag_array['oar-options'])) {
						$this->filters_now = true;
						//echo "In here" . $meta_tag_array['oar-options'];
						$this->oar_filters = $meta_tag_array['oar-options'];
					}
					
					
					//Now check for map marker meta tags
					if(isset($meta_tag_array['oar-mapmarker'])) {
						//echo "In here" . $meta_tag_array['oar-options'];
						$this->oar_mapmarker = $meta_tag_array['oar-mapmarker'];
					}
					
				} else {
			
					 $robotstxt = @file("http://{$parsed['host']}/robots.txt"); 
					 if($robotstxt) { 
			
						foreach($robotstxt as $line) { 
							if(preg_match('/OAR-server: (.*)/i', $line, $match)) {
								//Found a match
								 $this->oar_server = $match[1];
								 $a_match = $this->oar_server;
								 
								 //Check for options
								 if(preg_match('/OAR-options: (.*)/i', $line, $match)) {
								 	$this->oar_filters = $match[1];
								 	$this->filters_now = true;
								 } 
							} 
						} 
					}
				
				}
				
				//Get additional meta tags
				if(isset($meta_tag_array['oar-logo'])) {
					$this->oar_logo = $meta_tag_array['oar-logo'];
				}
				
				if(isset($meta_tag_array['oar-description'])) {
					$this->oar_description = $meta_tag_array['oar-description'];
				}
				
				//This is a temporary hack - need to read proper favicon tags
				if(isset($meta_tag_array['oar-favicon'])) {
					$this->favicon = $meta_tag_array['oar-favicon'];
				}
				
				if(isset($meta_tag_array['oar-ads-id'])) {
					$this->rvolve_user_id = $meta_tag_array['oar-ads-id'];
				}
				
			}  
		}
		
		
		return $a_match;
	}
	
	public function check_replace($param, $value, $replace, $with, $replace2, $with2, $post = false)
	{
		//Creates a URL name/value pair, but replaces an existing one with a new value if necessary
		if(($replace == $param)&&
		    ($replace != null)) {
		    $value = $with;
		}
		
		if(($replace2 == $param)&&
		    ($replace2 != null)) {
		    $value = $with2;
		}
		
		if($post == true) {
			return "<input type='hidden' name=\"". $param ."\" value=\"" . urldecode($value) . "\">";  //Added urldecode because of #hash tags on nakdeye
		} else {
			return "&" . $param . "=" . $value;
		}
	}
	
	public function get_current_url($replace = null, $with = null, $replace2 = null, $with2 = null, $external = false, $include_latlon = true, $post = false)
	{
	
		if($include_latlon === true) {
			if($post == false) {
				$layer = $layer . "lat=" . $this->latitude . "&lon=" . $this->longitude;
			}		//we always include lat/lon in the post request
				
		}
		
		//Add filter's parameters
		if($this->query_1_param) {
			//This has a text query too
			$query1 = $this->query_1_param;
			if($external == true) {
				$query1 = "query1_" . $this->query_1_param;
			}
			$layer .= $this->check_replace($query1, urlencode($this->query_1_val), $replace, $with, $replace2, $with2, $post);		//TODO: search for 'mobile phone' on thundre, eventually urlencodes one too many times
			
		} else {
			if(post == false) {
				//No filters and importantly, we pass a determine_filters request in.  At the server end this
				//can be use to not carry out a search, for speed, but just pass back the filters themselves.
				$layer .= $this->check_replace("determine_filters", "1", $replace, $with, $replace2, $with2);
			}
		}
		if($this->query_2_param) {
			//This has a text query too
			$query2 = $this->query_2_param;
			if($external == true) {
				$query1 = "query2_" . $this->query_2_param;
			}
			$layer .= $this->check_replace($query2, urlencode($this->query_2_val), $replace, $with, $replace2, $with2, $post);
		}
		if($this->query_3_param) {
			//This has a text query too
			$query3 = $this->query_3_param;
			if($external == true) {
				$query3 = "query3_" . $this->query_3_param;
			}
			$layer .= $this->check_replace($query3, urlencode($this->query_3_val), $replace, $with, $replace2, $with2, $post);

		}
		
		//echo "POST = " . $post;
		if($this->page_key != "") {
			if($post == false) {
				//This is a second page or further
				$layer .= $this->check_replace("pageKey", $this->page_key, $replace, $with, $replace2, $with2);
				//echo "In here";
			}   //we always include page key in the post

		}
		
		if($this->view_type != 0) {
			if($post == false) {
				$layer .= $this->check_replace("viewType", $this->view_type, $replace, $with, $replace2, $with2);
			}   ////we always include view type in the post
		}
		
		if($this->search_now != 0) {
		
			$layer .= $this->check_replace("srch", $this->search_now, $replace, $with, $replace2, $with2, $post);
		
		}
		
		if($this->address) {
			if($post == false) {
				$layer .= $this->check_replace("address", urlencode($this->address), $replace, $with, $replace2, $with2);
			}  //we always include the address in a post request
		
		}
		
		if($this->template_url != '') {
			
			$layer .= $this->check_replace("template", $this->template_url, $replace, $with, $replace2, $with2, $post);
		}
		
		if($this->link_target != '') {
			
			$layer .= $this->check_replace("linkTarget", $this->link_target, $replace, $with, $replace2, $with2, $post);
		}
		
		if($this->geo_bias != '') {
			
			$layer .= $this->check_replace("geoBias", $this->geo_bias, $replace, $with, $replace2, $with2, $post);
		}
		
		if($this->list_height != '') {
			
			$layer .= $this->check_replace("listHeight", $this->list_width . "," . $this->list_height, $replace, $with, $replace2, $with2, $post);
		}
		
		if($this->rvolve_user_id != '') {
			
			$layer .= $this->check_replace("rvolve", $this->rvolve_user_id, $replace, $with, $replace2, $with2, $post);
		}
		
	
		return $layer;
	
	}
	
	public function read_layer() 
	{
		//Read the JSON
		$results = array();

		if(strpos($this->oar_server, "?") === false) {
			$layer = $this->oar_server . "?";
		} else {
			$layer = $this->oar_server . "&";
		}


		$layer.= $this->get_current_url();
		
		//echo $layer;
		
		//Read the actual layer
		$json = file_get_contents($layer);
		if ($json != false) {
			$this->results = json_decode($json, true); 
		}
		
		//http://www.padzz-business.co.uk/layar-server.php?countryCode=NL&lon=-0.102996826172&timestamp=1262892521148&userId=6f85d06929d160a7c8a3cc1ab4b54b87db99f74b&developerId=2616&developerHash=f0293c7a476a8a157f116a2d7d946427ee75aabd&radius=5000&lat=51.4548626583&layerName=padzdev&phoneId=6f85d06929d160a7c8a3cc1ab4b54b87db99f74b&accuracy=100
		//http://www.padzz-business.co.uk/layar-server.php?radius=5000&lat=51.4548626583&lon=-0.102996826172&layerName=padzdev
		
		return $this->results;
	}
	
	

	
	public function display_layer($results)
	{
		//Called from the HTML layer file
		
			
		//Input an array in Layar format and display as a results set
		//print_r($results);
		if((($results['searchFilters'] === true)&&($this->search_now != 1))||		//JSON return case
			(($this->filters_now == true)&&($this->search_now != 1))) {		//Meta tag options case
			
			
			
			//We want to show the search filter(s)
			require_once("layouts/lay_search_filters.php");
		} else {
			//Show results
			switch($this->view_type) 
			{
				case LIST_VIEW:
				{
					$error_msg = "";
					if(count($results) > 0) {
						 if(is_array($results)) {
						     if($results['errorCode'] == 0) {
							   //Display the results
							   //require_once("layouts/lay_results.php");
						 
						 	  
						     }
						     else {	
						  	$error_msg = $results['errorString'];
						     }
						 
						  } else {
						  	$error_msg = "Sorry, the results were invalid.  Error message follows: " . $results;
						  							  	
						  }
				
					} else {
						$error_msg = "Sorry, there were no results found.";
					}
					
					//Display the results
					require_once("layouts/lay_results.php");
				}
				break;
				
				case MAP_VIEW:
				{
					//Display the map no matter what
					require_once("layouts/lay_map_results.php");
				
				}
				break;
			}

		}
		/*
		Array
(
    [layer] => padzdev
    [errorString] => ok
    [morePages] => 
    [errorCode] => 0
    [nextPageKey] => 
    [hotspots] => Array
        (
            [0] => Array
                (
                    [actions] => Array
                        (
                            [0] => Array
                                (
                                    [uri] => http://www.padz.com
                                    [label] => My Action
                                    [autoTriggerRange] => 
                                    [autoTriggerOnly] => 
                                )

                        )

                    [attribution] => LightRod.org
                    [distance] => 0.0496695185
                    [id] => 1715
                    [imageURL] => http://www.padzz-business.co.uk/assets/adverts/images/p-mayfair-house-95.jpg
                    [lat] => 51500152
                    [lon] => -126236
                    [line2] => Hi there
                    [line3] => 
                    [line4] => 
                    [title] => My Marker
                    [dimension] => 
                    [transform] => Array
                        (
                            [rel] => 
                            [angle] => 0
                            [scale] => 0
                        )

                    [object] => Array
                        (
                            [baseURL] => 
                            [full] => 
                            [reduced] => 
                            [icon] => 
                            [size] => 
                        )

                    [alt] => 
                    [relative_alt] => 
                    [type] => 0
                )

            [1] => Array
                (
                    [actions] => Array
                        (
                            [0] => Array
                                (
                                    [uri] => http://www.padz.com
                                    [label] => My Action
                                    [autoTriggerRange] => 
                                    [autoTriggerOnly] => 
                                )

                        )

		
		*/
	}
	
	

	static function limit_chars($input_string, $max_chars, $break_string, $clip_hard = true)
	{
		//Pass in a string and chop at the max number of chars, but on a word basis. Append break_string (usually ".." or "...")
		//afterwards.  Returns the new string.
		//Clip hard set to true, will chop a word in two at the max number of chars if it is overridden - this
		//is the case when you have a small number of $max_chars. 
		//Break_string is often ".."
		
		if(strlen($input_string) > $max_chars) {
			$input_string = current(explode("\n", wordwrap($input_string, $max_chars, "\n"))) . $break_string;  //This gets the full words. 
		}

		if($clip_hard == true) {
			if(strlen($author) > $max_chars+strlen($break_string)) {
				//Still longer than the size + the '..'s.  Must be a single long word.  Trim off the characters
				$author = substr($author, 0, $max_chars) . $break_string;
			}
		}
		
		return $input_string;
	}
	
	
	function get_favicon($html) {
		//TODO: make this function work and get the proper fav icon
		preg_match_all("|<link[^>]+name=\"([^\"]*)\"[^>]+content=\"([^\"]*)\"[^>]+>|i",  $html, $out,PREG_PATTERN_ORDER);

		for ($i=0;$i < count($out[1]);$i++) {
			// loop through the meta data - add your own tags here if you need
			if (strtolower($out[1][$i]) == "keywords") $meta['keywords'] = $out[2][$i];
			if (strtolower($out[1][$i]) == "description") $meta['description'] = $out[2][$i];
		}

		return $meta;   
	}
	
	
	public function get_body_onload()
	{
		//Gets the javascript for a body onload command - separated so that we can insert it into
		//a template
		$this->body_onload = "";
		
		
		if((isset($_REQUEST['url']))&&($this->latitude != 0.0)&&($this->longitude!=0.0)) {
			//Already have location
			if($this->view_type == MAP_VIEW) {
				$this->body_onload = "initializeMap(" . $this->latitude . "," . $this->longitude . "," . $this->init_map_zoom . ");";
			}
		} else {
			//Find location
			
			if($this->address != '') {
				//Use inputted location
				$this->body_onload .= "geocodeAddress(\"" . $this->address . "\"); initializeMap(document.lpf.lat.value, document.lpf.lon.value," . $this->init_map_zoom . ");";
				
				//if($this->view_type == LIST_VIEW) {
					//If it is a list view, then we have to do another search?
				//	$this->body_onload .= " document.lpf.submit()";
				//} 
			} else {
				//Get user to input location
			
				$this->body_onload = "atl_submit_on_success=false;  find_location();";
				if($this->view_type == MAP_VIEW) {
					$this->body_onload .= "initializeMap(" . $this->latitude . "," . $this->longitude . "," . $this->init_map_zoom . ");";
				}
			}
		}
	
	}
	
	
	public function parse_template_basic($template_url)
	{
		//Take the URL, extract the text from the file into a string and search for text 'OWLZ_FULL_BODY'
		//e.g. http://www.atomjump.com/clients/byke/, where would pass in 'clients/byke/'
		//Would have to be from the same domain as the content to stop site cross-scripting security holes.
		//So we append the url to the content url that is being browsed.
		
		//Also include in the body onload - the body onload var, and in the body unload, "GUnload();"
		//echo $this->url_with_http . $template_url;
		
		$full_url = $this->url_with_http;
		if(substr($full_url, -1) != '/') {		//append a / if not there already
			$full_url .= "/";
		}
		$full_url .= $template_url;
		
		
		$html = file_get_contents($full_url);
		if ($html != false) {
		
			//echo "In here";
			
			
			
			
			
			//Try inserting into the onload statement
			$pattern = '/onload[ ]*=[ ]*"(.*?)"/i';
			$replacement = 'onload=\"${1}' . ";" . $this->body_onload . "\"";
			$html = preg_replace($pattern, $replacement, $html, 1, $count);
			if($count < 1) {
				//No existing onload found. Insert the onload after the body
				//echo "no match";			
				$html = preg_replace("/\<[ ]*body[ ]*/i", "<body onload='" . $this->body_onload . "' ", $html, 1, $count_b);
						
			} else {
				//echo "match found";
			}
			
			
			//Now insert into the unload statement
			// onunload="GUnload();"
			$pattern = '/onunload[ ]*=[ ]*"(.*?)"/i';
			$replacement = '${1}' . "; GUnload();";
			$html = preg_replace($pattern, $replacement, $html, 1, $count);
			if($count < 1) {
				//No existing onunload found. Insert the onload after the body
				//echo "no match";			
				$html = preg_replace("/\<[ ]*body[ ]*/i", "<body onunload='GUnload();' ", $html, 1, $count_b);
						
			} else {
				//echo "match found";
			}
			
			
			
			//Now insert into the header some header stuff
			$header = $this->get_oar_header_as_var();
			$html = preg_replace("/\<head\>/i", "<head> " . $header, $html);
			
			
			//Get the text before 'OWLZ_FULL_BODY'
			//preg_match("/(.*?)OWLZ_FULL_BODY(.*?)/g", $html, $matches);
			
			$matches = preg_split("/OWLZ_FULL_BODY/", $html);
			
			$status = true;
		} else { 
		
			//echo "No template";
			//Default to no template - couldn't read properly
			$status = false;
		
		}
		
		$return_array[] = $matches[0];
		$return_array[] = $matches[1];
		$return_array[] = $status;
		
		return $return_array;
	
	}
	
	public function oar_header($oar_browser_dir)
	{
		
	   ?>
	   
	   
	   	<script type="text/javascript">
			function premap_message() {
			    document.getElementById("location_message").innerHTML = "We recommend downloading Firefox 3.5 and clicking 'Geolocate me', otherwise zoom in on your shopping destination by doubling clicking on the map to street level.";
			}

			function searchAgainIfResults() {
				<?php //If this is a results page, and we've just found a location, call the submit to do a search again
					//from this new location
					if(isset($this->results)) { ?>	
						document.lpf.submit();
				<?php } ?>
			}
	
	

		</script>
	   
	   	<script src="<?php echo $oar_browser_dir ?>js/geolocation.js" type="text/javascript"></script>
		<script src="<?php echo $oar_browser_dir ?>js/homepage.js" type="text/javascript"></script>

		<!-- We haven't yet styled this properly: TODO -->

		<link rel="stylesheet" type="text/css" href="css/main.css?version=1.1"/>
		<?php //See http://www.boutell.com/newfaq/creating/iphone.html ?>
		<!--[if !IE]>-->
			<link media="only screen and (max-width: 480px)"
		  	rel="stylesheet" type="text/css" href="css/phone.css"/>
		<!--<![endif]-->



		<script src="http://maps.google.com/maps?file=api&amp;v=2&amp;key=<?php echo GOOGLE_MAPS_KEY; ?>
	&sensor=true" 
	type="text/javascript"></script>
		<script src="http://code.google.com/apis/gears/gears_init.js" type="text/javascript" charset="utf-8"></script>
		<script src="<?php echo $oar_browser_dir ?>js/geo.js" type="text/javascript" charset="utf-8"></script>
		 <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
		<script src="<?php echo $oar_browser_dir ?>js/location-input.js?version=2" type="text/javascript"></script>
		 <script type="text/javascript" src="<?php echo $oar_browser_dir ?>js/jquery-1.3.1.min.js"></script>
		<?php 

		return;

	}
	
	public function get_oar_header_as_var() {
		//Put require output into a variable
   		ob_start();
   		$this->oar_header($this->oar_browser_dir);
   		return ob_get_clean();
   	}
	

}






//Get the body onload
$oar->get_body_onload();


if(!$oar->template_url) {

	//Include the main page
	require("layouts/lay_main_page.php");

} else {
	
	//A basic template - parse the template
	list($before_main, $after_main, $status) = $oar->parse_template_basic($oar->template_url);

	if($status == true) {
		echo $before_main;
		require("layouts/lay_main_page.php");
		echo $after_main;
	} else {
		//Just a normal page - error reading template
		$oar->template_url = "";
		require("layouts/lay_main_page.php");
	}
}

?>

