import requests
import json
import time

def lambda_handler(event, context):
    key = "b4shwnwrkeGwtQy8uOQ612"
    url = "https://maker.ifttt.com/trigger/sos_message/with/key/" + key
    url2 = "https://maker.ifttt.com/trigger/status_message/with/key/" + key

    for record in event['Records']:
            payload = record['body']
            payload = json.loads(str(payload))
            player_id = payload['player_id']
            time_stamp = payload['timestamp']
            longitude = payload['longitude']
            latitude = payload['latitude']

            req = requests.post(url, json={"value1": player_id, "value2": latitude, "value3": longitude})
            time.sleep(1)
            req2 = requests.post(url2, json={"value1": "15", "value2": "20","value3":time_stamp})




