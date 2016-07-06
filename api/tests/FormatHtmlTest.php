<?php

require_once ( __DIR__.'/../includes/FormatBase.php' );
require ( __DIR__.'/../includes/FormatHtml.php' );

class FormatHtmlTest extends PHPUnit_Framework_TestCase
{

	public function test_prettifyUrls_nomatch() {

		$input = 'not-a-link';
		$this->assertEquals( 'not-a-link', FormatHtml::prettifyUrls( $input ) );
	}

	public function test_prettifyUrls_match_plain() {

		// checks http->https, '_' -> ' '
		$input = 'http://fr.wikipedia.org/w/index.php?title=some_title&oldid=00000';
		$expected = '<a href="https://fr.wikipedia.org/w/index.php?title=some_title&amp;oldid=00000">some title</a>';
		$this->assertEquals( $expected, FormatHtml::prettifyUrls( $input ) );
	}

	public function test_prettifyUrls_match_encoded() {

		$input = 'http://sv.wikipedia.org/w/index.php?title=%C3%B6&oldid=00000';
		$expected = '<a href="https://sv.wikipedia.org/w/index.php?title=%C3%B6&amp;oldid=00000">ö</a>';
		$this->assertEquals( $expected, FormatHtml::prettifyUrls( $input ) );
	}

	public function test_genImage_empty() {

		$this->assertEquals( '', FormatHtml::genImage( '' ) );
	}

	public function test_genImage_value() {

		$input = 'Example.jpg';
		$expected = '<a href="//commons.wikimedia.org/wiki/File:Example.jpg"><img src="' .
			'//upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Example.jpg/100px-Example.jpg' .
			'" /></a>';
		$this->assertEquals( $expected, FormatHtml::genImage( $input ) );
	}

	public function test_makeHTMLlink_with_one_argument_uses_the_url_as_text() {
		$input = 'http://example.com';
		$expected = '<a href="http://example.com">http://example.com</a>';
		$this->assertEquals( $expected, FormatHtml::makeHTMLlink( $input ) );
	}

	public function test_makeHTMLlink_two_arguments() {
		$input1 = 'http://example.com';
		$input2= 'Example';
		$expected = '<a href="http://example.com">Example</a>';
		$this->assertEquals( $expected, FormatHtml::makeHTMLlink( $input1, $input2 ) );
	}

}
