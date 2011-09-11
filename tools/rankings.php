<?php
/* Tool to get the rankings
 * By default from http://commons.wikimedia.org/wiki/Category:Images_from_Wiki_Loves_Monuments_2011
 * if country if given, one of the subcategories.
 */
header("Cache-Control: no-cache, must-revalidate");
header("Expires: Thu, 01 Jan 1970 00:00:00 GMT");
header('Content-type: text/html;; charset=utf-8');
?><!DOCTYPE html>
<html><head>
    <title></title>
    <style>
    * {
        margin:0;
        padding:0;
    }
    #photos-wlm {
        margin: 0;
        padding: 0;
    }

    #photos-wlm li {
        list-style-type: none;
    }

    #photos-wlm a {
        float: left;
        width: <?php echo $size; ?>px;
        height: <?php echo $size; ?>px;
        margin: 9px;
        background-repeat: no-repeat;
        background-position: center center;
    }
<?php
    if (isset($_GET['width'])) {
        echo 'table { width: '.$_GET['width']."; }\n\n";
    }
?>
    td {
        text-align: right;
    }
    td.lbl {
        text-align: left;
    }
    </style>
    <link media="all" type="text/css" href="/~ntavares/patrimonio/api/jscss/style.css" rel="stylesheet">
    <script src="/~ntavares/patrimonio/api/jscss/custom.js" type="text/javascript"></script>
<body>

<?
$i18n = array(
    'pt' => array(
        'Participant' => 'Participante',
        'Participating in' => 'Participa em',
        'Submissions' => 'Fotografias',
        'Accepted'    => 'Validadas',
        'Images'      => 'Lista de imagens',
        'Country'     => 'Pa&iacute;s',
        'Different Users'     => 'Participantes distintos',
        'User Ratio'  => 'Rácio por utilizador',
    ),
);

function _T($lbl) {
    global $i18n, $lang;
    if (isset($i18n[$lang][$lbl])) {
        return $i18n[$lang][$lbl];
    }
    return $lbl;
}

