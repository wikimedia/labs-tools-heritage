<?php

/**
 * Base class for formatting
 * @author Platonides
 */
class FormatBase {
	protected $continueParams;
	
	function setContinueParams($params) {
		$this->continueParams = $params;
	}

	abstract function outputBegin($row);
	abstract function outputContinue($row, $continueKey, $primaryKey);
	abstract function outputRow($row);
	abstract function outputEnd($row);

	function output($result, $limit, $continueKey, $primaryKey) {
		$this->outputBegin();
		foreach ( $result as $row ) {
			if ( ++$count > $limit ) {
				$this->outputContinue( $row, $continueKey, $primaryKey );
			} else {
				$this->outputRow( $row );
			}
		}
		$this->outputEnd();
	}
}