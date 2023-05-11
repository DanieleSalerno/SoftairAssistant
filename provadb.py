import boto3
import os
os.environ['AWS_ACCESS_KEY_ID'] = 'test'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-2'

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


