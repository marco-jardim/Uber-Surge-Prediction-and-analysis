# Here is the script that is being run on AWS in order for our prediction app to work
# the script uses flask in order to connect to the website and is running at all times on the virtual machine

import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import json
from flask import Flask
import flask
from flask import request
import redis
import collections
import json
import numpy as np
from flask.ext.cors import CORS
import requests
from datetime import datetime


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


server_token = 'hZkOcNzbbAj1wa-HKIoY8g4dVfKTd0l7xJCL8JUb'
uber_url = "https://api.uber.com/v1/estimates/price"



def day_fix(string):
    if string == '1':
        return "Monday"
    elif string =='2':
        return "Tuesday"
    elif string =='3':
        return "Wednesday"
    elif string =='4':
        return 'Thursday'
    elif string == '5':
        return 'Friday'
    elif string == '6':
        return 'Saturday'
    elif string == '0':
        return 'Sunday'

def min_fix(string):
    num = int(string)
    return str(num - (num%10))

def weather_fix(string):
    if string == 'Light Rain':
        return 'Rain'
    elif string == 'ScatteredClouds':
        return 'Cloudy'
    elif string == 'Mostly Cloudy':
        return'Cloudy'
    elif string == 'Partly Cloudy':
        return'Cloudy'
    elif string =='Overcast':
        return'Clear'
    else:
        return string
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
# from sklearn.externals import joblib

# rf = joblib.load("RandomForestClassifier.pkl")
# columns = joblib.load('columns.pkl')
def get_surge(dates,time,zipcode):
    import datetime
    import calendar
    month, day, year = (int(x) for x in dates.split('/'))    
    ans = datetime.date(year, month, day)
    weekday = calendar.day_name[ans.weekday()]
    t1 = time.split(":")[0]
    path = "surge_last_week/" + weekday +"/"+ zipcode +".txt"
    file = open(path)
    for line in file:
        if t1==line.split(' ')[0]:
            return line.split(' ')[1].strip('\n')

