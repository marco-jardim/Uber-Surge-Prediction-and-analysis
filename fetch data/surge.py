from __future__ import print_function # Python 2/3 compatibility
import requests
import json
import time
import boto3
import database_total
import decimal
import urllib2, urllib
import requests
import redis

conn = redis.Redis()


location = [{"lat": 40.75368539999999, "lng": -73.9991637, "zipcode": 10001, "area": "Chelsea and Clinton"} 
,{"lat": 40.7464969, "lng": -74.0094471, "zipcode": 10011, "area": "Chelsea and Clinton"},
{"lat": 40.755322, "lng": -73.9932872, "zipcode": 10018, "area": "Chelsea and Clinton"},
{"lat": 40.7686973, "lng": -73.9918181, "zipcode": 10019, "area": "Chelsea and Clinton"},
{"lat": 40.7605505, "lng": -73.98226830000002, "zipcode": 10020, "area": "Chelsea and Clinton"},
{"lat": 40.7602619, "lng": -73.9932872, "zipcode": 10036, "area": "Chelsea and Clinton"},
{"lat": 40.8032131, "lng": -73.95258249999999, "zipcode": 10026, "area": "Central Harlem"},
{"lat": 40.8138912, "lng": -73.96243270000001, "zipcode": 10027, "area": "Central Harlem"},
{"lat": 40.8173411, "lng": -73.9433299, "zipcode": 10030, "area": "Central Harlem"},
{"lat": 40.8140369, "lng": -73.9374517, "zipcode": 10037, "area": "Central Harlem"},
{"lat": 40.8288377, "lng": -73.9374517, "zipcode": 10039, "area": "Central Harlem"},
{"lat": 40.79164069999999, "lng": -73.9447994, "zipcode": 10029, "area": "East Harlem"},
{"lat": 40.794065, "lng": -73.9271644, "zipcode": 10035, "area": "East Harlem"},
{"lat": 40.7250632, "lng": -73.9976946, "zipcode": 10012, "area": "Greenwich Village and SoHo"},
{"lat": 40.7217861, "lng": -74.0094471, "zipcode": 10013, "area": "Greenwich Village and SoHo"},
{"lat": 40.7366138, "lng": -74.0094471, "zipcode": 10014, "area": "Greenwich Village and SoHo"},
{"lat": 40.7388319, "lng": -73.98153370000001, "zipcode": 10010, "area": "Gramercy Park and Murray Hill"},
{"lat": 40.74727, "lng": -73.9800645, "zipcode": 10016, "area": "Gramercy Park and Murray Hill"},
{"lat": 40.7519846, "lng": -73.9697795, "zipcode": 10017, "area": "Gramercy Park and Murray Hill"},
{"lat": 40.7593941, "lng": -73.9697795, "zipcode": 10022, "area": "Gramercy Park and Murray Hill"},
{"lat": 40.7038704, "lng": -74.0138541, "zipcode": 10004, "area": "Lower Manhattan"},
{"lat": 40.6998433, "lng": -74.0072436, "zipcode": 10005, "area": "Lower Manhattan"},
{"lat": 40.709329, "lng": -74.0131196, "zipcode": 10006, "area": "Lower Manhattan"},
{"lat": 40.7136487, "lng": -74.0087126, "zipcode": 10007, "area": "Lower Manhattan"},
{"lat": 40.7071498, "lng": -74.0021019, "zipcode": 10038, "area": "Lower Manhattan"},
{"lat": 40.7084274, "lng": -74.0173484, "zipcode": 10280, "area": "Lower Manhattan"},
{"lat": 40.7135097, "lng": -73.9859414, "zipcode": 10002, "area": "Lower East Side"},
{"lat": 40.7322535, "lng": -73.9874105, "zipcode": 10003, "area": "Lower East Side"},
{"lat": 40.7275043, "lng": -73.9800645, "zipcode": 10009, "area": "Lower East Side"},
{"lat": 40.7700703, "lng": -73.9580246, "zipcode": 10021, "area": "Upper East Side"},
{"lat": 40.77664120000001, "lng": -73.9521468, "zipcode": 10028, "area": "Upper East Side"},
{"lat": 40.7573053, "lng": -73.9550857, "zipcode": 10044, "area": "Upper East Side"},
{"lat": 40.7645239, "lng": -73.96243270000001, "zipcode": 10065, "area": "Upper East Side"},
{"lat": 40.7728432, "lng": -73.9558204, "zipcode": 10075, "area": "Upper East Side"},
{"lat": 40.7826039, "lng": -73.9506774, "zipcode": 10128, "area": "Upper East Side"},
{"lat": 40.8270209, "lng": -73.9506774, "zipcode": 10031, "area": "Inwood and Washington Heights"},
{"lat": 40.8409822, "lng": -73.9447994, "zipcode": 10032, "area": "Inwood and Washington Heights"},
{"lat": 40.8557765, "lng": -73.9447994, "zipcode": 10033, "area": "Inwood and Washington Heights"},
{"lat": 40.8721452, "lng": -73.92128579999999, "zipcode": 10034, "area": "Inwood and Washington Heights"},
{"lat": 40.8639624, "lng": -73.93304289999999, "zipcode": 10040, "area": "Inwood and Washington Heights"},
{"lat": 40.7769059, "lng": -73.9800645, "zipcode": 10023, "area": "Upper West Side"},
{"lat": 40.7859464, "lng": -73.97418739999999, "zipcode": 10024, "area": "Upper West Side"},
{"lat": 40.7999209, "lng": -73.96831019999999, "zipcode": 10025, "area": "Upper West Side"}]


