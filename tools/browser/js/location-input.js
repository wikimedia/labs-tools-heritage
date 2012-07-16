 
 var geocoder;
 
 
 
  function place(latitude, longitude, formatted_address)
  {
  	//Relocate the map to this place
  	point = new google.maps.LatLng(latitude, longitude);
  	//mapview.setCenter(point);
  	
  	
	//mainMarker.setPosition(point);
	
	document.getElementById("did-you-mean").innerHTML = "";  
  	
  	document.lpf.lat.value = latitude;
  	document.lpf.lon.value = longitude;
  	thisFormattedAddress = formatted_address.replace(/&apos/g,"'");	//bring back apostrophes 
  	document.lpf.address.value = thisFormattedAddress;
  	
  	document.lpf.submit();
  	
  	//formattedAddress = formatted_address.replace(/&apos/g, "'"); 	//Set the global version, but replace apos with "'"
  									//for insertion into the database correctly
  	//formattedAddress = formatted_address;	//Set the global version
  	
  	
  }
 
 
 
  function geocodeAddress(geoBias) {
  
    geocoder = new google.maps.Geocoder();
    
    var address = document.getElementById("newaddress").value;
    if (geocoder) {
      geocoder.geocode( { 'address': address, 'region': geoBias }, function(results, status) {
	if (status == google.maps.GeocoderStatus.OK) {
	  //mapview.setCenter(results[0].geometry.location);
	  
	  
	  //mainMarker.setPosition(results[0].geometry.location);
	  
	  
	 document.lpf.lat.value = results[0].geometry.location.lat();
  	 document.lpf.lon.value = results[0].geometry.location.lng();

	
	
	  if(results.length > 1) { 
	  	$("#did-you-mean").show();
		document.getElementById("did-you-mean").innerHTML = "Did you mean:";
		// Loop through the results
		for (var i=0; i<results.length; i++) {
		  var p = results[i].geometry.location;
		  thisFormattedAddress = results[i].formatted_address;
		  //alert(thisFormattedAddress);
		  //thisFormattedAddress = thisFormattedAddress.split("'").join("\'");		//Get rid of apostrophes
		  thisFormattedAddress = thisFormattedAddress.replace(/'/g, "&apos"); 
		  //alert(thisFormattedAddress);
		  newHTML = "<br><a href='javascript:place(" +p.lat()+","+p.lng()+",\""+ thisFormattedAddress + "\")'>"+ results[i].formatted_address+"<\/a>";
		  //alert(newHTML);
		  document.getElementById("did-you-mean").innerHTML += newHTML;
		}
	  } else {
		//A single result - research
		//formattedAddress = results[0].formatted_address;
	  	
	  	$("#did-you-mean").hide();
	  	
	  	document.lpf.address.value = address;
	  	
	  	//Submit the main form
	  	document.lpf.submit();
	  	return true;
		
	  }

	  
	 
	
	} else {
	  alert("Finding location was not successful: " + status);
	}
      });
    }
    
    return false;
  }
