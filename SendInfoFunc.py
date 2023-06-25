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
    table = dynamodb.Table('info_data')
    print(table)


    for record in event['Records']:

        payload=record['body']
        print(payload)
        payload=json.loads(str(payload))

        player_id = payload['player_id']

        measure_data = datetime.datetime.strptime(payload['timestamp'], "%Y-%m-%d %H:%M:%S")

        hittedby = payload['hittedby']
        game_id=payload['game_id']
        life=payload['life']

        item = {
            'player_id': player_id,
            'timestamp': str(measure_data),
            'hittedby': hittedby,
            'game_id': game_id,
            'life': life
        }
        table.put_item(Item=item)


        print(item)




