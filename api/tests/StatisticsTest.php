<?php

require(dirname(__FILE__).'/../includes/StatisticsBase.php');
require(dirname(__FILE__).'/../includes/Statistics.php');

class StatisticsTest extends PHPUnit_Framework_TestCase
{

	public function test_makeIdx()
	{
		$row = array('country','municipality','lang','project');
		$this->assertEquals(
			"country:municipality:lang:project",
			Statistics::makeIdx($row)
		);
	}

	public function test_makeIdx_colon()
	{
		$row = array('country','[[se:municipality]]','lang','project');
		$this->assertEquals(
			"country:[[se&#58;municipality]]:lang:project",
			Statistics::makeIdx($row)
		);
	}

	public function test_invertIdx()
	{
		$idx = "country:municipality:lang:project";
		$this->assertEquals(
			array('country','municipality','lang','project'),
			Statistics::invertIdx($idx)
		);
	}

	public function test_invertIdx_colon()
	{
		$idx = "country:[[se&#58;municipality]]:lang:project";
		$this->assertEquals(
			array('country','[[se:municipality]]','lang','project'),
			Statistics::invertIdx($idx)
		);
	}

}
?>
