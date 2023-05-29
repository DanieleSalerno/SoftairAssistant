import datetime
import json
import boto3
import os

def lambda_handler(event, context):
    print('## ENVIRONMENT VARIABLES')
    print(os.environ['AWS_LAMBDA_LOG_GROUP_NAME'])
    print(os.environ['AWS_LAMBDA_LOG_STREAM_NAME'])

    DYNAMODB_ENDPOINT_URL = 'http://%s:4566' % os.environ['LOCALSTACK_HOSTNAME']
    print(DYNAMODB_ENDPOINT_URL)
    print('## EVENT')
    print(event)




    dynamodb = boto3.resource('dynamodb', endpoint_url=DYNAMODB_ENDPOINT_URL)
    print(dynamodb)
    #dynamodb = boto3.client('dynamodb', endpoint_url="http://localhost:4566")
    table = dynamodb.Table('GPS_data')
    print(table)


    for record in event['Records']:

        payload=record['body']
        print(payload)
        payload=json.loads(str(payload))

        player_id = payload['player_id']
        print("ciaooooo")
        measure_data = datetime.datetime.strptime(payload['timestamp'], "%Y-%m-%d %H:%M:%S")

        latitude = payload['latitude']
        longitude =payload['longitude']
        print(player_id)
        print(latitude)
        print(longitude)
        print(measure_data)
        game_id=payload['game_id']
        munition=payload['munition']
        item = {
            'player_id': player_id,
            'timestamp': str(measure_data),
            'latitude': latitude,
            'longitude': longitude,
            'game_id':game_id,
            'munition':munition
        }
        table.put_item(Item=item)


        print(item)








