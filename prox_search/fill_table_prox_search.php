<?
error_reporting(E_ALL);
ini_set('display_errors', true);
ini_set('html_errors', false);

require('/home/project/e/r/f/erfgoed/public_html/api/includes/clsBasicGeosearch.php');


function connect_monuments_db() {
    $host = 'sql.toolserver.org';
    $database = 'p_erfgoed_p';

    $ts_pw = posix_getpwuid(posix_getuid());
    $ts_mycnf = parse_ini_file($ts_pw['dir'] . "/.my.cnf");
    $db = mysql_connect($host, $ts_mycnf['user'], $ts_mycnf['password']);
    unset($ts_mycnf, $ts_pw);
    if (!$db) {
        die('Not connected : ' . mysql_error());
    }

    $db_selected = mysql_select_db($database, $db); 
    if (!$db_selected) {
        die('Can\'t use db : ' . mysql_error());
    }    
    
    $init_query = "SET NAMES 'utf8' COLLATE 'utf8_unicode_ci'";
    mysql_query($init_query);
    
    return $db;
} //func


//main

$bg = new clsBasicGeosearch();

connect_monuments_db();


$query = "SELECT `country`, `lang`, `id`, `lat`, `lon`
       FROM `monuments_all`
	   WHERE (lat <>0 AND lon<>0)";


   
$result = mysql_query($query);

if (!$result) 
{
  die('Invalid query: ' . mysql_error());
}

while ($row = @mysql_fetch_assoc($result)) {

	if ( $row['lat'] >= -90 and $row['lat'] <= 90 and 
	     $row['lon'] >= -180 and $row['lon'] <= 180 ) {
		 
		$peano1 = $bg->generate_peano1($row['lat'], $row['lon']);	
		$peano2 = $bg->generate_peano2($row['lat'], $row['lon']);
		$peano1iv = $bg->generate_peano_iv($peano1);
		$peano2iv = $bg->generate_peano_iv($peano2);
	
		$r_query = sprintf("TRUNCATE TABLE prox_search;
		REPLACE INTO `prox_search` (mon_country, mon_lang, mon_id, lat, lon, int_peano1, int_peano2, int_peano1iv, int_peano2iv)
                     VALUES ('%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s');",
                 $row['country'],
                 $row['lang'],
                 $row['id'],
                 $row['lat'],
                 $row['lon'],
				 $peano1,
				 $peano2,
				 $peano1iv,
				 $peano2iv);
		$r_result = mysql_query($r_query);
		if (!$r_result) {
			die('Invalid query: ' . mysql_error());
		}
	} else {
		echo('Location data out of range: ');
		print_r($row);
	}
}
