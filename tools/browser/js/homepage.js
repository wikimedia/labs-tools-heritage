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

For assistance:
	peter AT lightrod.org
	or the LightRod forums
*/

//Handles the user's homepage recording in a cookie
var home_url = '';
	
	
function initialize_home() {
    var last_location = get_home_cookie();
    if (last_location) {
    	//alert(last_location.home_url);
	if(last_location.home_url) {
		home_url = last_location.home_url;
	} else {
		home_url = 'http://';
	}
    } else {
	home_url = 'http://';
    }
    document.lpf.url.value = home_url;
    
}

function get_home_cookie() {

    var location = {}; // hash with latitude, longitude, accuracy properties
    if (document.cookie) {
       var reg_exp = /home_url=([^\;]*)/; // match cookie format "latitude=..." for example
       //alert(document.cookie);
       var match = reg_exp.exec(document.cookie);
       if (match) {
	   location.home_url = match[1];
       }
       
    }

    return (location);
}

function set_home_cookie(url) {

    // set the cookie expiration date far in future.
    document.cookie = 'home_url=' + url + ';path=/;expires=Thu,31-Dec-2020 00:00:00 GMT;';

     //alert('cookie : ' + document.cookie);

}

function clear_home_cookie() {

    // delete the cookies by setting an expiration date in the past.
    if (document.cookie) {
	document.cookie = 'home_url=;path=/;expires=Sat,1-Jan-2000 00:00:00 GMT;';
    };
    return;
}

function set_default_search_cookie(url) {

    // set the cookie expiration date far in future.
    document.cookie = 'default_search_engine=' + url + ';path=/;expires=Thu,31-Dec-2020 00:00:00 GMT;';

    alert('You can now enter your search term (e.g. Layer name) directly in the browser bar');
     //alert('cookie : ' + document.cookie);

}

