<?php

/**
 * Base class for formatting
 * @author Platonides
 */
abstract class FormatBase {
	protected $continueParams;
	
	function setContinueParams($params) {
		$this->continueParams = $params;
	}

	function headers() {
		header( "Content-Type: " . $this->getContentType() );
	}

	abstract function getContentType();
	abstract function outputBegin();
	abstract function outputContinue($row, $continueKey, $primaryKey);
	abstract function outputRow($row, $selectedItems);
	abstract function outputEnd();

	function output($result, $limit, $continueKey, $selectedItems, $primaryKey) {
		$this->headers();
		
		$this->outputBegin();
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
}
