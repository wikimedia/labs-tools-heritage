<?php

if ( get_magic_quotes_gpc() ) {
	die( 'Magic quotes are enabled!' );
}

/**
 * Definition of Monuments API
 * @author Platonides
 */
class ApiMonuments extends ApiBase {

	const MAX_GEOSEARCH_AREA = 0.04;// 0.2 * 0.2 degrees
	const GRANULARITY = 20;

	protected function getParamDescription() {
		return array(
			/* FIXME: Copy from http://etherpad.wikimedia.org/WLM-tech*/
		);
	}
	
	function getAllowedParams() {
    	$params = array(
    		'props' => array( ApiBase::PARAM_DFLT => Monuments::$dbFields,
				ApiBase::PARAM_TYPE => Monuments::$dbFields, ApiBase::PARAM_ISMULTI => true ),
    		'format' => array( ApiBase::PARAM_DFLT => 'xmlfm', 
    			ApiBase::PARAM_TYPE => array( 'csv', 'dynamickml', 'kml', 'gpx', 'googlemaps', 'poi', 'html', 'htmllist', 'layar', 'json', 'osm', 'xml', 'xmlfm', 'wikitable' ) ),
    		'callback' => array( ApiBase::PARAM_DFLT => false, ApiBase::PARAM_TYPE => 'callback' ),
    		'limit' => array( ApiBase::PARAM_MIN => 0, ApiBase::PARAM_MAX => 5000, 
				ApiBase::PARAM_DFLT => 100, ApiBase::PARAM_TYPE => 'integer' ),
    			
    		'action' => array( ApiBase::PARAM_DFLT => 'help', 
    			ApiBase::PARAM_TYPE => array( 'help', 'search', 'statistics' ) ),
    			
    		'srquery' => array( ApiBase::PARAM_DFLT => false, ApiBase::PARAM_TYPE => 'string' ),
    		'bbox' => array( ApiBase::PARAM_DFLT => false, ApiBase::PARAM_TYPE => 'string' ),
    		'BBOX' => array( ApiBase::PARAM_DFLT => false, ApiBase::PARAM_TYPE => 'string' ),
    		'srcontinue' => array( ApiBase::PARAM_DFLT => false, ApiBase::PARAM_TYPE => 'string' ),
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
			case 'help':
				$this->help();
				break;
			case 'search':
				$this->search();
				break;
			case 'statistics':
				$this->statistics();
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
        
        if ( $this->getParam('bbox') or $this->getParam('BBOX') ) {
			if ( $this->getParam('bbox') ) {
                $bbox = $this->getParam('bbox');
            } else {
                $bbox = $this->getParam('BBOX');
            }
            $coords = preg_split('/,|\s/', $bbox);
            $bl_lon = floatval( $coords[0] );
            $bl_lat = floatval( $coords[1] );
            $tr_lon = floatval( $coords[2] );
            $tr_lat = floatval( $coords[3] );
			if ( $bl_lat > $tr_lat || $bl_lon > $tr_lon ) {
				$this->error( 'Invalid bounding box' );
			}
			if ( ( $tr_lat - $bl_lat ) * ( $tr_lon - $bl_lon ) > self::MAX_GEOSEARCH_AREA ) {
				$this->error( 'bbox is too large' );
			}
			$where['lat_int'] = self::intRange( $bl_lat, $tr_lat );
			$where['lon_int'] = self::intRange( $bl_lon, $tr_lon );
			$where[] = "`lat` BETWEEN $bl_lat AND $tr_lat";
			$where[] = "`lon` BETWEEN $bl_lon AND $tr_lon";
        }

        //for kml and bbox get only monuments with coordinates
        if ( ($this->getParam('format') == 'kml') ) {
            $where[] = 'lat<>0 AND lon<>0';
        }

        /* FIXME: User should be able to set sort fields and order */
		if ( $this->getParam('format') == 'kml' ) {
			$orderby = array('image', 'id'); /* FIXME: Randomize the KML output. */
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
		$st = new Statistics( $db = Database::getDb() );
        $items = $this->getParam( 'stitem' );
        $filters = explode('|', $this->getParam('stcountry'));
        $limit = $this->getParam( 'limit' );

        $r = $st->retrieveReport($items, $filters, $limit);
        $this->getFormatter()->output($r, 9999999, 'stcontinue', array_merge(array('country', 'municipality'), $st->getAxis('columns')), Monuments::$dbPrimaryKey );
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
