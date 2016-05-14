// Surge Estimation functions

// Global variable declarations


// TO DO: MAKE SURE TIME ZONES DON'T MESS UP SAN FRANCISCO WEATHER REQUESTS


var coordinate_lat = [40.77400588989258, 40.75625991821289];
var coordinate_lng = [-73.9822769165039, -73.99146270751953];


function updateWeather(date, time, rideType) {
	
	// Calculate index based on time input
 	var hourBlock = roundHourBlock(date, time);
 	var day = new Date(date).getDay();

 	// console.log(hourBlock);


 	//call weather data from Weather Underground API and update display divs
 	
	var w_url = "http://api.wunderground.com/api/51192aa9f8ab44fb/hourly10day/q/"+String(lat)+","+String(lat)+".json";
	$.getJSON(w_url, function(json) {
			// console.log(json);
			// console.log(json.hourly_forecast[hourBlock].temp.english);
			changeText("selectedTemp", json.hourly_forecast[hourBlock].temp.english + "°F");
			changeText("selectedWeather", json.hourly_forecast[hourBlock].condition);
			predictSurge(json.hourly_forecast[hourBlock].temp.english,time, json.hourly_forecast[hourBlock].condition, zipcode,json.hourly_forecast[1].condition, json.hourly_forecast[hourBlock].temp.english,time,date);
	});
}

// Function called when use submits selections
function submitChanges() {
	// when selections change, get values for weather calculations
	
	var date = document.getElementById("datepicker").value;
	var time = document.getElementById("timepicker").value;
	var rideType = document.getElementById("rideType").value;
	console.log(date,time,rideType,zipcode)

	// changes global temp and weather variables
	//alert("Lat=" + lat + "; Lng=" + lng);
	 updateWeather(date, time, rideType);

	// update other display text
	// changeText("selectedCity", city);
	//changeText("selectedDate", date);
	changeText("selectedTime", time);
}
function submitChanges_page() {
	// when selections change, get values for weather calculations
	window.location.href = 'index.html';
	
}

function recommendation() {
       window.location.href = 'recommendation.html';
       console.log(date);
}
function recommendation_page() {
       var date = document.getElementById("datepicker").value;
       var time = document.getElementById("timepicker").value;
       var rideType = document.getElementById("rideType").value;
       console.log(date);
       var modelURL = "http://127.0.0.1:5000/recommend?time="+String(time)+"&date="+String(date);
	   console.log(modelURL);
	   $.getJSON(modelURL, function(json) {
		
		
		coordinate_lat = json["coordinate_lat"];
 		coordinate_lng = json["coordinate_lng"];
 		changeText("recom1", json["product_top3_result"][0]);
 		changeText("recom2", json["product_top3_result"][1]);
 		changeText("recom3", json["product_top3_result"][2]);
 		console.log(coordinate_lat,coordinate_lng);

  	});

     initMap(coordinate_lat,coordinate_lng);     
       
}  	
  	   
	

function predictSurge(temp, time, weather, zipcode,weather_hour, temp_hour,time,date) {
	var now = new Date().getTime();
	var modelURL = "http://127.0.0.1:5000/predict?zipcode="+String(zipcode)+"&temp="+String(temp)+"&weather="+String(weather)+"&weather_hour="+String(weather_hour)+"&temp_hour="+String(temp_hour)+"&time="+String(time)+"&date="+String(date);
	console.log(modelURL);
	
	// make $.getJSON() call to AWS to return prediction in json format
	$.getJSON(modelURL, function(json) {
		console.log("hey");
		
		changeText("Current_surge", json["surge"]);
		changeText("10_minutes", json["prediction_10"]);
		changeText("30_minutes", json["prediction_30"]);
		// getSurge(json);
// 		/*changeText("noSurge", json["No Surge"]);
// 		changeText("highSurge", json["High Surge"]);
// 		changeText("lowSurge", json[""]);
// 		changeText("midSurge", json[3]);*/
// 		
  	});
}

// To update innerHTML of certain display
function changeText(id, text) {
	var element = document.getElementById(id);
	element.innerHTML = text;
}

function getSurge() {
	var ids = ["5_minutes", "10_minutes", "30_minutes"];
	var c = 0;
	for (i = 0; i < 3; i++) {
		changeText(ids[c], 1.2);
		// changeText(ids[c], String((Math.round(json[i]*1000)/10)).concat("%"));
		c+=1;
	}
}

// For 5-day forecasts, 3-hour blocks
function roundHourBlock(d, t) {
	var hb;
	var now = new Date().getTime();
  	//console.log(now);

 	var dt = d.concat(" "+t);
 	dt = new Date(dt);
 	var diff = new Date(dt - now);

 	// convert to hours difference for indexing into weather forecast data
 	var hb = (diff - diff%3600000)/3600000;
 	// console.log(hb);

 	if (diff <= 0) {
		alert("Please enter a future date and time");
 	} else if (hb > 239) {
		alert("Please select a time within the next 240 hours so we can factor in weather forecasts");
 	} else {
 		return hb;
 	};
}

function toggleHeatmap() {
  heatmap.setMap(heatmap.getMap() ? null : map);
}
function changeGradient() {
  var gradient = [
    'rgba(0, 255, 255, 0)',
    'rgba(0, 255, 255, 1)',
    'rgba(0, 191, 255, 1)',
    'rgba(0, 127, 255, 1)',
    'rgba(0, 63, 255, 1)',
    'rgba(0, 0, 255, 1)',
    'rgba(0, 0, 223, 1)',
    'rgba(0, 0, 191, 1)',
    'rgba(0, 0, 159, 1)',
    'rgba(0, 0, 127, 1)',
    'rgba(63, 0, 91, 1)',
    'rgba(127, 0, 63, 1)',
    'rgba(191, 0, 31, 1)',
    'rgba(255, 0, 0, 1)'
  ]
  heatmap.set('gradient', heatmap.get('gradient') ? null : gradient);
}

function changeRadius() {
  heatmap.set('radius', heatmap.get('radius') ? null : 20);
}

function changeOpacity() {
  heatmap.set('opacity', heatmap.get('opacity') ? null : 0.2);
}

// function getPoints() {
//          var rawLat = [40.77400588989258, 40.75625991821289, 40.80630111694336, 40.77403259277344, 40.806026458740234, 40.7996711730957, 40.73762130737305]
//         console.log(rawLat.length);
//         var rawLng = [-73.9822769165039, -73.99146270751953, -73.95401763916016, -73.90462493896484, -73.96513366699219, -73.9696044921875, -74.00663757324219]
//         console.log(rawLng.length);  // for test on log
//         var result = []
// 
//         for (var i = 0; i < rawLat.length; i++) {
//             result.push(new google.maps.LatLng(rawLat[i], rawLng[i]));
//         }
// 
//         return result;    //return heatmap result
//     }