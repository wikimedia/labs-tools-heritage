<html>
	<head>
		<title>Monuments in OpenStreetMap</title>
		
		<style type="text/css">
			body {
				padding: 0;
				margin: 0;
			}
			
			.olControlAttribution
			{
				bottom: 5px !important;
				right: 80px !important;
			}
			
			.olControlPermalink {
				bottom: 5px !important;
				right: 5px !important;
				width: 60px;
				text-align: center;
			}
			
			.olControlAttribution, .olControlPermalink {
				background-color: white;
				border-color: black;
				border-style: solid;
				border-width: 1px;
				cursor: pointer;
				padding: 2px 4px;
				
				opacity: 0.5;
			}
			
			.olPopupContent, .olControlAttribution, .olControlPermalink {
				font-family: arial, sans-serif;
				font-size: 12px;
			}
			
			.olControlAttribution:hover, .olControlPermalink:hover {
				opacity: 1.0;
			}
			
			.olPopupContent a, .olControlAttribution a, .olControlPermalink a {
				color: #0645AD;
				text-decoration: none;
			}
			
			.olPopupContent a:hover, .olControlAttribution a:hover, .olControlPermalink a:hover {
				text-decoration: underline;
			}
			
			#activetooltip {
				background-color: #ffffcb !important;
				overflow: hidden;
				
				border: 1px solid #DBDBD3 !important;
				
				font-family: arial, sans-serif;
				font-size: 12px;
				height: 8px;
				text-align: center;
			}
			
			#activetooltip .olPopupContent {
				padding: 5px 0 0 0 !important;
			}
			
			.olPopupContent {
				
			}

			.mapBtnOuter {
			border: 1px solid #444;
			background-color: #fff;
			z-index: 2000;
			}
			.mapBtnInner {
			cursor: pointer;
			font-size: 12px;
			font-family: arial, sans-serif;
			border-color:white #bbb #bbb white;
			border-style:solid;
			border-width:1px;
			padding: 2px 4px 2px 4px ;
			}
			#mapInsetMenu {
			position: absolute;
			left: 50px;
			top: 7px;
			}

			div.olLayerDiv {
			  -khtml-user-select: none;
			}

			.olControlScaleLineBottom {
			  display: none;
			}

			#mapInsetMenuDropdown { 
			visibility: hidden;
			padding: 2px 4px 2px 4px ;
			font-size: 12px;
			font-family: arial, sans-serif;
			background-color: #fff;
			border-color: #444;
			border-style:solid;
			border-width:1px;
			position: absolute;
			left: -1px;
			top: 20px;
			width: 250px;
			box-shadow: 2px 2px 2px #666;
			-moz-box-shadow: 2px 2px 2px #666;
			}


		</style>

<?php
require_once ( "geo_param.php" ) ;
$lang=addslashes(urldecode($_GET[lang]));
$srcountry=addslashes(urldecode($_GET[srcountry]));
$srlang=addslashes(urldecode($_GET[srlang]));
$srid=addslashes(urldecode($_GET[srid]));
$srname=addslashes(urldecode($_GET[srname]));
$sraddress=addslashes(urldecode($_GET[sraddress]));
$srmunicipality=addslashes(urldecode($_GET[srmunicipality]));
$srsource=addslashes(urldecode($_GET[srsource]));
$srwithoutimage=addslashes(urldecode($_GET[srwithoutimage]));
$limit=addslashes(urldecode($_GET[limit]));

if ($srcountry<>""){$srcountryex="&srcountry=".$srcountry;}
if ($srlang<>""){$srlangex="&srlang=".$srlang;}
if ($srid<>""){$sridex="&srid=".$srid;}
if ($srname<>""){$srnameex="&srname=".$srname;}
if ($sraddress<>""){$sraddressex="&sraddress=".$sraddress;}
if ($srmunicipality<>""){$srmunicipalityex="&srmunicipality=".$srmunicipality;}
if ($srsource<>""){$srsourceex="&srsource=".$srsource;}
if ($srwithoutimage<>""){$srwithoutimageex="&srwithoutimage=".$srwithoutimage;}
if ($limit<>""){$limitex="&limit=".$limit;}

if ( isset ( $_REQUEST['params'] ) ) {
	$p = new geo_param(  $_REQUEST['params'] , "Dummy" ); ;
	$x = $p->londeg ;
	$y = $p->latdeg ;
$position= "
  args.lon = $x;
   args.lat = $y;";

echo "<!--- //position:".$position." --->\n";
}

