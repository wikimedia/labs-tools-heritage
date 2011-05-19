<?php

/**
 * Basic configuration for monuments
 */
class Monuments {
	
	static $dbServer = 'sql.toolserver.org';
	static $dbUser = 'erfgoed';
	static $dbTable = 'p_erfgoed_p';
	
	static $dbFields = array( 'country', 'lang', 'id', 'name', 'address', 'municipality', 
'lat', 'lon', 'image', 'source', 'changed' );

	static $dbPrimaryKey = array( 'country', 'lang', 'id' );
}
