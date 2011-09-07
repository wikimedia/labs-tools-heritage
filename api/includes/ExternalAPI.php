<?php

/**
 * External API wrapper
 * @author Nuno Tavares <nuno.tavares@wikimedia.pt>
 */

ini_set('user_agent', 'WLM bot/1.0');

class ExternalAPI {
    private $apiUrl = 'http://commons.wikimedia.org/w/api.php';
    private $__bDebug = true;


    function debug($msg) {
        if ( $this->__bDebug ) {
            print "[d] ".$msg."\n";
        }
    }

    function fetchPage($url) {
        return file_get_contents($url);
    }

    function getPageText($title) {
        //$this->debug('Fetching: '.$title);
        $url_api = 'http://commons.wikimedia.org/w/api.php';
        $url = $this->apiUrl.'?action=query&format=json&prop=revisions&rvprop=content&rvprop=timestamp|user|comment|content&titles='.urlencode($title);
        //$this->debug(' + URL: '.$url);
        $page = $this->fetchPage($url);

        if ( is_null($page) ) {
            return false;
        }
        $retobj = json_decode($page, true);
        if ( isset($retobj['query']['pages']) ) {
            $revs = reset($retobj['query']['pages']);
            if ( isset($revs['revisions'][0]['*']) ) {
                return $revs['revisions'][0]['*'];
            }
        }
        return false;
    }

}
