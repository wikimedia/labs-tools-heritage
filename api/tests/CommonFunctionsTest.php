<?php

require(dirname(__FILE__).'/../includes/CommonFunctions.php');

class CommonFunctionsTest extends PHPUnit_Framework_TestCase
{

	public function test_getImageFromCommons()
	{
		$this->assertEquals(
			"//upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Example.jpg/200px-Example.jpg",
			getImageFromCommons('Example.jpg', 200)
		);
	}

	public function test_processWikitext_empty()
	{
		$this->assertEquals(
			'',
			processWikitext('fr', '', True)
		);
	}

	public function test_processWikitext_nolinks_form_1()
	{
		$this->assertEquals(
			'Lorem Ipsum Dolor',
			processWikitext('fr', 'Lorem [[Ipsum]] Dolor', False)
		);
	}

	public function test_processWikitext_nolinks_form_2()
	{
		$this->assertEquals(
			'Lorem Sin amet Dolor',
			processWikitext('fr', 'Lorem [[Ipsum|Sin amet]] Dolor', False)
		);
	}

	public function test_processWikitext_nolinks_wikiproject()
	{
		$this->assertEquals(
			'Lorem Ipsum Dolor',
			processWikitext('fr', 'Lorem [[Ipsum]] Dolor', False, 'wikivoyage')
		);
	}

	public function test_processWikitext_makelinks_form_1()
	{
		$this->assertEquals(
			'Lorem <a href="//fr.wikipedia.org/wiki/Ipsum">Ipsum</a> Dolor',
			processWikitext('fr', 'Lorem [[Ipsum]] Dolor', True)
		);
	}

	public function test_processWikitext_makelinks_form_2()
	{
		$this->assertEquals(
			processWikitext('fr', 'Lorem [[Ipsum|Sin amet]] Dolor', True),
			'Lorem <a href="//fr.wikipedia.org/wiki/Ipsum">Sin amet</a> Dolor'
		);
	}

	public function test_processWikitext_makelinks_wikiproject()
	{
		$this->assertEquals(
			'Lorem <a href="//fr.wikivoyage.org/wiki/Ipsum">Ipsum</a> Dolor',
			processWikitext('fr', 'Lorem [[Ipsum]] Dolor', True, 'wikivoyage')
		);
	}

	public function test_matchWikiprojectLink_no_match()
	{
		$input = 'not-a-link';
		$this->setExpectedException('Exception');  // present in phpUnit 4.8
		// $this->expectException('Exception');  // present in phpUnit 5.2+
		// $this->expectExceptionMessage('No project link in text.');  // present in phpUnit 5.2+
		matchWikiprojectLink( $input );
	}

	public function test_matchWikiprojectLink_match()
	{
		$input = 'https://fr.wikipedia.org/w/index.php?title=some_title&oldid=00000';
		$expected = Array(
			"https://fr.wikipedia.org/w/index.php?title=some_title&oldid=00000",
			"https:",
			"fr.wikipedia.org/w/index.php?title=some_title&oldid=00000",
			"fr",
			"wikipedia",
			"some_title",
			"00000"
			);
		$this->assertEquals($expected, matchWikiprojectLink($input));
	}

	public function test_matchWikiprojectLink_match_wikimedia()
	{
		$input = 'https://commons.wikimedia.org/w/index.php?title=some_title&oldid=00000';
		$expected = Array(
			"https://commons.wikimedia.org/w/index.php?title=some_title&oldid=00000",
			"https:",
			"commons.wikimedia.org/w/index.php?title=some_title&oldid=00000",
			"commons",
			"wikimedia",
			"some_title",
			"00000"
			);
		$this->assertEquals($expected, matchWikiprojectLink($input));
	}

	public function test_matchWikiprojectLink_match_with_hyphen()
	{
		$input = 'https://be-tarask.wikipedia.org/w/index.php?title=some_title&oldid=00000';
		$expected = Array(
			"https://be-tarask.wikipedia.org/w/index.php?title=some_title&oldid=00000",
			"https:",
			"be-tarask.wikipedia.org/w/index.php?title=some_title&oldid=00000",
			"be-tarask",
			"wikipedia",
			"some_title",
			"00000"
			);
		$this->assertEquals($expected, matchWikiprojectLink($input));
	}

	public function test_matchWikiprojectLink_match_with_unicode()
	{
		$input = 'https://sv.wikipedia.org/w/index.php?title=ö&oldid=00000';
		$expected = Array(
			"https://sv.wikipedia.org/w/index.php?title=ö&oldid=00000",
			"https:",
			"sv.wikipedia.org/w/index.php?title=ö&oldid=00000",
			"sv",
			"wikipedia",
			"ö",
			"00000"
			);
		$this->assertEquals($expected, matchWikiprojectLink($input));
	}

	public function test_urlencodeWikiprojectLink_without_unicode()
	{
		$input = Array(
			"https://fr.wikivoyage.org/w/index.php?title=Hello_World&oldid=00000",
			"https:",
			"fr.wikivoyage.org/w/index.php?title=Hello_World&oldid=00000",
			"fr",
			"wikivoyage",
			"Hello_World",
			"00000"
			);
		$expected = 'fr.wikivoyage.org/w/index.php?title=Hello_World&oldid=00000';
		$this->assertEquals($expected, urlencodeWikiprojectLink($input));
	}

