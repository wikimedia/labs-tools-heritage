<?php

/**
 * Base class for formatting
 * @author Platonides
 */
abstract class FormatBase {
	
	protected $api;
	protected $continueParams;
	
	function __construct(ApiBase $api) {
		$this->api = $api;
	}
	
	function setContinueParams($params) {
		$this->continueParams = $params;
	}

	function headers() {
		header( "Content-Type: " . $this->getContentType() );
	}

	abstract function getContentType();
	abstract function outputBegin($selectedItems);
	abstract function outputContinue($row, $continueKey, $primaryKey);
	abstract function outputRow($row, $selectedItems);
	abstract function outputEnd();

	function output($result, $limit, $continueKey, $selectedItems, $primaryKey) {
		$this->headers();
		
		$this->outputBegin( $selectedItems );
        $count = 0;
		foreach ( $result as $row ) {
			if ( ++$count > $limit ) {
				$this->outputContinue( $row, $continueKey, $primaryKey );
			} else {
				$this->outputRow( $row, $selectedItems );
			}
		}
		$this->outputEnd();
	}

	/**
	 * @param array|string $errors: Error message or array of them
	 */
	function outputErrors( $errors ) {
		// Does nothing by default because not every format has the means of reporting errors
	}
}
