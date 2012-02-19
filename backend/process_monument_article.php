<?
// extract wikilinks where needed from monuments_all.monument_article field
// read conf from fill_table_monuments_all.sql

error_reporting(E_ALL);
ini_set('display_errors', true);
ini_set('html_errors', false);


//functions

function mb_ucasefirst($str) { 
    $str[0] = mb_strtoupper($str[0]); 
    return $str; 
} 

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

function read_conf( $in_file_name ) {
    $out_wikilinks_arr = array();
    
    $sql_file = file_get_contents( $in_file_name );
    
    preg_match_all("/(REPLACE INTO .+?;)/is",
                $sql_file , $matches);
    
    $replace_statements = $matches[0];
    
    foreach ( $replace_statements as $statement ) {
        if ( preg_match("/monument_article.+?WIKILINK/", $statement) ) {
            //print $statement;
            $country = '';
            $lang = '';
            if ( preg_match("/'([\w\-]+)'.+?`country`/", $statement, $matches) ) {
                $country = $matches[1];
            }
            if ( preg_match("/'([\w\-]+)'.+?`lang`/", $statement, $matches) ) {
                $lang = $matches[1];
            }
            if ( $country and $lang ) {
                $out_wikilinks_arr[] = array("country" => $country, "lang" => $lang);
            } else {
                die("Coudn't match country and lang from: $statement");
            }
        }
    }
    
    return $out_wikilinks_arr;
    
} //func


//main

$fill_sql_file = '/home/project/e/r/f/erfgoed/erfgoedbot/sql/fill_table_monuments_all.sql';

$get_wikilinks_arr = read_conf( $fill_sql_file );

//print_r( $get_wikilinks_arr );

if ( $get_wikilinks_arr ) {
    
    connect_monuments_db();

    foreach ( $get_wikilinks_arr as $get_wikilink ) {
        $update_count = 0;
        $query = sprintf("SELECT monument_article, id FROM `monuments_all` 
        WHERE monument_article <> '' AND country = '%s' AND lang = '%s'",
                 $get_wikilink['country'],
                 $get_wikilink['lang'] );
   
        $result = mysql_query($query);

        if (!$result) {
            die('Invalid query: ' . mysql_error());
        }

        while ($row = @mysql_fetch_assoc($result)) {

            if ( $row['monument_article'] ) {
                $wikilink = '';
                if ( preg_match("/\[\[(.+?)(\||\])/", $row['monument_article'], $matches) ) {
                    $wikilink = $matches[1];
                    $wikilink = str_replace(" ", "_" , $wikilink);
                    #wikipedia page titles should be upper case first
                    $wikilink = mb_ucasefirst($wikilink);
                }
            
                $update_query = sprintf("UPDATE `monuments_all` SET monument_article = '%s'
                    WHERE country = '%s' AND lang = '%s' AND id = '%s'",
                    $wikilink,
                    $get_wikilink['country'],
                    $get_wikilink['lang'],
                    $row['id']);
                $r_result = mysql_query($update_query);
                if (!$r_result) {
                    die('Invalid query: ' . mysql_error());
                }
                $update_count++;
            }
        }  // while
        
        print "Updated $update_count rows for: " . $get_wikilink['country'] . ":" . $get_wikilink['lang'] . "\n";
    }  // foreach

} // if