<?php

/***
 * This library reads the and parses them to show appropiate messages 
 * to the users.
 * The file format is documented at
 *  http://lists.wikimedia.org/pipermail/toolserver-l/2007-September/000912.html
 * and in the comments at the top of the file.
 */
 
 
class ToolserverStatus {

	/**
	 * List of clusters
	 * @const
	 */
	static public $databaseClusters = array( 's1', 's2', 's3', 's4', 's5', 's6', 's7', 'sql', 'sql-toolserver' );

	/* Constants for the status levels */
	const LEVEL_OK = 0;
	const LEVEL_INFO = 1;
	const LEVEL_WARN = 2;
	const LEVEL_DOWN = 3;
	const LEVEL_ERRO = 4;
	const LEVEL_UNKNOWN = 7;
	const LEVEL_MISSING = 8;
	

	static protected $clusterStatus = array();

	/**
	 * Returns the filename for a given cluster
	 */
	static public function filenameFromClusterName($clusterName) {
		# We access the status files through /var/www which is the
		# documented path, although currently (August 2011) /var/www
		# is just a symlink to /www

		return "/var/www/status_$clusterName";
	}

	/**
	 * Given a status file, read the status line
	 */
	static function statusLineFromFile ($filename) {
		/**
		 * Suppress errors if the files are missing.
		 * (eg. this happenned 2011-06-01)
		 */

		$file = @fopen( $filename, "rt" );
		 
		if ( $file === false )
			return false;
		
		$line = false;
		while ( ( $line = fgets( $file ) ) !== false ) {
			if ( strlen( $line ) && $line[0] != '#' ) {
				break;
			}
		}
		
		fclose( $file );
		
		return $line;
	}

	/**
	# Returns the status for any given cluster:
	# Possible values are:
	# OK: 
	#	All Ok, nothing to show.
	#
	# INFO: 
	#	A Information (like a planed maintaince in far future).
	#	Please show the line in your tools as information.
	#
	# WARN:
	#	A Warning (like a planed maintaine in near future).
	#	Please show the line in your tools.
	#
	# ERRO:
	#	An Error (like a unplaned maintaice)
	#	Please show the text instead of your tools
	#	(or be very sure that your tools do work).
	#
	# DOWN:
	#	Like ERRO, but planed.
	#
	# UNKNOWN:
	# 	The status files are missing or do not provide one of the above states.
	#
	# MISSING:
	#	The user provided a bad cluster name.
	*/
	static function getClusterStatus($clusterName) {
		list( $status ) = self::getClusterStatusAndText( $clusterName );
		return $status;
	}

	/**
	 * Return the cluster status as a numeric ToolserverStatus::LEVEL_* constant.
	 */
	static function getClusterStatusLevel($clusterName) {
		return constant( "self::LEVEL_" . self::getClusterStatus( $clusterName ) );
	}

	/**
	 * Returns the status of the cluster and its text if anything goes wrong
	 * 
	 * list($status, $text) = ToolserverStatus::getClusterStatusAndText('s1');
	 */
	static function getClusterStatusAndText($clusterName) {
		if ( !isset( self::$clusterStatus[$clusterName] ) ) {
			if ( !in_array( $clusterName, self::$databaseClusters ) )
				return array( 'MISSING', '' );
			
			$line = self::statusLineFromFile( self::filenameFromClusterName( $clusterName ) );
			if ( $line === false ) { $line = ''; }
			$line = rtrim( $line );
			
			$s = explode( ';', $line, 2 ) + array('','');
			if ( !in_array( $s[0], array( 'OK', 'INFO', 'WARN', 'ERRO', 'DOWN' ) ) ) {
				$s = array( 'UNKNOWN', '' );
			}
			self::$clusterStatus[$clusterName] = $s;
		}
		return self::$clusterStatus[$clusterName];
	}
	
	/**
	 * Provides an array with suitable class and text for the given cluster
	 * @param $clusterName Name of the cluster for which the link is requested
	 */
	static function clusterLinkArray($clusterName) {
		global $I18N;
		
		$status = strtolower( self::getClusterStatus( $clusterName ) );

		return array(
			'class' => "cluster-status cluster-$clusterName-$status cluster-$status",
			'text' => $I18N->msg( "toolserver-status-short-$status", array( 'domain' => 'toolserverstatus', 'escape' => 'plain', 'variables' => array( $clusterName ) ) )
			);
	}
	
	static function clusterLinkArrays($databaseClusters = '*') {
		if ( $databaseClusters == '*' ) {
			$databaseClusters = self::$databaseClusters;
		}
		foreach ( $databaseClusters as &$entry ) {
			$entry = self::clusterLinkArray( $entry );
		}
		return $databaseClusters;
	}
	
	/**
	 * Returns the html of a pretty box. See documentation of showPrettyBox()
	 */
	static function prettyBox($databaseClusters = '*', $fromLevel = self::LEVEL_INFO) {
		if ( $databaseClusters == '*' ) {
			$databaseClusters = self::$databaseClusters;
		}
		
		$box = '';
		foreach( $databaseClusters as $cluster ) {
			global $I18N;
			
			if ( self::getClusterStatusLevel( $cluster ) >= $fromLevel ) {
				list( $status, $text ) = self::getClusterStatusAndText( $cluster );
				
				$msg = $I18N->msg( 'toolserver-status-' . strtolower( $status ), 
					array( 'domain' => 'toolserverstatus', 'escape' => 'html', 'variables' => array( $cluster, $text ) ) );
				$box .= "<li>$msg</li>";
			}
		}
		
		return $box ? "<ul>$box</ul>" : '';
	}
	
	/**
	 * Show a box with the status of the given clusters.
	 * @param $databaseClusters Array of clusters to check
	 * @param $fromLevel ToolserverStatus::LEVEL_* enum  Show a message from this level onwards
	 *  Remember that for ERRO and DOWN you MUST show the text, so at most it should be LEVEL_DOWN
	 */
	static function showPrettyBox($databaseClusters = '*', $fromLevel = self::LEVEL_INFO) {
		echo self::prettyBox( $databaseClusters, $fromLevel );
	}
}
