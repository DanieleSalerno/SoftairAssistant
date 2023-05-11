import boto3
import datetime
import json
import time

def lambda_handler(event, context):
    sqs = boto3.resource('sqs', endpoint_url='http://localhost:4566')
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

    table = dynamodb.Table('GPS_data')

    teams = ['Vitality', 'PGNAT']

    for team in teams:
        queue = sqs.get_queue_by_name(QueueName=team)
        messages = []
        while True:
            response = queue.receive_messages(MaxNumberOfMessages=10, VisibilityTimeout=10, WaitTimeSeconds=10)
            if response:
                messages.extend(response)

                avg_temperature = 0
                last_GPS_data = datetime.datetime.combine(datetime.date.min, datetime.datetime.min.time())
                for message in messages:
                    content = json.loads(message.body)
                    player_id = content["player_id"]

                    measure_data = datetime.datetime.strptime(content["time_stamp"], "%Y-%m-%d %H:%M:%S")

                    if measure_data > last_measured_data:
                        last_measured_data = measure_data


                    latitude = float(content["latitude"])
                    longitude = float(content["longitude"])
                    message.delete()


                    item = {
                        'player_id': player_id,
                        'time_stamp': str(last_measured_data),
                        'latitude': latitude,
                        'longitude': longitude
                    }
                    table.put_item(Item=item)
            else:
                break


sqs = boto3.resource('sqs', endpoint_url='http://localhost:4566')
dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

table = dynamodb.Table('GPS_data')

teams = ['Vitality', 'PGNAT']

for team in teams:
    #per ogni città apri la coda
    print("=======================================team=======================================")
    print(team)
    queue = sqs.get_queue_by_name(QueueName=team)
    messages = []
    while True:
        response = queue.receive_messages(MaxNumberOfMessages=10, VisibilityTimeout=10, WaitTimeSeconds=10)
        if response:
            messages.extend(response)



            #last_measured_data = datetime.datetime.combine(datetime.date.min, datetime.datetime.min.time())
            for message in messages:


                #load each message
                content = json.loads(message.body)
                #print("===Content=============================================")
                #print(content)


                player_id = content["player_id"]
                print(player_id)
                measure_data = datetime.datetime.strptime(content["timestamp"], "%Y-%m-%d %H:%M:%S")
                #print(measure_data)
                #if measure_data > last_measured_data:
                    #last_measured_data = measure_data

                print("===========================================================")


                latitude = float(content["latitude"])
                longitude = float(content["longitude"])
                message.delete()


                item = {
                    'player_id': player_id,
                    'timestamp': str(measure_data),
                    'latitude': str(latitude),
                    'longitude': str(longitude)
                }
                print("=========================saved item======================")
                print(item)
                table.put_item(Item=item)

        else:
            break


