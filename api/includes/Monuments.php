<?php

/**
 * Basic configuration for monuments
 */
class Monuments {
	static $dbTable = 'monuments_all';

	static $dbFields = [
		'country', 'lang', 'project', 'id', 'adm0', 'adm1', 'adm2', 'adm3',
		'adm4', 'name', 'address', 'municipality', 'lat', 'lon', 'image',
		'commonscat', 'source', 'monument_article', 'wd_item', 'registrant_url',
		'changed'
	];

	static $dbPrimaryKey = [ 'country', 'lang', 'id' ];
}