#key = "ISmwDOKPbPCsUW1RD2yG5CnYwKG5MdQ2"
# key = "6x4CSaJfsPLf8NF5CEP88fE0OVX83Eti"

key ="E29dET2KzAF6Xren5DPpHcPyhZnUSIV9"

mapquest_url = 'http://www.mapquestapi.com/traffic/v2/incidents'

# get favored locations' information
def getBoundingBox(latitude, longitude, milesFromCenter) :   # define the function which is to get a range for given latitiude and longtitude
                                                            # according to given radius
  #These values are temporary until I actually do the math
  
  #close to accurate
        approxLatDegreeMiles = 69  
  
  #accurate around 40 degrees north
        approxLonDegreeMiles = 53
  
  #calculate upper left
        ulLat = latitude + float(milesFromCenter) / float(approxLatDegreeMiles)
        ulLon = longitude + float(milesFromCenter) / float(approxLonDegreeMiles)
  
  #calculate lower right
        lrLat = latitude - float(milesFromCenter) / float(approxLatDegreeMiles)
        lrLon = longitude - float(milesFromCenter) / float(approxLonDegreeMiles)
  
        box = str(ulLat) + "," + str(ulLon) + "," + str(lrLat) + "," + str(lrLon)

        return box

# uber surge data get
server_token = 'hZkOcNzbbAj1wa-HKIoY8g4dVfKTd0l7xJCL8JUb'
uber_url = "https://api.uber.com/v1/estimates/price"

# read table name
tablename = "Uber_total"

# create database if not exist
#dynamodb_table = database_total.create_database(tablename)

dynamodb_table = database_total.get_table(tablename)



while True:

    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select item.condition from weather.forecast where woeid = 12761478"   # use yahoo query sentence to get manhattan weather
    yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"   # constitute the url to request
    result = urllib2.urlopen(yql_url).read()  # get the result returned by yahoo_weather api
    preprocess_data = json.loads(result)   # transform result from json format to python dictionary format
    try:
        weather = preprocess_data['query']['results']['channel']['item']['condition']['text'].encode('utf-8') 
         # try to get weather result
    except:
        continue
    try:
        temp = preprocess_data['query']['results']['channel']['item']['condition']['temp'].encode('utf-8')
    except:
        continue
    #Time = preprocess_data['query']['results']['channel']['item']['condition']['date'].encode('utf-8')   # extract time information
    
    # insert into dynamodb 
    
    for index in location:
        zipcode = index['zipcode']
        start_latitude = end_latitude = index['lat']
        start_longitude = end_longitude = index['lng']
        area = index ['area']

        parameters = {
            'server_token': server_token,
            'start_latitude': start_latitude,
            'end_latitude': end_latitude,
            'start_longitude': start_longitude,
            'end_longitude': end_longitude
            }
        try:
            response_incident = requests.get("http://www.mapquestapi.com/traffic/v2/incidents?key=" + key + "&boundingBox=" + getBoundingBox(start_latitude,start_longitude, 1.5) + "&filters=construction,incidents,Congestion&inFormat=kvp&outFormat=json")
            
            data_incident = response_incident.json()
            #print (1111)
        except:
            continue
        
        try:
            if data_incident["incidents"][0]["type"] == 1:
                situation = "Construction"
            elif data_incident["incidents"][0]["type"] == 2:
                situation = "Event"
            elif data_incident["incidents"][0]["type"] == 3:
                situation = "Congestion"
            elif data_incident["incidents"][0]["type"] == 4:
                situation = "Accident"
        except:
            continue

        try:
            response = requests.get(uber_url, params=parameters)
            data = response.json()
        except:
            continue
        #print (1111)

        try:
            for price in data["prices"]:
                
                if price["display_name"] == "uberX":
                # insert into dynamodb 
                    item = json.loads('{"area":"%s","time":"%s","surge_multiplier":"%s","lat":"%s","lon":"%s","zipcode":"%s","weather":"%s","temperature":"%s","incident":"%s"}' % (area, time.time(), price["surge_multiplier"], start_latitude, start_longitude,zipcode,weather,temp,situation),)
                    print(item)
                    database_total.insert(dynamodb_table, item)  
                    # conn.setex("item",item,3000)   
        except:
            continue

    time.sleep(60)

