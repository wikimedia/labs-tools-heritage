<?php

require_once ( __DIR__.'/../includes/FormatBase.php' );
require ( __DIR__.'/../includes/FormatWikitable.php' );

class FormatWikitableTest extends PHPUnit_Framework_TestCase
{

	public function test_prettifyUrls_nomatch() {

		$input = 'not-a-link';
		$this->assertEquals( 'not-a-link', FormatWikitable::prettifyUrls( $input ) );
	}

	public function test_prettifyUrls_match_plain() {

		$input = 'http://fr.wikipedia.org/w/index.php?title=some_title&oldid=00000';
		$expected = '[//fr.wikipedia.org/w/index.php?title=some_title&amp;oldid=00000 fr: some title]';
		$this->assertEquals( $expected, FormatWikitable::prettifyUrls( $input ) );
	}

	public function test_prettifyUrls_match_encoded() {

		$input = 'http://sv.wikipedia.org/w/index.php?title=ö&oldid=00000';
		$expected = '[//sv.wikipedia.org/w/index.php?title=%C3%B6&amp;oldid=00000 sv: ö]';
		$this->assertEquals( $expected, FormatWikitable::prettifyUrls( $input ) );
	}

	public function test_genImage_empty() {

		$this->assertEquals( '', FormatWikitable::genImage( '' ) );
	}

	public function test_genImage_value() {

		$input = 'Example.jpg';
		$expected = '[[File:Example.jpg|100px]]';
		$this->assertEquals( $expected, FormatWikitable::genImage( $input ) );
	}

}
