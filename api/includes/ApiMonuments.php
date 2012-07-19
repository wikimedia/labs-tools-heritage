<?php

if ( get_magic_quotes_gpc() ) {
	die( 'Magic quotes are enabled!' );
}

/**
 * Definition of Monuments API
 * @author Platonides
 */
class ApiMonuments extends ApiBase {
	const EARTH_RADIUS = 6371010;
	const MAX_GEOSEARCH_AREA = 0.04;// 0.2 * 0.2 degrees
	const GRANULARITY = 20;

	protected function getParamDescription() {
		return array(
			/* FIXME: Copy from http://etherpad.wikimedia.org/WLM-tech*/
		);
	}
	
	function getAllowedParams() {
		global $dbMiserMode;
    	$params = array(
    		'props' => array( ApiBase::PARAM_DFLT => Monuments::$dbFields,
				ApiBase::PARAM_TYPE => Monuments::$dbFields, ApiBase::PARAM_ISMULTI => true ),
    		'format' => array( ApiBase::PARAM_DFLT => 'xmlfm', 
    			ApiBase::PARAM_TYPE => $dbMiserMode
					? array( 'json', 'xml', 'xmlfm' )
					: array( 'csv', 'dynamickml', 'kml', 'gpx', 'googlemaps', 'poi', 'html', 'htmllist', 'layar', 'json', 'osm', 'xml', 'xmlfm', 'wikitable' ) ),
    		'callback' => array( ApiBase::PARAM_DFLT => false, ApiBase::PARAM_TYPE => 'callback' ),
    		'limit' => array( ApiBase::PARAM_MIN => 0, ApiBase::PARAM_MAX => $dbMiserMode ? 500 : 5000,
				ApiBase::PARAM_DFLT => 100, ApiBase::PARAM_TYPE => 'integer' ),
    			
    		'action' => array( ApiBase::PARAM_DFLT => 'help', 
    			ApiBase::PARAM_TYPE => array( 'help', 'search', 'statistics', 'adminlevels' ) ),
    			
    		'srquery' => array( ApiBase::PARAM_DFLT => false, ApiBase::PARAM_TYPE => 'string' ),
    		'bbox' => array( ApiBase::PARAM_DFLT => false, ApiBase::PARAM_TYPE => 'string' ),
    		'BBOX' => array( ApiBase::PARAM_DFLT => false, ApiBase::PARAM_TYPE => 'string' ),
			'coord' => array( ApiBase::PARAM_DFLT => false, ApiBase::PARAM_TYPE => 'string' ),
			'radius' => array(
				ApiBase::PARAM_DFLT => false,
				ApiBase::PARAM_TYPE => 'integer',
				ApiBase::PARAM_MIN => 1,
				ApiBase::PARAM_MAX => $dbMiserMode ? 500000 : 10000,
			),
    		'srcontinue' => array( ApiBase::PARAM_DFLT => false, ApiBase::PARAM_TYPE => 'string' ),
			'admlevel' => array(
				ApiBase::PARAM_MIN => 0,
				ApiBase::PARAM_MAX => 4,
				ApiBase::PARAM_DFLT => 0,
				ApiBase::PARAM_TYPE => 'integer',
			),
			'admval' => array(
				ApiBase::PARAM_DFLT => false,
				ApiBase::PARAM_TYPE => 'string',
			),
			'admid' => array(
				ApiBase::PARAM_DFLT => false,
				ApiBase::PARAM_TYPE => 'integer',
				ApiBase::PARAM_MIN => 1,
				ApiBase::PARAM_MAX => 999999999,
			),
    	);
    	
    	foreach ( Monuments::$dbFields as $field ) {
			$params["sr$field"] = array( ApiBase::PARAM_DFLT => false, ApiBase::PARAM_TYPE => 'string' );
			$params["srwith$field"] = array( ApiBase::PARAM_DFLT => false, ApiBase::PARAM_TYPE => 'boolean' );
			$params["srwithout$field"] = array( ApiBase::PARAM_DFLT => false, ApiBase::PARAM_TYPE => 'boolean' );
		}

        $params['stcountry'] = array( ApiBase::PARAM_DFLT => 'pt', ApiBase::PARAM_TYPE => 'string' );
        $params['stitem'] = array( ApiBase::PARAM_DFLT => Statistics::$aItems,
            ApiBase::PARAM_TYPE => Statistics::$aItems, ApiBase::PARAM_ISMULTI => true );
		
		return $params;
	}
	
