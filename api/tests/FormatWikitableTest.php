<?php

require_once(dirname(__FILE__).'/../includes/FormatBase.php');
require(dirname(__FILE__).'/../includes/FormatWikitable.php');

class FormatWikitableTest extends PHPUnit_Framework_TestCase
{

    public function test_prettifyUrls_nomatch()
    {
        $input = 'not-a-link';
        $this->assertEquals(FormatWikitable::prettifyUrls($input), 'not-a-link');
    }

    public function test_prettifyUrls_match_plain()
    {
        $input = 'http://fr.wikipedia.org/w/index.php?title=some_title&oldid=00000';
        $output = '[//fr.wikipedia.org/w/index.php?title=some_title&amp;oldid=00000 fr: some title]';
        $this->assertEquals(FormatWikitable::prettifyUrls($input), $output);
    }

    public function test_prettifyUrls_match_encoded()
    {
        $input = 'http://sv.wikipedia.org/w/index.php?title=%C3%B6&oldid=00000';
        $output = '[//sv.wikipedia.org/w/index.php?title=%C3%B6&amp;oldid=00000 sv: ö]';
        $this->assertEquals(FormatWikitable::prettifyUrls($input), $output);
    }

    public function test_genImage_empty()
    {
        $this->assertEquals(FormatWikitable::genImage(''), '');
    }

    public function test_genImage_value()
    {
        $input = 'Example.jpg';
        $output = '[[File:Example.jpg|100px]]';
        $this->assertEquals(FormatWikitable::genImage($input), $output);
    }

}
?>
