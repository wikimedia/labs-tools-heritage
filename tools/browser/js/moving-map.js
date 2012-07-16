function isDefined(object)
{
	//alert(object);
	return (typeof(object) === undefined) ? false : true;
}




var has_been_mapped = false;
var properties;

var poiMarkers = [];
var sameLocationArray = new Array();
var ajaxString;
var advertMarkers = [];

var queries_cnt = 0;		//debugging
var showQueries = 'false';

var insideInfoBox = false;

var initializingMap = false;
var initializedMapZoom = false;


//See http://code.google.com/apis/maps/documentation/events.html#Event_Closures
function createMarkerOLD(point, number, options, content, linkTarget) {
  //var marker = new google.maps.Marker(point, options);
 
  var marker = new google.maps.Marker(options);
   marker.value = number;
   
   
   
   //alert(content.actions[0].uri);
   if(eval("content.actions[0]") != undefined) {

	
   	 if(eval("content.actions[0].uri") != undefined) {
	   	var url = content.actions[0].uri;
	   	
	   	
	   	 //Special case conduit -- yerg
	 	if(linkTarget == '_conduit') {
	 		 url = url + '#_new';
	  	}
	  } else {
	  	var url = "";
	  }
    } else {
	 var url = "";
    }

   
  

 
  
  if(url != '') {
  	titleLink = '<a href="' + url+ '" target="' + linkTarget + '">'+ content.title +'</a>';
  	
  	 if(content.imageURL != "") {
  		imageSrc = '<a href="' + url+ '" target="' + linkTarget + '"><img align="right" src="' + content.imageURL + '" border="0"></a>';
	  } else {
	  	imageSrc = '';
	  }
  } else {
  	titleLink = content.title;
  	 if(content.imageURL != "") {
  		imageSrc = '<img align="right" src="' + content.imageURL + '" border="0">';
	  } else {
	  	imageSrc = '';
	  }
  	
  }
  
  if((content.line2 != '')&&(content.line2 != null)) {
  	line2 = content.line2;
  } else {
  	line2 = '';
  }
 
  if((content.line3 != '')&&(content.line3 != null)) {
  	line3 = content.line3;
  } else {
  	line3 = '';
  } 
  
  if((content.line4 != '')&&(content.line4 != null)) {
  	line4 = content.line4;
  } else {
  	line4 = '';
  }  
  
  var contentString = '<div id="content">'+
    '<div id="siteNotice">'+
    '</div>'+
        '<h3 class="heading" style="font-size: 12px">' + titleLink + '</h3>'+
        '<div id="bodyContent">'+
        imageSrc +
        '</div>'+
        '<div class="regular" style="font-size: 11px">'+
        line2 + '<br>'+
        line3 + '<br>'+
        line4 + '<br>'+
        '</div>'+
        '</div>';
    
    '</div>'+
    '</div>';


	var infowindow = new google.maps.InfoWindow({
	    content: contentString
	});

	google.maps.event.addListener(marker, 'click', function() {
	  infowindow.open(mapview,marker);
	});
  
  return marker;

}