	function executeModule() {
		switch ( $this->getParam( 'action' ) ) {
			case 'search':
				$this->search();
				break;
			case 'statistics':
				$this->statistics();
				break;
			case 'adminlevels':
				$this->adminlevels();
				break;
			case 'help':
			default:
				$this->help();
				break;
		}
	}

	private $isComplex = false;
	private function complexQuery() {
		if ( $this->isComplex ) {
			$this->error( 'Only one pattern matching (%) or full-text (~) condition allowed' );
		}
		$this->isComplex = true;
	}
	
	function search() {
		$fulltextColumns = array( 'name' => 1 );
        
        if ( $this->getParam('format') == 'dynamickml' ) {
            #don't search just pass along the search parameters to kml network link file
            $DynKml = new DynamicKml;
            $reqUrl = 'http://' . $_SERVER['SERVER_NAME'] . $_SERVER['REQUEST_URI'];
            $DynKml->output($reqUrl);
            return;
        }

		$where = array();
		$forceIndex = false;
		$orderby = Monuments::$dbPrimaryKey;
		$db = Database::getDb();
		
		foreach ( Monuments::$dbFields as $field ) {
			if ( $this->getParam( "srwith$field" ) ) {
				$where[] = $db->escapeIdentifier( $field ) . " <> ''";
			}
			if ( $this->getParam( "srwithout$field" ) ) {
				$where[] = $db->escapeIdentifier( $field ) . " = ''";
			}
		}
		foreach ( Monuments::$dbFields as $field ) {
			$value = $this->getParam( "sr$field" );
			if ( $value === false ) continue;
			
			if ( is_string( $value ) && substr( $value, 0, 1 ) == '~' ) {
				if ( !isset( $fulltextColumns[$field] ) ) {
					$this->error( "Column `$field` does not support full-text search`" );
				}
				$this->complexQuery();
				$where[] = "MATCH ({$db->escapeIdentifier( $field )}) AGAINST ("
					. $db->quote( substr( $value, 1 ) ) . ' IN BOOLEAN MODE)';
				// Postfix the name with primary key because name can be duplicate.
				// Filesort either way.
				$orderby = array_merge( array( $field ), $orderby );
			} elseif ( is_string( $value ) && strpos( $value, '%' ) !== false ) {
				$this->complexQuery();
				$where[] = $db->escapeIdentifier( $field ) . ' LIKE ' .
					$db->quote( $value );
			} else {
				if ( is_string( $value ) ) {
					$value = explode( '|', $value );
				}
				
				$where[$field] = $value;
			}
		}
        
        if ( $this->getParam('bbox') || $this->getParam('BBOX') || $this->getParam( 'coord' ) ) {
			if ( $this->getParam('bbox') ) {
                $bbox = $this->getParam('bbox');
            } else {
                $bbox = $this->getParam('BBOX');
            }
			if ( $bbox ) {
				$coords = preg_split('/,|\s/', $bbox);
				if ( count( $coords ) != 4 ) {
					$this->error( 'Invalid bounding box format, 4 comma-delimited numbers are expected' );
				}
				$bl_lon = floatval( $coords[0] );
				$bl_lat = floatval( $coords[1] );
				$tr_lon = floatval( $coords[2] );
				$tr_lat = floatval( $coords[3] );
				if ( $bl_lat > $tr_lat || $bl_lon > $tr_lon ) {
					$this->error( 'Invalid bounding box' );
				}
			} else {
				$radius = $this->getParam( 'radius' );
				if ( $radius === false || $radius <= 0 ) {
					$this->error( 'Radius not set or is invalid' );
				}
				$coords = array_map( 'floatval', preg_split( '/,|\s/', $this->getParam( 'coord' ) ) );
				if ( count( $coords ) != 2 ) {
					$this->error( 'Invalid coordinate format, 2 comma-delimited numbers are expected' );
				}
				list( $bl_lat, $bl_lon, $tr_lat, $tr_lon ) =
					self::rectAround( $coords[0], $coords[1], $this->getParam( 'radius' ) );
			}
			global $dbMiserMode;
			if ( $dbMiserMode && ( $tr_lat - $bl_lat ) * ( $tr_lon - $bl_lon ) > self::MAX_GEOSEARCH_AREA ) {
				$this->error( 'Bounding box is too large' );
			}
			$where['lat_int'] = self::intRange( $bl_lat, $tr_lat );
			$where['lon_int'] = self::intRange( $bl_lon, $tr_lon );
			$where[] = "`lat` BETWEEN $bl_lat AND $tr_lat";
			$where[] = "`lon` BETWEEN $bl_lon AND $tr_lon";
        }

        /* FIXME: User should be able to set sort fields and order */
		if ( $this->getParam('format') == 'kml' ) {
			$orderby = array('monument_random');
		} elseif ( $this->getParam('format') == 'html' ) {
			$orderby = array('country', 'municipality', 'address');
		}
		$continue = $this->getParam( 'srcontinue' );
		if ( $continue ) {
			$v = explode( '|', $continue );
			if ( count( $orderby ) != count( $v ) ) {
				$this->error( 'Invalid continue parameter' );
			}
			for ( $i = 0; $i < count( $orderby ); $i++ ){
				$where[] = $db->escapeIdentifier( $orderby[$i] ) . '>='
					. $db->quote( rawurldecode( $v[$i] ) );
			}
		}

		$limit = $this->getParam( 'limit' );
		
		$res = $db->select( array_merge( Monuments::$dbPrimaryKey, $this->getParam( 'props' ) ), Monuments::$dbTable, $where,
			$orderby, $limit + 1, $forceIndex );
		$this->getFormatter()->output( $res, $limit, 'srcontinue', $this->getParam( 'props' ), $orderby );
	}
	
