/*
    LightRod OAR Browser
    
    Copyright (C) 2001 - 2010  High Country Software Ltd.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see http://www.gnu.org/licenses/.



Usage:
	See http://www.lightrod.org/  'LightRod OAR Browser' section for the most up-to-date instructions.

Based on AlienGoggles.com code by Philip Abrahamson

For assistance:
	peter AT lightrod.org
	or the LightRod forums
*/


function test_func() {
	alert('In test func');
	return;
}



var map;

// this global (we tried a closure but it was returning a function pointer instead of a value) is used to 
// determine whether we submit form lpf (true) or not (false) once we have coordinates returned.
var atl_submit_on_success = false;

// global that is either 'search' or 'manage' which is used to modify messages intended for searchers, or people managing products
var atl_scenario = 'search';

// global defaults
var default_latitude = 0;
var default_longitude = 0;
var default_accuracy = 0;



function find_location () {

	//alert('In here a');

    var latitude = '';
    var longitude = '';
    var accuracy = '';
    // lookup the cookie - if available
    var last_location = get_location_cookie();
    if (last_location) {
	latitude = (last_location.latitude === '') ? default_latitude : last_location.latitude;
	longitude = (last_location.longitude === '') ? default_longitude : last_location.longitude;
	accuracy = (last_location.accuracy === '') ? default_accuracy : last_location.accuracy;
	home_url = (last_location.accuracy === '') ? default_accuracy : last_location.home_url;
    } else {
	latitude = default_latitude;
	longitude = default_longitude;
	accuracy = default_accuracy;
    }
    document.lpf.lat.value = latitude;
    document.lpf.lon.value = longitude;
    document.lpf.acc.value = accuracy;
     if(document.srch) {
    	document.srch.lat.value = latitude;
    	document.srch.lon.value = longitude;
    }


	//alert('Press OK to find your location now');

	if(geo_position_js.init()){
		document.getElementById("location_message").innerHTML = ''; //Click the "Share Location" button above to begin Geolocating...';
		geo_position_js.getCurrentPosition(location_func_pointer,no_location,{enableHighAccuracy:true});
	}
	else {
		if(typeof(window.blackberry)!="undefined") {
						//A Blackberry without location sharing
						alert("This location browser requires you to set the option Browser->General->Javascript Location Support to 'enabled' on your Blackberry so that it can search from your location.  Only Blackberries with GPS are known to be supported.");
								                        	
                }
		no_location();
	}


    /* W3C method:
    if (navigator.geolocation) {
	document.getElementById("location_message").innerHTML = ''; //Click the "Share Location" button above to begin Geolocating...';
        navigator.geolocation.getCurrentPosition(location_func_pointer);
    } else {
	document.getElementById("location_message").innerHTML = 'Zoom into your location by clicking on this map';
	//alert('****latitude = ' + latitude + ' longitude = ' + longitude + ' accuracy = ' + accuracy + '****');
	initialize_oar_map(latitude,longitude,accuracy);
    }*/
    return;
}


function no_location () {

        //alert("Lat:" + document.lpf.lat.value + " Lon:" + position.coords.longitude + " Accuracy:" + accuracy);  //Testing


	document.getElementById("location_message").innerHTML = 'Zoom into your location by <span class=\'phone-only\' >double </span>clicking on this map';
	//alert('****latitude = ' + latitude + ' longitude = ' + longitude + ' accuracy = ' + accuracy + '****');
	initialize_oar_map(document.lpf.lat.value,document.lpf.lon.value,document.lpf.acc.value);

}

function location_func_pointer (position) {
    document.lpf.lat.value = position.coords.latitude;
    document.lpf.lon.value = position.coords.longitude;
    if(document.srch) {
    	document.srch.lat.value = position.coords.latitude;
    	document.srch.lon.value = position.coords.longitude;
    }
    
    //Set accuracy if it doesn't exist
    if(!position.coords.accuracy) {
    	var accuracy = 0;
    } else {
    
    	var accuracy = position.coords.accuracy;
    }
    
    //alert("Lat:" + position.coords.latitude + " Lon:" + position.coords.longitude + " Accuracy:" + accuracy);  //Testing
    
    //Blackberry has 0 accuracy: if (accuracy) {
	if (document.lpf.acc) {
	    document.lpf.acc.value = accuracy;
	}
	
	
	if(accuracy >= 0) {  //TODO: can make this 1000
	    location_found_message(accuracy, 'geo');
	    //initialize_oar_map(position.coords.latitude, position.coords.longitude, accuracy);	
	} else {
	    if (atl_submit_on_success == true) {
		document.lpf.submit();
	    } else {
		location_found_message(accuracy, 'geo');
	    }
	}
    //Blackberry has 0 accuracy
    //} else {
	//document.getElementById("location_message").innerHTML = "Sorry, but your location could not be found!";
    //}
    return;
}

