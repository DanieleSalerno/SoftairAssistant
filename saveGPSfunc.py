import requests



def lambda_handler(event, context):
    key = "b4shwnwrkeGwtQy8uOQ612"
    url = "https://maker.ifttt.com/trigger/{event}/with/key/" + key

    for record in event['Records']:
            payload = record['body']
            #payload = json.loads(str(payload))
            #device_id = payload['player_id']
            #error_date = payload['timestamp']
            req = requests.post(url, json={"value1": str(event), "value2": str(payload)})

