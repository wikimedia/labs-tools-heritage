<?php

	//Read in the data from the remote server and wrap it with JASONP
	//$jsonData = getDataAsJson($_GET['symbol']);
	$jsonData = file_get_contents($_GET['url']);
	echo $_GET['callback'] . '(' . $jsonData . ');';


?> 
