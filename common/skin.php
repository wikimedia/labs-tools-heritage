<?php

/**
 * This file provides a skin for the different tools
 * 
 * Requisites: Intuition must be already loaded to $I18N global.
 * Helper functions are not needed.
 * 
 * 
 * Set variable $useskin to the name of the default skin script
 * (can be overriden by the user with the url parameter `useskin` or 
 * with a cookie).
 * 
 * Can be configured by defining the following constants before including:
 *  TITLE: Title for the article and the window. Defaults to the title message
 *  SUBTITLE: A subtitle for the article
 *  MAINPAGE: Link to be ginen for the logo. Defaults to the user home.
 *  LOGO: Image to override the toolserver logo.
 * 
 */

/* Tool title */
$title = defined( 'TITLE' ) ? TITLE : $I18N->msg( 'title' );
$subtitle = defined( 'SUBTITLE' ) ? SUBTITLE : '';

/* If a main page is not provided, link with the user root web space */
$mainpage = defined( 'MAINPAGE' ) ? MAINPAGE : substr( $_SERVER['REQUEST_URI'], 0, 1 + strpos( $_SERVER['REQUEST_URI'], '/', 1 ) );
$logo = defined( 'LOGO' ) ? LOGO : 'http://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Wikimedia_Community_Logo-Toolserver.svg/135px-Wikimedia_Community_Logo-Toolserver.svg.png';

/**
 * Name of the parameter and cookie name that sets the skin
 */
define ( 'SKIN_PARAM', 'useskin' );

require_once __DIR__ . '/status.php';

/**
 * Load list of skins
 */
$skinsFolder = __DIR__ . '/skins';
$skins = scandir( $skinsFolder ) or die ( 'No skins are available' );
$skins = array_filter( $skins, create_function( '$skinName', 'return  substr( $skinName, -4 ) == ".php" ;' ) );
array_walk( $skins, create_function( '&$name', '$name = basename( $name, ".php" );' ) );
$lcskins = array_map( 'strtolower', $skins );
$skins = array_combine( $lcskins, $skins );

$_REQUEST = $_POST + $_GET + $_COOKIE;

/* Load from cookie / url if appropiate. */
if ( isset( $_REQUEST[SKIN_PARAM] ) )
	$useskin = $_REQUEST[SKIN_PARAM];

$useskin = @strtolower( $useskin );

/**
 * Validate the $useskin parameter.
 * We require that skin names are sane.
 */
if ( !isset( $useskin ) || !isset( $skins[$useskin] ) ) {
	$useskin = 'monobook';
}

if ( !defined( 'MEDIAWIKI' ) )
	define( 'MEDIAWIKI', true );

//$IP = __DIR__;
require_once "$IP/includes/AutoLoader.php";
require_once "$IP/includes/Defines.php";
require_once "$IP/includes/DefaultSettings.php";
require_once "$IP/includes/GlobalFunctions.php";
require_once "$IP/includes/profiler/ProfilerStub.php";
require_once "$skinsFolder/{$skins[$useskin]}.php";

$wgVectorUseIconWatch = false;
$wgEnableTooltipsAndAccesskeys = false; /* This way the Linker doesn't try to use MediaWiki i18n system */
$tmplName = $skins[$useskin] . "Template";
$tpl = new $tmplName;

$I18N->loadTextdomainFromFile( __DIR__ . '/Skin.18n.php', 'skin' );

class ToolSkin extends Skin {
	function outputPage( OutputPage $out = null ) {
	}
	function setupSkinUserCss( OutputPage $out ) {
	}
}

$wgStylePath = htmlspecialchars('/~kentaur/common/skins'); //htmlspecialchars('http://bits.wikimedia.org/skins-1.17');
$headelement = 
'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html lang="' . $I18N->getLang() . '" dir="' . $I18N->getDir() . '" xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>' . htmlspecialchars( $title ) . '</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta http-equiv="Content-Style-Type" content="text/css" />
<link rel="stylesheet" href="'.$wgStylePath.'/common/commonPrint.css" type="text/css" media="print" />
<link rel="stylesheet" href="'.$wgStylePath.'/common/shared.css" type="text/css" media="screen" />
<link rel="stylesheet" href="/~kentaur/common/skins/toolserver.css" type="text/css" media="screen" />
' .

