
---
name: Sihan Wu, Yitong Wang
uni: sw3013, yw2786
course: Advanced Big data Analysis
project: Final Project
---
# Uber Surge Prediction and Analysis

This repository includes codes of our web application, back end program, web framework program and front end program.

## Description for files

Fetch data: `surge.py` is the main program to fetch surge multipliers, weather and temperature data, traffic and incident data, and then store them into DynamoDB.
            `database_total.py` is the program which will be called when `surge.py` runs. It includes the code to connect to my database and create new table, delete table, insert item to specified table.
            
