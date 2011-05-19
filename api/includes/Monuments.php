<?php

/**
 * Basic configuration for monuments
 */
class Monuments {
	
	static $dbServer = 'sql1-user';
	static $dbUser = 'erfgoed';
	static $dbTable = 'monuments_all';
	
	static $dbFields = array( 'country', 'lang', 'id', 'name', 'address', 'municipality', 
'lat', 'lon', 'image', 'source', 'changed' );

	static $dbPrimaryKey = array( 'country', 'lang', 'id' );
}