	function statistics() {
		global $dbMiserMode;
		if ( $dbMiserMode ) {
			$this->error( 'action=statistics is disabled due to miser mode' );
		}
		$st = new Statistics( $db = Database::getDb() );
        $items = $this->getParam( 'stitem' );
        $filters = explode('|', $this->getParam('stcountry'));
        $limit = $this->getParam( 'limit' );

        $r = $st->retrieveReport($items, $filters, $limit);
        $this->getFormatter()->output($r, 9999999, 'stcontinue', array_merge(array('country', 'municipality'), $st->getAxis('columns')), Monuments::$dbPrimaryKey );
	}

	public function adminlevels() {
		$admval = $this->getParam( 'admval' );
		$admlevel = $this->getParam( 'admlevel' );
		$admid = $this->getParam( 'admid' );
		$db = Database::getDb();

		if ( $admlevel === 0 && $admval === false && $admid === false) {
			$this->getTopLevelAdmNames();
			return;
		} elseif ( $admid ) {
			if ( $admval || $admlevel ) {
				$this->error( 'You may not specify admval or admlevel with admid.' );
			}
			$this->getAdmById( $admid );
			return;
		} elseif ( $admval === false ) {
			$this->error( 'You must specify a value for admval.' );
		}

		$fields = array( 'id', 'name', 'level' );
		$where = array(
			'name' => $admval,
			'level' => $admlevel,
		);
		$res = $db->select( $fields, 'admin_tree', $where );
		if ( $row = mysql_fetch_object( $res->result ) ) {
			$data = $this->getImmediateAdminLevelChildren( $row->id, $row->level );
		} else {
			$data = array();
		}
		$this->getFormatter()->output( $data, 999999999, null, $fields, null );
	}

	/**
	 * Fetches an admin_tree row by id
	 *
	 * @return ResultWrapper
	 */
	private function getAdmById( $admid ) {
		$db = Database::getDb();
		$fields = array( 'id', 'name', 'level' );
		$where = array( 'id' => $admid );
		$res = $db->select( $fields, 'admin_tree', $where );
		$this->getFormatter()->output( $res, 999999999, null, $fields, null );
	}