function map_finish_mesage() {
    var finish_message = '';
    if (atl_submit_on_success == false) {
	if (atl_scenario == 'manage') {
	    // special message while editing shop data
	    finish_message = "You are ready to continue";
	} else {
	    if(atl_scenario == 'adminpanel') {
	    	finish_message = "Copy the latitude and longitude into the POI fields above.";
	    } else {
	    	finish_message = "Ready to browse."; //"You are ready to find products from this location";
	    	//document.lpf.s.focus();
	    }
	}
    } else {
	finish_message = "Browsing from this location now...";
    }
    return finish_message;
}

function initialize_oar_map(my_lat, my_long, my_accuracy) { //lat, long, accuracy) {

	   var hybrid_cutoff = 14; // zoom level at which to become a hybrid map
	    if (isNaN(my_lat)) {
		my_lat = 0;
	    }
	    if (isNaN(my_long)) {
		my_long = 0;
	    }
	    if (isNaN(my_accuracy)) {
		my_accuracy = 0;
	    }
	    //alert('****latitude = ' + my_lat + ' longitude = ' + my_long + ' accuracy = ' + my_accuracy + '****');
	    var start_zoomlevel;
	    if (my_accuracy && my_accuracy != 0) {
		//alert ('zoomed map - accuracy is true -- accuracy="' + my_accuracy + '"');
		// note this zoomlevel is recalculated in get_limits_from_radius() for compatible browsers 
		start_zoomlevel = 15;
		map_message();
	    } else {
		//alert ('world map - accuracy is false');
		start_zoomlevel = 1;
		world_map_message();
	    }
	    if (GBrowserIsCompatible()) {
	      	document.getElementById('map_canvas').style.display = 'block';
	        map = new GMap2(document.getElementById("map_canvas"));
	        map.setCenter(new GLatLng(my_lat, my_long), start_zoomlevel);
	        map.setUIToDefault();
	
		// set the zoom level accurately depending on the browser type
		get_limits_from_radius(my_accuracy, my_lat, my_long);
	
		// set the map type depending on the zoom level too 
		zoomlevel = map.getZoom();
		if (zoomlevel > hybrid_cutoff) {
		    map.setMapType(G_HYBRID_MAP);
		} else {
		    map.setMapType(G_NORMAL_MAP);
		}
	
		// Recenter Map and add Coords by clicking the map
		GEvent.addListener(map, 'click', function(overlay, point) {
			document.lpf.lat.value=point.y;
			document.lpf.lon.value=point.x;
			if(document.srch) {
			 	document.srch.lat.value = point.y;
			   	document.srch.lon.value = point.x;
			}
			
			zoomlevel = map.getZoom();
			if (zoomlevel > hybrid_cutoff) {
			    map.setMapType(G_HYBRID_MAP);
			} else {
			    map.setMapType(G_NORMAL_MAP);
			}
			var zoomin = 3;
			if (zoomlevel > 8) {
			    zoomin = 2;
			}
			if (zoomlevel > 12) {
			    zoomin = 1;
			}
			if(zoomlevel > 17) { // was 16
			    close_map();
			} else {
			    map.setCenter(new GLatLng(point.y, point.x), zoomlevel + zoomin);		//Zoom in
			}
		    });
		  
		  
		  //Adds coords when move the map too  
		 GEvent.addListener(map, 'moveend', function() {
		 	center = map.getCenter();
		 	document.lpf.lat.value=center.lat();
			document.lpf.lon.value=center.lng();
			if(document.srch) {
			 	document.srch.lat.value = center.lat();
			   	document.srch.lon.value = center.lng();
			}
	
		  }); 
		 
		   //Adds coords when double click the map too  
		  GEvent.addListener(map, 'dblclick', function(overlay, point) {
		  	document.lpf.lat.value=point.y;
			document.lpf.lon.value=point.x;
		  	if(document.srch) {
			 	document.srch.lat.value = point.y;
			   	document.srch.lon.value = point.x;
			}
		  	
		  	zoomlevel = map.getZoom();
			if (zoomlevel > hybrid_cutoff) {
			    map.setMapType(G_HYBRID_MAP);
			} else {
			    map.setMapType(G_NORMAL_MAP);
			}
			var zoomin = 3;
			if (zoomlevel > 8) {
			    zoomin = 2;
			}
			if (zoomlevel > 12) {
			    zoomin = 1;
			}
			if(zoomlevel > 17) { // was 16
			    close_map();
			} else {
			    map.setCenter(new GLatLng(point.y, point.x), zoomlevel + zoomin);		//Zoom in
			}
		  });  
		  
		   
	    }
}

