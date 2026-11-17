<?php
//FIXME: functions used in API should be moved to some(?) class

function getImageFromCommons($filename, $size) {
	if ($filename and $size) {
		$filename = str_replace(' ', '_', $filename);
		$md5hash = md5($filename);
		// The filename is harvested wikitext, so encode it for use in a URL
		// and HTML attribute
		$encoded = rawurlencode($filename);
		$width = intval($size);
		// TODO: could use https://commons.wikimedia.org/w/thumb.php?f=<file>&width=<px> instead of computing the md5 path
		$url = "//upload.wikimedia.org/wikipedia/commons/thumb/" . $md5hash[0] . "/" . $md5hash[0] . $md5hash[1] . "/" . $encoded . "/" . $width . "px-" . $encoded;
		return $url;
	}
}

/**
 * Process harvested wikitext into HTML or plain text.
 *
 * With $makelinks, the result is HTML: all of the text is escaped, line breaks
 * (<br>, <br/>, <br /> or </br>) are kept and wikilinks become <a> links.
 * Entities written in the wikitext are kept.
 *
 * Without $makelinks, the result is plain text, not escaped: wikilinks are
 * replaced by their labels and line breaks by spaces. Callers escape it for
 * the context they put it in.
 *
 * @param string $wikilang Language of the wiki the links point to
 * @param string $text The wikitext
 * @param bool $makelinks Whether to return HTML with links or plain text
 * @param string $wikiproject Project of the wiki the links point to
 * @return string
 */
function processWikitext($wikilang, $text, $makelinks, $wikiproject = "wikipedia") {
	/**
	 * Mapping of multilingual sites not following the lang.project.org pattern
	 */
	static $multilingualSiteMap = [
		'commons' => 'commons.wikimedia.org',
		'wikidata' => 'www.wikidata.org',
	];

	if ( array_key_exists( $wikiproject, $multilingualSiteMap ) ) {
		$wikiUrl = '//' . $multilingualSiteMap[ $wikiproject ] . '/wiki/';
	} else {
		$wikiUrl = '//' . $wikilang . '.' . $wikiproject . '.org/wiki/';
	}

	/**
	 * @param string $target Page title, HTML escaped
	 * @param string $label Link text, HTML escaped
	 */
	$makeLink = function ( $target, $label ) use ( $wikiUrl ) {
		// Decode the escaped target back to plain text before URL encoding it
		$href = $wikiUrl . rawurlencode( html_entity_decode( $target, ENT_QUOTES, 'UTF-8' ) );
		return '<a href="' . htmlspecialchars( $href ) . '">' . $label . '</a>';
	};

	$result = $text;
	$differentLinkRegex="/\[\[([^\]\|]*)\|([^\]]*)\]\]/";
	$simpleLinkRegex="/\[\[([^\]]*)\\]\]/";
	$lineBreakRegex = '#\s*</?br\s*/?>\s*#i';
	if ( $makelinks ) {
		// Escape first; this leaves "[", "]" and "|" so links can still be found
		$escape = fn ( $part ) => htmlspecialchars( $part, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8', false );
		$result = implode( '<br />', array_map( $escape, preg_split( $lineBreakRegex, $result ) ) );
		$result = preg_replace_callback( $differentLinkRegex,
			fn ( $m ) => $makeLink( $m[1], $m[2] ), $result );
		$result = preg_replace_callback( $simpleLinkRegex,
			fn ( $m ) => $makeLink( $m[1], $m[1] ), $result );
	} else {
		$result = preg_replace( $lineBreakRegex, ' ', $result );
		$result = preg_replace($differentLinkRegex, "$2", $result);
		$result = preg_replace($simpleLinkRegex, "$1", $result);
	}
	return $result;
}

//Separates the parsing from the prettifying
function matchWikidataLink($url) {
	/* Determine if a string is a Wikidata page or entity link
	 * If the pattern matches, returns an array with the matching parts
	 * If the pattern doesn't match, returns NULL
	 *
	 * The format of the array is designed to be compatible with that for
	 * matchWikiprojectLink().
	 */
	$var = NULL;
	$pattern = '/(https?:)?\/\/((www)\.(wikidata)\.org\/(wiki|entity)\/(.*))/';
	if ( !preg_match( $pattern, $url, $var )) {
		throw new Exception('The provided url was not a wikidata link.');
	}
	else {
		unset( $var[5] );
		$var = array_values( $var );  // rebase array
	}
	return $var;
}

function matchWikiprojectLink($text) {
	/* Determine if a string is a Wikipedia link
	 * If the pattern matches, returns an array with the matching parts
	 * If the pattern doesn't match, returns NULL
	 */
	$projects = array("wikipedia", "wikivoyage", "wikidata", "wikimedia");
	$projectRegex = "(" . join("|", $projects) . ")";
	$var = NULL;
	$pattern = '/(https?:)?\/\/(([a-z\-]+)\.' . $projectRegex . '\.org\/w\/index\.php\?title=(.*)&oldid=(.*))/';
	if ( !preg_match( $pattern, $text, $var )) {
		throw new Exception('No project link in text.');
	}
	return $var;
}

/**
 * Return a mathing wikiproject or wikidata url
 */
function matchUrl( $url ) {
	try {
		$m = matchWikiprojectLink( $url );
	} catch ( Exception $e ) {
		// Possibly a wikidata entity/wiki link
		try {
			$m = matchWikidataLink( $url );
		} catch ( Exception $e ) {
			// Normal text
			$m = null;
		}
	}
	return $m;
}

function urlencodeWikiprojectLink($var, $drop_oldid = false) {
	/* Takes a matching group from matchWikiprojectLink
	 * and returns an url with the pagename urlencoded.
	 */
	$site = $var[3] . '.' . $var[4] . '.org';
	$title = urlencode( $var[5] );
	if ( $drop_oldid or !isset( $var[6] ) ){
		return $site . '/w/index.php?title=' . $title;
	}
	return $site . '/w/index.php?title=' . $title . '&oldid=' . $var[6];
}

function replaceSpaces( $in_string ) {
	return str_replace(' ', '_', $in_string);
}

function makeWikidataUrl($qid) {
	/* Creates a URL to Wikidata from a Qid */
	if ( $qid ) {
		return "https://www.wikidata.org/wiki/$qid";
	} else {
		return '';
	}
}

function makeWikidataWikilink($qid) {
	/* Creates a wikilink to Wikidata from a Qid */
	if ( $qid ) {
		return "[[d:$qid]]";
	} else {
		return '';
	}
}

function makeHTMLlink( $url, $text=false ) {
	/*
	 * Creates a html link with correctly escaped characters.
	 * Defaults to using the url as link text if no alternative is given.
	 */
	if ( ! $text ) {
		$text = $url;
	}
	return '<a href="' . htmlspecialchars( $url ) . '">' . htmlspecialchars( $text ) . '</a>';
}

function makeCommonsCatUrl($cat) {
	/* Creates a URL to Commons from a category name */
	if ( $cat ) {
		return "https://commons.wikimedia.org/wiki/Category:$cat";
	} else {
		return '';
	}
}

function makeCommonsCatWikilink($cat) {
	/* Creates a wikilink to Commons from a category name */
	if ( $cat ) {
		return "[[c:Category:$cat]]";
	} else {
		return '';
	}
}
