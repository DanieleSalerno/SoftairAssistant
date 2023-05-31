import requests
import json
import time
import os
import boto3
#requests 2.29.0

def lambda_handler(event, context):
    key = "b4shwnwrkeGwtQy8uOQ612"
    url = "https://maker.ifttt.com/trigger/sos_message/with/key/" + key
    url2 = "https://maker.ifttt.com/trigger/status_message/with/key/" + key
    DYNAMODB_ENDPOINT_URL = 'http://%s:4566' % os.environ['LOCALSTACK_HOSTNAME']





    dynamodb = boto3.resource('dynamodb', endpoint_url=DYNAMODB_ENDPOINT_URL)

    #dynamodb = boto3.client('dynamodb', endpoint_url="http://localhost:4566")
    table = dynamodb.Table('SOS_data')






    for record in event['Records']:
            payload = record['body']
            payload = json.loads(str(payload))
            player_id = payload['player_id']
            time_stamp = payload['timestamp']
            longitude = payload['longitude']
            latitude = payload['latitude']
            game_id=payload['game_id']
            oxygen=payload['oxygen']
            heartbeat=payload['heartbeat']
            status=payload['status']



            item = {
                'player_id': player_id,
                'timestamp': str(time_stamp),
                'latitude': latitude,
                'longitude': longitude,
                'game_id':game_id,
                'heartbeat':heartbeat,
                'oxigen':oxygen,
                'status':status
            }
            #saving data into db
            table.put_item(Item=item)

            #sending request to IFTT

            if(status != "resolved"):
                req = requests.post(url, json={"value1": player_id, "value2": latitude, "value3": longitude})
                time.sleep(1)
                req2 = requests.post(url2, json={"value1": heartbeat, "value2": oxygen,"value3":time_stamp})