function close_map() {
    document.getElementById('map_canvas').style.display = 'none';
    document.lpf.acc.value=calculate_accuracy_from_zoomlevel();
    location_found_message( document.lpf.acc.value || 0, 'map' );
    if (atl_submit_on_success == true) {
	document.lpf.submit();
    }
    return;
}
function calculate_accuracy_from_zoomlevel() {
    var bounds = map.getBounds();
    var southWest = bounds.getSouthWest();
    var northEast = bounds.getNorthEast();
    //var lngSpan = northEast.lng() - southWest.lng();
    var latSpan = northEast.lat() - southWest.lat();
    // Now convert the latitude from decimal degrees into metres
    // lat/360 = delta-y/circumference of world 
    // => delta-y = lat * circum-world/360 = lat * 2piR/360 = lat * piR/180
    var piR_over_180 = 111195; //= (3.1415927*6371000)/180 in metres
    var delta_y = latSpan * piR_over_180;
    var radius = parseInt(delta_y / 2); 
    return radius;
}

function get_limits_from_radius(radius_meters, latitude, longitude) {

    //Function sets $this->top_left_latitude = 90.0;
    //		$this->top_left_longitude = -180.0;
    //		$this->bottom_right_longitude = 180.0;
    //		$this->bottom_right_latitude = -90.0;	
    //with a square around latitude/longitude based on the radius
    //Radius = 6371 km (959 mi).

    var bottom_right_longitude;
    var top_left_longitude;
    var top_left_latitude;
    var bottom_right_latitude;

    if ( (! radius_meters)||(radius_meters == 0)) {

	//alert ('no radius_meters = ' + radius_meters);

	// Special case entry - set the map to world size
	//bottom_right_longitude = 180;
	//top_left_longitude = -180;
	//top_left_latitude = 90;
	//bottom_right_latitude = -90;

	//alert ('about to hardcode the map to zoom level 1');
	map.setZoom(1);	

    } else {

	//alert ('radius_meters = ' + radius_meters);

	radius = radius_meters/1000;	//Get km

	pi = 3.1415927;
	two_pi_r_by_360 = 0;
	c360_by_two_pi_r = 0.008993216; //= 360/(2*3.1415927*6371)

	pi_over_180 = 0.0174533; //pi/180 is the degree to radian converter		


	//get the latitude of the current position in radians so
	//it can be used in cos(lat) to calculate how much to scale x
	lat_radians = latitude * pi_over_180;

	//y deg = dist * 360 / 2 PI R
	//x deg = dist * cos (latitude) * 360 / 2 PI R
	dx = (c360_by_two_pi_r * Math.cos(lat_radians)) * radius; //in km units
	dy = c360_by_two_pi_r * radius; //in km units

	//alert ('dx = ' + dx + ' dy = ' + dy);
	//alert ('longitude = ' + longitude + ' latitude = ' + latitude);
	//alert ('longitude + dx = ' + (longitude + dx));
	//alert ('longitude - dx = ' + (longitude - dx));
	//alert ('latitude + dy = ' + (latitude + dy));
	//alert ('latitude - dy = ' + (latitude - dy));
	//echo "Dx= $dx  Dy=$dy";
	// The following (+number) convert strings into numbers
	// stupid javascript was concatenating strings instead of adding numbers
	bottom_right_longitude = (+longitude) + (+dx);
	top_left_longitude = (+longitude) - (+dx);
	top_left_latitude = (+latitude) + (+dy);
	bottom_right_latitude = (+latitude) - (+dy);
		
	//Change zoom level to size of place
	nw = new GLatLng(top_left_latitude, top_left_longitude , true);
	se = new GLatLng(bottom_right_latitude, bottom_right_longitude , true);
	//alert ('nw = ' + nw + ' se = ' + se);
	bounds = new GLatLngBounds(nw, se);
	//alert('About to set the map to zoom level: ' + map.getBoundsZoomLevel(bounds));
	map.setZoom(map.getBoundsZoomLevel(bounds));

    }
		
    return; 
}

