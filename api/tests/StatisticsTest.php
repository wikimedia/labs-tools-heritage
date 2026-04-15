<?php

require __DIR__ . '/../includes/StatisticsBase.php';
require __DIR__ . '/../includes/Statistics.php';

class StubSanitizingDb {
	public function sanitize( $s ) {
		return $s;
	}
}

class StatisticsTest extends PHPUnit\Framework\TestCase {

	public function test_packIdxFromIndex_short_muni_unchanged() {
		$db = new StubSanitizingDb();
		$row = [ 'by', 'Minsk', 'be', 'wikipedia' ];
		$this->assertEquals(
			[ 'by', 'Minsk', 'be', 'wikipedia' ],
			Statistics::packIdxFromIndex( $row, $db )
		);
	}

	public function test_packIdxFromIndex_truncates_on_character_boundary() {
		$db = new StubSanitizingDb();
		// 120 Cyrillic characters = 240 bytes, well past the 100-char cap.
		// Byte-level substr() would slice mid-character and yield invalid
		// UTF-8; mb_substr() must not.
		$muni = str_repeat( 'Ё', 120 );
		$row = [ 'by', $muni, 'be-tarask', 'wikipedia' ];

		$result = Statistics::packIdxFromIndex( $row, $db );
		$truncated = $result[1];

		// Exactly maxMuniLength characters: (maxMuniLength - 1) original + '…'.
		$this->assertEquals( Statistics::$maxMuniLength, mb_strlen( $truncated, 'UTF-8' ) );
		// Ends with the ellipsis marker.
		$this->assertEquals( '…', mb_substr( $truncated, -1, 1, 'UTF-8' ) );
		// Still valid UTF-8 (the original bug was: it wasn't).
		$this->assertTrue( mb_check_encoding( $truncated, 'UTF-8' ) );
	}

	public function test_makeIdxString() {
		$idx = [ 'country','municipality','lang','project' ];
		$this->assertEquals(
			"country:municipality:lang:project",
			Statistics::makeIdxString( $idx )
		);
	}

	public function test_makeIdxString_colon() {
		$idx = [ 'country','[[se:municipality]]','lang','project' ];
		$this->assertEquals(
			"country:[[se&#58;municipality]]:lang:project",
			Statistics::makeIdxString( $idx )
		);
	}

	public function test_invertIdxString() {
		$idx = "country:municipality:lang:project";
		$this->assertEquals(
			[ 'country','municipality','lang','project' ],
			Statistics::invertIdxString( $idx )
		);
	}

	public function test_invertIdxString_colon() {
		$idx = "country:[[se&#58;municipality]]:lang:project";
		$this->assertEquals(
			[ 'country','[[se:municipality]]','lang','project' ],
			Statistics::invertIdxString( $idx )
		);
	}

}
