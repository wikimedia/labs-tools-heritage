<?php

require(dirname(__FILE__).'/../includes/CommonFunctions.php');

class CommonFunctionsTest extends \PHPUnit\Framework\TestCase
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

	public function test_processWikitext_makelinks_multilingual_commons()
	{
		$this->assertEquals(
			'Lorem <a href="//commons.wikimedia.org/wiki/Ipsum">Ipsum</a> Dolor',
			processWikitext('en', 'Lorem [[Ipsum]] Dolor', True, 'commons')
		);
	}

	public function test_processWikitext_makelinks_multilingual_wikidata()
	{
		$this->assertEquals(
			'Lorem <a href="//www.wikidata.org/wiki/Ipsum">Ipsum</a> Dolor',
			processWikitext('en', 'Lorem [[Ipsum]] Dolor', True, 'wikidata')
		);
	}

	public function test_getImageFromCommons_encodes_filename()
	{
		$this->assertEquals(
			'//upload.wikimedia.org/wikipedia/commons/thumb/c/c8/a%22_onerror%3D%22x.jpg/100px-a%22_onerror%3D%22x.jpg',
			getImageFromCommons('a" onerror="x.jpg', 100)
		);
	}

	public function test_getImageFromCommons_encodes_non_ascii_filename_and_size()
	{
		// The hash is taken from the unencoded name, as Commons does
		$md5 = md5('Église_x.jpg');
		$this->assertEquals(
			"//upload.wikimedia.org/wikipedia/commons/thumb/{$md5[0]}/{$md5[0]}{$md5[1]}/%C3%89glise_x.jpg/100px-%C3%89glise_x.jpg",
			getImageFromCommons('Église x.jpg', '100" onerror="y')
		);
	}

	public function test_processWikitext_makelinks_keeps_entities()
	{
		$this->assertEquals(
			'A&nbsp;<a href="//fr.wikipedia.org/wiki/B">B</a> &lt;i&gt; &amp; C',
			processWikitext('fr', 'A&nbsp;[[B]] &lt;i&gt; & C', True)
		);
	}

	public function test_processWikitext_makelinks_keeps_entities_in_label()
	{
		$this->assertEquals(
			'<a href="//fr.wikipedia.org/wiki/X">3&ndash;5</a>',
			processWikitext('fr', '[[X|3&ndash;5]]', True)
		);
	}

	public function test_processWikitext_makelinks_escapes_text()
	{
		$this->assertEquals(
			'Lorem &lt;b&gt;&amp; <a href="//fr.wikipedia.org/wiki/Ipsum">Ipsum</a> &lt;/b&gt;',
			processWikitext('fr', 'Lorem <b>& [[Ipsum]] </b>', True)
		);
	}

	public function test_processWikitext_makelinks_escapes_label()
	{
		$this->assertEquals(
			'Kerk <a href="//nl.wikipedia.org/wiki/X">&lt;img src=x onerror=alert(1)&gt;</a>',
			processWikitext('nl', 'Kerk [[X|<img src=x onerror=alert(1)>]]', True)
		);
	}

	public function test_processWikitext_makelinks_encodes_target()
	{
		$this->assertEquals(
			'<a href="//fr.wikipedia.org/wiki/A%22%3E%3Cb%3E">A&quot;&gt;&lt;b&gt;</a>',
			processWikitext('fr', '[[A"><b>]]', True)
		);
	}

	public function test_processWikitext_makelinks_decodes_entities_in_target()
	{
		$this->assertEquals(
			'<a href="//fr.wikipedia.org/wiki/A%20%26%20B">A &amp; B</a>',
			processWikitext('fr', '[[A &amp; B]]', True)
		);
	}

	public function test_processWikitext_makelinks_several_links()
	{
		$this->assertEquals(
			'<a href="//fr.wikipedia.org/wiki/A">A</a>, <a href="//fr.wikipedia.org/wiki/B">C</a>',
			processWikitext('fr', '[[A]], [[B|C]]', True)
		);
	}

	public function test_processWikitext_nolinks_several_links()
	{
		$this->assertEquals(
			'A, C',
			processWikitext('fr', '[[A]], [[B|C]]', False)
		);
	}

	public function test_processWikitext_makelinks_keeps_unmatched_brackets()
	{
		$this->assertEquals(
			'a [b] [[c',
			processWikitext('fr', 'a [b] [[c', True)
		);
	}

	public function test_processWikitext_makelinks_substitutes_invalid_utf8()
	{
		$this->assertEquals(
			"Caf\u{FFFD} <a href=\"//fr.wikipedia.org/wiki/A\">A</a>",
			processWikitext('fr', "Caf\xe9 [[A]]", True)
		);
	}

	public function test_processWikitext_makelinks_keeps_line_breaks()
	{
		$this->assertEquals(
			'A<br />B<br />C<br />D<br />E',
			processWikitext('fr', 'A<br>B<br/>C<BR />D</br>E', True)
		);
	}

	public function test_processWikitext_nolinks_line_breaks_become_spaces()
	{
		$this->assertEquals(
			'A B C',
			processWikitext('fr', 'A <br />B<br>C', False)
		);
	}

	public function test_processWikitext_nolinks_does_not_escape()
	{
		// Callers escape the plain text for the context they put it in
		$this->assertEquals(
			'<b> Ipsum',
			processWikitext('fr', '<b> [[Ipsum]]', False)
		);
	}

	public function test_matchWikiprojectLink_no_match()
	{
		$input = 'not-a-link';
		// $this->setExpectedException('Exception');  // present in phpUnit 4.8
		// $this->expectException('Exception');  // present in phpUnit 5.2+
		$this->expectExceptionMessage('No project link in text.');  // present in phpUnit 5.2+
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

	public function test_matchWikidataLink_no_match()
	{
		$input = 'not-a-link';
		// $this->setExpectedException('Exception');  // present in phpUnit 4.8
		// $this->expectException('Exception');  // present in phpUnit 5.2+
		$this->expectExceptionMessage('The provided url was not a wikidata link.');  // present in phpUnit 5.2+
		matchWikidataLink( $input );
	}

	public function test_matchWikidataLink_entity()
	{
		$input = "https://www.wikidata.org/entity/Q5943";
		$expected = Array(
			"https://www.wikidata.org/entity/Q5943",
			"https:",
			"www.wikidata.org/entity/Q5943",
			"www",
			"wikidata",
			"Q5943"
			);
		$this->assertEquals($expected, matchWikidataLink($input));
	}

	public function test_matchWikidataLink_wikipage()
	{
		$input = "https://www.wikidata.org/wiki/Q5943";
		$expected = Array(
			"https://www.wikidata.org/wiki/Q5943",
			"https:",
			"www.wikidata.org/wiki/Q5943",
			"www",
			"wikidata",
			"Q5943"
			);
		$this->assertEquals($expected, matchWikidataLink($input));
	}

	public function test_matchWikidataLink_http()
	{
		$input = "http://www.wikidata.org/entity/Q5943";
		$expected = Array(
			"http://www.wikidata.org/entity/Q5943",
			"http:",
			"www.wikidata.org/entity/Q5943",
			"www",
			"wikidata",
			"Q5943"
			);
		$this->assertEquals($expected, matchWikidataLink($input));
	}

	public function test_matchWikidataLink_no_protocol()
	{
		$input = "//www.wikidata.org/entity/Q5943";
		$expected = Array(
			"//www.wikidata.org/entity/Q5943",
			"",
			"www.wikidata.org/entity/Q5943",
			"www",
			"wikidata",
			"Q5943"
			);
		$this->assertEquals($expected, matchWikidataLink($input));
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
