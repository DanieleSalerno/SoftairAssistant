import datetime
import json
import boto3

def lambda_handler(event, context):

    #dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
    dynamodb = boto3.client('dynamodb', endpoint_url="http://localhost:4566")
    #table = dynamodb.Table('GPS_data')



    for record in event['Records']:
        payload=record['body']
        payload=json.loads(str(payload))

        player_id = payload['player_id']

        measure_data = datetime.datetime.strptime(payload['timestamp'], "%Y-%m-%d %H:%M:%S")

        latitude = float(payload['latitude'])
        longitude = float(payload['longitude'])

        item = {
            'player_id': player_id,
            'timestamp': str(measure_data),
            'latitude': str(latitude),
            'longitude': str(longitude)
        }

        dynamodb.put_item(TableName='GPS_data',Item=item)






