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



"""def create_teams():
    dynamodb=boto3.resource('dynamodb',
                            endpoint_url="http://localhost:4566")
    print("here")
    table=dynamodb.create_table(
        TableName='teams',
        KeySchema=[
            {
                'AttributeName': 'team_name',
                'KeyType': 'HASH' #partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName':'team_name',
                'AttributeType':'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits':10,
            'WriteCapacityUnits':10
        }
        ,)
        """

#This table contains the information about every hut that a player receive
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

