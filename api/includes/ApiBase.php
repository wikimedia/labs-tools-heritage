<?php

/**
 * Similar to MediaWiki ApiBase
 * @author Platonides
 */
abstract class ApiBase {

	const PARAM_DFLT = 0; // Default value of the parameter
	const PARAM_ISMULTI = 1; // Boolean, do we accept more than one item for this parameter (e.g.: titles)?
	const PARAM_TYPE = 2; // Can be either a string type ['integer','string','boolean','callback'] or an array of allowed values
	const PARAM_MAX = 3; // Max value allowed for a parameter. Only applies if TYPE='integer'
	const PARAM_MIN = 5; // Lowest value allowed for a parameter. Only applies if TYPE='integer'

	/**
	 * The name of the encapsulating node for data output
	 * @param string
	 */
	protected $toplevel_node_name = "nodes";

	/**
	 * The name of the object nodes for data output
	 * @param string
	 */
	protected $object_node_name = "node";

	protected abstract function executeModule();

	protected $errors = array();
	function setError($errorCode) {
		$this->errors[] = $errorCode;
	}
	
	public function getDefaultAllowedParams() {
		global $dbMiserMode;
		$params = array(
			'format' => array( ApiBase::PARAM_DFLT => 'xmlfm', 
    			ApiBase::PARAM_TYPE => $dbMiserMode
					? array( 'json', 'xml', 'xmlfm' )
					: array( 'csv', 'dynamickml', 'kml', 'gpx', 'googlemaps', 'poi', 'html', 'htmllist', 'layar', 'json', 'osm', 'xml', 'xmlfm', 'wikitable' ) ),
				'callback' => array( ApiBase::PARAM_DFLT => false, ApiBase::PARAM_TYPE => 'callback' ),
				'limit' => array( ApiBase::PARAM_MIN => 0, ApiBase::PARAM_MAX => $dbMiserMode ? 500 : 5000,
				ApiBase::PARAM_DFLT => 100, ApiBase::PARAM_TYPE => 'integer' ),
    		'action' => array(
				ApiBase::PARAM_DFLT => 'help', 
    			ApiBase::PARAM_TYPE => ApiMain::getActions()
			),
			'uselang' => array(
				ApiBase::PARAM_DFLT => false,
				ApiBase::PARAM_TYPE => 'string'
			),
		);
		return $params;
	}

	abstract function getAllowedParams();

	private $paramCache;
	function getParam($name) {
		$this->paramCache = array();
		if ( !isset( $cache[$name] ) ) {
			$allowed = $this->getAllowedParams();
			if ( !isset($allowed[$name]) ) {
				throw new Exception( sprintf( 'Asked for a forbidden parameter: %s', $name ) );
			}

			if ( isset( $_GET[$name] ) and strlen( $_GET[$name] ) ) {
				$p = $allowed[$name][ApiBase::PARAM_TYPE];
				if ( is_array( $p ) ) {
					if ( empty( $allowed[$name][ApiBase::PARAM_ISMULTI] ) ) {
						if ( in_array( $_GET[$name], $p ) ) {
							$cache[$name] = $_GET[$name];
						} else {
							$this->setError( 'bad-param', $name );
							$cache[$name] = $allowed[$name][ApiBase::PARAM_DFLT];
						}
					} else {
						$items = explode( '|', $_GET[$name] );
						$cache[$name] = array();
						foreach ( $items as $item ) {
							if ( in_array( $item, $p ) ) {
								$cache[$name][] = $item;
							} else {
								$this->setError( 'bad-param-item', $item );
							}
						}
					}
				} elseif ( $p == 'integer' ) {
					$i = intval( $_GET[$name] ); // @fixme this will return 0 on failure, or 1 if it's a non-empty array... is this desired?
					$cache[$name] = min( max( $i, $allowed[$name][ApiBase::PARAM_MIN] ), 
						$allowed[$name][ApiBase::PARAM_MAX]);
				} elseif ( $p == 'boolean' ) {
					if ( $_GET[$name] == '0' || ( $_GET[$name] == 'no' ) ) {
						$cache[$name] = false;
					} elseif ( $_GET[$name] == '1' || ( $_GET[$name] == 'yes' ) ) {
						$cache[$name] = true;
					} else {
						$this->setError( 'bad-param', $name );
						$cache[$name] = $allowed[$name][ApiBase::PARAM_DFLT];
					}
				} elseif ( $p == 'callback' ) {
					if ( !preg_match( '/^[A-Za-z0-9]+$/', $_GET[$name] ) ) {
						$this->setError( 'bad-callback-name', $_GET[$name] );
						$cache[$name] = $allowed[$name][ApiBase::PARAM_DFLT];
					} else {
						$cache[$name] = $_GET[$name];
					}
				} elseif ( $p == 'string' ) {
					if ( empty( $allowed[$name][ApiBase::PARAM_ISMULTI] ) ) {
						$cache[$name] = (string)$_GET[$name];
					} elseif ( is_array( $_GET[$name] ) ) {
						$cache[$name] = $_GET[$name];
					} else {
						$cache[$name] = explode( '|', $_GET[$name] );
					}
				} else {
					throw new Exception( "Unknown param type $p" );
				}
			} else {
				$cache[$name] = $allowed[$name][ApiBase::PARAM_DFLT];
			}
		}
		return $cache[$name];
	}
	