//See http://code.google.com/apis/maps/documentation/events.html#Event_Closures
function createMarkerCombined(point, number, options, contentGroup, linkTarget) {
  //var marker = new google.maps.Marker(point, options);
 
  //Create one physical marker
  var marker = new google.maps.Marker(options);
   marker.value = number;
   var contentString = "";
   
 
   for(var cnt=0; cnt<contentGroup.length; cnt++) {
   
      var content = contentGroup[cnt];
   	
 
 
 
   
   
   
	   //alert(content.actions[0].uri);
	   if(eval("content.actions[0]") != undefined) {

	
	   	 if(eval("content.actions[0].uri") != undefined) {
		   	var url = content.actions[0].uri;
		   	
		   	
		   	 //Special case conduit -- yerg
		 	if(linkTarget == '_conduit') {
		 		 url = url + '#_new';
		  	}
		  } else {
		  	var url = "";
		  }
	    } else {
		 var url = "";
	    }

	   
	  

	 
	  
	  if(url != '') {
	  	titleLink = '<a href="' + url+ '" target="' + linkTarget + '">'+ content.title +'</a>';
	  	
	  	 if(content.imageURL != "") {
	  		imageSrc = '<a href="' + url+ '" target="' + linkTarget + '"><img align="right" src="' + content.imageURL + '" border="0"></a>';
		  } else {
		  	imageSrc = '';
		  }
	  } else {
	  	titleLink = content.title;
	  	 if(content.imageURL != "") {
	  		imageSrc = '<img align="right" src="' + content.imageURL + '" border="0">';
		  } else {
		  	imageSrc = '';
		  }
	  	
	  }
	  
	  if((content.line2 != '')&&(content.line2 != null)) {
	  	line2 = content.line2;
	  } else {
	  	line2 = '';
	  }
	 
	  if((content.line3 != '')&&(content.line3 != null)) {
	  	line3 = content.line3;
	  } else {
	  	line3 = '';
	  } 
	  
	  if((content.line4 != '')&&(content.line4 != null)) {
	  	line4 = content.line4;
	  } else {
	  	line4 = '';
	  }  
	  
	  contentString = contentString + '<div id="content">'+
	    '<div id="siteNotice">'+
	    '</div>'+
	    	'<span id="bodyContent">'+
		imageSrc +
		'</span>'+
		'<h3 class="heading" style="font-size: 12px">' + titleLink + '</h3>'+
		'<div class="regular" style="font-size: 11px">'+
		line2 + '<br>'+
		line3 + '<br>'+
		line4 + '<br>'+
		'</div>'+
		'</div>';
	    
	    '</div>'+
	    '</div>';
	}

	//Fill string with all content
	var infowindow = new google.maps.InfoWindow({
	    content: contentString
	});

	google.maps.event.addListener(marker, 'click', function() {
	  infowindow.open(mapview,marker);
	});

  return marker;

}






function bubbleSort(inputArray, start, rest) {
	for (var i = rest - 1; i >= start;  i--) {
		for (var j = start; j <= i; j++) {
			if (inputArray[j+1].sum < inputArray[j].sum) {
				var tempValue = inputArray[j];
				inputArray[j] = inputArray[j+1];
				inputArray[j+1] = tempValue;
      			}
   		}
	}
	return inputArray;
}


