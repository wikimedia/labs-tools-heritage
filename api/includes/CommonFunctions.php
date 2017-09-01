<?php
//FIXME: functions used in API should be moved to some(?) class

function getImageFromCommons($filename, $size) {
	if ($filename and $size) {
		$filename = str_replace(' ', '_', $filename);
		$md5hash = md5($filename);
		//urlencode($filename);
		//TODO: can be replaced by something like https://commons.wikimedia.org/w/thumb.php?f=" . $filename . "&width=" . $size;
		$url = "//upload.wikimedia.org/wikipedia/commons/thumb/" . $md5hash[0] . "/" . $md5hash[0] . $md5hash[1] . "/" . $filename . "/" . $size . "px-" . $filename;
		return $url;
	}
}

function processWikitext($wikilang, $text, $makelinks, $wikiproject = "wikipedia") {
	/* Process the wikitext.
	 * If makelinks is true, make html links
	 * If makelinks is false, remove wikitext to produce normal text without links
	 */
	$result = $text;
	$differentLinkRegex="/\[\[([^\|]*)\|([^\]]*)\]\]/";
	$simpleLinkRegex="/\[\[([^\]]*)\\]\]/";
	$wikiUrl = '//' . $wikilang . '.' . $wikiproject . '.org/wiki/';
	$differentLinkReplace = function($m) use($wikiUrl) {
		return '<a href="' . $wikiUrl . rawurlencode( $m[1] ) . '">'. $m[2] .'</a>';
	};
	$simpleLinkReplace = function($m) use($wikiUrl) {
		return '<a href="' . $wikiUrl . rawurlencode( $m[1] ) . '">'. $m[1] .'</a>';
	};
	if ( $makelinks ) {
		$result = preg_replace_callback(
			$differentLinkRegex,
			$differentLinkReplace,
			$result);
		$result = preg_replace_callback(
			$simpleLinkRegex,
			$simpleLinkReplace,
			$result);
		$result = $result;
	} else {
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
