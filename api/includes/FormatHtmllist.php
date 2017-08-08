<?php
error_reporting( E_ALL );
/**
 * HTML list output type, based on XML
 * This output is for users (and not automated tools) so internationalization will be used.
 *
 */
// functions: processWikitext, matchWikiprojectLink, matchWikidataQid
require_once ( 'CommonFunctions.php' );

class FormatHtmllist extends FormatBase {

	private $rowNumberIsOdd = 0;

	function getContentType() {
		return "text/html";
	}

	function headers() {
		parent::headers();
		echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">';
	}

	function outputBegin( $selectedItems ) {
		echo '<html>';
		echo '<head>';
		echo '<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">';
		echo '<style type="text/css">';
		echo '.main { max-width:540px; }
			  .row { padding:8px; }
			  .oddRow { background-color:#F1F1F1; }
			  .evenRow { background-color:#F9F9F9; }';
		echo '</style>';

	}

	function outputTitle( $result, $numRows ) {

		$title = '';
		if ( $numRows == 1 ) {
			foreach ( $result as $row ) {
				if ( isset( $row->name ) and $row->name ) {
					$title = htmlspecialchars( processWikitext( '', $row->name, false ) );
				}
				break;
			}
		} else {
			$title = 'Monuments list';
		}
		echo '<title>'. $title .'</title>';
		echo "</head>\n<body>\n";
		echo '<div class="main">';
	}

	function outputContinue( $row, $continueKey, $primaryKey ) {
		global $I18N;
		$continue = '';
		foreach ( $primaryKey as $key ) {
			$continue .= "|" . rawurlencode( $row->$key );
		}
		$continue = substr( $continue, 1 );

		echo '<p style="text-align:right;"><a href="' .
			htmlspecialchars( $this->api->getUrl( [ $continueKey => $continue ] ) ) . '">' . $I18N->msg( 'next-page' ) . '</a></p>';
	}

	function outputRow( $row, $selectedItems ) {
		global $I18N;
		$desc = '';
		$this->rowNumberIsOdd = 1 - $this->rowNumberIsOdd;

		if ( $this->rowNumberIsOdd ) {
			$desc .= '<div class="row oddRow">';
		} else {
			$desc .= '<div class="row evenRow">';
		}

		if ( isset( $row->image ) and $row->image ) {
			$imgsize = 100;
			$desc .= '<a href="//commons.wikimedia.org/wiki/File:' . rawurlencode( $row->image ) . '">';
			$desc .= '<img src="' . getImageFromCommons( $row->image, $imgsize ) . '" align="right" />';
			$desc .= '</a>';
		}

		if ( isset( $row->name ) and $row->name ) {
			if ( isset( $row->monument_article ) and $row->monument_article ) {
				$makeLinks = false;
				$article_url = '//'. $row->lang .'.'. $row->project .'.org/wiki/'. htmlspecialchars( $row->monument_article );
				$desc .= '<h2><a href="'. $article_url .'">'. processWikitext( $row->lang, $row->name, $makeLinks, $row->project ) . '</a></h2>';
			} else {
				$makeLinks = true;
				$desc .= '<h2>'. processWikitext( $row->lang, $row->name, $makeLinks, $row->project ) . '</h2>';
			}
		}
		$desc .= '<ul>';
		$hasWikitext = [ 'address', 'municipality' ];
		$sepListedFields = [ 'name', 'image', 'lat', 'lon', 'source', 'monument_article', 'registrant_url' ];
		foreach ( $row as $name => $value ) {
			if ( in_array( $name, $selectedItems ) ) {
				if ( !in_array( $name, $sepListedFields ) ) {
					$desc .= '<li> ' . htmlspecialchars( $I18N->msg( 'db-field-' . $name ) ) . ': ';
					if ( in_array( $name, $hasWikitext ) ) {
						$makeLinks = true;
						$desc .= processWikitext( $row->lang, $value, $makeLinks, $row->project );
					} else {
						if ( strcmp( $name, 'id' ) == 0 and
							   isset( $row->registrant_url ) and $row->registrant_url ) {
							$desc .= '<a href="' . htmlspecialchars( $row->registrant_url ) . '">';
							$desc .= htmlspecialchars( $value );
							$desc .= '</a>';
						} elseif ( strcmp( $name, 'wd_item' ) == 0 ) {
							$desc .= '<a href="' . makeWikidataUrl( $value ) . '">';
							$desc .= htmlspecialchars( $value );
							$desc .= '</a>';
						} else {
							$desc .= htmlspecialchars( $value );
						}
					}
					$desc .= '</li>';
				}
			}
		}
		if ( isset( $row->lat ) and $row->lat ) {
			$desc .= '<li>' . $I18N->msg( 'location' ) . ': ' . $row->lat . ', ' . $row->lon . '</li>';
		}

		if ( isset( $row->source ) and $row->source ) {
			$wikiListUrl = self::matchUrl( $row->source );
			if ( $wikiListUrl ) {
				$desc .= '<li><a href="//' . $wikiListUrl. '">' . $I18N->msg( 'source-monuments-list' ) . '</a></li>';
			}
		}

		$desc .= '</ul>';
		$desc .= '</div>';

		echo $desc;
	}

	function outputEnd() {
		echo '</div>';
		echo "</body>\n</html>";
	}

	function output( $result, $limit, $continueKey, $selectedItems, $primaryKey ) {
		$this->headers();

		$numRows = $result->numRows();
		$this->outputBegin( $selectedItems );
		$this->outputTitle( $result, $numRows );
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
	 * Return a mathing wikiproject or wikidata url
	 */
	static function matchUrl( $url ) {
		try {
			$m = matchWikiprojectLink( $url );
			return $m[2];
		} catch ( Exception $e ) {
			// Possibly a wikidata entity/wiki link
			try {
				$m = matchWikidataQid( $url );
				return $m[2];
			} catch ( Exception $e ) {
				// Normal text
				return null;
			}
		}
	}

}
