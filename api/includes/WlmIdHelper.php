<?php

/**
 * External API wrapper
 * @author Nuno Tavares <nuno.tavares@wikimedia.pt>
 */

class WlmIdHelper extends ExternalAPI {
	static $wlmids = [
		'Portugal' => 'WLM-PT',
		];

	function parseWlmId( $img, $country ) {
		$text = $this->getPageText( 'File:' . $img );
		if ( !$text ) {
			return false;
		}
		// $this->debug(' + TPL for '.$country.': '.$tpl);
		if ( !isset( self::$wlmids[$country] ) ) {
			return false;
		}
		$matches = [];
		if ( !preg_match_all( '/\{\{' . self::$wlmids[$country] . '\|([^\|\}]+)/', $text, $matches ) ) {
			return false;
		}
		if ( !isset( $matches[1][0] ) ) {
			return false;
		}
		return $matches[1][0];
	}
}
