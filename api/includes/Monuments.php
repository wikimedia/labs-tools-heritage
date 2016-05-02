<?php

/**
 * Basic configuration for monuments
 */
class Monuments {
	static $dbTable = 'monuments_all';

	static $dbFields = array(
		'country', 'lang', 'project', 'id', 'adm0', 'adm1', 'adm2', 'adm3',
		'adm4', 'name', 'address', 'municipality', 'lat', 'lon', 'image',
		'commonscat', 'source', 'monument_article', 'registrant_url', 'changed'
	);

	static $dbPrimaryKey = array( 'country', 'lang', 'id' );
}