def model_lasso_10(zipcode,weather,temperature,weather_hour,temp_hour,situation,surge_multiplier):
    import numpy as np
    from sklearn import linear_model
    clf = linear_model.Lasso(alpha=0.1)
    f1= np.loadtxt('matrix_x_10/'+zipcode+".txt")
    name = 'matrix_x_10/'+zipcode+".txt"
    f2= np.loadtxt('matrix_y_10/'+zipcode+".txt")
    Y=f2.T.tolist()
    X=[]
    new_predict =[]
    situation = situation.replace("Construction","0").replace("Congestion","1").replace("Accident","0.5")
    weather = weather.replace("Partly Cloudy","0").replace("Mostly Cloudy","0").replace("Cloudy","0").replace("Breezy","0").replace("Clear","0").replace("Mostly Sunny","0").replace("Sunny","0").replace("Rain","1").replace("Overcast","0").replace("Chance of 1","0.5").replace("Thunderstorm","0.5").replace("Chance of a Thunderstorm","0.5")
    weather_hour = weather_hour.replace("Partly Cloudy","0").replace("Mostly Cloudy","0").replace("Cloudy","0").replace("Breezy","0").replace("Clear","0").replace("Mostly Sunny","0").replace("Sunny","0").replace("Rain","1").replace("Overcast","0").replace("Chance of 1","0.5").replace("Thunderstorm","0.5").replace("Chance of a Thunderstorm","0.5")
    new_predict.append(temperature)
    new_predict.append(weather)
    new_predict.append(situation)
    new_predict.append(surge_multiplier)
    new_predict.append(temp_hour)
    new_predict.append(weather_hour)
    results = map(float, new_predict)
    def file_len(fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1
    for i in range(0,file_len(name)):
        b=f1[i].tolist()
        X.append(b)
    clf.fit(X,Y)
    predict=clf.predict(results)
    return predict
def model_lasso_30(zipcode,weather,temperature,weather_hour,temp_hour,situation,surge_multiplier):
    import numpy as np
    from sklearn import linear_model
    clf = linear_model.Lasso(alpha=0.1)
    f1= np.loadtxt('matrix_x_30/'+zipcode+".txt")
    name = 'matrix_x_30/'+zipcode+".txt"
    f2= np.loadtxt('matrix_y_30/'+zipcode+".txt")
    Y=f2.T.tolist()
    X=[]
    new_predict =[]
    situation = situation.replace("Construction","0").replace("Congestion","1").replace("Accident","0.5")
    weather = weather.replace("Partly Cloudy","0").replace("Mostly Cloudy","0").replace("Cloudy","0").replace("Breezy","0").replace("Clear","0").replace("Mostly Sunny","0").replace("Sunny","0").replace("Rain","1").replace("Thunderstorm","0.5").replace("Chance of a Thunderstorm","0.5").replace("Overcast","0")
    weather_hour = weather_hour.replace("Partly Cloudy","0").replace("Mostly Cloudy","0").replace("Cloudy","0").replace("Breezy","0").replace("Clear","0").replace("Mostly Sunny","0").replace("Sunny","0").replace("Rain","1").replace("Thunderstorm","0.5").replace("Chance of a Thunderstorm","0.5").replace("Overcast","0")
    new_predict.append(temperature)
    new_predict.append(weather)
    new_predict.append(situation)
    new_predict.append(surge_multiplier)
    new_predict.append(temp_hour)
    new_predict.append(weather_hour)
    results = map(float, new_predict)
    def file_len(fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1
    for i in range(0,file_len(name)):
        b=f1[i].tolist()
        X.append(b)
    clf.fit(X,Y)
    predict=clf.predict(results)
    return predict

def get_zipcode(dates,time):
    import datetime
    import calendar
    import os
    list =[]
    dict ={}
    month, day, year = (int(x) for x in dates.split('/'))    
    ans = datetime.date(year, month, day)
    weekday = calendar.day_name[ans.weekday()]
    t1 = time.split(":")[0]
    txt_list = os.listdir("surge_last_week/"+ weekday)
    for txt in txt_list:
        if txt[0]!='.':
            path = "surge_last_week/" + weekday +"/"+ txt
            file = open(path)
            for line in file:
                if line.split(' ')[0]==t1 and line.split(' ')[1].strip('\n') > '1.2':
                    dict[txt.split('.')[0]] = line.split(' ')[1].strip('\n')
    list.append(dict) 
    return list

app = Flask(__name__)
CORS(app)

@app.route("/")
def good():
    print "hey"
    return'hey'


@app.route("/recommend")
def recommend():
    date = request.args.get('date')
    time = request.args.get('time')

    result = get_zipcode(date,time)[0]
    print (result)
    # print result
    file_rec = open('average.csv','r')

    product = {}
    heatmap=[]

    hour = int(time[0:2])
    
    for key in result:
        # print key
        heatmap.append(key)
        for line in file_rec:
            line = json.loads(line)
          
            #print int(hour)+1,int(line["time"][0:2])
            # print int(line["zipcode"])
            if int(line["zipcode"]) == int(key) and int(hour) <= int(line["time"][0:2]) <= int(hour)+1 :
                # print int(key)
                product[int(key)] = float(line["average"])*float(result[key])
                break
    file_rec.close()
    print product
    product_top3_result = []
    product_top3 = sorted(product.iteritems(), key=lambda d:d[1], reverse = True)
    for i in product_top3[0:3]:
        one,two = i
        product_top3_result.append(one)
    print product_top3_result

    coordinate_lat = []
    coordinate_lng = []

    for zipcode in heatmap:
        for index in location:
            if int(zipcode) == int(index["zipcode"]):
                # print int(zipcode) 
                coordinate_lat.append(float(index['lat']))
                coordinate_lng.append(float(index['lng']))
    return json.dumps({"product_top3_result":product_top3_result,"coordinate_lat":coordinate_lat,"coordinate_lng":coordinate_lng})
    # return json.dumps({"coordinate_lat":coordinate_lat,"coordinate_lng":coordinate_lng,"product_top3":product_top3})

conn = redis.Redis()

@app.route("/predict")
def predict():
    print "hey"

    key = "G5xXXAxzhGMQPsA2Ur3V6PfSMV0zA24G"

    mapquest_url = 'http://www.mapquestapi.com/traffic/v2/incidents'


    zipcode = request.args.get('zipcode')
    temperature = request.args.get('temp')
    date = request.args.get('date')
    time = request.args.get('time')
    weather = request.args.get('weather')
    weather_hour = request.args.get('weather_hour')
    temp_hour = request.args.get('temp_hour')



    for index in location:

        if int(zipcode) == index['zipcode']:
            # print ("hahha")
            start_latitude = end_latitude = index['lat']
            start_longitude = end_longitude = index['lng']
            break

    parameters = {
            'server_token': server_token,
            'start_latitude': start_latitude,
            'end_latitude': end_latitude,
            'start_longitude': start_longitude,
            'end_longitude': end_longitude
            }
    response = requests.get(uber_url, params=parameters)
    data = response.json()

    for price in data["prices"]:
        if price["display_name"] == "uberX":
            surge_multiplier_now = price["surge_multiplier"] 
            # print surge_multiplier_now
            break
    response_incident = requests.get("http://www.mapquestapi.com/traffic/v2/incidents?key=" + key + "&boundingBox=" + getBoundingBox(start_latitude,start_longitude, 1.5) + "&filters=construction,incidents,Congestion&inFormat=kvp&outFormat=json")
    data_incident = response_incident.json()

    # print data_incident

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
        situation = "Construction"

    date_now = str(datetime.now())[0:19]
    day_now = date_now[8:10]
    hour_now = date_now[11:13]
    minute_now = date_now[14:16]
    print str(time)[3:5]
    if int(str(date)[3:5]) == int(day_now):
        if hour_now == int(str(time)[0:2]):
            if int(str(time))[3:5] < int(minute_now)+2:
                surge_multiplier = surge_multiplier_now

    ss = get_surge(date,time,zipcode)
    print "ss"
    print ss
    surge_multiplier = get_surge(date,time,zipcode)

  

    prediction_10 = model_lasso_10(zipcode,weather,temperature,weather_hour,temp_hour,situation,surge_multiplier)

    prediction_10 = round(prediction_10,1)

    prediction_30 = model_lasso_30(zipcode,weather,temperature,weather_hour,temp_hour,situation,surge_multiplier)

    prediction_30 = round(prediction_30,1)




    
    #weather = request.args.get('weather')
    

    return json.dumps({"zipcode":zipcode,"prediction_10":prediction_10,"prediction_30":prediction_30,"surge":surge_multiplier_now})
    

if __name__ == '__main__':
    # app.run(host='0.0.0.0')
    app.debug = True
    app.run()
