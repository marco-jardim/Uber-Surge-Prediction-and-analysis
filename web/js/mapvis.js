
var lat = 0;
var lng = 0;
var latlng = {lat: 0, lng: 0};
var zipcode = 10000;
function initMap() {
		var mapDiv = document.getElementById('map');
    	map = new google.maps.Map(mapDiv, {
        	center: {
            	lat: 40.7577,
            	lng: -73.9857
        	},
        	zoom: 14,
        	showTip: true
    	});
		var geocoder = new google.maps.Geocoder;
  		var infowindow = new google.maps.InfoWindow;
		// google.maps.event.addListener(map, 'click', function(event) {
//     		addMarker(event.latLng, map);
//   		});


  		google.maps.event.addListener(map, "click", function(event) {
    		lat = event.latLng.lat();
    		lng = event.latLng.lng();
//     		
//   	// var input = event.latLng.lat();
//   	// console.log(input);
//   	// var latlngStr = input.split(',', 2);
	   	
		
		// changeText("selectedlocation", lat+','+lng);
		if (lat != 0){
		
		geocodeLatLng(geocoder, map, infowindow);
		}
	});
}	

function geocodeLatLng(geocoder, map, infowindow) {
	var latlng = {lat: parseFloat(lat), lng: parseFloat(lng)};
  	geocoder.geocode({'location': latlng}, function(results, status) {
  		
  	
    	if (status === google.maps.GeocoderStatus.OK) {
      	if (results[0]) {
        	map.setZoom(14);
        	var marker = new google.maps.Marker({
          	position: latlng,
          	map: map
        	});
        	infowindow.setContent(results[0].formatted_address);
        	// location = results[1].formatted_address ; 
        	var address = results[0].formatted_address;
        	var add_display = address.substring(0,address.length-25);
        	zip =address.split("NY ").pop();
        	zipcode = zip.substring(0, zip.length - 5);
        	changeText("selectedlocation", add_display);
        	infowindow.open(map, marker);
      	} else {
        	window.alert('No results found');
      	}
    	} else {
      	window.alert('Geocoder failed due to: ' + status);
    	}
  		});
}
		
//   		
//     	
//     // populate yor box/field with lat, lng
//     		// alert("Lat=" + lat + "; Lng=" + lng);
	

function changeText(id, text) {
	var element = document.getElementById(id);
	element.innerHTML = text;
}

