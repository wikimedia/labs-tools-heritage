<?php

require_once ( dirname( __DIR__ ) . '/api/common.php' );

class ToolboxPage {
	private $I18N = null;

	function __construct( $I18N ) {
		$this->I18N = $I18N;
	}

	public function getIndexPage() {
		return $this->getPage( $this->getIndexBody() );
	}

	public function getPageIntro() {
		$result = [];
		$result[] = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" ' .
		            '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">';
		$result[] = '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="' .
			        $this->I18N->getLang() . '" lang="' .
			        $this->I18N->getLang() . '">';
		$result = array_merge( $result, $this->getHead() );
		$result[] = '<body>';
		$result[] = '  <div id="wrapper">';
		$result[] = '  <div id="header">';
		$result = array_merge( $result, $this->getBodyHeader() );
		$result[] = '  <div id="maincontainer">';
		$result = array_merge( $result, $this->getLeftNav() );

		return implode( "\n", $result );
	}

	public function getPageOutro() {
		$result = [];
		$result[] = '  </div><!-- end maincontainer -->';
		$result[] = '  <br style="clear:left;" />';
		$result[] = '  <hr/>';
		$result[] = $this->I18N->getPromoBox();
		$result[] = '  </div> <!-- end wrapper -->';
		$result[] = '</body>';
		$result[] = '</html>';

		return implode( "\n", $result );
	}
	public function getHead() {
		$result = [];
		$result[] = '<head>';
		$result[] = '  <title>'. _( 'toolbox-meta-title' ) .'</title>';
		$result[] = '  <meta http-equiv="content-type" content="text/html; charset=utf-8">';
		$result[] = '  <link rel="stylesheet" type="text/css" href="css/default_css.css" />';
		$result[] = '  <link rel="shortcut icon" href="img/favicon.ico" type="image/x-icon"/>';
		$result[] = '  <script src="js/jquery.js" type="text/javascript" /></script>';
		$result[] = '</head>';
		return $result;
	}

	public function getLeftNav() {
		$result = [];
		$result[] = '    <div id="leftnav">';
		$result[] = '    <ul class="first">';
		$result[] = '      <li><a href="index.php">'. _( 'toolbox-nav-homepage' ) .'</a>';
		$result[] = '      <ul>';
		$result[] = '      <li><a href="statistics.php">'. _( 'toolbox-nav-statistics' ) .'</a></li>';
		$result[] = '      <li><a href="search.php">'. _( 'toolbox-nav-search' ) .'</a></li>';
		$result[] = '      </ul>';
		$result[] = '      </li>';
		$result[] = '  </ul>';
		$result[] = '  </div><!-- end leftnav-->';
		return $result;
	}

	public function getBodyHeader() {
		$result = [];
		$result[] = '  <div id="header">';
		$result[] = '    <a href="#"><img id="wlm-logo" src="img/logo-wiki-loves-monuments.png" width="80" alt="'. _( 'toolbox-main-logo-alt' ) .'" /></a>';
		$result[] = '    <h2>'. _( 'toolbox-main-title' ) .'</h2>';
		$wlm = [
			'variables' => [
				'<span>' . _( 'toolbox-wikilovesmonuments' ) . '</span>' ]
			];
		$result[] = '    <h1>'. _( 'toolbox-main-description', $wlm ) .'</h1>';
		$result[] = '  </div><!-- end header -->';
		return $result;
	}

}
