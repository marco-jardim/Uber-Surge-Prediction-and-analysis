from __future__ import print_function  # Python 2/3 compatibility
import boto3
import json
import decimal
import ConfigParser



# get access to dynomodb
dynamodb = boto3.resource('dynamodb',region_name='us-east-1', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")  #connect with dynamodb

# for the use to delete the database
def delete_database(table):
    try:
        table.delete()
    except Exception, e:
        raise e

# create a dynamodb table
def create_database(tablename):
    table = dynamodb.create_table(
        TableName=tablename,
        KeySchema=[
            {
                'AttributeName': 'area',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'time',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'area',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'time',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print("Table %s is creating" % tablename)
    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName=tablename)

    print("Table status: %s" % table.table_status)
    return table


# access the database table
def get_table(tablename):
    return dynamodb.Table(tablename)


# wrapper function to insert item into table, data format specified
def insert(table, item):
    response = table.put_item(
        Item={
            'area': item["area"],
            'time': item["time"],
            'surge_multiplier': item["surge_multiplier"],
            'zipcode': item["zipcode"],
            'lat': item["lat"],
            'weather': item["weather"],
            'temperature': item["temperature"],
            'incident': item["incident"],
            'lon': item["lon"]
        }
    )