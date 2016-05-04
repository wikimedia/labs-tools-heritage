<?php
error_reporting(E_ALL);
/**
 * HTML output type, based on XML. This output is for users (and not automated tools) so internationalization will be used.
 * @author Joancreus (jcreus), based on Platonides work 
 */
//functions: processWikitext, matchWikiprojectLink, getImageFromCommons
require_once('CommonFunctions.php');

class FormatHtml extends FormatBase {
	function getContentType() {
		return "text/html";
	}
	
	function headers() {
		parent::headers();
		echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">';
	}
	
	function linebreak() {
		echo "\n";
	}

	private $isTableOpen;
	
	function outputBegin($selectedItems) {
		echo '<html>';$this->linebreak();
		echo '<head>';$this->linebreak();
		echo '<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">';$this->linebreak();
		echo '<link media="all" type="text/css" href="jscss/style.css" rel="stylesheet">';$this->linebreak();
		echo '<script src="jscss/custom.js" type="text/javascript"></script>';
        echo "</head>\n<body>\n<table class=\"sortable wlm-result\" id=\"sortable_table_id_0\">\n";
		
		$this->isFirstRow = true;
	}
	
	function outputContinue($row, $continueKey, $primaryKey) {
		global $I18N;
		$continue = '';
		foreach ( $primaryKey as $key ) {
			$continue .= "|" . rawurlencode( $row->$key );
		}
		$continue = substr( $continue, 1 );
		
		echo '</table>';
		$this->isTableOpen = false;
		
		echo '<p style="text-align:right;"><a href="' .
			htmlspecialchars( $this->api->getUrl( array( $continueKey => $continue ) ) ) . '">' . $I18N->msg('next-page') . '</a></p>';
	}
	
	function outputRow($row, $selectedItems) {
		global $I18N;
		if (!$this->isTableOpen) {
			echo '<tr id="header">';
			
			foreach ( $row as $name => $value ) {
				if ( in_array( $name, $selectedItems ) ) {
                    //$label = $name.'<a href="#" class="sortheader" onclick="ts_resortTable(this);return false;"><span class="sortarrow" sortdir="down"><img src="http://commons.wikimedia.org/skins-1.17/common/images/sort_none.gif" alt="↑"></span></a>';
					echo '<th class="sortheader">' . $I18N->msg('db-field-' . $name ) . '</th>'; $this->linebreak();
				}
			}
			echo '</tr>';
			$this->isTableOpen = true;
		}
		
		$hasWikitext = array('name', 'address', 'municipality');
		
		echo '<tr>';
		$this->linebreak();
		foreach ( $row as $name => $value ) {
            $tdattrs = '';
			$cellData = '';
			if ( in_array( $name, $selectedItems ) ) {
				if ($name == "image" || $name == "img_name") {
					$cellData = self::genImage($value);
				} elseif ($name == "registrant_url") {
					$cellData = self::makeHTMLlink($value);
				} elseif ($name == "source" || $name == "img_thumb") {
					$cellData = self::prettifyUrls( $value );
				} elseif ( in_array( $name, $hasWikitext ) ) {
					$makeLinks = true;
                    // not all datasets are ResultWrapper
                    if ( is_object($row) && isset($row->lang) ) {
                        $lang = $row->lang;
                        $project = $row->project;
                    } else { // assume $row is array
                        $lang = $row['lang'];
                        $project = $row['project'];
                    }
                    $cellData = processWikitext($lang, $value, $makeLinks, $project);
				} elseif (strpos(strrev($name),'tcp_') === 0) { // capture Statistics _pct fields
                    $tdattrs = ' class="ht'.(intval($value/10)).'"';
                    $cellData = $value; //.' %' // this will break sorting! :(;
				} else {
					$cellData = htmlspecialchars( $value );
				}
				
				echo '<td'.$tdattrs.'>' . $cellData . '</td>';$this->linebreak(); 
			}
		}
		echo '</tr>';$this->linebreak();
	}
	
	function outputEnd() {
		if ($this->isTableOpen)
			echo "</table>\n";

		echo "</body>\n</html>";
	}
	
	/**
	 * Make this a nice link if it is a url (source column)
	 */
	static function prettifyUrls($text) {
		try {
			$m = matchWikiprojectLink( $text );
			$encodedLinkText = str_replace( '_', ' ', $m[5] );
			$linkText = urldecode( $encodedLinkText );
			return '<a href="https://' . htmlspecialchars( $m[2] ) . '">' .
				htmlspecialchars( $linkText ) . '</a>';
		} catch (Exception $e) {
			// Normal text
			return htmlspecialchars( $text );
		}
	}

	static function makeHTMLlink($text) {
		return '<a href="' . htmlspecialchars( $text ) . '">' . htmlspecialchars( $text ) . '</a>';
	}

	static function genImage($img) {
		if ( $img == "" )
			return '';

		$img = str_replace(" ", "_", $img);
		$url = getImageFromCommons( $img, 100 );
		// FIXME: Check if this is save (just including $url)
		return '<a href="//commons.wikimedia.org/wiki/File:' . rawurlencode($img) . '"><img src="' . $url . '" /></a>';
	}
}