function searchCompleteOLD(pois)
{
	
	/*for (myKey in pois){
			alert ("pois["+myKey +"] = "+pois[myKey]);
		}
	alert('got to here a');*/
	//var pois = [];
	//eval("pois="+data);		//Turn JSON string into array

	/*alert(pois.layer);
	alert(pois.hotspots[0].lat);*/

	
	//If on an initialization, we want to zoom out to the level of the first two results
	if((initializingMap == true)&&(initializedMapZoom == false)) {
		//alert('in here');
		
		var bounds = new google.maps.LatLngBounds();

		//Include self location in bounds
		centerPoint = mapview.getCenter();
		bounds.extend(centerPoint);

		

		for (var i = 0; i < 3; i++) {
		  // Insert code to add marker to map here
		  if(eval("pois.hotspots[i]") != undefined) {
			  var point = new google.maps.LatLng(pois.hotspots[i].lat/1000000,pois.hotspots[i].lon/1000000);

			   if(eval("point") != undefined) {
				// Extend the LatLngBound object
				//alert(point);
			  	bounds.extend(point);
			   }
		   }
		}
		
		centerPoint = mapview.getCenter();
		zoom = mapview.getZoom(mapview.fitBounds(bounds));
		//alert(bounds + ' zoom = ' + zoom);
		if(zoom > 15) { zoom = 15 };		
		mapview.setZoom(zoom-1);
		mapview.setCenter(centerPoint);		
		

		
		initializingMap = false;	//Zoom out to the right level
	}
	
	
	
	
	//Loop through array
    	for(cnt=0; cnt<pois.hotspots.length; cnt++) {
    		//Get the marker from the point
    		//var point = new google.maps.Point(pois.hotspots[cnt].lat/1000000, pois.hotspots[cnt].lon/1000000);
		//var point = new google.maps.Point(51, 0);

		var point = new google.maps.LatLng(pois.hotspots[cnt].lat/1000000,pois.hotspots[cnt].lon/1000000);


    		if(eval("poiMarkers[cnt]") != undefined) {

			poiMarkers[cnt].setMap(null);
    			//mapview.removeOverlay(poiMarkers[cnt]);		//Delete the old one
    			//LEAVE OUT delete propertyMarkers[cnt];   //clear element of array
    		}

    		var markerOptions = {
    			position: point, 
    			title: pois.hotspots[cnt].title,
    			icon: markerImage,
    			shadow: markerShadow
    		};
    		
    		
		
		if(markerOptions.title == '') {
			markerOptions.title = pois.hotspots[cnt].line2;
		}

    		//Create the new one
    		poiMarkers[cnt] = createMarker(point, cnt, markerOptions, pois.hotspots[cnt], linkTarget);
    		poiMarkers[cnt].setMap(mapview);
    		//mapview.addOverlay(poiMarkers[cnt]);	//Add to the map

    	}
    	//http://stackoverflow.com/questions/1220063/dynamically-adding-listeners-to-google-maps-markers &



    	//Remove the trailing icons - start off at the end of the list of new pois
    	for(cnt; cnt<poiMarkers.length; cnt++) {
    		if(eval("poiMarkers[cnt]") != undefined) {
			
			poiMarkers[cnt].setMap(null);
    			//mapview.removeOverlay(poiMarkers[cnt]);		//Delete the old one
    			//LEAVE OUT delete propertyMarkers[cnt];   //clear element of array
    		}
    	}

	

}





function sameLocationList()
{

	this.sum = new Number;
	this.id = new Number;

}


//Initial sort
function sortIntoClumps(pois)
{
	
	for(var cnt=0; cnt<pois.hotspots.length; cnt++) {
			var location_sum = pois.hotspots[cnt].lat + pois.hotspots[cnt].lon;
			sameLocationArray[cnt] = new sameLocationList();
			sameLocationArray[cnt].sum = location_sum;
			sameLocationArray[cnt].id = cnt;
		
			//alert(sameLocationArray[cnt].sum);
	}


	bubbleSort(sameLocationArray, 0, sameLocationArray.length-1);
}


function generateClump(pois, sameLoc, sameCnt)
{


	//alert('Creating list of markers at same location');
	var thisTitle = pois.hotspots[sameLoc[0]].title;
	var hotspots = new Array();
	
	//Know we have one hotspot
	hotspots[0] = pois.hotspots[sameLoc[0]];
	
	//Loop through all at this location
	if(sameCnt > 0) {
	
		thisTitle = thisTitle + " And More.. ";
		
		//More than one at location
		for(var cntb = 1; cntb<(sameCnt+1); cntb++) {

			//Show together
			//alert(sameLoc[cntb]);
			//alert(pois.hotspots[sameLoc[cntb]].lat + ' ' + pois.hotspots[sameLoc[cntb]].lon);
			
			hotspots[cntb] = pois.hotspots[sameLoc[cntb]];
		
			//Clear off this marker if it used to exist
			if(eval("poiMarkers[sameLoc[cntb]]") != undefined) {
				poiMarkers[sameLoc[cntb]].setMap(null);
			}
	

		}
	}
	
	//Get the marker from the point
	var point = new google.maps.LatLng(pois.hotspots[sameLoc[0]].lat/1000000,pois.hotspots[sameLoc[0]].lon/1000000);


	if(eval("poiMarkers[sameLoc[0]]") != undefined) {
		poiMarkers[sameLoc[0]].setMap(null);
	}

	var markerOptions = {
		position: point, 
		title: thisTitle,
		icon: markerImage,
		shadow: markerShadow
	};
	
	

	if(markerOptions.title == '') {
		markerOptions.title = pois.hotspots[sameLoc[0]].line2;
	}

	//Create the new one
	poiMarkers[sameLoc[0]] = createMarkerCombined(point, sameLoc[0], markerOptions, hotspots, linkTarget);
	poiMarkers[sameLoc[0]].setMap(mapview);
	return;


}


