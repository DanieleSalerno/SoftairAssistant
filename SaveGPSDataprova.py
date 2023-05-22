import datetime
import json
import boto3



dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
#dynamodb = boto3.client('dynamodb', endpoint_url="http://localhost:4566")
table = dynamodb.Table('GPS_data')





measure_data = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
player_id="sdaasdasd"
latitude = str(75.000000)
longitude =str(75.000000)

item = {
    'player_id': player_id,
    'timestamp': str(measure_data),
    'latitude': str(latitude),
    'longitude': str(longitude)
}

table.put_item(Item=item)

print(table)








