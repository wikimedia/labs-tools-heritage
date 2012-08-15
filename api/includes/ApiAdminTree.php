<?php

if ( get_magic_quotes_gpc() ) {
	die( 'Magic quotes are enabled!' );
}

/**
 * Definition of AdminTree API
 * @author Arthur Richards <arichards@wikimedia.org>
 */
class ApiAdminTree extends ApiBase {
	private $country;

	public function __construct() {
		$this->setTopLevelNodeName( 'admin_levels' );
		$this->setObjectNodeName( 'admin_level' );
	}

	public function getAllowedParams() {
		$defaultParams = $this->getDefaultAllowedParams();

		$params = array(
			'admtree' => array(
				ApiBase::PARAM_DFLT => false,
				ApiBase::PARAM_TYPE => 'string',
			),
			'admlang' => array(
				ApiBase::PARAM_DFLT => false,
				ApiBase::PARAM_TYPE => 'string',
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

	protected function getCountry() {
		return $this->country;
	}

	/**
	 * Display admin tree data based on a supplied query
	 *
	 * With no params, this will return just the top level
	 * adm names.
	 */
	public function adminlevels() {
		$admtree = $this->getParam( 'admtree' );
		$display_fields = array( 'name' );

		if ( $admtree ) {
			$display_fields[] = 'level';
			$admintree_array = explode( "|", $admtree );
			$this->country = $admintree_array[0];
			$data = $this->getChildrenFromTree( $this->getUseLang(), $admintree_array );
		} else {
			$data = $this->getTopLevelAdmNames();
		}

		$this->getFormatter()->output( $data, 999999999, null, $display_fields, null );
	}

	/**
	 * Fetch ResultWrapper object of adm details for an adm zone
	 *
	 * @param string $lang Language code
	 * @param string $name The name of the adm zone to look up
	 * @param bool|int $level The adm level of the adm zone to look up
	 * @param bool|int $parent The parent ID to ensure for the adm zone to look up
	 *
	 * @return array
	 */
	private function getAdmDetails( $lang, $name, $level=false, $parent=false ) {
		$data = array();
		$db = Database::getDb();
		$fields = array( 'id', 'name', 'level' );
		$where = array( 'name' => $name, 'lang' => $lang );
		if ( $level !== false ) {
			$where['level'] = $level;
		}
		if ( $parent !== false ) {
			$where['parent'] = $parent;
		}
		$res = $db->select( $fields, 'admin_tree', $where );
		while ( $row = $db->fetchAssoc( $res ) ) {
			$data[] = $row;
		}
		return $data;
	}

	/**
	 * Fetches top-most admin tree item names (countries)
	 *
	 * @return array
	 */
	private function getTopLevelAdmNames() {
		$data = array();
		$db = Database::getDb();
		// get a list of countries
		$res = new ResultWrapper( $db, $db->query( 'SELECT `id`, `name` FROM `admin_tree` WHERE `level` = 0 GROUP BY `name`' ) );
		while( $row = $db->fetchAssoc( $res ) ) {
			$data[] = $row;
		}
		return $data;
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
		while ( $row = $db->fetchAssoc( $res ) ) {
			$data[] = $row;
		}
		return $data;
	}

	/**
	 * Fetches admin zone children for a given admin zone tree
	 *
	 * 'admin zone tree' referes to a given tree of... adimn zones, like
	 *   us -> us-ca -> Solano County, California
	 *
	 * This is a little more complex than you might think it needs to be,
	 * but to prevent dupes and false information, we need to walk the
	 * three from top to bottom to make sure we have the correct zone
	 * associations and ids.
	 *
	 * @param string $lang Language code
	 * @param array $admtree An array of admin zones - level => zone
	 *
	 * @return array
	 */
	private function getChildrenFromTree( $lang, array $admtree ) {
		$data = array();
		$tree_depth = count( $admtree );

		// get the topmost level details
		$adm0_name = $admtree[0];
		$adm0_details = $this->getAdmDetails( $lang, $adm0_name, 0 );
		if ( !count( $adm0_details ) ) {
			// could not find the toplevel zone
			return $data;
		}
		$parent_id = $adm0_details[0]['id'];

		// determine the id of the bottom-most requested zone
		if ( $tree_depth > 1 ) {
			for ( $i=1; $i < $tree_depth; $i++ ) {
				$adm_name = $admtree[$i];
				$adm_details = $this->getAdmDetails( $lang, $adm_name, $i, $parent_id );
				if ( !count( $adm_details ) ) {
					// there's are no child zones
					return $data;
				} elseif ( count( $adm_details ) > 1 ) {
					$parent_id = array();
					foreach ( $adm_details as $adm_detail ) {
						$parent_id[] = $adm_detail['id'];
					}
				} else {
					$parent_id = $adm_details[0]['id'];
				}
			}
		}

		// get the admin zones who's parent id is the id of the bottom-most requested zone
		$data = $this->getImmediateAdminLevelChildren( $parent_id );
		return $data;
	}
}