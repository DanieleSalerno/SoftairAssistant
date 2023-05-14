import boto3
import datetime
import json


def lambda_handler():
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
