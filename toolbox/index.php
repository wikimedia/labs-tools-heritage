<?php
require_once ( 'toolbox.php' );

$toolboxPage = new ToolboxPage( $I18N );
echo $toolboxPage->getPageIntro();
?>

<div id="content">
	<h2>Home</h2>
	<p>this is only a starting point</p>
</div><!-- end content -->

<?php
echo $toolboxPage->getPageOutro();
