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

		$params = array(
			'country' => array(
				ApiBase::PARAM_DFLT => false,
				ApiBase::PARAM_TYPE => 'string',
			),
			'id' => array(
				ApiBase::PARAM_DFLT => false,
				ApiBase::PARAM_TYPE => 'string',
			),
			'width' => array(
				 ApiBase::PARAM_DFLT => 220,
				 ApiBase::PARAM_TYPE => 'integer',
				 ApiBase::PARAM_MIN => 1,
				 ApiBase::PARAM_MAX => 9999999999,
			),
		);
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
		$display_fields = array( 'country', 'id', 'img_name', 'img_thumb', 'img_page');
		
		$country = $this->getParam( "country" );
		$id = $this->getParam( "id" );
		$width = $this->getParam( "width" );
		$limit = $this->getParam( "limit" );
		
		$data = array();
		$db = Database::getDb();
		$fields = array( 'country', 'id', 'img_name' );

		// FIXME: Escaping?
		$where = array( 'country' => $country, 'id' => $id );
		
		$res = $db->select( $fields, 'image', $where );
		while ( $row = $db->fetchAssoc( $res ) ) {
			$this->imageLinksRow( $row, $width );
			$data[] = $row;
		}
		// FIXME: Implement the paging
		$continueKey = null;
		$this->getFormatter()->output( $data, $limit, $continueKey, $display_fields, null );
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
