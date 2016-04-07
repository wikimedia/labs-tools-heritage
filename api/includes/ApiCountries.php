<?php

class ApiCountries extends ApiBase {
	public static $defaultLanguages = array(
		'be' => 'nl',
		'ch' => 'de',
		'es' => 'es',
		'fr' => 'fr',
		'sk' => 'sk',
		'it' => 'it',
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

	public static function getDefaultLanguage( $country ) {
		if ( isset( self::$defaultLanguages[$country] ) ) {
			return self::$defaultLanguages[$country];
		} else {
			$languages = self::getInfo();
			if ( isset( $languages[$country] ) ) {
				return $languages[$country][0]; // Hope we have defaults for all multilingual countries:P
			}
		}
		return false;
	}

	public static function getAllLanguages() {
		static $languages = null;
		if ( $languages !== null ) {
			return $languages;
		}
		$info = self::getInfo();
		$languages = array();
		foreach ( $info as $country ) {
			$languages = array_merge( $languages, $country );
		}
		$languages = array_unique( $languages );
		return $languages;
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

	public static function pickCountryLanguage( $country, $useLang ) {
		$languages = self::getInfo();

		// Use default if the language is not used in this country
		if ( !isset( $languages[$country] ) || !in_array( $useLang, $languages[$country] ) ) {
			$useLang = false;
		}
		return $useLang;
	}
}
