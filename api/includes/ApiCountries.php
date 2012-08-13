<?php

class ApiCountries extends ApiBase {
	public static $defaultLanguages = array(
		'be' => 'fr',
		'ch' => 'de',
		'es' => 'es',
		'fr' => 'fr',
		'sk' => 'sk',
		// 'it' => ???
	);

	public function __construct() {
		$this->setTopLevelNodeName( 'countries' );
		$this->setObjectNodeName( 'country' );
	}

	public function getAllowedParams() {
		return $this->getDefaultAllowedParams();
	}

	public function executeModule() {
		$countries = self::getInfo();
		$res = array();
		$formatter = $this->getFormatter();
		$isJson = stripos( 'json', get_class( $formatter ) ) !== false;
		foreach ( $countries as $code => $languages ) {
			$row = new stdClass;
			$row->code = $code;
			$row->languages = $isJson ? $languages : implode( ',', $languages );
			if ( isset( self::$defaultLanguages[$code] ) ) {
				$row->default = self::$defaultLanguages[$code];
			}
			$res[] = $row;
		}
		$formatter->output( $res, 10000, null, array( 'code', 'languages', 'default' ), null );
	}

	public static function getInfo() {
		static $cached = null;
		if ( $cached !== null ) {
			return $cached;
		}
		$cached = self::getCachedInfo();
		return $cached;
	}

	private static function getCachedInfo() {
		global $cacheDir;

		$fname = "$cacheDir/countries.ser";
		if ( file_exists( $fname ) ) {
			$data = unserialize( file_get_contents( $fname ) );
		} else {
			$data = self::getInfoFromDB();
			file_put_contents( $fname, serialize( $data ) );
		}
		return $data;
	}

	private static function getInfoFromDB() {
		$ret = array();
		$db = Database::getDb();
		$res = new ResultWrapper( $db, $db->query( 'SELECT country, lang, adm0 FROM `monuments_all` GROUP BY country, lang' ) );
		foreach ( $res as $row ) {
			$country = $row->adm0;
			$lang = $row->lang;
			if ( !isset( $ret[$country] ) ) {
				$ret[$country] = array();
			}
			if ( !isset( $ret[$country][$lang] ) ) {
				$ret[$country][$lang] = count( $ret[$country] );
			}
		}
		return array_map( 'array_flip', $ret );
	}
}
