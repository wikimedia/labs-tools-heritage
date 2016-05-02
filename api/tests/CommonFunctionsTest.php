<?php

require(dirname(__FILE__).'/../includes/CommonFunctions.php');

class CommonFunctionsTest extends PHPUnit_Framework_TestCase
{

    public function test_getImageFromCommons()
    {
        $this->assertEquals(
            getImageFromCommons('Example.jpg', 200),
            "//upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Example.jpg/200px-Example.jpg"
        );
    }

    public function test_processWikitext_empty()
    {
        $this->assertEquals(
            processWikitext('fr', '', True),
            ''
        );
    }

    public function test_processWikitext_nolinks_form_1()
    {
        $this->assertEquals(
            processWikitext('fr', 'Lorem [[Ipsum]] Dolor', False),
            'Lorem Ipsum Dolor'
        );
    }

    public function test_processWikitext_nolinks_form_2()
    {
        $this->assertEquals(
            processWikitext('fr', 'Lorem [[Ipsum|Sin amet]] Dolor', False),
            'Lorem Sin amet Dolor'
        );
    }

    public function test_processWikitext_makelinks_form_1()
    {
        $this->assertEquals(
            processWikitext('fr', 'Lorem [[Ipsum]] Dolor', True),
            'Lorem <a href="//fr.wikipedia.org/wiki/Ipsum">Ipsum</a> Dolor'
        );
    }

    public function test_processWikitext_makelinks_form_2()
    {
        $this->assertEquals(
            processWikitext('fr', 'Lorem [[Ipsum|Sin amet]] Dolor', True),
            'Lorem <a href="//fr.wikipedia.org/wiki/Ipsum">Sin amet</a> Dolor'
        );
    }

    public function test_replaceSpaces()
    {
        $this->assertEquals(
            replaceSpaces("a b c"),
            "a_b_c"
        );
    }

}
?>