<?php

require ( __DIR__.'/../includes/StatisticsBase.php' );
require ( __DIR__.'/../includes/Statistics.php' );

class StatisticsTest extends PHPUnit_Framework_TestCase
{

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
