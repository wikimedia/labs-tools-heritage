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

	protected $errors = array();
	function setError($errorCode) {
		$this->errors[] = $errorCode;
	}
	
	abstract function getAllowedParams();
	
	private $paramCache;
	function getParam($name) {
		$this->paramCache = array();
		if ( !isset( $cache[$name] ) ) {
			$allowed = $this->getAllowedParams();
			if ( !isset($allowed[$name]) ) {
				throw new Exception( 'Asked for a forbidden parameter' );
			}

			if ( isset( $_GET[$name] ) ) {
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
						$items = explode( '|', $_GET['name'] );
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
					$i = intval( $_GET[$name] );
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
						$cache[$name] = $_GET['name'];
					}
				} elseif ( $p == 'string' ) {
					$cache[$name] = $_GET['name'];
				} else {
					throw new Exception( "Unknown param type $p" );
				}
			} else {
				$cache[$name] = $allowed[$name][ApiBase::PARAM_DFLT];
			}
		}
		return $cache[$name];
	}
	
	function getFormatter() {
		$formatter = "Format" . ucfirst( $this->getParam( 'format' ) );
		return new $formatter;
	}
	
	function help() {
		/* TODO: Write me! */
		echo "This should show some help information. Collaborate writing it!";
	}
}
