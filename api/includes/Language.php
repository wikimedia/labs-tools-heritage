<?php
class Language {
	private $data;
	private $code;
	private static $languageCache = array();
	private $fallback;

	private static $subdivisionOverrides = array(
		'Be' => 'Be-x-old',
	);

	private static $cldrOverrides = array(
		'No' => 'Nb',
		'Sr' => 'Sr_ec',
		'Be_x_old' => 'Be',
	);

	private function __construct( $code, array $data ) {
		$this->code = $code;
		$this->data = $data;

		$fallbacks = $this->getFallbacks();
		if ( $fallbacks ) {
			$this->fallback = self::newFromCode( $fallbacks[0] );
		}
	}

	public static function newFromCode( $code, $countryLang = false ) {
		if ( isset( self::$languageCache[$code] ) ) {
			return self::$languageCache[$code];
		}
		if ( !preg_match( '/^[-a-z0-9]+$/i', $code ) ) {
			throw new Exception( "Invalid language code '$code'!" );
		}
		$data = self::getRawData( $code );
		if ( !$data && $countryLang ) {
			$data = self::getRawData( $countryLang );
		}

		self::$languageCache[$code] = new Language( $code, $data );
		return self::$languageCache[$code];
	}

	private static function getRawData( $code ) {
		global $cldrPath, $subdivisionsPath;
		$data = array();
		if ( $cldrPath && $subdivisionsPath ) {
			$prettyCode = ucfirst( $code );
			$subCode = isset( self::$subdivisionOverrides[$prettyCode] )
				? self::$subdivisionOverrides[$prettyCode]
				: $prettyCode;
			$file = "{$subdivisionsPath}/subdivisions/Subdivisions{$subCode}.php";
			if ( is_file( $file ) ) {
				$subdivisions = array();
				require_once( $file );
				$overrides_file = "{$subdivisionsPath}/overrides/Overrides{$subCode}.php";
				if ( is_file( $overrides_file ) ) {
					require_once( $overrides_file );
				}
				$data['subdivisions'] = $subdivisions;
			}
			$prettyCode = str_replace( '-', '_', $prettyCode );
			$cldrCode = isset( self::$cldrOverrides[$prettyCode] )
				? self::$cldrOverrides[$prettyCode]
				: $prettyCode;
			$file = "{$cldrPath}/CldrNames/CldrNames{$cldrCode}.php";
			if ( is_file( $file ) ) {
				$countryNames = array();
				require_once( $file );
				$data['countryNames'] = $countryNames;
			}
		}
		return $data;
	}

	private function getFallbacks() {
		static $fallbacks = null;
		if ( $fallbacks === null ) {
			// Run tools/scrape-fallbacks.php to update this information
			$fallbacks = unserialize( file_get_contents( dirname( __DIR__ ) . '/data/LanguageFallbacks.ser' ) );
			// WLM-specific overrides due to the state of CLDR
			$fallbacks['pt'] = array( 'pt-br' );
			$fallbacks['pt-br'] = array( 'en' );
		}

		if ( isset( $fallbacks[$this->code] ) ) {
			return $fallbacks[$this->code];
		}
		return array();
	}

	public function hasData() {
		return !empty( $this->data );
	}

	public function getCode() {
		return $this->code;
	}

	public function getName( $code ) {
		if ( !$this->hasData() ) {
			return false;
		}
		$code = strtoupper( $code );
		$parts = explode( '-', $code, 2 );

		if ( count( $parts ) == 1 ) {
			if ( isset( $this->data['countryNames'][$code] ) ) {
				return $this->data['countryNames'][$code];
			} elseif ( isset( $this->data['subdivisions']['GB'][$code] ) ) {
				// GB is only country that has subdivisions that may not have two-letter prefixes
				return $this->data['subdivisions']['GB'][$code]['name'];
			}
		} else {
			if ( isset( $this->data['subdivisions'][$parts[0]] ) && isset( $this->data['subdivisions'][$parts[0]][$code] ) ) {
				return $this->data['subdivisions'][$parts[0]][$code]['name'];
			}
		}
		return $this->fallback ? $this->fallback->getName( $code ) : false;
	}
}