( ( $useskin == 'vector' ) ?
'<link rel="stylesheet" href="'.$wgStylePath.'/vector/screen.css" type="text/css" media="screen" />' :
'<link rel="stylesheet" href="'.$wgStylePath.'/monobook/main.css" type="text/css" media="screen" />
<link rel="stylesheet" href="'.$wgStylePath.'/chick/main.css" type="text/css" media="handheld" />
<!--[if lt IE 5.5000]><link rel="stylesheet" href="'.$wgStylePath.'/monobook/IE50Fixes.css?301-3" type="text/css" media="screen" /><![endif]-->
<!--[if IE 5.5000]><link rel="stylesheet" href="'.$wgStylePath.'/monobook/IE55Fixes.css?301-3" type="text/css" media="screen" /><![endif]-->
<!--[if IE 6]><link rel="stylesheet" href="'.$wgStylePath.'/monobook/IE60Fixes.css?301-3" type="text/css" media="screen" /><![endif]-->
<!--[if IE 7]><link rel="stylesheet" href="'.$wgStylePath.'/monobook/IE70Fixes.css?301-3" type="text/css" media="screen" /><![endif]-->
' ) . '
<style type="text/css" media="all">a{text-decoration:underline}a.new,#quickbar a.new{color:#ba0000}
#translate { font-weight: bold }
li.active { font-weight: bold }
</style>
</head>
<body class="mediawiki">'; //--><?php

class Translator {
	function translate( $value ) {
		global $I18N;
		
		return $I18N->msg( $value, array( 'domain' => 'skin', 'escape' => 'plain' ) );
	}
}

/* Helper function to create links to the current script keeping the GET parameters */
function CurrentUrl( $paramOverride = array() ) {
	return $_SERVER['SCRIPT_NAME'] . '?' . http_build_query( $paramOverride + $_GET );
}

$translator = new Translator;
$tpl->setTranslator( $translator );
$tpl->set( 'skin', new ToolSkin );
$tpl->set( 'headelement', $headelement );
$tpl->set( 'specialpageattributes', '' );
$tpl->set( 'title', $title );
$tpl->set( 'subtitle', $subtitle );
$tpl->set( 'isarticle', true );
$tpl->set( 'undelete', false ); # Space for undelete links
$tpl->set( 'newtalk', ToolserverStatus::prettyBox() /*'Server is lagged'*/ ); # Show all cluster warnings regardless of actual db usage of the script
$tpl->set( 'showjumplinks', false );

$tpl->set( 'printfooter', '' );
$tpl->set( 'debughtml', '' );
$tpl->set( 'catlinks', false );
$tpl->set( 'dataAfterContent', false );
$tpl->set( 'sitenotice', false );
$tpl->set( 'debug', false );
$tpl->set( 'userlangattributes', '' );
$tpl->set( 'jsmimetype', 'text/javascript' );
$tpl->set( 'bottomscripts', '' );
$tpl->set( 'reporttime', '' );

$content_actions = array(
	'tool' => array( 'href' => CurrentUrl(), 'text' => $I18N->msg( 'tool', array( 'domain' => 'skin', 'escape' => 'plain' ) ), 'class' => 'selected' ), 
	'view-source' => array( 'href' => CurrentUrl( array( 'action' => 'source' ) ), 'text' => $I18N->msg( 'viewsource', array( 'domain' => 'skin', 'escape' => 'plain' ) ) ) 
);
foreach ( $content_actions as &$ca ) $ca += array( 'class' => '', 'primary' => true ); // Vector wants these

$tpl->set( 'content_navigation', array( 'namespaces' => $content_actions, 'views' => array(), 'actions' => array(), 'variants' => array() ) );
$tpl->set( 'personal_urls', array() );

$tpl->set( 'logopath', $logo );

/* Set the link to the main page the logo will link to */
$nav_urls = array();
$nav_urls['mainpage']['href'] = $mainpage;
$tpl->set( 'nav_urls', $nav_urls );

$tpl->set( 'footericons', array() );
$tpl->set( 'footerlinks', array( 'places' => array( 'privacy', 'about', 'disclaimer' ) ) );
$tpl->set( 'content_actions', $content_actions );

$toolbox = array( 
	array( 'msg' => 'set-as-default-skin', 
		'href' => "javascript:if (confirm('" . addslashes( $I18N->msg( 'query-set-default-skin', array( 'domain' => 'skin', 'escape' => 'plain', 'variables' => array( $useskin ) ) ) ) .
		"') ) void(document.cookie = 'useskin=$useskin; path=/')" ), 
	array( 'msg' => 'set-default-lang', 'href'=> $I18N->getDashboardReturnToUrl(), 'id' => 'configure-intuition' ) );


$links = array();
$paramName = $I18N->getParamName( 'userlang' );

$availableLangs = $I18N->getAvailableLangs( false );
foreach( $availableLangs as $code => $name ) {
	if ( $I18N->getLang() == $code ) {
		$links[$code] = array( 'text' => $name );
		$links[$code]['class'] = 'active';
	} else {
		$links[$code] = array( 'text' => $name, 
		'href' => CurrentUrl( array( $paramName => $code ) ) );
	}
}
$twParams = http_build_query( array( 'title' => 'Special:Translate', 'language' => $I18N->getLang(), 'group' => "tsint-" . strtolower( $I18N->getDomain() ) ) );
$links['translate'] = array( 'msg' => 'translate-tool-msg', 'href'=>"http://translatewiki.net/w/i.php?$twParams", 'id' => 'translate' );
$tpl->set( 'language_urls', $links );

$skinLinks = array();
foreach ( $skins as $lowerName => $skinName ) {
	if ( $useskin == $lowerName ) {
		$skinLinks[$skinName] = array( 'text' => $skinName );
		$skinLinks[$skinName]['class'] = 'active';
	} else {
		$skinLinks[$skinName] = array( 'text' => $skinName, 
		'href' => CurrentUrl( array( SKIN_PARAM => $skinName ) ) );
	}
}
$tpl->set( 'sidebar', array( 'toolbox' => $toolbox, 'skins' => $skinLinks, 'LANGUAGES' => true, 'server-status' => ToolserverStatus::clusterLinkArrays(), 'SEARCH' => false, 'TOOLBOX' => false ) );

$wgLang = $I18N; /* Vector only uses $wgLang->isRTL() */

$tpl->execute();

//->msg( 'bl-changelanguage', 'tsintuition' );
register_shutdown_function( array( $tpl, 'afterContent' ) );

/**
 * Page content is now printed normally.
 * With an unmodified BaseTemplate, the content would
 * have been instead provided by using $tpl->set( 'bodytext', ... ); 
 */

