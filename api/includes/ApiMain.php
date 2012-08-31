<?php

class ApiMain {

	/**
	 * Mapping of available actions to the class that handles them
	 *   action => API name (class name without 'API' prefix)
	 * NOTE: if you are creating new API actions, you MUST make sure
	 * they are mapped here.
	 * @TODO refactor this list to get registered either by config or somehow
	 *   automagically so new API action creators do not have to edit this file
	 */
	protected static $actionMap = array(
		'search' => 'Monuments',
		'statistics' => 'Monuments',
		'statisticsdb' => 'Monuments',
		'statisticsct' => 'Monuments',
		'adminlevels' => 'AdminTree',
		'countries' => 'Countries',
	);

	public static function getActions() {
		return array_keys( self::$actionMap );
	}

	public static function dispatch() {
		Debug::init();

		$api = new ApiDummy;
		try {
			$action = $api->getParam( 'action' );
			if ( $action == 'help' ) {
				self::help();
				return;
			}
			$actionClass = 'Api' . self::$actionMap[$action];
			$obj = new $actionClass;
			$obj->executeModule();
		} catch( Exception $e ) {
			Debug::log( 'Exception: ' . $e->getMessage() );
			$format = $api->getFormatter();
			$format->headers();
			$format->outputErrors( $e->getMessage() );
		}

		Debug::saveLog();
	}

