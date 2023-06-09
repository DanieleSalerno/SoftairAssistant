import json
import time
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

table_name = "GPS_data"
#ScanIndexForward


players=['Vitality_0','Vitality_1','Vitality_2','Vitality_3']
table = dynamodb.Table(table_name)
print("------------------------------------------------------------------------------------------------")
while True:
    for player in players:
        try:
            response = table.query(
                KeyConditionExpression=Key('player_id').eq(player),
                ScanIndexForward=False,
                Limit=1
                )
        except ClientError as e:
            print(e.response['Error']['Message'])

        player_id=response['Items'][0]['player_id']

        print(player_id)

    time.sleep(2)