?>
		<script src="http://toolserver.org/~osm/libs/openlayers/2.10/OpenLayers.js"></script>
		<script src="http://toolserver.org/~osm/libs/openstreetmap/latest/OpenStreetMap.js"></script>
		
		<script type="text/javascript">
			// map object
			var map;
			
			// initiator
			function init()
			{ 	var urlRegex = new RegExp('^http://([abc]).www.toolserver.org/tiles/([^/]+)/(.*)$');
				
				// show an error image for missing tiles
				OpenLayers.Util.onImageLoadError = function()
				{
					if(urlRegex.test(this.src))
					{
						var style = RegExp.$2;
						if(style == 'osm')
						{
							var tile = RegExp.$3;
							var inst = RegExp.$1;
							this.src = 'http://'+inst+'.tile.openstreetmap.org/'+tile;;
							
							if(console && console.log)
								console.log('redirecting request for '+tile+' to openstreetmap.org: '+this.src);
							
							return;
						}
						
						this.src = 'http://www.openstreetmap.org/openlayers/img/404.png';
					}
				};

				// show an error image for missing tiles
				OpenLayers.Util.onImageLoadError=function(){
					this.src = 'http://www.openstreetmap.org/openlayers/img/404.png';
				};
				
				// get the request-parameters
				var args = OpenLayers.Util.getParameters();
				
				// main map object
				map = new OpenLayers.Map ("map", {
					controls: [
						new OpenLayers.Control.Navigation(),
						new OpenLayers.Control.PanZoomBar(),
						new OpenLayers.Control.Attribution(), 
						new OpenLayers.Control.LayerSwitcher(), 
						new OpenLayers.Control.Permalink()
					],
					
					// mercator bounds
					maxExtent: new OpenLayers.Bounds(-20037508.34,-20037508.34,20037508.34,20037508.34),
					maxResolution: 156543.0399,
					
					numZoomLevels: 19,
					units: 'm',
					projection: new OpenLayers.Projection("EPSG:900913"),
					displayProjection: new OpenLayers.Projection("EPSG:4326")
				});
				
				  // create the custom layer
				OpenLayers.Layer.OSM.Toolserver = OpenLayers.Class(OpenLayers.Layer.OSM, {
					
					initialize: function(name, options) {
						var url = [
							"http://a.www.toolserver.org/tiles/" + name + "/${z}/${x}/${y}.png", 
							"http://b.www.toolserver.org/tiles/" + name + "/${z}/${x}/${y}.png", 
							"http://c.www.toolserver.org/tiles/" + name + "/${z}/${x}/${y}.png"
						];
						
						options = OpenLayers.Util.extend({numZoomLevels: 19}, options);
						OpenLayers.Layer.OSM.prototype.initialize.apply(this, [name, url, options]);
					},
					
					CLASS_NAME: "OpenLayers.Layer.OSM.Toolserver"
				});
				// add the osm from Toolserver layers
				var osm = new OpenLayers.Layer.OSM.Toolserver('osm');
				map.addLayer(osm);




    var bboxStrategy = new OpenLayers.Strategy.BBOX( {
        ratio : 1.1,
        resFactor: 1
    });	

var pois = new OpenLayers.Layer.Vector("Monuments", {
		attribution:' <a href="http://commons.wikimedia.org/wiki/Wiki_Loves_Monuments">Wiki Loves Monuments</a>',
		projection: new OpenLayers.Projection("EPSG:4326"),
		strategies: [bboxStrategy],
		protocol: new OpenLayers.Protocol.HTTP({
				url: "http://toolserver.org/%7Eerfgoed/api/api.php?action=search&format=kml<?php echo $srcountryex.$srlangex.$sridex.$srnameex.$sraddressex.$srmunicipalityex.$srsourceex.$srwithoutimageex.$limitex;?>",
				format: new OpenLayers.Format.KML({
                           extractStyles: true, 
                           extractAttributes: true
                })		
        })
	});
      
    map.addLayer(pois);


var firstpoisload=false;
//zoom callback
pois.events.register("featuresadded",pois,function(){
    var bounds = pois.getDataExtent();
     //alert (bounds);
    if(bounds && !(firstpoisload)){ map.zoomToExtent(bounds,false); 
			    firstpoisload=true; }
});


    var feature = null;
    var highlightFeature = null;
    var lastFeature = null;
    var selectPopup = null;
    var tooltipPopup = null;
    
    var selectCtrl = new OpenLayers.Control.SelectFeature(pois, {
        toggle:true, 
  	    clickout: true
  	});
    pois.events.on({ "featureselected": onMarkerSelect, "featureunselected": onMarkerUnselect});

    function onMarkerSelect  (evt) {
        eventTooltipOff(evt);
        if(selectPopup != null) {
            map.removePopup(selectPopup);
            selectPopup.feature=null;
            if(feature != null && feature.popup != null){
                feature.popup = null;
            }
        }    
        feature = evt.feature;
        //console.log("feature selected", feature) ;
        //console.log("features in layer", pois.features.length);
        selectPopup = new OpenLayers.Popup.AnchoredBubble("activepopup",
                feature.geometry.getBounds().getCenterLonLat(),
                new OpenLayers.Size(320,320),
                text='<b>'+feature.attributes.name +'</b><br>'+ feature.attributes.description, 
                null, true, onMarkerPopupClose );
    	
        selectPopup.closeOnMove = false;
        selectPopup.autoSize = false;    	
    	feature.popup = selectPopup;
    	selectPopup.feature = feature;     	
    	map.addPopup(selectPopup);
    }

    function onMarkerUnselect  (evt) {
    	feature = evt.feature;
        if(feature != null && feature.popup != null){
            selectPopup.feature = null;            
            map.removePopup(feature.popup);
            feature.popup = null;
        } 
    }
    

    function onMarkerPopupClose(evt) {
        if(selectPopup != null) {
            map.removePopup(selectPopup);
            selectPopup.feature = null;            
            if(feature != null && feature.popup != null) {
                feature.popup = null;
            }    
        }    
        selectCtrl.unselectAll();
    }


    var highlightCtrl = new OpenLayers.Control.SelectFeature(pois, {
        hover: true,
        highlightOnly: true,
        renderIntent: "temporary",
        eventListeners: {
            featurehighlighted: eventTooltipOn,
            featureunhighlighted: eventTooltipOff
        }
    });

    function eventTooltipOn  (evt) {
        highlightFeature = evt.feature;           
        if(tooltipPopup != null) {
            map.removePopup(tooltipPopup);
            tooltipPopup.feature=null;
            if(lastFeature != null) {
                lastFeature.popup = null;                                
            }    
        }    
        lastFeature = highlightFeature;
             
      	//document.getElementById("map_OpenLayers_Container").style.cursor = "pointer";
      	
        tooltipPopup = new OpenLayers.Popup("activetooltip",
                highlightFeature.geometry.getBounds().getCenterLonLat(),
                new OpenLayers.Size(200,200),
                "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+highlightFeature.attributes.name, null, false, null );
	    tooltipPopup.contentDiv.style.backgroundColor='ffffcb';
    	tooltipPopup.contentDiv.style.overflow='hidden';
    	tooltipPopup.contentDiv.style.padding='0px';
    	tooltipPopup.contentDiv.style.margin='3px';
    	tooltipPopup.border = '0px solid #DBDBD3';
    	tooltipPopup.closeOnMove = true;
    	tooltipPopup.autoSize = true;    	
    	highlightFeature.popup = tooltipPopup;
    	map.addPopup(tooltipPopup);    	
    }
    function eventTooltipOff  (evt) {
        highlightFeature = evt.feature;            
      	//document.getElementById("map_OpenLayers_Container").style.cursor = "default";      	
        if(highlightFeature != null && highlightFeature.popup != null){
            map.removePopup(highlightFeature.popup);
            highlightFeature.popup = null;
            tooltipPopup = null;
            lastFeature = null;            
        } 
  	}
    
    map.addControl(highlightCtrl);
    map.addControl(selectCtrl);
    highlightCtrl.activate();
    selectCtrl.activate();    



				// default zoon
				var zoom = 1;
			        

			      <?php echo $position;?>

				// lat/lon requestes
				if(args.lon && args.lat)
				{
					// zoom requested
					if(args.zoom)
					{
						zoom = parseInt(args.zoom);
						var maxZoom = map.getNumZoomLevels();
						if (zoom >= maxZoom) zoom = maxZoom - 1;
					}
					
					// transform center
					var center = new OpenLayers.LonLat(parseFloat(args.lon), parseFloat(args.lat)).
						transform(map.displayProjection, map.getProjectionObject())
					
					// move to
					map.setCenter(center, zoom);
				}
				
				// bbox requestet
				else if (args.bbox)
				{
					// transform bbox
					var bounds = OpenLayers.Bounds.fromArray(args.bbox).
						transform(map.displayProjection, map.getProjectionObject());
					
					// move to
					map.zoomToExtent(bounds)
				}
				
				// default center
				else
				{
					// set the default center
					var center = new OpenLayers.LonLat(4.88, 52.37).
						transform(map.displayProjection, map.getProjectionObject());
					
					// move to
					map.setCenter(center, zoom);
				}

            var size = new OpenLayers.Size(16,16);
            var offset = new OpenLayers.Pixel(-(size.w/2), -(size.h/2));
            var icon = new OpenLayers.Icon('Ol_icon_red_example.png',size,offset);
            markers.addMarker(new OpenLayers.Marker(new OpenLayers.LonLat(map.center.lon,map.center.lat),icon));


			}
		</script>

		

	</head>
	 
	<body onload="init();" id="map">
	</body>
</html> 
