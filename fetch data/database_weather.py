from __future__ import print_function  # Python 2/3 compatibility
import boto3
import json
import decimal
import ConfigParser  



dynamodb = boto3.resource('dynamodb',region_name='us-east-1', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")  #connect with dynamodb

def delete_database(table):  #define a function to delete database and if there are any exception, the raise error
    try:
        table.delete()
    except Exception, e:
        raise e


def create_database(tablename): # define a function to create database
''' attribute is time, order
'''
    table = dynamodb.create_table(
        TableName=tablename,
        KeySchema=[
            {
                'AttributeName': 'time',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'order',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'time',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'order',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,   
            'WriteCapacityUnits': 10
        } # define the capacity of database
    )
    print("Table %s is creating" % tablename) # if we are creating table, then show the information on terminal
    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName=tablename)

    print("Table status: %s" % table.table_status)  # show the status of table
    return table  #function complete, return the table


def get_table(tablename):   # define a function to get the table to deal with
    return dynamodb.Table(tablename)


def insert(table, item):   # insert new item to the table
    response = table.put_item(
        Item={
            'weather': item["weather"],
            'time': item["time"],
	    'order': item["order"],
        }
    )
    # insert item according to specific format
