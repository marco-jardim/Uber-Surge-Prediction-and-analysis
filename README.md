---
name: Sihan Wu, Yitong Wang
uni: sw3013, yw2786
Group id: 201605-17
course: Advanced Big data Analysis
project: Final Project
---

# Uber Surge Prediction and Analysis

This repository includes codes of our web application, back end program, web framework program and front end program.

## Description for files

### Fetch data: 

`surge.py` is the main program to fetch surge multipliers, weather and temperature data, traffic and incident data, and then store them into DynamoDB.

 `database_total.py` is the program which will be called when `surge.py` runs. It includes the code to connect to my database and create new table, delete table, insert item to specified table.
 
 Other files are for independent functions and their database program.
 
### Flask:

`Prediction.py` is our Webframework program which can receive requests from frond end program, calculate corresponding results through our machine learning model and then deliver them to Javascript program. Other data files are for model calculation.

### Heatmap:

`heatmap_final.py` is to calculate average distance of passengers who depart from certain areas. Heatmap programs are integrated into flask program.

### Web:

`index.html` is for our prediction webpage and `recommendation.html` is for our driver recommendation webpage. 
JS folder includes the Javascript files for Google map and prediction and recommendation process.(`mapvis.js` and `surgeEstimator.js`) 

CSS and libs are for webpage layout.
