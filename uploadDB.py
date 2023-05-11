from decimal import Decimal
import json
import boto3
from botocore.exceptions import ClientError


def load_gps():
    dynamodb=boto3.resource('dynamodb',endpoint_url='http://localhost:4566')
    table=dynamodb.Table('GPS_data')
    item={
        'player_id': "player_1",
        'time_stamp':"2023-05-10-16:03",
        'latitude':27,
        'longitude':30,


    }
    table.put_item(Item=item)

def read_item():
    table_name = "GPS_data"

    dynamodb=boto3.resource('dynamodb',endpoint_url='http://localhost:4566')


    players = "1 2"
    players = players.split()
    table = dynamodb.Table(table_name)
    print("------------------------------------------------------------------------------------------------")
    for player in players:
        print(type(player))
        try:
            response = table.get_item(Key={'player_id': int(player), 'time_stamp':'2022 15 07'})
        except ClientError as e:
            print(e.response['Error']['Message'])

        print("position of player %s at time %s is lon %s / lat %s"
              % (response['Item']['player_id'], response['Item']['time_stamp'],response['Item']['longitude'],response['Item']['latitude']))

        print("------------------------------------------------------------------------------------------------")


read_item()



