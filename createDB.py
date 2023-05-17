import boto3
import os

def create_table_gps():
    dynamodb=boto3.resource('dynamodb',
                            endpoint_url="http://localhost:4566")
    print("here")
    table=dynamodb.create_table(
        TableName='GPS_data',
        KeySchema=[
            {
                'AttributeName': 'player_id',
                'KeyType': 'HASH' #partition key
            },
            {
                'AttributeName': 'timestamp',
                'KeyType': 'RANGE' #Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName':'player_id',
                'AttributeType':'S'
            },
            {
                'AttributeName':'timestamp',
                'AttributeType':'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits':10,
            'WriteCapacityUnits':10
        }
        ,)


