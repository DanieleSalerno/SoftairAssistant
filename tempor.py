sqs = boto3.resource('sqs', endpoint_url='http://localhost:4566')
dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

table = dynamodb.Table('GPS_data')
context.log("ciaooo")

if event:
    for record in event['Records']:
        context.log(record)
        payload=record['body']

        #content=payload.replace('\'', '\"')

        payload=json.loads(str(payload))

        player_id = payload['player_id']
        print(player_id)
        measure_data = datetime.datetime.strptime(payload['timestamp'], "%Y-%m-%d %H:%M:%S")
        #print(measure_data)
        #if measure_data > last_measured_data:
        #last_measured_data = measure_data

        print("===========================================================")


        latitude = float(payload['latitude'])
        longitude = float(payload['longitude'])



        item = {
            'player_id': player_id,
            'timestamp': str(measure_data),
            'latitude': str(latitude),
            'longitude': str(longitude)
        }
        print("=========================saved item======================")
        print(item)
        table.put_item(Item=item)