	public function test_urlencodeWikiprojectLink_with_unicode()
	{
		$input = Array(
			"https://sv.wikipedia.org/w/index.php?title=ö&oldid=00000",
			"https:",
			"sv.wikipedia.org/w/index.php?title=ö&oldid=00000",
			"sv",
			"wikipedia",
			"ö",
			"00000"
			);
		$expected = 'sv.wikipedia.org/w/index.php?title=%C3%B6&oldid=00000';
		$this->assertEquals($expected, urlencodeWikiprojectLink($input));
	}

	public function test_urlencodeWikiprojectLink_drop_oldid()
	{
		$input = Array(
			"https://fr.wikivoyage.org/w/index.php?title=Hello_World&oldid=00000",
			"https:",
			"fr.wikivoyage.org/w/index.php?title=Hello_World&oldid=00000",
			"fr",
			"wikivoyage",
			"Hello_World",
			"00000"
			);
		$expected = 'fr.wikivoyage.org/w/index.php?title=Hello_World';
		$this->assertEquals($expected, urlencodeWikiprojectLink($input, true));
	}

	public function test_replaceSpaces()
	{
		$this->assertEquals(
			"a_b_c",
			replaceSpaces("a b c")
		);
	}

	public function test_matchWikidataQid_no_match()
	{
		$input = 'not-a-link';
		$this->setExpectedException('Exception');  // present in phpUnit 4.8
		// $this->expectException('Exception');  // present in phpUnit 5.2+
		// $this->expectExceptionMessage('The provided url was not a wikidata link.');  // present in phpUnit 5.2+
		matchWikidataQid( $input );
	}

	public function test_matchWikidataQid_entity()
	{
		$input = "https://www.wikidata.org/entity/Q5943";
		$expected = Array(
			"https://www.wikidata.org/entity/Q5943",
			"https:",
			"www.wikidata.org/entity/Q5943",
			"entity",
			"Q5943"
			);
		$this->assertEquals($expected, matchWikidataQid($input));
	}

	public function test_matchWikidataQid_wikipage()
	{
		$input = "https://www.wikidata.org/wiki/Q5943";
		$expected = Array(
			"https://www.wikidata.org/wiki/Q5943",
			"https:",
			"www.wikidata.org/wiki/Q5943",
			"wiki",
			"Q5943"
			);
		$this->assertEquals($expected, matchWikidataQid($input));
	}

	public function test_matchWikidataQid_http()
	{
		$input = "http://www.wikidata.org/entity/Q5943";
		$expected = Array(
			"http://www.wikidata.org/entity/Q5943",
			"http:",
			"www.wikidata.org/entity/Q5943",
			"entity",
			"Q5943"
			);
		$this->assertEquals($expected, matchWikidataQid($input));
	}

	public function test_matchWikidataQid_no_protocol()
	{
		$input = "//www.wikidata.org/entity/Q5943";
		$expected = Array(
			"//www.wikidata.org/entity/Q5943",
			"",
			"www.wikidata.org/entity/Q5943",
			"entity",
			"Q5943"
			);
		$this->assertEquals($expected, matchWikidataQid($input));
	}

	public function test_makeWikidataUrl()
	{
		$this->assertEquals(
			"https://www.wikidata.org/wiki/Q5943",
			makeWikidataUrl("Q5943")
		);
	}

	public function test_makeWikidataUrl_empty_returns_empty_string()
	{
		$this->assertEquals(
			"",
			makeWikidataUrl("")
		);
	}

	public function test_makeWikidataWikilink()
	{
		$this->assertEquals(
			"[[d:Q5943]]",
			makeWikidataWikilink("Q5943")
		);
	}

	public function test_makeWikidataWikilink_empty_returns_empty_string()
	{
		$this->assertEquals(
			"",
			makeWikidataWikilink("")
		);
	}

	public function test_makeHTMLlink_with_one_argument_uses_the_url_as_text() {
		$input = 'http://example.com';
		$expected = '<a href="http://example.com">http://example.com</a>';
		$this->assertEquals( $expected, makeHTMLlink( $input ) );
	}

	public function test_makeHTMLlink_two_arguments() {
		$input1 = 'http://example.com';
		$input2 = 'Example';
		$expected = '<a href="http://example.com">Example</a>';
		$this->assertEquals( $expected, makeHTMLlink( $input1, $input2 ) );
	}

	public function test_makeCommonsCatUrl()
	{
		$this->assertEquals(
			"https://commons.wikimedia.org/wiki/Category:Foreground flowers",
			makeCommonsCatUrl("Foreground flowers")
		);
	}

	public function test_makeCommonsCatUrl_empty_returns_empty_string()
	{
		$this->assertEquals(
			"",
			makeCommonsCatUrl("")
		);
	}

	public function test_makeCommonsCatWikilink()
	{
		$this->assertEquals(
			"[[c:Category:Foreground flowers]]",
			makeCommonsCatWikilink("Foreground flowers")
		);
	}

	public function test_makeCommonsCatWikilink_empty_returns_empty_string()
	{
		$this->assertEquals(
			"",
			makeCommonsCatWikilink("")
		);
	}
}
?>
