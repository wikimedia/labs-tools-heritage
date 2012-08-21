<?php
class Language {
	private $data;
	private $code;
	private static $languageCache = array();

	private static $subdivisionOverrides = array(
		'Be' => 'Be-x-old',
	);

	private static $cldrOverrides = array(
		'No' => 'Nb',
		'Pt' => 'Pt_br', // While we don't have smart fallbacks
		'Sr' => 'Sr_ec',
		'Be_x_old' => 'Be',
	);

	private function __construct( $code, array $data ) {
		$this->code = $code;
		$this->data = $data;
	}

	public static function newFromCode( $code ) {
		if ( isset( self::$languageCache[$code] ) ) {
			return self::$languageCache[$code];
		}
		if ( !preg_match( '/^[-a-z0-9]+$/i', $code ) ) {
			throw new Exception( "Invalid language code '$code'!" );
		}

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
		self::$languageCache[$code] = new Language( $code, $data );
		return self::$languageCache[$code];
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
			}
		} else {
			if ( isset( $this->data['subdivisions'][$parts[0]] ) && isset( $this->data['subdivisions'][$parts[0]][$code] ) ) {
				return $this->data['subdivisions'][$parts[0]][$code]['name'];
			}
		}
		return false;
	}
}