	/**
	 * Returns an array with all the parameters
	 * If $params is an array, they override existing values
	 */
	function getParams($params = false) {
		$p = array();
		foreach ($this->getAllowedParams() as $name => $value) {
			if (isset($params[$name])) {
				$p[$name] = $params[$name];
			} elseif ( isset( $_GET[$name] ) and strlen( $_GET[$name] ) ) {
				$p[$name] = $this->getParam($name);
				if ( is_array( $p[$name] ) ) {
					$p[$name] = implode( '|', $p[$name] );
				}
			}
		}
		return $p;
	}

	/**
	 * Returns the url for this page.
	 * If $params is an array, they override existing values
	 */
	function getUrl($params = false) {
		$p = $this->getParams($params);
		
		if ( version_compare( PHP_VERSION, '5.4', '>=' ) ) {
			$query = http_build_query( $p, '', '&', PHP_QUERY_RFC3986 );
		} else {
			$query = http_build_query( $p, '', '&' );
		}
		return $_SERVER["SCRIPT_NAME"] . "?$query";
	}
	
	function getFullUrl($params = false) {
		if ( isset( $_SERVER['HTTPS'] ) && ( $_SERVER['HTTPS'] == 'on' ) ) {
			$url = 'https://';
		} else {
			$url = 'http://';
		}
		if ( isset( $_SERVER["HTTP_HOST"] ) ) {
			$url .= $_SERVER["HTTP_HOST"];
		} else {
			$url .= $_SERVER["SERVER_NAME"];
		}
		return $url . $this->getUrl( $params );
	}

	/**
	 * Returns the user's preferred language
	 *
	 * @param bool $useDefault: Whether default language for this country should be returned if user hasn't provided a language
	 *
	 * @return string|bool: Language code or false if uselang was not specified
	 */
	function getUseLang( $useDefault = true ) {
		$useLang = $this->getParam( 'uselang' );
		$country = $this->getCountry();

		// Don't know for which country
		if ( $useLang && !$country ) {
			$this->error( 'uselang needs a country code' );
		}
		// No uselang, no country - just don't filter by language
		if ( !$useLang && !$country ) {
			return false;
		}

		$languages = ApiCountries::getInfo();

		// Use default if the language is not used in this country
		if ( !isset( $languages[$country] ) || !in_array( $useLang, $languages[$country] ) ) {
			$useLang = false;
		}

		if ( !$useLang && $useDefault ) {
			$useLang = ApiCountries::getDefaultLanguage( $country );
		}
		return $useLang;
	}

	/**
	 * @return string|bool: Country code to be used by getUseLang() or false if none available/needed
	 */
	protected function getCountry() {
		return false;
	}

	/**
	 * @return FormatBase
	 */
	function getFormatter() {
		$formatter = "Format" . ucfirst( $this->getParam( 'format' ) );
		return new $formatter( $this );
	}
	
	function error( $message ) {
		throw new Exception( $message );
	}

	/**
	 * Setter for $this->toplevel_node_name
	 * @param string
	 */
	public function setTopLevelNodeName( $toplevel_node_name ) {
		$this->toplevel_node_name = $toplevel_node_name;
	}

	/**
	 * Getter for $this->toplevel_node_name
	 * @return string
	 */
	public function getTopLevelNodeName() {
		return $this->toplevel_node_name;
	}

	/**
	 * Setter for $this->object_node_name
	 * @param string
	 */
	public function setObjectNodeName( $object_node_name ) {
		$this->object_node_name = $object_node_name;
	}

	/**
	 * Getter for $this->object_node_name
	 * @return string
	 */
	public function getObjectNodeName() {
		return $this->object_node_name;
	}

	/**
	 * Handle pipes in strings within a pipe-delimited string
	 *
	 * There are times, particularly in wikitext, when a value may
	 * contain a pipe. Eg:
	 *    [[Alameda, California|Alameda]]
	 *
	 * This is problematic when you are receiving a pipe-delimited
	 * string that contains one or more of these cases, particularly
	 * when you wish to explode that string into an array.
	 *
	 * This static method turns a '|' present in wikitext and
	 * escapes string into another string, '//pipe//', then explodes
	 * the overall string on '|', and then replaces '//pipe//' with '|'
	 * for every element in the resulting array.
	 *
	 * @param string
	 * @return array
	 */
	public static function fixWikiTextPipeExplosion( $value ) {
		$pattern = "/(\[\[[^\]]+)(\|)([^\]]+\]\])/";
		$replacement = "$1//pipe//$3";
		$value = preg_replace( $pattern, $replacement, $value );
		$value = explode( '|', $value );
		return array_map( function ( $val ) { return str_replace( "//pipe//", "|", $val ); }, $value );
	}
}
