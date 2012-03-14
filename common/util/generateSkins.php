<?php

if ( isset($_SERVER['REQUEST_METHOD']) ) {
	die( "I am not a web script" );
}

$IP = "../../../../regression";
$skinpath = "$IP/skins";
$targetdir = __DIR__ . "/../skins";

@mkdir( $targetdir );

$d = opendir( $skinpath );
while ( ( $filename = readdir( $d ) ) !== false ) {
	if ( !preg_match( '/^[A-Za-z]+\.php$/', $filename ) ) {
		continue;
	}
	
	echo  "$filename\n";
	
	$in = fopen( "$skinpath/$filename", "rt" );
	$out = false;
	
	while ( ( $l = fgets( $in ) ) !== false ) {
		if ( !$out ) {
			if ( preg_match( '/^class .*Template extends BaseTemplate {\n$/', $l ) ) {
				$out = fopen( "$targetdir/$filename", "w" );
				fputs( $out, "<?php\n$l" );
			}
		} else {
			if ( preg_match( "/<\?php \\\$this->html\( ?'bodytext' ?\) \?>\n/", $l ) ) {
				fputs( $out, "<?php\n}\n\n	function afterContent() {\n?>\n" );
			} else {
				$l = preg_replace( '/(\$[A-Za-z]+) = wfMessage\( (\$[A-Za-z]+) \); echo htmlspecialchars\( \1->exists\(\) \? \1->text\(\) : \2 \);/', 'global $I18N; echo $I18N->msg( \\2, array( "domain" => "skin", "escape" => "html" ) );', $l );
				$l = str_replace( ", 'SEARCH'", '', $l ); # Vector call to renderNavigation()
				$l = str_replace( "wfUILang()", '$GLOBALS["I18N"]', $l );
				fputs( $out, $l );
			}
		}
	}
	
	fclose( $in );
	if ( $out )
		fclose( $out );
}