function createMarkerClumps(pois)
{
	//Loop through sorted array
	var oldLat = 0;
	var oldLon = 0;
	var same = false;
	var sameLoc = new Array();
	sameLoc[0] = sameLocationArray[0].id;		//Initialiser
	var sameCnt = 0;


	for(var cnt=0; cnt<sameLocationArray.length; cnt++) {
	

	
		var newLat = pois.hotspots[sameLocationArray[cnt].id].lat;
		var newLon = pois.hotspots[sameLocationArray[cnt].id].lon;
		
		//alert("NewLat=" + newLat);
	
	
		if((newLat != oldLat)||(newLon != oldLon)) {
			//A different, new lat/lon
			//alert('Different location: ' + sameCnt);
		
			//Create the previous list of markers at one point
			if(same == true) {
				//alert('sameLoc[0] = ' + sameLoc[0]);
				generateClump(pois, sameLoc, sameCnt);
				
				
				
				
			
				same = false;  //Don't register until we have a new one
			}	
		
			//Don't create a new marker yet - just start logging which markers to create
			sameCnt = 0;
			sameLoc = new Array();
			sameLoc[sameCnt] = sameLocationArray[cnt].id;
		
			//alert('sameLoc['+sameCnt+'] = ' + sameLocationArray[cnt].id);
		
			same = true;
			oldLat = newLat;
			oldLon = newLon;
	
		} else {
			same = true;
			sameCnt ++;
			//The same lat/lon - append to the list
		
		
			sameLoc[sameCnt] = sameLocationArray[cnt].id;
			//alert('sameLoc['+sameCnt+'] = ' + sameLocationArray[cnt].id);
		
		
		}
	
	
	
	
	}

	//Final case
	if(same == true) {
		//alert("About to do final generateClump");
		generateClump(pois, sameLoc, sameCnt);
	}
}





function searchComplete(pois)
{



	
	//If on an initialization, we want to zoom out to the level of the first two results
	if((initializingMap == true)&&(initializedMapZoom == false)) {
		//alert('in here');
		
		var bounds = new google.maps.LatLngBounds();

		//Include self location in bounds
		centerPoint = mapview.getCenter();
		bounds.extend(centerPoint);

		

		for (var i = 0; i < 3; i++) {
		  // Insert code to add marker to map here
		  if(eval("pois.hotspots[i]") != undefined) {
			  var point = new google.maps.LatLng(pois.hotspots[i].lat/1000000,pois.hotspots[i].lon/1000000);

			   if(eval("point") != undefined) {
				// Extend the LatLngBound object
				//alert(point);
			  	bounds.extend(point);
			   }
		   }
		}
		
		centerPoint = mapview.getCenter();
		zoom = mapview.getZoom(mapview.fitBounds(bounds));
		//alert(bounds + ' zoom = ' + zoom);
		if(zoom > 15) { zoom = 15 };		
		mapview.setZoom(zoom-1);
		mapview.setCenter(centerPoint);		
		

		
		initializingMap = false;	//Zoom out to the right level
	}
	
	
	
	sortIntoClumps(pois);
	createMarkerClumps(pois);


	
    	//http://stackoverflow.com/questions/1220063/dynamically-adding-listeners-to-google-maps-markers &



    	//Remove the trailing icons - start off at the end of the list of new pois
    	for(var cnt; cnt<poiMarkers.length; cnt++) {
    		if(eval("poiMarkers[cnt]") != undefined) {
			
			poiMarkers[cnt].setMap(null);
    			//mapview.removeOverlay(poiMarkers[cnt]);		//Delete the old one
    			//LEAVE OUT delete propertyMarkers[cnt];   //clear element of array
    		}
    	}

	

}






