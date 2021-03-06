<?php

/**
 * Definition of Images API
 * @author Maarten Dammers (multichill)
 */
class ApiImages extends ApiBase {

	public function __construct() {
		$this->setTopLevelNodeName( 'images' );
		$this->setObjectNodeName( 'image' );
	}

	public function getAllowedParams() {
		$defaultParams = $this->getDefaultAllowedParams();

		$params = [
			'imcountry' => [
				ApiBase::PARAM_DFLT => false,
				ApiBase::PARAM_TYPE => 'string',
			],
			'imid' => [
				ApiBase::PARAM_DFLT => false,
				ApiBase::PARAM_TYPE => 'string',
			],
			'imwidth' => [
				 ApiBase::PARAM_DFLT => 220,
				 ApiBase::PARAM_TYPE => 'integer',
				 ApiBase::PARAM_MIN => 1,
				 ApiBase::PARAM_MAX => 9999999999,
			 ],
			 'imcontinue' => [
				 ApiBase::PARAM_DFLT => '',
				 ApiBase::PARAM_TYPE => 'string',
			 ],
			 'props' => [
				 ApiBase::PARAM_DFLT => [ 'country', 'id', 'img_name' ],
				 ApiBase::PARAM_TYPE => [ 'country', 'id', 'img_name' ],
				 ApiBase::PARAM_ISMULTI => true ,
			 ],
		];
		$params = array_merge_recursive( $defaultParams, $params );
		return $params;
	}

	function executeModule() {
		switch ( $this->getParam( 'action' ) ) {
			case 'images':
				$this->images();
				break;
			case 'help':
			default:
				ApiBase::help();
				break;
		}
	}

	/**
	 * Display images based on country and id
	 *
	 */
	public function images() {
		// $display_fields = array( 'country', 'id', 'img_name', 'img_thumb', 'img_page');

		$country = $this->getParam( "imcountry" );
		$id = $this->getParam( "imid" );
		$width = $this->getParam( "imwidth" );
		$limit = $this->getParam( "limit" );
		$continue = $this->getParam( "imcontinue" );

		$db = Database::getDb();
		$fields = [ 'country', 'id', 'img_name' ];
		$props = $this->getParam( "props" );

		// FIXME: Escaping?
		$where = [ 'country' => $country, 'id' => $id ];

		$res = $db->select( $props, 'image', $where );
		$rows = [];
		while ( $row = $db->fetchAssoc( $res ) ) {
			$this->imageLinksRow( $row, $width );
			$rows[] = $row;
		}
		// FIXME: Implement the paging
		// $continueKey = null;
		$limit = 99999999;
		$primaryKey = [ 'country', 'id' ];
		$this->getFormatter()->output( $rows, $limit, 'continue', $props, $primaryKey );
	}
	/*
	 * Add a link to a thumbnail and to the image page
	 *
	 */
	private function imageLinksRow( &$row, $width ) {
		$row['img_thumb'] = 'http://commons.wikimedia.org/w/thumb.php?f=' . $row['img_name'] . '&width=' . $width;
		$row['img_page'] = 'https://commons.wikimedia.org/w/index.php?title=File:' . $row['img_name'];
	}
}
