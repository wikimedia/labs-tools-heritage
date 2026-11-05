<?php

require_once __DIR__ . '/../includes/ApiBase.php';
require_once __DIR__ . '/../includes/FormatBase.php';
require_once __DIR__ . '/../includes/FormatGpx.php';
require_once __DIR__ . '/../includes/FormatKml.php';
require_once __DIR__ . '/../includes/Monuments.php';

/**
 * Searches fetch the primary key, the requested props and the format's
 * required props, so the formats must render rows holding nothing else.
 */
class FormatRequiredPropsTest extends PHPUnit\Framework\TestCase {

	protected function setUp(): void {
		set_error_handler( static function ( $errno, $errstr, $errfile, $errline ) {
			throw new ErrorException( $errstr, 0, $errno, $errfile, $errline );
		} );
	}

	protected function tearDown(): void {
		restore_error_handler();
	}

	/**
	 * A row as a search with an empty props selection returns it.
	 */
	private static function makeRow( FormatBase $format, array $values ) {
		$row = new stdClass;
		$fields = array_merge( Monuments::$dbPrimaryKey, $format->getRequiredProps() );
		foreach ( $fields as $field ) {
			$row->$field = $values[$field] ?? 'x';
		}
		return $row;
	}

	private function makeFormat( string $class ) {
		// headers() would send HTTP headers, which the test runner can't
		return $this->getMockBuilder( $class )
			->setConstructorArgs( [ $this->createMock( ApiBase::class ) ] )
			->onlyMethods( [ 'headers' ] )
			->getMock();
	}

	private static function render( FormatBase $format, array $rows ) {
		ob_start();
		try {
			$format->output( $rows, 10, 'srcontinue', $format->getRequiredProps(),
				Monuments::$dbPrimaryKey );
		} finally {
			$output = ob_get_clean();
		}
		return $output;
	}

	public function test_gpx_renders_row_with_only_required_props() {
		$format = $this->makeFormat( FormatGpx::class );
		$row = self::makeRow( $format, [
			'lang' => 'sv',
			'project' => 'wikipedia',
			'id' => 'A1',
			'lat' => '59.85',
			'lon' => '17.65',
			'changed' => '2026-11-03 03:58:09',
			'name' => 'Domkyrkan',
			'source' => '//sv.wikipedia.org/wiki/Lista',
			'monument_article' => 'Uppsala_domkyrka',
		] );

		$output = self::render( $format, [ $row ] );

		$this->assertStringContainsString( '<wpt lat="59.85" lon="17.65">', $output );
		$this->assertStringContainsString( '<time>' . date( 'c', strtotime( '2026-11-03 03:58:09' ) ) . '</time>', $output );
		$this->assertStringContainsString( '<name>A1</name>', $output );
		$this->assertStringContainsString( '<desc>Domkyrkan</desc>', $output );
		$this->assertStringContainsString( '<src>//sv.wikipedia.org/wiki/Lista</src>', $output );
		$this->assertStringContainsString(
			'<link>http://sv.wikipedia.org/wiki/Uppsala_domkyrka</link>', $output );
	}

	public static function provideMissingCoordinates() {
		return [
			'NULL in the database' => [ static function ( $row ) {
				$row->lat = null;
				$row->lon = null;
			} ],
			'0,0 removed by the search row filter' => [ static function ( $row ) {
				unset( $row->lat, $row->lon );
			} ],
		];
	}

	/**
	 * @dataProvider provideMissingCoordinates
	 */
	public function test_gpx_skips_row_without_coordinates( $removeCoordinates ) {
		$format = $this->makeFormat( FormatGpx::class );
		$row = self::makeRow( $format, [ 'id' => 'A1' ] );
		$removeCoordinates( $row );

		$output = self::render( $format, [ $row ] );

		$this->assertStringNotContainsString( '<wpt', $output );
		$this->assertStringEndsWith( '</gpx>', $output );
	}

	public function test_kml_renders_row_with_only_required_props() {
		$format = $this->makeFormat( FormatKml::class );
		$row = self::makeRow( $format, [
			'country' => 'se',
			'lang' => 'sv',
			'id' => 'A1',
			'lat' => '59.85',
			'lon' => '17.65',
		] );

		$output = self::render( $format, [ $row ] );

		$this->assertStringContainsString( '<Placemark id="sesvA1">', $output );
		$this->assertStringContainsString(
			'<Point><coordinates>17.65,59.85</coordinates></Point>', $output );
	}

}
