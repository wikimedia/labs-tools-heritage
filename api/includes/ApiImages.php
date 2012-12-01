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
		$display_fields = array( 'country', 'id', 'img_name');
		
		// Escaping?
		$country = $this->getParam( "country" )
		$id = $this->getParam( "id" )
		
		$data = array();
		$db = Database::getDb();
		$fields = array( 'country', 'id' );
		$where = array( 'country' => $country, 'id' => $id );
		
		$res = $db->select( $fields, 'images', $where );
		while ( $row = $db->fetchAssoc( $res ) ) {
			$data[] = $row;
		}
		$continueKey = null
		$this->getFormatter()->output( $data, $limit, $continueKey, $display_fields, null );
	}
}