function getUserRankings($limit, $country, $showopts){
    //print "showopts: ".implode('|',$showopts)."\n";
    $ts_pw = posix_getpwuid(posix_getuid());
    $ts_mycnf = parse_ini_file($ts_pw['dir'] . "/.my.cnf");
//    $db = new mysqli('commonswiki-p.rrdb.toolserver.org',
    $db = new mysqli('sql-s2-rr.toolserver.org',
                     $ts_mycnf['user'],
		  $ts_mycnf['password'],
		    'commonswiki_p');
    $db->set_charset('utf-8');
    unset($ts_mycnf);
    unset($ts_pw);


    $limit = intval($limit);
    if($country) {
	    $category = 'Images_from_Wiki_Loves_Monuments_2011_in_' . $db->real_escape_string($country);
	    $categoryr = 'Reviewed_images_from_Wiki_Loves_Monuments_2011_in_' . $db->real_escape_string($country);
        $sql = 'SELECT u.user_name
                , COUNT(1) AS total
                , SUM(IF(cl2.cl_to IS NULL, 0, 1)) AS reviewed
                , GROUP_CONCAT(DISTINCT p.page_title SEPARATOR "[,]") AS images
                , INSTR(GROUP_CONCAT(DISTINCT ug.ug_group), "bot") AS found_bot
            FROM categorylinks cl 
            LEFT JOIN categorylinks cl2 ON cl2.cl_from = cl.cl_from
                AND cl2.cl_to = "'.$categoryr.'"
            JOIN page p ON cl.cl_from = p.page_id 
                AND p.page_namespace = 6 
                AND p.page_is_redirect = 0
            JOIN image i ON i.img_name = p.page_title
            JOIN user u ON u.user_id = i.img_user
            LEFT JOIN user_groups ug ON ug.ug_user = u.user_id
            WHERE cl.cl_to = "'.$category.'"
            GROUP BY u.user_name
            HAVING found_bot <= 0 OR found_bot IS NULL
            ORDER BY total DESC
            LIMIT '.$limit;
    } else {
	    $category = 'Images_from_Wiki_Loves_Monuments_2011';
	    $categoryr = 'Reviewed_images_from_Wiki_Loves_Monuments_2011';

        // I don't want to go to recentchanges to get the initial upload 
        // (Rotatebot will reupload a version of the image and be marked as the user_text)
        // So I just exclude the bots from the queries
        $sql = 'SELECT u.user_name
                , COUNT(1) AS total
                , SUM(IF(cl2.cl_to IS NULL, 0, 1)) AS reviewed
                , GROUP_CONCAT(DISTINCT cl3.country SEPARATOR "[,]") AS countries
                , count(DISTINCT cl3.country) AS n_countries
                , GROUP_CONCAT(DISTINCT p.page_title SEPARATOR "[,]") AS images
                , INSTR(GROUP_CONCAT(DISTINCT ug.ug_group), "bot") AS found_bot
            FROM categorylinks cl 
            LEFT JOIN categorylinks cl2 ON cl2.cl_from = cl.cl_from
                AND cl2.cl_to = "Reviewed images_from_Wiki_Loves_Monuments_2011"
            JOIN (SELECT cl.cl_from AS image_id, SUBSTR(cl3.cl_to, 42) AS country
                    FROM categorylinks cl 
                    JOIN categorylinks cl3 ON cl.cl_from = cl3.cl_from AND cl3.cl_to LIKE "Images_from_Wiki_Loves_Monuments_2011_in_%"
                    WHERE cl.cl_to = "Images_from_Wiki_Loves_Monuments_2011"
                    GROUP BY cl.cl_from
                    ) cl3 ON cl.cl_from = image_id
            JOIN page p ON cl.cl_from = p.page_id 
                AND p.page_namespace = 6 /* image */ 
                AND p.page_is_redirect = 0
            JOIN image i ON i.img_name = p.page_title
            JOIN user u ON u.user_id = i.img_user
            LEFT JOIN user_groups ug ON ug.ug_user = u.user_id
            WHERE cl.cl_to = "Images_from_Wiki_Loves_Monuments_2011"
            GROUP BY u.user_name
            HAVING found_bot <= 0 OR found_bot IS NULL
            ORDER BY /* n_countries DESC, */ total DESC
            LIMIT '.$limit;
    }

    //print "SQL: $sql\n";

    $result = $db->query($sql);

    echo '<table class="sortable">';
    echo '<tr><th>'._T('Participant').'</th><th>'._T('Submissions').'</th><th>'._T('Accepted').'</th>';
    if ( !$country ) {
        echo '<th>'._T('Participating in').'</th>';
    }
    if ( in_array('images', $showopts) ) {
        echo '<th>'._T('Images').'</th>';
    }
    echo '</tr>';
    while ($row = $result->fetch_assoc()) {
        if ( in_array('links', $showopts) ) {
                $username = '<a target="_blank" href="http://commons.wikimedia.org/wiki/Special:ListFiles/'.$row['user_name'].'">'.$row['user_name'].'</a>';
        } else {
                $username = $row['user_name'];
        }
        echo '<tr><td class="lbl">'.$username.'</td>';
        echo '<td>'.$row['total'].'</td><td>'.$row['reviewed'].'</td>';
        if ( !$country ) {
            $countries = explode('[,]', $row['countries']);
            $countries_a = array();
            for($i=0;$i<count($countries);$i++) {  
                if ( in_array('links', $showopts) ) {
                    $countries_a[] .= '<a target="_blank" href="rankings.php?limit='.$limit.'&show='.implode('|',$showopts).'&country='.$countries[$i].'">'.$countries[$i].'</a>';
                } else {
                    $countries_a[] .= $countries[$i];
                }
            }
            echo '<td>'.implode(',', $countries_a).' ('.$row['n_countries'].')</td>';
        }
        if ( in_array('images', $showopts) ) {
            $images = explode('[,]', $row['images']);
            // GROUP_CONCAT has default 1024 output limit. 
            // We use it to determine "..."
            $endmarker = '';
            if ( strlen($row['images']) > 1023 ) { 
                array_pop($images);
                $endmarker = '...';
            }
            $images_a = array();
            for($i=0;$i<count($images);$i++) {
                $images_a[] = '<a target="_blank" href="http://commons.wikimedia.org/wiki/Image:'.$images[$i].'">['.($i+1).']</a>';
            }
            echo '<td><small>'.implode(', ', $images_a).'</small>'.$endmarker.'</td>';
        }
        echo '</tr>';
    }
    echo '</table>';
}