	/**
	 * Print a help message
	 * @TODO build this dynamically
	 */
	public static function help() {
		/* TODO: Expand me and generate automagically! */
		echo '
			<html>
			<head>
				<title>Monuments API</title>
			</head>
			<body>
			<pre>


			  <b>******************************************************************************************</b>
			  <b>**                                                                                      **</b>
			  <b>**              This is an auto-generated Monuments API documentation page              **</b>
			  <b>**                                                                                      **</b>
			  <b>**                            Documentation:                                            **</b>
			  **      <a href="http://commons.wikimedia.org/wiki/Commons:Wiki_Loves_Monuments_2011/Tools#Search_and_export_tool">http://commons.wikimedia.org/wiki/Commons:Wiki_Loves_Monuments_2011/Tools#Search_and_export_tool</a>                        **
			  <b>**                                                                                      **</b>
			  <b>******************************************************************************************</b>


			Parameters:
			  format         - The format of the output
			                   One value: dynamickml, kml, gpx, poi, html, htmllist, layar, json, xml, xmlfm
			                   Default: xmlfm
			  action         - What action you would like to perform. 
			                   One value: search, statistics, help
			                   Default: help

			<b>*** *** *** *** *** *** *** *** *** ***  Modules  *** *** *** *** *** *** *** *** *** ***</b> 

			<b>* action=search *</b>

			Parameters:
			  srcountry       - Search for monuments in country. Supply the country code.
			  srlang          - Search for monuments in lang. Supply the language code.
			  srid            - Search for id.
			  srname          - Search for name.
			  sraddress       - Search for address.
			  srmunicipality  - Search for municipality.
			  srlat           - Search for latitude.
			  srlon           - Search for longitude.
			  srimage         - Search for imagename in monument lists.
			  srsource        - Search for source monument list wiki page.
			  srchanged       - Search for changed.
			  bbox            - left,bottom,right,top
			                    Bounding box with topleft and bottomright latlong coordinates. E.g. bbox=11.54,48.14,11.543,48.145
			  coord           - Coordinate to search around
			  radius          - Search radius, used in conjunction with coord
			  limit           - [integer]: the maximum number of results you will get back
			  props           - [country|lang|id|name|address|municipality|lat|lon|image|source|changed]: the properties which should be returned. (By default all of them.)


			Examples:
			  <a href="api.php?action=search&amp;srname=%burgerhuizen%">api.php?action=search&amp;srname=%burgerhuizen%</a>
			  <a href="api.php?action=search&amp;srcountry=fr&amp;srlang=ca">api.php?action=search&amp;srcountry=fr&amp;srlang=ca</a>

            <b id="action-statisticsdb">* action=statisticsdb *</b>
            <b>* action=statistics *</b>

            Parameters:
              stcountry       - Statistics for country. Supply the country code.
              stitem          - [total|name|name_pct|address|address_pct|municipality|municipality_pct|image|image_pct|coordinates|coordinates_pct]: the stats fields which should be returned (By default, all of them).
              limit           - [integer]: the maximum number of results you will get back (0 for all)
              
              
            Examples:
              <a href="api.php?action=statisticsdb&stitem=total|name_pct|address_pct|municipality_pct|image_pct|coordinates_pct&stcountry=pt&format=html&limit=0">api.php?action=statistics&amp;stitem=total|name_pct|address_pct|municipality_pct|image_pct|coordinates_pct&amp;stcountry=pt&amp;format=html&amp;limit=0</a>
              <a href="api.php?action=statisticsdb&stcountry=pt&format=csv&limit=0">api.php?action=statistics&amp;stcountry=pt&amp;format=csv&amp;limit=0</a>


            <b id="action-statisticsct">* action=statisticsct *</b>

            Parameters:
              ctscope         - [country|user|dump|image] Type of statistics you are interested in. 
                                The "image" scope is the activity on the contest (accepting "ctcountry"). 
                                It will dump activity per hour, in countries "ctcountry" only, if specified. 
                                For each scope, ctitems may differ. 
              ctitem          - Columns you are interested in. Separate values with a pipe "|"
                                For scope "user":
                                  . user - user name
                                  . n_images - number of uploaded images from user
                                  . images - sample of images from the user
                                  . n_images_accepted - status of qualification of the image (0=not accepted, 1=otherwise). Des not work for all countries.
                                  . n_countries - number of countries the user is participating in
                                  . countries - names of countries the user is participating in
                                  . n_wlm_ids - number of distinct WLM IDs the user submitted to
                                  . wlm_ids - sample of WLM IDs the user submitted to
                                  . n_images_all - total number of images uploaded from user in all countries
                                  . images_all - samples for images uploaded from user in all countries
                                  . n_images_accepted_all - same as above, but in all countries
                                  . n_wlm_ids_all - same as above, but in all countries
                                  . wlm_ids_all - same as above, but in all countries
                                For scope "country":
                                  . country - country name
                                  . images - number of images uploaded for each country contest
                                  . users - number of users found participating
                                  . new_users - number of recent users (created after contest start)
                                  . new_users_ratio - ratio between the above
                                For scope "dump":
                                  [name,user_id,user_name,page_id,wlm_country,wlm_id,timestamp,user_first_rev,is_valid] - table fields requested
              ctorderby       - return results order by this field(s) - may not work with some scopes
              ctcountry       - selection of countries
              ctfrom          - timestamp from where to start dumping (ctscope=dump only)
              limit           - [integer]: the maximum number of results you will get back (0 for all)
              
              
            Examples:
              <a href="api.php?action=statisticsct&format=html&ctscope=country">api.php?action=statisticsct&amp;format=html&amp;ctscope=country</a>
              <a href="api.php?action=statisticsct&format=html&ctscope=image&ctcountry=Portugal">api.php?action=statisticsct&amp;format=html&amp;ctscope=image&amp;ctcountry=Portugal</a>
              <a href="api.php?action=statisticsct&format=html&ctscope=user&ctcountry=Portugal&ctitem=user|n_countries|n_images|n_images_accepted">api.php?action=statisticsct&amp;format=html&amp;ctscope=user&amp;ctcountry=Portugal&amp;ctitem=user|n_countries|n_images|n_images_accepted</a>
              <a href="api.php?action=statisticsct&format=html&ctscope=dump&ctcountry=Portugal&ctitem=name|user_name&ctfrom=20110903000000&limit=10">api.php?action=statisticsct&amp;format=html&amp;ctscope=dump&amp;ctcountry=Portugal&amp;ctitem=name|user_name&amp;ctfrom=20110903000000&amp;limit=10</a>

			<b>*** *** *** *** *** *** *** *** *** ***  Formats  *** *** *** *** *** *** *** *** *** ***</b> 

			  <b>* format=dynamickml *</b>
			  Generate KML network link file.

			Examples:
			  <a href="api.php?action=search&amp;format=dynamickml">api.php?action=search&amp;format=dynamickml</a>

			  <b>* format=html *</b>
			  Output data in HTML format. Table layout.

			  <b>* format=htmllist *</b>
			  Output data in HTML format. List layout.

			  <b>* format=json *</b>
			  Output data in JSON format.

			Parameters:
			  callback       - If specified, wraps the output into a given function call.

			  <b>* format=kml *</b>
			  Output data in KML format

			Examples:
			  <a href="api.php?action=search&amp;format=kml">api.php?action=search&amp;format=kml</a>

			  <b>* format=xml *</b>
			  Output data in XML format

			Examples:
			  <a href="api.php?action=search&amp;format=xml">api.php?action=search&amp;format=xml</a>

			<b>*** *** *** *** *** *** *** *** *** ***  Special matching rules  *** *** *** *** *** *** *** *** *** ***</b> 

			Terms containing percent sign (%): match these terms using prefix search

			Terms starting with "~": match these terms using full-text search

			</pre>
			</body>
			</html>
			        ';
	}
}

/**
 * Dummy API class to expose some functionality from ApiBase that is useful
 * to us before we know which API class to invoke.
 */
class ApiDummy extends ApiBase {
	protected function executeModule() {
		return;
	}

	public function getAllowedParams() {
		return $this->getDefaultAllowedParams();
	}
}

?>
