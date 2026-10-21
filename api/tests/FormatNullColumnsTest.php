<?php

require_once __DIR__ . '/../includes/ApiBase.php';
require_once __DIR__ . '/../includes/FormatBase.php';
require_once __DIR__ . '/../includes/FormatCsv.php';
require_once __DIR__ . '/../includes/FormatGpx.php';
require_once __DIR__ . '/../includes/FormatHtml.php';
require_once __DIR__ . '/../includes/FormatHtmllist.php';
require_once __DIR__ . '/../includes/FormatWikitable.php';
require_once __DIR__ . '/../includes/FormatXml.php';

if ( !function_exists( '_i18n' ) ) {
	// Normally provided by api/common.php; only used for table headers.
	function _i18n( $key ) {
		return $key;
	}
}

/**
 * Rows from monuments_all frequently have NULL in the nullable columns
 * (most commonly lat/lon). Every output format must cope with them
 * without raising notices, since display_errors would print those into
 * the response body.
 */
class FormatNullColumnsTest extends PHPUnit\Framework\TestCase {

	protected function setUp(): void {
		// FormatHtmllist reads its labels from the global Intuition instance.
		$GLOBALS['I18N'] = new class {
			public function msg( $key ) {
				return $key;
			}
		};
		set_error_handler( static function ( $errno, $errstr, $errfile, $errline ) {
			throw new ErrorException( $errstr, 0, $errno, $errfile, $errline );
		} );
	}

	protected function tearDown(): void {
		restore_error_handler();
		unset( $GLOBALS['I18N'] );
	}

	private static function makeRow() {
		return (object)[
			'country' => 'se',
			'lang' => 'sv',
			'project' => 'wikipedia',
			'id' => '123',
			'adm0' => 'se',
			'adm1' => null,
			'name' => 'Example',
			'lat' => null,
			'lon' => null,
			'image' => '',
			'wd_item' => null,
			'commonscat' => '',
			'source' => '',
			'changed' => '2024-01-02 03:04:05',
			'monument_article' => '',
		];
	}

	private function renderRow( $formatClass, $selectedItems ) {
		$format = new $formatClass( $this->createMock( ApiBase::class ) );
		ob_start();
		try {
			$format->outputRow( self::makeRow(), $selectedItems );
		} finally {
			$output = ob_get_clean();
		}
		return $output;
	}

	public static function provideFormats() {
		return [
			'csv' => [ FormatCsv::class, '"123","",""' ],
			'gpx' => [ FormatGpx::class, '<wpt lat="" lon="">' ],
			'html' => [ FormatHtml::class, '<td>123</td>' . "\n" . '<td></td>' ],
			'htmllist' => [ FormatHtmllist::class, '<li> db-field-adm1: </li>' ],
			'wikitable' => [ FormatWikitable::class, "|123\n|\n|\n" ],
			'xml' => [ FormatXml::class, ' id="123" adm1="" lat="" lon=""' ],
		];
	}

	/**
	 * @dataProvider provideFormats
	 */
	public function test_outputRow_nullColumns( $formatClass, $expected ) {
		$output = $this->renderRow( $formatClass, [ 'id', 'adm1', 'lat', 'lon', 'wd_item' ] );
		$this->assertStringContainsString( $expected, $output );
	}

}
