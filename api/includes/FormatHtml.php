<?php
error_reporting( E_ALL );
/**
 * HTML output type, based on XML. This output is for users (and not automated tools) so internationalization will be used.
 * @author Joancreus (jcreus), based on Platonides work
 */
// functions: processWikitext, getImageFromCommons, makeWikidataUrl, matchUrl, urlencodeWikiprojectLink
require_once ( 'CommonFunctions.php' );

class FormatHtml extends FormatBase {
	function getContentType() {
		return "text/html";
	}

	function getRequiredOrderBy() {
		return [ 'country', 'municipality', 'address' ];
	}

	function headers() {
		parent::headers();
		echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">';
	}

	function linebreak() {
		echo "\n";
	}

	private $isTableOpen;

	function outputBegin( $selectedItems ) {
		echo '<html>';
		$this->linebreak();
		echo '<head>';
		$this->linebreak();
		echo '<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">';
		$this->linebreak();
		echo '<link media="all" type="text/css" href="jscss/style.css" rel="stylesheet">';
		$this->linebreak();
		echo '<link type="text/css" href="https://tools-static.wmflabs.org/cdnjs/ajax/libs/jquery.tablesorter/2.29.0/css/theme.default.min.css" rel="stylesheet">';
		$this->linebreak();
		echo '<script src="https://tools-static.wmflabs.org/cdnjs/ajax/libs/jquery/1.2.6/jquery.min.js" type="text/javascript"></script>';
		$this->linebreak();
		echo '<script src="https://tools-static.wmflabs.org/cdnjs/ajax/libs/jquery.tablesorter/2.29.0/js/jquery.tablesorter.min.js" type="text/javascript"></script>';
		$this->linebreak();
		echo '<script src="https://tools-static.wmflabs.org/cdnjs/ajax/libs/jquery.tablesorter/2.29.0/js/jquery.tablesorter.widgets.min.js" type="text/javascript"></script>';
		$this->linebreak();
		echo "<script>
				$(function(){
				$('table').tablesorter({
					widgets        : ['zebra', 'columns'],
					usNumberFormat : false,
					sortReset      : true,
					sortRestart    : true
				});
			});
			</script>";
		$this->linebreak();
		echo "</head>\n<body>\n<table class=\"sortable wlm-result\" id=\"sortable_table_id_0\">\n";

		$this->isFirstRow = true;
	}

	function outputContinue( $row, $continueKey, $primaryKey ) {
		$continue = '';
		foreach ( $primaryKey as $key ) {
			$continue .= "|" . rawurlencode( $row->$key );
		}
		$continue = substr( $continue, 1 );

		echo '</table>';
		$this->isTableOpen = false;

		echo '<p style="text-align:right;"><a href="' .
			htmlspecialchars( $this->api->getUrl( [ $continueKey => $continue ] ) ) . '">' . _i18n( 'next-page' ) . '</a></p>';
	}

	function outputRow( $row, $selectedItems ) {
		if ( !$this->isTableOpen ) {
			echo '<thead><tr id="header">';

			foreach ( $row as $name => $value ) {
				if ( in_array( $name, $selectedItems ) ) {
					echo '<th class="sortheader">' . _i18n( 'db-field-' . $name ) . '</th>';
					$this->linebreak();
				}
			}
			echo '</tr></thead>';
			$this->isTableOpen = true;
		}

		$hasWikitext = [ 'name', 'address', 'municipality' ];

		echo '<tr>';
		$this->linebreak();
		foreach ( $row as $name => $value ) {
			$tdattrs = '';
			$cellData = '';
			if ( in_array( $name, $selectedItems ) ) {
				if ( $name == "image" || $name == "img_name" ) {
					$cellData = self::genImage( $value );
				} elseif ( $name == "registrant_url" ) {
					$cellData = makeHTMLlink( $value );
				} elseif ( $name == "source" || $name == "img_thumb" ) {
					$cellData = self::prettifyUrls( $value );
				} elseif ( $name == "wd_item" ) {
					$link = makeWikidataUrl( $value );
					$cellData = makeHTMLlink( $link, $value );
				} elseif ( $name == "commonscat" ) {
					$link = makeCommonsCatUrl( $value );
					$cellData = makeHTMLlink( $link, $value );
				} elseif ( in_array( $name, $hasWikitext ) ) {
					$makeLinks = true;
					// not all datasets are ResultWrapper
					if ( is_object( $row )
							&& isset( $row->lang )
							&& isset( $row->project ) ) {
						$lang = $row->lang;
						$project = $row->project;
					} else { // assume $row is array
						$lang = $row['lang'];
						$project = $row['project'];
					}
					$cellData = processWikitext( $lang, $value, $makeLinks, $project );
				} elseif ( strpos( strrev( $name ), 'tcp_' ) === 0 ) { // capture Statistics _pct fields
					$tdattrs = ' class="ht'.( intval( $value/10 ) ).'"';
					$cellData = $value; // .' %' // this will break sorting! :(;
				} else {
					$cellData = htmlspecialchars( $value );
				}

				echo '<td'.$tdattrs.'>' . $cellData . '</td>';
				$this->linebreak();
			}
		}
		echo '</tr>';
		$this->linebreak();
	}

	function outputEnd() {
		if ( $this->isTableOpen ) {
			echo "</table>\n";
	 }

		echo "</body>\n</html>";
	}

	/**
	 * Make this a nice link if it is a url (source column)
	 */
	static function prettifyUrls( $text ) {
		$m = matchUrl( $text );
		if ( $m ) {
			$linkText = str_replace( '_', ' ', $m[5] );
			$encodedLink = urlencodeWikiprojectLink( $m );
			return makeHTMLlink( 'https://' . $encodedLink, $linkText );
		} else {
			return htmlspecialchars( $text );
		}
	}

	static function genImage( $img ) {
		if ( $img == "" ) {
			return '';
		}

		$img = str_replace( " ", "_", $img );
		$url = getImageFromCommons( $img, 100 );
		// FIXME: Check if this is save (just including $url)
		return '<a href="//commons.wikimedia.org/wiki/File:' . rawurlencode( $img ) . '"><img src="' . $url . '" /></a>';
	}
}
