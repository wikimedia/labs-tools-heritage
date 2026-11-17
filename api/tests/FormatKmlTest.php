<?php

require_once __DIR__ . '/../includes/ApiBase.php';
require_once __DIR__ . '/../includes/CommonFunctions.php';
require_once __DIR__ . '/../includes/FormatBase.php';
require_once __DIR__ . '/../includes/FormatKml.php';

if ( !function_exists( '_i18n' ) ) {
	// Normally provided by api/common.php; only used for labels.
	function _i18n( $key ) {
		return $key;
	}
}

/**
 * The placemark description is HTML, escaped once more for the XML, so a
 * KML viewer decodes it back into HTML for the balloon.
 */
class FormatKmlTest extends PHPUnit\Framework\TestCase {

	private function getDescription( $row ) {
		$format = new FormatKml( $this->createMock( ApiBase::class ) );
		ob_start();
		try {
			$format->outputRow( $row, [ 'id', 'name' ] );
		} finally {
			$output = ob_get_clean();
		}
		$this->assertSame( 1, preg_match( '#<description>(.*)</description>#s', $output, $m ) );
		// The HTML the viewer shows in the balloon
		return htmlspecialchars_decode( $m[1] );
	}

	public function test_description_escapes_harvested_values() {
		$row = (object)[
			'country' => 'se',
			'lang' => 'sv',
			'project' => 'wikipedia',
			'id' => 'A1<img src=x onerror=alert(1)>',
			'name' => 'Kerk [[X|<b>Y</b>]]',
			'lat' => '59.85',
			'lon' => '17.65',
		];

		$description = $this->getDescription( $row );

		$this->assertStringContainsString( 'A1&lt;img src=x onerror=alert(1)&gt;', $description );
		$this->assertStringContainsString(
			'Kerk <a href="//sv.wikipedia.org/wiki/X">&lt;b&gt;Y&lt;/b&gt;</a>', $description );
		$this->assertStringNotContainsString( '<img', $description );
	}

}
