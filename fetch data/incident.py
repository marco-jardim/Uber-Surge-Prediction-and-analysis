# -*- coding: utf-8 -*-

from __future__ import print_function # Python 2/3 compatibility
import requests
import json
import time
import boto3
import database_incident
import ConfigParser
import decimal
import urllib2, urllib
import requests
import ConfigParser

# import kinds of libraries

# read table name
tablename = "uber_incident"

# create database if not exist

dynamodb_table = database_incident.create_database(tablename)  

dynamodb_table = database_incident.get_table(tablename) # get table

with open('location.json') as data_file:       # read company information from json file
    location = json.load(data_file)

order = 0 #initialize order to 0

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

while True:
    for company in location["places"]:
        order = order + 1
        start_latitude = end_latitude = float(company["lat"])
        start_longitude = end_longitude = float(company["lon"])

    # load config file

        # key = config.get('mapquest_api', 'ISmwDOKPbPCsUW1RD2yG5CnYwKG5MdQ2')
        key = "ISmwDOKPbPCsUW1RD2yG5CnYwKG5MdQ2"

        mapquest_url = 'http://www.mapquestapi.com/traffic/v2/incidents'

# load config file
    
        response = requests.get("http://www.mapquestapi.com/traffic/v2/incidents?key=" + key + "&boundingBox=" + getBoundingBox(start_latitude,start_longitude, 1.5) + "&filters=construction,incidents,Congestion&inFormat=kvp&outFormat=json")
        # 
        data = response.json()
        if data["incidents"][0]["type"] == 1:
            situation = "Construction"
        elif data["incidents"][0]["type"] == 2:
            situation = "Event"
        elif data["incidents"][0]["type"] == 3:
            situation = "Congestion"
        elif data["incidents"][0]["type"] == 4:
            situation = "Accident"
        # print(data)
        
        # print(data["incidents"][0]["type"])
        # insert into dynamodb 
        item = {"time":str(time.time()),"order":order,"latitude":str(start_latitude),"longtitude":str(start_longitude),"incident":situation,"company":company["name"]} 
        print(item)
        database_incident.insert(dynamodb_table, item)            

        time.sleep(120)
