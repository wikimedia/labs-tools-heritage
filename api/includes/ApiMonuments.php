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

	public function __construct() {
		$this->setTopLevelNodeName( 'monuments' );
		$this->setObjectNodeName( 'monument' );
	}

	protected function getParamDescription() {
		return array(
			/* FIXME: Copy from http://etherpad.wikimedia.org/WLM-tech*/
		);
	}
	
	function getAllowedParams() {
		global $dbMiserMode;
		$defaultParams = $this->getDefaultAllowedParams();
		$params = array(
			'props' => array( ApiBase::PARAM_DFLT => Monuments::$dbFields,
				ApiBase::PARAM_TYPE => Monuments::$dbFields, ApiBase::PARAM_ISMULTI => true ),
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
		);
		$params = array_merge( $defaultParams, $params );

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
			case 'help':
			default:
				ApiBase::help();
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

	protected function getCountry() {
		return $this->getParam( 'sradm0' );
	}

	function search() {
		global $dbMiserMode;

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
		$enableUseLang = true;
		$useDefaultLang = false;
		$smartFilter = false;

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
				$useDefaultLang = true;
				$where[] = "MATCH ({$db->escapeIdentifier( $field )}) AGAINST ("
					. $db->quote( substr( $value, 1 ) ) . ' IN BOOLEAN MODE)';
				// Postfix the name with primary key because name can be duplicate.
				// Filesort either way.
				$orderby = array_merge( array( $field ), $orderby );
			} elseif ( is_string( $value ) && strpos( $value, '%' ) !== false ) {
				if ( $dbMiserMode && !preg_match( '/^[^%]+%$/', $value ) ) {
					$this->error( 'Only prefix search is allowed in miser mode' );
				}
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
			$enableUseLang = false;
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
			if ( $dbMiserMode && ( $tr_lat - $bl_lat ) * ( $tr_lon - $bl_lon ) > self::MAX_GEOSEARCH_AREA ) {
				$this->error( 'Bounding box is too large' );
			}
			$where['lat_int'] = self::intRange( $bl_lat, $tr_lat );
			$where['lon_int'] = self::intRange( $bl_lon, $tr_lon );
			$where[] = "`lat` BETWEEN $bl_lat AND $tr_lat";
			$where[] = "`lon` BETWEEN $bl_lon AND $tr_lon";
			$smartFilter = true;
			$useDefaultLang = true;
        }
		$useLang = $this->getUseLang( $useDefaultLang );
		if ( $enableUseLang && $useLang && !isset( $where['lang'] ) ) {
			$where['lang'] = $useLang;
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

		if ( $smartFilter ) {
			$rows = array();
			$numRows = 0;

			// Prepare an array of language weights signifying how much desireable each of them is
			$country = $this->getCountry();
			$weights = array_flip( ApiCountries::getAllLanguages() );
			$weights = array_map( function() { return 1; }, $weights ); // Prefer no language
			$weights[$useLang] = 1000; // ...other than uselang
			$defaultLang = ApiCountries::getDefaultLanguage( $country ); // And country's default language
			$weights[$defaultLang] = 500;

			foreach ( $res as $row ) {
				$numRows++;
				$id = "{$row->country}-{$row->id}";
				if ( !isset( $weights[$row->lang] ) ) { // foolproof in case cache is out of date
					$weights[$row->lang] = 1;
				}
				if ( !isset( $rows[$id] ) || ( $weights[$row->lang] > $weights[$rows[$id]->lang] ) ) {
					$rows[$id] = $row;
				}
			}
			if ( $numRows > $limit ) {
				// Tweak limit to ensure pagination will happen
				$limit = count( $rows ) - 1;
			}
			$res = $rows;
		}

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
