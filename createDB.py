import boto3
import os

#this table contains the gps data of each player
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


#This table contains the information about every hit that a player receive
def create_table_info():
    dynamodb=boto3.resource('dynamodb',
                            endpoint_url="http://localhost:4566")
    print("here")
    table=dynamodb.create_table(
        TableName='SOS_data',
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


#this table contain information about every emergency that occur during the games
def create_table_SOS():
    dynamodb=boto3.resource('dynamodb',
                            endpoint_url="http://localhost:4566")
    print("here")
    table=dynamodb.create_table(
        TableName='info_data',
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

if __name__ == "__main__":
    create_table_gps()
    create_table_info()
    create_table_SOS()
