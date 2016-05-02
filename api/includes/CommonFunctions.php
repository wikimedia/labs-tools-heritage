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
//FIXME: should support other wikiprojects
function matchWikiprojectLink($text) {
	/* Determine if a string is a wikipedia link
	 * If the pattern matches returns 1, and populates $m with the matches
	 * If the pattern doesn't match returns 0
	 */
	$projects = array("wikipedia", "wikivoyage", "wikidata", "wikimedia");
	$projectRegex = "(" . join("|", $projects) . ")";
	$var = NULL;
	if (!preg_match( '/(https?:)?\/\/(([a-z\-]+)\.' . $projectRegex . '\.org\/w\/index\.php\?title=(.*)&oldid=(.*))/', $text, $var )) {
		throw new Exception('No project link in text.');
	}
	return $var;
}

function replaceSpaces( $in_string ) {
	return str_replace(' ', '_', $in_string);
}
