<?php

if ( get_magic_quotes_gpc() ) {
	die( 'Magic quotes are enabled!' );
}

/**
 * Definition of Monuments API
 * @author Platonides
 */
class ApiMonuments extends ApiBase {

	protected function getParamDescription() {
		return array(
			/* FIXME: Copy from http://etherpad.wikimedia.org/WLM-tech*/
		);
	}
	
	function getAllowedParams() {
    	$params = array(
    		'props' => array( ApiBase::PARAM_DFLT => Monuments::$dbFields,
				ApiBase::PARAM_TYPE => Monuments::$dbFields ),
    		'format' => array( ApiBase::PARAM_DFLT => 'xmlfm', 
    			ApiBase::PARAM_TYPE => array( 'kml', 'gpx', 'poi', 'html', 'layar', 'json', 'xml', 'xmlfm' ) ),
    		'action' => array( ApiBase::PARAM_DFLT => 'help',
    			ApiBase::PARAM_TYPE => array( 'search', 'statistics', 'help' ) ),
    		'callback' => array( ApiBase::PARAM_TYPE => 'callback' ),
    		'limit' => array( ApiBase::PARAM_MIN => 0, ApiBase::PARAM_MAX => 200, 
				ApiBase::PARAM_DFLT => 100, ApiBase::PARAM_TYPE => 'integer' ),
    			
    		'action' => array( ApiBase::PARAM_DFLT => 'help', 
    			ApiBase::PARAM_TYPE => array( 'help', 'search', 'statistics' ) ),
    			
    		'srquery' => array( ApiBase::PARAM_DFLT => false, ApiBase::PARAM_TYPE => 'string' ),
    		'srcontinue' => array( ApiBase::PARAM_DFLT => false, ApiBase::PARAM_TYPE => 'string' ),
    	);
    	
    	foreach ( Monuments::$dbFields as $field ) {
			$params["sr$field"] = array( ApiBase::PARAM_DFLT => false, ApiBase::PARAM_TYPE => 'string' );
			$params["srwith$field"] = array( ApiBase::PARAM_DFLT => false, ApiBase::PARAM_TYPE => 'boolean' );
			$params["srwithout$field"] = array( ApiBase::PARAM_DFLT => false, ApiBase::PARAM_TYPE => 'boolean' );
		}
		
		return $params;
	}
	
	function execute() {
		switch ( $this->getParam( 'action' ) ) {
			case 'help':
				$this->help();
				break;
			case 'search':
				$this->search();
				break;
			case 'statistics':
				$this->statistics();
		}
	}
	
	function search() {
		$where = array();
		$db = Database::getDb();
		
		$continue = $this->getParam( 'srcontinue' );
		if ( $continue ) {
			$v = explode( '|', $continue );
			for ( $i = 0; $i < count( Monuments::$dbPrimaryKey ); $i++ ){
				 $where[] = $db->escapeIdentifier( Monuments::$dbPrimaryKey[$i] ) . '>=' . 
				 	$db->quote( rawurldecode( $v[$i] ) );
			}
		}
		
		foreach ( Monuments::$dbFields as $field ) {
			if ( $this->getParam( "srwith$field" ) ) {
				$where[] = $db->escapeIdentifier( $field ) . ' IS NOT NULL';
			}
			if ( $this->getParam( "srwithout$field" ) ) {
				$where[] = $db->escapeIdentifier( $field ) . ' IS NULL';
			}
		}
		foreach ( Monuments::$dbFields as $field ) {
			$value = $this->getParam( "sr$field" );
			if ( $value === false ) continue;
			
			if ( strpos( $value, '%' ) !== false ) {
				$where[] = "'" . $db->escapeIdentifier( $field ) . '\' LIKE ' .
					$db->quote( $field );
			} else {
				$where[] = $db->escapeIdentifier( $field ) . '=' . $db->quote( $field );
			}
		}
		
		$limit = $this->getParam( 'limit' );
		
		$res = $db->select( $this->getParam( 'props' ), Monuments::$dbTable, $where, Monuments::$dbPrimaryKey, $limit + 1 );
		$this->getFormatter()->output( $res, $limit, 'srcontinue', Monuments::$dbPrimaryKey );
	}
	
	function statistics() {
		// TODO: Code me
		echo "Provide some statistics code here, please\n";
	}
}
