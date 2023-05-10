from decimal import Decimal
import json
import boto3


def load_gps(gpsinfo):
    dynamodb=boto3.resource('dynamodb',
                            endpoint_url='http://localhost:4566')
    table=dynamodb.Table('GPS_data')
    for data in gpsinfo:
        player_id=int(gpsinfo['player_id'])
        timestamp=gpsinfo['timestamp']
        print("Adding gpsinfo:", player_id,timestamp)
        table.put_item(Item=data)


with open("gpsdata.json") as json_file:
    gps_list=json.load(json_file,parse_float=Decimal)
    load_gps(gps_list)

