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
	const MAX_GEOSEARCH_AREA = 0.041;// 0.2 * 0.2 degrees
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

        $params['ctcountry'] = array( ApiBase::PARAM_DFLT => array_keys(ContestStatistics::$activeCountries), 
            ApiBase::PARAM_TYPE => array_keys(ContestStatistics::$activeCountries), ApiBase::PARAM_ISMULTI => true );
        $params['ctscope'] = array( ApiBase::PARAM_DFLT => ContestStatistics::$ctScopes[0], ApiBase::PARAM_TYPE => ContestStatistics::$ctScopes );
        $params['ctitem'] = array( ApiBase::PARAM_DFLT => array(),
            ApiBase::PARAM_TYPE => array_merge( ContestStatistics::$reportUserCols, ContestStatistics::$reportCountryCols, ContestStatistics::$reportDumpCols ), ApiBase::PARAM_ISMULTI => true );
		$params['ctfrom'] = array( ApiBase::PARAM_DFLT => '20110901000000', ApiBase::PARAM_TYPE => 'string' );
		$params['ctorderby'] = array( ApiBase::PARAM_DFLT => 'n_images', ApiBase::PARAM_TYPE => 'string' );

		return $params;
	}
	
	function executeModule() {
		switch ( $this->getParam( 'action' ) ) {
			case 'search':
				$this->search();
				break;
			case 'statistics':
			case 'statisticsdb':
				$this->statistics_db();
                break;
			case 'statisticsct':
				$this->statistics_ct();
                break;
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

	/**
	 * @param $fileds array|string
	 * @param $query string
	 *
	 * @return string
	 */
	private function fulltextSearch( $fileds, $query ) {
		$db = Database::getDb();
		$this->complexQuery();
		$fieldList = implode( ', ',
			array_map( array( $db, 'escapeIdentifier' ),
				(array)$fileds
			)
		);
		return "MATCH ($fieldList) AGAINST ({$db->quote( $query )} IN BOOLEAN MODE)";
	}

	protected function getCountry() {
		return $this->getParam( 'sradm0' );
	}

	function search() {
		global $dbMiserMode;

		// @todo: set to empty array after beta 3 is released
		$fulltextColumns = array( 'name' => 1 );
        
        if ( $this->getParam('format') == 'dynamickml' ) {
            #don't search just pass along the search parameters to kml network link file
            $DynKml = new DynamicKml;
            $reqUrl = 'http://' . $_SERVER['SERVER_NAME'] . $_SERVER['REQUEST_URI'];
            $DynKml->output($reqUrl);
            return;
        }

		$props = $this->getParam( 'props' );
		$where = array();
		$forceIndex = false;
		$orderby = Monuments::$dbPrimaryKey;
		$db = Database::getDb();
		$enableUseLang = true;
		$useDefaultLang = false;
		$smartFilter = false;
		$spatialMode = false;

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
				$useDefaultLang = true;
				$where[] = $this->fulltextSearch( $field, substr( $value, 1 ) );
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
					$value = static::fixWikiTextPipeExplosion( $value );
				}
				
				$where[$field] = $value;
			}
		}

		$fulltextQuery = $this->getParam( 'srquery' );
		if ( $fulltextQuery ) {
			$useDefaultLang = true;
			$orderby = array_merge( array( 'name' ), $orderby );
			$where[] = $this->fulltextSearch( array( 'name', 'address' ), $fulltextQuery );
		}
        
        if ( $this->getParam('bbox') || $this->getParam('BBOX') || $this->getParam( 'coord' ) ) {
			$spatialMode = true;
			$smartFilter = true;
			$enableUseLang = false;
			$useDefaultLang = true;
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
				$lat = ( $bl_lat + $tr_lat ) / 2;
				$lon = ( $bl_lon + $tr_lon ) / 2;
			} else {
				$radius = $this->getParam( 'radius' );
				if ( $radius === false || $radius <= 0 ) {
					$this->error( 'Radius not set or is invalid' );
				}
				$coords = array_map( 'floatval', preg_split( '/,|\s/', $this->getParam( 'coord' ) ) );
				if ( count( $coords ) != 2 ) {
					$this->error( 'Invalid coordinate format, 2 comma-delimited numbers are expected' );
				}
				list( $lat, $lon ) = $coords;
				list( $bl_lat, $bl_lon, $tr_lat, $tr_lon ) =
					self::rectAround( $lat, $lon, $this->getParam( 'radius' ) );
			}
			if ( $dbMiserMode && ( $tr_lat - $bl_lat ) * ( $tr_lon - $bl_lon ) > self::MAX_GEOSEARCH_AREA ) {
				$this->error( 'Bounding box is too large' );
			}
			$where['lat_int'] = self::intRange( $bl_lat, $tr_lat );
			$where['lon_int'] = self::intRange( $bl_lon, $tr_lon );
			$where[] = "`lat` BETWEEN $bl_lat AND $tr_lat";
			$where[] = "`lon` BETWEEN $bl_lon AND $tr_lon";
			$orderby = false; // We'll sort manually later
			$props[] = 'lat';
			$props[] = 'lon';
			$props = array_unique( $props );
        } elseif ( $this->getParam( 'sradm0' ) ) {
			for ( $i = 0; $i < 5 && $this->getParam( "sradm{$i}" ) !== false; $i++) {
				$forceIndex = "admin_levels{$i}";
			}
			$orderby = array( 'name', 'country', 'id' );
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
		if ( $continue && !$spatialMode ) {
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
		
		$res = $db->select( array_merge( Monuments::$dbPrimaryKey, $props ), Monuments::$dbTable, $where,
			$orderby, $spatialMode ? null : ( $limit + 1 ), $forceIndex );

		if ( $smartFilter ) {
			$rows = array();
			$numRows = 0;

			if ( !$useLang ) {
				$useLang = $this->getParam( 'uselang' );
			}

			foreach ( $res as $row ) {
				$numRows++;
				if ( $spatialMode ) {
					$row->dist = self::distance( $row->lat, $row->lon, $lat, $lon );
				}
				if ( $useLang ) {
					$id = "{$row->country}-{$row->id}";
					if ( !isset( $rows[$id] )
						|| $this->rowWeight( $row, $useLang ) > $this->rowWeight( $rows[$id], $useLang ) )
					{
						$rows[$id] = $row;
					}
				} else {
					$rows[] = $row;
				}
			}
			if ( $spatialMode ) {
				$props[] = 'dist';
				usort( $rows,
					function( $a, $b ) {
						if ( $a->dist == $b->dist ) {
							return 0;
						}
						return ( $a->dist < $b->dist ) ? -1 : 1;
					}
				);
				// Enumerate all the rows for continue to work
				$rows = array_values( $rows );
				for ( $i = 0; $i < count( $rows ); $i++ ) {
					$rows[$i]->number = $i;
				}
				$orderby = array( 'number' );
				if ( $continue ) {
					array_splice( $rows, 0, intval( $continue ) );
				}
			} elseif ( $numRows > $limit ) {
				// Tweak limit to ensure pagination will happen
				$limit = count( $rows ) - 1;
			}
			$res = $rows;
		}

		$formatter = $this->getFormatter();
		$formatter->setRowFilter(
			function( $row ) {
				if ( isset( $row->lat ) && isset( $row->lon )
					&& !$row->lat && !$row->lon )
				{
					unset( $row->lat );
					unset( $row->lon );
				}
			}
		);

		$formatter->output( $res, $limit, 'srcontinue', $props, $orderby );
	}

	private $countryDefaults = array();
	private function rowWeight( $row, $useLang ) {
		if ( $useLang ) {
			if ( $row->lang == $useLang ) {
				return 1000;
			}
			if ( isset( $row->adm0 ) ) {
				if ( isset( $this->countryDefaults[$row->adm0] ) ) {
					$defaultLang = $this->countryDefaults[$row->adm0];
				} else {
					$defaultLang = ApiCountries::getDefaultLanguage( $row->adm0 );
					$this->countryDefaults[$row->adm0] = $defaultLang;
				}
				if ( $row->lang == $defaultLang ) {
					return 500;
				}
			}
		}
		return 1;
	}
	
	function statistics_db() {
        
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

	function statistics_ct() {
		$st = new ContestStatistics( $db = Database::getDb() );


        $ctscope = $this->getParam( 'ctscope' );
        $ctitems = $this->getParam( 'ctitem' );
        if ( count($ctitems)<=0 ) {
            if ( $ctscope == 'user' ) {
                $ctitems = ContestStatistics::$reportUserCols;
            } elseif ( $ctscope == 'country' ) {
                $ctitems = ContestStatistics::$reportCountryCols;
            } else { /* scope=images */
                $ctitems = array();
            }
        }
        $ctcountries = $this->getParam( 'ctcountry' );
        $limit = $this->getParam( 'limit' );
        $ctfrom = $this->getParam( 'ctfrom' );
        $ctorderby = $this->getParam( 'ctorderby' );

        $r = $st->retrieveReport($ctscope, $ctitems, $ctcountries, $ctfrom, $limit, $ctorderby);
        $this->getFormatter()->output($r, 9999999, 'stcontinue', $st->getAxis('columns'), ContestStatistics::$dbPrimaryKey );
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

	/**
	 * Calculates distance between two coordinates
	 * @see https://en.wikipedia.org/wiki/Haversine_formula
	 *
	 * @param float $lat1
	 * @param float $lon1
	 * @param float $lat2
	 * @param float $lon2
	 * @return float Distance in meters
	 */
	public static function distance( $lat1, $lon1, $lat2, $lon2 ) {
		$lat1 = deg2rad( $lat1 );
		$lon1 = deg2rad( $lon1 );
		$lat2 = deg2rad( $lat2 );
		$lon2 = deg2rad( $lon2 );
		$sin1 = sin( ( $lat2 - $lat1 ) / 2 );
		$sin2 = sin( ( $lon2 - $lon1 ) / 2 );
		return 2 * self::EARTH_RADIUS * asin( sqrt( $sin1 * $sin1 + cos( $lat1 ) * cos( $lat2 ) * $sin2 * $sin2 ) );
	}

}