function addAdvert(options, advert, returnLink)
{

	 var marker = new google.maps.Marker(options);
	 var titleLink = '<a href="' + advert.url+ '" target="_new">'+ advert.fullText +'</a>';
	  
	  var contentString = '<div id="content">'+
	    '<div id="siteNotice">'+
	    '</div>'+
		'<h3 class="heading" style="font-size: 12px">' + titleLink + '</h3>'+
	        '<div class="regular" style="font-size: 11px" target="_new"><a href="' + returnLink + '">Rvolve Ads</a></div>' + 
	    '</div>'+
	    '</div>';	 
		 
	var infowindow = new google.maps.InfoWindow({
	    content: contentString
	});

	google.maps.event.addListener(marker, 'click', function() {
	  infowindow.open(mapview,marker);
	});
	 
	 return marker;
}




function advertsComplete(data)
{
	
	var cnt = 0;
	
	//Loop through array
    	$.each(data.advert, function(i,advert){ 
    	
    		//Get the marker from the point

		
		var point = new google.maps.LatLng(advert.lat,advert.lon);
		
		//alert(point);
		
		/*
    		if(eval("poiMarkers[cnt]") != undefined) {

			poiMarkers[cnt].setMap(null);
    			//mapview.removeOverlay(poiMarkers[cnt]);		//Delete the old one
    			//LEAVE OUT delete propertyMarkers[cnt];   //clear element of array
    		}*/

    		var markerOptions = {
    			position: point, 
    			title: advert.fullText,
    			icon: advertImage,
    			zIndex: -1
    			
    		};		//shadow: advertShadow
    				//setZIndex(zIndex:number)
    		//alert(advert.fullText);

    		//Create the new one
    		
    		if(eval("advertMarkers[cnt]") != undefined) {
			
			advertMarkers[cnt].setMap(null);
    		}
    		advertMarkers[cnt] = addAdvert(markerOptions, advert, data.returnLink);
    		advertMarkers[cnt].setMap(mapview);
    		
    		cnt++;
    	});
    	//http://stackoverflow.com/questions/1220063/dynamically-adding-listeners-to-google-maps-markers &



    	//Remove the trailing icons - start off at the end of the list of new pois
    	/*for(cnt; cnt<poiMarkers.length; cnt++) {
    		if(eval("poiMarkers[cnt]") != undefined) {
			
			poiMarkers[cnt].setMap(null);
    			//mapview.removeOverlay(poiMarkers[cnt]);		//Delete the old one
    			//LEAVE OUT delete propertyMarkers[cnt];   //clear element of array
    		}
    	}*/

	

}




  var mapview;
  var geocoder;
  var mainMarker;
  var formattedAddress;
  

  
  
  function initializeMap(startingLatitude, startingLongitude, startingZoom) {
  
    //geocoder = new google.maps.Geocoder();

    if(startingZoom != false) {
    	initializedMapZoom = true;
    } else {
    	//The default zoom level to start at
    	startingZoom = 15;
    } 

    var latlng = new google.maps.LatLng(startingLatitude, startingLongitude);
    
        
    var myOptions = {
      zoom: startingZoom,
      center: latlng,
      mapTypeId: google.maps.MapTypeId.ROADMAP,
      scaleControl: true,
      navigationControlOptions: {  
	     style: google.maps.NavigationControlStyle.ZOOM_PAN  
       }  
    };
    

    
    mapview = new google.maps.Map(document.getElementById("mapview"), myOptions);
    
    
    mainMarker = new google.maps.Marker({
	      map: mapview, 
	      position: latlng,
	      draggable: false,
	      zIndex: 0
	  });
    
    
   // movingMapInit();
   initializingMap = true;	//Zoom out to the right level
    getResultsData(startingLatitude,startingLongitude,50);  //50
    //getNakdData('lessent',startingLatitude,startingLongitude, 50);
    
    google.maps.event.addListener(mapview, 'dragend', function moveEnd() {
		//When the map moves, AJAX the results to the center
		
		var center = mapview.getCenter();
		//alert(center.lat());
		
		getResultsData(center.lat(),center.lng(),50); //50

    });
    
  }
  





