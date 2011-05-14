<?php
/*
 * Class to take care of database connections
 */
?>

class monumentsDatabase {
    public function connect() {
	mysql_connect('sql.toolserver.org',$toolserver_username,$toolserver_password);
	@mysql_select_db('p_erfgoed_p') or print mysql_error();
    }
}

