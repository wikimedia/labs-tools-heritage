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
				ApiBase::PARAM_TYPE => Monuments::$dbFields, ApiBase::PARAM_ISMULTI => true ),
    		'format' => array( ApiBase::PARAM_DFLT => 'xmlfm', 
    			ApiBase::PARAM_TYPE => array( 'kml', 'gpx', 'poi', 'html', 'layar', 'json', 'xml', 'xmlfm' ) ),
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
				$where[] = $db->escapeIdentifier( $field ) . ' LIKE ' .
					$db->quote( $value );
			} else {
				$where[] = $db->escapeIdentifier( $field ) . '=' . $db->quote( $value );
			}
		}
        
        //for kml get only monuments with coordinates
        if ($this->getParam('format') == 'kml') {
            $where[] = 'lat<>0 AND lon<>0';
        }
		
		$limit = $this->getParam( 'limit' );
		
		$res = $db->select( array_merge( Monuments::$dbPrimaryKey, $this->getParam( 'props' ) ), Monuments::$dbTable, $where, Monuments::$dbPrimaryKey, $limit + 1 );
		$this->getFormatter()->output( $res, $limit, 'srcontinue', $this->getParam( 'props' ), Monuments::$dbPrimaryKey );
	}
	
	function statistics() {
		// TODO: Code me
		echo "Provide some statistics code here, please\n";
	}
    
	function help() {
		/* TODO: Expand me! */
		echo '
<html>
<head>
	<title>Monuments API</title>
</head>
<body>
<pre>
  
  
  <b>******************************************************************************************</b>
  <b>**                                                                                      **</b>
  <b>**              This is an auto-generated Monuments API documentation page              **</b>
  <b>**                                                                                      **</b>
  <b>**                            Documentation:                                            **</b>
  **      <a href="http://commons.wikimedia.org/wiki/Commons:Wiki_Loves_Monuments_2011/Tools#Search_and_export_tool">http://commons.wikimedia.org/wiki/Commons:Wiki_Loves_Monuments_2011/Tools#Search_and_export_tool</a>                        **
  <b>**                                                                                      **</b>
  <b>******************************************************************************************</b>
  
  
Parameters:
  format         - The format of the output
                   One value: kml, gpx, poi, html, layar, json, xml, xmlfm
                   Default: xmlfm
  action         - What action you would like to perform. 
                   One value: search, statistics, help
                   Default: help
                   
<b>*** *** *** *** *** *** *** *** *** ***  Modules  *** *** *** *** *** *** *** *** *** ***</b> 

<b>* action=search *</b>

Parameters:
  srcountry       - Search for monuments in country. Supply the country code.
  srlang          - Search for monuments in lang. Supply the language code.
  srid            - Search for id.
  srname          - Search for name.
  sraddress       - Search for address.
  srmunicipality  - Search for municipality.
  srlat           - Search for latitude.
  srlon           - Search for longitude.
  srimage         - Search for imagename in monument lists.
  srsource        - Search for source monument list wiki page.
  srchanged       - Search for changed.
  
Examples:
  <a href="api.php?action=search&amp;srname=%burgerhuizen%">api.php?action=search&amp;srname=%burgerhuizen%</a>
  <a href="api.php?action=search&amp;srcountry=fr&amp;srlang=ca">api.php?action=search&amp;srcountry=fr&amp;srlang=ca</a>

<b>*** *** *** *** *** *** *** *** *** ***  Formats  *** *** *** *** *** *** *** *** *** ***</b> 

<b>* format=xml *</b>
  Output data in XML format

Examples:
  <a href="api.php?action=search&amp;format=xml">api.php?action=search&amp;format=xml</a>
  
</pre>
</body>
</html>
        ';
	}    
}
