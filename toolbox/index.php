<?php

/* Localization. */
require_once( '/home/project/i/n/t/intuition/ToolserverI18N/ToolStart.php' );

$opts = array(
    'domain' => 'MonumentsAPI', // name of your main text-domain here
    'globalfunctions' => true, // defines _(), _e() and _g() as shortcut for $I18N->msg( .. )
);
$I18N = new TsIntuition( $opts );

?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
    <title>Wiki Loves Monuments Toolbox</title>
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
    <link rel="stylesheet" type="text/css" href="css/default_css.css" />
    <link rel="shortcut icon" href="img/favicon.ico" type="image/x-icon"/>
</head>
<body>
    <div id="wrapper">
	<div id="header">
	    <a href="#"><img id="wlm-logo" src="img/logo-wiki-loves-monuments.png" width="80"  alt="Wiki loves monuments logo" /></a>
	    <h2>Wlm Toolbox</h2>
	    <h1>A set of tools related to <span>Wiki Loves Monuments</span></span></h1>  	 
	</div><!-- end header --> 
	<div id="maincontainer">
	    <div id="leftnav">
		<ul class="first">
		    <li><a href="#">Home</a>
		    <ul>
			<li><a href="statistics.php">Statistics</a></li>
			<li><a href="search.php">Search Form</a></li>
		    </ul>
		    </li>
		</ul>
	    </div><!-- end leftnav--> 
	    <div id="content">
		<h2>Home</h2>
		<p>this is only a starting point</p>
	    </div><!-- end content --> 
	</div><!-- end maincontainer --> 		
	<br style="clear:left;" />
    </div> <!-- end wrapper -->
</body>
</html>
