<?php

if ( get_magic_quotes_gpc() ) {
	die( 'Magic quotes are enabled!' );
}

/**
 * Definition of AdminTree API
 * @author Arthur Richards <arichards@wikimedia.org>
 */
class ApiAdminTree extends ApiBase {

	public function __construct() {
		$this->setTopLevelNodeName( 'admin_levels' );
		$this->setObjectNodeName( 'admin_level' );
	}

	public function getAllowedParams() {
		$defaultParams = $this->getDefaultAllowedParams();

		$params = array(
			'admlevel' => array(
				ApiBase::PARAM_MIN => 0,
				ApiBase::PARAM_MAX => 4,
				ApiBase::PARAM_DFLT => 0,
				ApiBase::PARAM_TYPE => 'integer',
			),
			'admval' => array(
				ApiBase::PARAM_DFLT => false,
				ApiBase::PARAM_TYPE => 'string',
			),
			'admid' => array(
				ApiBase::PARAM_DFLT => false,
				ApiBase::PARAM_TYPE => 'integer',
				ApiBase::PARAM_MIN => 1,
				ApiBase::PARAM_MAX => 999999999,
			),
		);
		$params = array_merge_recursive( $defaultParams, $params );
		return $params;
	}

	function executeModule() {
		switch ( $this->getParam( 'action' ) ) {
			case 'adminlevels':
				$this->adminlevels();
				break;
			case 'help':
			default:
				ApiBase::help();
				break;
		}
	}

	public function adminlevels() {
		$admval = $this->getParam( 'admval' );
		$admlevel = $this->getParam( 'admlevel' );
		$admid = $this->getParam( 'admid' );
		$db = Database::getDb();

		if ( $admlevel === 0 && $admval === false && $admid === false) {
			$this->getTopLevelAdmNames();
			return;
		} elseif ( $admid ) {
			if ( $admval || $admlevel ) {
				$this->error( 'You may not specify admval or admlevel with admid.' );
			}
			$this->getAdmById( $admid );
			return;
		} elseif ( $admval === false ) {
			$this->error( 'You must specify a value for admval.' );
		}

		$fields = array( 'id', 'name', 'level' );
		$where = array(
			'name' => $admval,
			'level' => $admlevel,
		);
		$res = $db->select( $fields, 'admin_tree', $where );
		if ( $row = mysql_fetch_object( $res->result ) ) {
			$data = $this->getImmediateAdminLevelChildren( $row->id, $row->level );
		} else {
			$data = array();
		}
		$this->getFormatter()->output( $data, 999999999, null, $fields, null );
	}

	/**
	 * Fetches an admin_tree row by id
	 *
	 * @return ResultWrapper
	 */
	private function getAdmById( $admid ) {
		$db = Database::getDb();
		$fields = array( 'id', 'name', 'level' );
		$where = array( 'id' => $admid );
		$res = $db->select( $fields, 'admin_tree', $where );
		$this->getFormatter()->output( $res, 999999999, null, $fields, null );
	}

	/**
	 * Fetches top-most admin tree item names (countries)
	 *
	 * @return ResultWrapper
	 */
	private function getTopLevelAdmNames() {
		$db = Database::getDb();
		// get a list of countries
		$fields = array( 'id', 'name' );
		$where = array(
			'level' => 0,
		);
		$res = $db->select( $fields, 'admin_tree', $where );
		$this->getFormatter()->output( $res, 999999999, null, $fields, null );
	}

	/**
	 * Fetches immediate children of a given admin_tree id
	 * @param int $id The id of the admin_tree item for which to fetch children
	 * @return array
	 */
	private function getImmediateAdminLevelChildren( $id ) {
		$data = array();
		$db = Database::getDb();
		$fields = array( 'id', 'name', 'level' );
		$where = array(
			'parent' => $id,
		);
 		$res = $db->select ( $fields, 'admin_tree', $where );
		while ( $row = mysql_fetch_object( $res->result ) ) {
			$data[] = array( 'id' => $row->id, 'name' => $row->name, 'level' => $row->level );
		}
		return $data;
	}
}