function location_found_message(accuracy, via_map_or_geo) {
    // accuracy is in metres, via_map_or_geo is how this location was found (geolocation, or from clicking on a map)
    
    
    var readable_accuracy;
    var fine_tune_vs_edit = (accuracy >= 1000) ? 'Fine-tune&nbsp;your&nbsp;location' : 'Change&nbsp;your&nbsp;location';
    if (accuracy > 1000) {
	// round the accuracy to the nearest km
	readable_accuracy = parseInt((accuracy + 500) / 1000) + ' km';
    } else {
	readable_accuracy = parseInt(accuracy) + ' meters';
    }
    var location_verb = (via_map_or_geo == 'geo') ? 'Geolocated' : 'located';
    var location_sentence = 'Accuracy: ' + readable_accuracy + '.';
    // Turn off location sentence if the accuracy is sufficiently high
    //if (accuracy < 1000) { 
    //	location_sentence = ''; 
    //}
    // Turn off location sentence if the user clicked on a map
    if (via_map_or_geo == 'map') { 
	location_sentence = ''; 
    }
    
    //Pete: taken away ||0 on locations, that may not work on google phone browser  alert(document.lpf.lat.value+\' \'+document.lpf.lon.value);
    
    if(atl_scenario == 'adminpanel') {
    	var saveLocationButton = '';
    } else {
    	var saveLocationButton = '<button onclick="set_location_cookie((document.lpf.lat.value), (document.lpf.lon.value), (document.lpf.acc.value)); return false;" style="margin:3px; font-weight:normal"><small>Save location</small></button>';
    }
    
    document.getElementById("location_message").innerHTML = map_finish_mesage() + ' ' + location_sentence + '<br/>' + saveLocationButton + '<button onclick="initialize_oar_map((document.lpf.lat.value || 0), (document.lpf.lon.value || 0), (document.lpf.acc.value || 0)); return false;" style="margin:3px; font-weight:normal"><small>' + fine_tune_vs_edit + '</small></button>';

    searchAgainIfResults();

    return;
}

function map_message() {
    document.getElementById("location_message").innerHTML = "Keep <span class=\'phone-only\' >double </span>clicking on your location to zoom in and set it<br/>" + clear_location_link() + ' ' + close_map_link();
    return;
}

function world_map_message() {
    document.getElementById("location_message").innerHTML = "Keep <span class=\'phone-only\' >double </span>clicking on your location to zoom in and set it<br/>" + clear_location_link() + ' ' + close_map_link();
    return;
}

function close_map_link() {
    return "<button onclick=\"close_map(); return false;\" style=\"margin:3px; font-weight:normal\"><small>Finish</small></button>";
}

function clear_location_link() {
    return "<button onclick=\"document.lpf.lat.value=0;document.lpf.lon.value=0;document.lpf.acc.value=0;initialize_oar_map(0,0,0); clear_location_cookie(); return false;\" style=\"margin:3px; font-weight:normal\"><small>Reset</small></button>";
}

function get_location_cookie() {

    var location = {}; // hash with latitude, longitude, accuracy properties
    if (document.cookie) {
       var reg_exp = /latitude=([^\;]*)/; // match cookie format "latitude=..." for example
       var match = reg_exp.exec(document.cookie);
       if (match) {
	   location.latitude = match[1];
       }
       reg_exp = /longitude=([^\;]*)/; // match cookie format "longitude=..." for example
       match = reg_exp.exec(document.cookie);
       if (match) {
	   location.longitude = match[1];
       }
       reg_exp = /accuracy=([^\;]*)/; // match cookie format "accuracy=..." for example
       match = reg_exp.exec(document.cookie);
       if (match) {
	   location.accuracy = match[1];
       }
       var reg_exp = /home=([^\;]*)/; // match cookie format "latitude=..." for example
       var match = reg_exp.exec(document.cookie);
       if (match) {
	   location.home = match[1];
       }
       
    }

    return (location);
}

function set_location_cookie(latitude, longitude, accuracy, gmapzoom) {

    // set the cookie expiration date far in future.
    document.cookie = 'latitude=' + latitude + '; path=/; expires=Thu,31-Dec-2020 00:00:00 GMT;';
    document.cookie = 'longitude=' + longitude + '; path=/; expires=Thu,31-Dec-2020 00:00:00 GMT;';
    document.cookie = 'accuracy=' + accuracy + '; path=/; expires=Thu,31-Dec-2020 00:00:00 GMT;';

}

function clear_location_cookie() {

    // delete the cookies by setting an expiration date in the past.
    if (document.cookie) {
	document.cookie = 'latitude=; path=/; expires=Sat,1-Jan-2000 00:00:00 GMT;';
	document.cookie = 'longitude=; path=/; expires=Sat,1-Jan-2000 00:00:00 GMT;';
	document.cookie = 'accuracy=; path=/; expires=Sat,1-Jan-2000 00:00:00 GMT;';
    };
    return;
}

