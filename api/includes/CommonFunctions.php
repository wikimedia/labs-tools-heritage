<?php
//FIXME: functions used in API should be moved to some(?) class

function getImageFromCommons($filename, $size) {
    if ($filename and $size) {
        $md5hash=md5($filename);
        $filename = str_replace(' ', '_', $filename);
        //urlencode($filename);
        $url = "http://upload.wikimedia.org/wikipedia/commons/thumb/" . $md5hash[0] . "/" . $md5hash[0] . $md5hash[1] . "/" . $filename . "/" . $size . "px-" . $filename;
        return $url;
    }
}

function processWikitext($wikilang, $text, $makelinks) {
    /* Process the wikitext.
     * If makelinks is true, make html links
     * If makelinks is false, remove wikitext to produce normal text without links
     */
    $result = $text;
    $differentLinkRegex="/\[\[([^\|]*)\|([^\]]*)\]\]/";
    $simpleLinkRegex="/\[\[([^\]]*)\\]\]/";
    $wikiUrl = 'http://' . $wikilang . '.wikipedia.org/wiki/';
    $differentLinkReplace = "'<a href=\"" . $wikiUrl ."' . rawurlencode('$1') . '\">$2</a>'";
    $simpleLinkReplace = "'<a href=\"". $wikiUrl ."' . rawurlencode('$1') . '\">$1</a>'";
    if ( $makelinks ) {
        $result = preg_replace($differentLinkRegex . "e", $differentLinkReplace, $result);
        $result = preg_replace($simpleLinkRegex . "e", $simpleLinkReplace, $result);
        $result = $result;
    } else {
        $result = preg_replace($differentLinkRegex, "$2", $result);
        $result = preg_replace($simpleLinkRegex, "$1", $result);
    }
    return $result;
}

function replaceSpaces( $in_string ) {
    return str_replace(' ', '_', $in_string);
}
