import csv
from datetime import timedelta, date
import datetime
import os
from geopy.distance import vincenty
import json
# cwd = os.getcwd()

# files = os.listdir(cwd)  # Get all the files in that directory
# print("Files in '%s': %s" % (cwd, files))

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
  
        box = [str(ulLat) , str(ulLon), str(lrLat), str(lrLon)]

        return box

def find_box(zipcode):
    for index in location:
        if zipcode == index['zipcode']:
            latitude = index['lat']
            longitude = index['lng']
            center = (latitude,longitude)
            box = getBoundingBox(latitude, longitude, 2)
            return center, box









# GS:
longi_low = -74.016179
longi_high = -74.013117
lati_low = 40.713644
lati_high = 40.715562  


def daterange(start_date, end_date):  
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)

def drop_off(start_date, end_date, pick_time_start,pick_time_end,longi_low, longi_high, lati_low, lati_high):

    start_year = int(start_date[0:4])
    start_month = int(start_date[5:7])
    start_day = int(start_date[8:10])   

    # get the year, month, day information of end_date
    end_year = int(end_date[0:4])    
    end_month = int(end_date[5:7])
    end_day = int(end_date[8:10])

    start_d = date(start_year, start_month, start_day)   # set start date info
    end_d = date(end_year, end_month, end_day)           # set end date info
    range_date = []
    for single_date in daterange(start_d, end_d):
        if single_date.isoweekday() != 6 and single_date.isoweekday() != 7:  # only use weekdays
            range_date.append(single_date.strftime('%Y-%m-%d'))

    f = open('yellow_tripdata_2015-04.csv', "rb") # open up local file
    rows = csv.reader(f, delimiter=' ', quotechar='|') # set up local file csv reader
    longi_dropoff = [] # initialize 
    lati_dropoff = []
    for i, row_raw in enumerate(rows):  # at peak hours for each company, research the drop off location for the rides which departure 
                                        # from that six companies of our choice
        if i > 0:
            row = row_raw[0].split(",") + row_raw[1].split(",") + row_raw[2].split(",")
            if row[1] == row[3] and row[3] in range_date and pick_time_start <= row[2] and row[2] <= pick_time_end:
                if longi_low <= float(row[7]) and float(row[7]) <= longi_high and lati_low <= float(row[8]) and float(
                        row[8]) <= lati_high:
                    longi_dropoff.append(float(row[11]))
                    lati_dropoff.append(float(row[12]))

    # pick out the rides which satisfy the time window and location demands.
    result_dic = {}
    result_dic["longi_dropoff"] = longi_dropoff
    result_dic["lati_dropoff"] = lati_dropoff
    return result_dic
def cal_dis(zipcode,pick_time_start):
    filename = 'yellow_tripdata_2015-04.csv'
    start_date = '2015-04-07'
# end_date = '2015-04-07'
# pick_time_start = '18:00:00'
# pick_time_end = '19:29:59'

    end_date = start_date  #= date

#pick_time_start = time

# pick_time_end = pick_time_start
    year = int(start_date[0:4])
    month = int(start_date[6:7])
    day = int(start_date[9:10])

    hour = int(pick_time_start[0:2])

    minute = int(pick_time_start[4:5])

    second = int(pick_time_start[7:8])

    dt = datetime.datetime(year, month, day, hour, minute, second)

    # user = time.mktime(dt.timetuple())

    # print(datetime.datetime.utcnow())
    # print (timedelta(hours=1))

    one_hour_from_now = dt + timedelta(hours=1)
    # print one_hour_from_now

    # zipcode = 10027

    pick_time_end = format(one_hour_from_now, '%H:%M:%S')

    center, box = find_box(zipcode)

    # print box, center

    result = drop_off(start_date, end_date, pick_time_start, pick_time_end, float(box[3]), float(box[1]), float(box[2]),float(box[0]))

    temp_result = []

    # print result
    for i in range(0,len(result["longi_dropoff"])):
        # print i
        a = vincenty((result["lati_dropoff"][i],result["longi_dropoff"][i]), center).miles
        if a>30:
            continue
        temp_result.append(vincenty((result["lati_dropoff"][i],result["longi_dropoff"][i]), center).miles)
        #temp_result.append((result["longi_dropoff"][i], result["lati_dropoff"][i]))

    # print max(temp_result)
    average_distance = sum(temp_result)/len(temp_result)
    file2 = open('average.csv','a')
    b=json.dumps({"zipcode":zipcode,"average":average_distance,"time":pick_time_start})
    file2.write(b)
    file2.write('\n')
    file2.close()
    print average_distance


for index in location:
    zipcode = index['zipcode']
    cal_dis(zipcode,'12:00:00')
            





