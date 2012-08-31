<?php
/* Tool to get the latest uploaded files for Wiki Loves Monuments
 * By default from http://commons.wikimedia.org/wiki/Category:Images_from_Wiki_Loves_Monuments_2012
 * if country if given, one of the subcategories.
 * TODO: Implement subcats
 */
header("Cache-Control: no-cache, must-revalidate");
header("Expires: Thu, 01 Jan 1970 00:00:00 GMT");
header('Content-type: text/javascript;; charset=utf-8');
function getLatest($size, $number, $country){
    $ts_pw = posix_getpwuid(posix_getuid());
    $ts_mycnf = parse_ini_file($ts_pw['dir'] . "/.my.cnf");
    $db = new mysqli('commonswiki-p.rrdb.toolserver.org',
                     $ts_mycnf['user'],
		  $ts_mycnf['password'],
		    'commonswiki_p');
    $db->set_charset('utf-8');
    unset($ts_mycnf);
    unset($ts_pw);
    
    if($country) {
	$category = 'Images_from_Wiki_Loves_Monuments_2012_in_' . $db->real_escape_string($country);
    } else {
	$category = 'Images_from_Wiki_Loves_Monuments_2012';
    }

    $result = $db->query("SELECT rc_title, img_width, img_user_text, img_timestamp
    FROM recentchanges
    JOIN page ON (rc_namespace=page_namespace AND rc_title=page_title)
    JOIN categorylinks ON page_id=cl_from
    JOIN image ON rc_title=img_name
    WHERE rc_namespace = 6
    AND rc_log_type='upload'
    AND rc_log_action='upload'
    AND page_namespace =6
    AND page_is_redirect=0
    AND cl_to='" . $category . "'
    ORDER BY rc_timestamp DESC
    LIMIT " . $number);
    
    $returnResult = array();
    $firstrow = True; 

    while ($row = $result->fetch_assoc()) {
	$upload = array();
	$upload['title'] = $row['rc_title'];
	$upload['uploader'] = $row['img_user_text'];
	$upload['timestamp'] = $row['img_timestamp'];
	$upload['url'] = "http://commons.wikimedia.org/wiki/Image:" . $row['rc_title'];

	$hash = md5($row['rc_title']);
	$fullimg = "http://upload.wikimedia.org/wikipedia/commons/" . $hash[0] . "/" . $hash[0] . $hash[1] . "/" . $row['rc_title'];
	$thumbprefix = "http://upload.wikimedia.org/wikipedia/commons/thumb/"  . $hash[0] . "/" . $hash[0] . $hash[1] . "/" . $row['rc_title'];
    
	if (!($size==-1) && $size < $row['img_width']) {
	    $upload['image'] = $thumbprefix . "/" .  (int)$_GET["size"] . "px-" . $title;
	} else {
	    $upload['image'] = $fullimg;
	}
	$returnResult[]=$upload;
    }
    return json_encode($returnResult);
}

$size=-1;
if (isset($_GET["size"])) {
    $size=(int)$_GET["size"];
}
$number=5;
$max_number=20;
if (isset($_GET["number"])) {
    $number=(int)$_GET["number"];
    if ($number > $max_number) {
	$number = $max_number;
    }
}
$country = '';
if (isset($_GET["country"])) {
    $country = $_GET["country"];
}


$jsonData = getLatest($size, $number, $country);
echo $_GET['callback'] . '(' . $jsonData . ');';