	/**
	 * Fetches top-most admin tree item names (countries)
	 *
	 * @return ResultWrapper
	 */
	private function getTopLevelAdmNames() {
		$db = Database::getDb();
		// get a list of countries
		$fields = array( 'id', 'name' );
		$where = array(
			'level' => 0,
		);
		$res = $db->select( $fields, 'admin_tree', $where );
		$this->getFormatter()->output( $res, 999999999, null, $fields, null );
	}

	/**
	 * Fetches immediate children of a given admin_tree id
	 * @param int $id The id of the admin_tree item for which to fetch children
	 * @return array
	 */
	private function getImmediateAdminLevelChildren( $id ) {
		$data = array();
		$db = Database::getDb();
		$fields = array( 'id', 'name', 'level' );
		$where = array(
			'parent' => $id,
		);
 		$res = $db->select ( $fields, 'admin_tree', $where );
		while ( $row = mysql_fetch_object( $res->result ) ) {
			$data[] = array( 'id' => $row->id, 'name' => $row->name, 'level' => $row->level );
		}
		return $data;
	}

	/**
	 * Returns a bounding rectangle around a given point
	 *
	 * @param float $lat
	 * @param float $lon
	 * @param float $radius
	 * @return Array
	 */
	public static function rectAround( $lat, $lon, $radius ) {
		if ( !$radius ) {
			return array( $lat, $lon, $lat, $lon );
		}
		$r2lat = rad2deg( $radius / self::EARTH_RADIUS );
		// @todo: doesn't work around poles, should we care?
		if ( abs( $lat ) < 89.9 ) {
			$r2lon = rad2deg( $radius / cos( deg2rad( $lat ) ) / self::EARTH_RADIUS );
		} else {
			$r2lon = 0.1;
		}
		$res = array(
			$lat - $r2lat,
			$lon - $r2lon,
			$lat + $r2lat,
			$lon + $r2lon
		);
		self::wrapAround( $res[0], $res[2], -90, 90 );
		self::wrapAround( $res[1], $res[3], -180, 180 );
		return $res;
	}

	private static function wrapAround( &$from, &$to, $min, $max ) {
		if ( $from < $min ) {
			$from = $max - ( $min - $from );
		}
		if ( $to > $max ) {
			$to = $min + $to - $max;
		}
	}

	function help() {
		/* TODO: Expand me! */
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

<b>* action=statistics *</b>

Parameters:
  stcountry       - Statistics for country. Supply the country code.
  stitem          - [total|name|name_pct|address|address_pct|municipality|municipality_pct|image|image_pct|coordinates|coordinates_pct]: the stats fields which should be returned (By default, all of them).
  limit           - [integer]: the maximum number of results you will get back (0 for all)
  
  
Examples:
  <a href="api.php?action=statistics&stitem=total|name_pct|address_pct|municipality_pct|image_pct|coordinates_pct&stcountry=pt&format=html&limit=0">api.php?action=statistics&amp;stitem=total|name_pct|address_pct|municipality_pct|image_pct|coordinates_pct&amp;stcountry=pt&amp;format=html&amp;limit=0</a>
  <a href="api.php?action=statistics&stcountry=pt&format=csv&limit=0">api.php?action=statistics&amp;stcountry=pt&amp;format=csv&amp;limit=0</a>

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

	/**
	 * Returns a range of tenths of degree. Borrowed from Extension:GeoData
	 * @param float $start
	 * @param float $end
	 * @return Array
	 */
	public static function intRange( $start, $end ) {
		$start = round( $start * self::GRANULARITY );
		$end = round( $end * self::GRANULARITY );
		// @todo: works only on Earth
		if ( $start > $end ) {
			return array_merge(
				range( -180 * self::GRANULARITY, $end ),
				range( $start, 180 * self::GRANULARITY )
			);
		} else {
			return range( $start, $end );
		}
	}

}