function getCountryRankings($limit, $showopts) {
    //print "showopts: ".implode('|',$showopts)."\n";
    $ts_pw = posix_getpwuid(posix_getuid());
    $ts_mycnf = parse_ini_file($ts_pw['dir'] . "/.my.cnf");
    $db = new mysqli('commonswiki-p.rrdb.toolserver.org',
                     $ts_mycnf['user'],
		  $ts_mycnf['password'],
		    'commonswiki_p');
    $db->set_charset('utf-8');
    unset($ts_mycnf);
    unset($ts_pw);


    $sql = 'SELECT cl3.country
            , COUNT(1) AS n_images
            , COUNT(DISTINCT u.user_name) AS n_users
            , COUNT(1)/COUNT(DISTINCT u.user_name) AS user_ratio
        FROM categorylinks cl 
        JOIN (SELECT cl.cl_from AS image_id, SUBSTR(cl3.cl_to, 42) AS country
            FROM categorylinks cl 
            JOIN categorylinks cl3 ON cl.cl_from = cl3.cl_from AND cl3.cl_to LIKE "Images_from_Wiki_Loves_Monuments_2011_in_%"
            WHERE cl.cl_to = "Images_from_Wiki_Loves_Monuments_2011"
            GROUP BY cl.cl_from
            ) cl3 ON cl.cl_from = image_id
        JOIN page p ON cl.cl_from = p.page_id 
            AND p.page_namespace = 6 /* image */ 
            AND p.page_is_redirect = 0
        JOIN image i ON i.img_name = p.page_title
        JOIN user u ON u.user_id = i.img_user
        WHERE cl.cl_to = "Images_from_Wiki_Loves_Monuments_2011"
        GROUP BY cl3.country
        ORDER BY n_images DESC
        LIMIT '.$limit;

    //print "SQL: $sql\n";

    $result = $db->query($sql);

    echo '<table class="sortable">';
    echo '<tr><th>'._T('Country').'</th><th>'._T('Submissions').'</th><th>'._T('Different Users').'</th><th>'._T('User Ratio').' (%)</th></tr>';
    while ($row = $result->fetch_assoc()) {
        if ( in_array('links', $showopts) ) {
                $country = '<a target="_blank" href="rankings.php?limit='.$limit.'&show='.implode('|',$showopts).'&country='.$row['country'].'">'.$row['country'].'</a>';
                $images = '<a target="_blank" href="http://commons.wikimedia.org/wiki/Category:Images from Wiki Loves Monuments 2011 in '.$row['country'].'">'.$row['n_images'].'</a>';
        } else {
                $country = $row['country'];
                $images = $row['n_images'];
        }
        $users = $row['n_users'];
        $user_ratio = sprintf("%.2f", $row['user_ratio']); // .' %'; // this breaks sorting :(

        echo '<tr>';
        echo '<td class="lbl">'.$country.'</td>';
        echo '<td>'.$images.'</td>';
        echo '<td>'.$users.'</td>';
        echo '<td>'.$user_ratio.'</td>';
        echo '</tr>';
    }
    echo '</table>';
}



$limit = 30;
if (isset($_GET['limit'])) {
    $limit = $_GET['limit'];
}

$lang = 'en';
if (isset($_GET['lang'])) {
    $lang = $_GET['lang'];
}

$show = ''; // images
if (isset($_GET['show'])) {
    $show = $_GET['show'];
}
$showopts = explode('|', $show);

$scope = 'user'; // images
if (isset($_GET['scope'])) {
    $scope = $_GET['scope'];
}

if ( $scope === 'user' ) {
    getUserRankings($limit, $_GET['country'], $showopts);
} else {
    getCountryRankings($limit, $showopts);
}

?>
</body>
</html>
