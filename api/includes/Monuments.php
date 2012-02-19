<?php

/**
 * Basic configuration for monuments
 */
class Monuments {
	
	static $dbServer = 'sql.toolserver.org';
	static $dbUser = 'erfgoed';
	static $dbDatabase = 'p_erfgoed_p';
	static $dbTable = 'monuments_all';
	
	static $dbFields = array( 'country', 'lang', 'id', 'name', 'address', 'municipality', 
'lat', 'lon', 'image', 'source', 'monument_article', 'changed' );

	static $dbPrimaryKey = array( 'country', 'lang', 'id' );
}
