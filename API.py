import time

import boto3
from fastapi import FastAPI
import random
from fastapi.middleware.cors import CORSMiddleware
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
origins=[
    "http://localhost:63342"
]
#remember to install "FastAPI[All]"
#and fastapi unicorn
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)
@app.get('/gpsdata')
#that will be the first thing do when user use api
async def root():

    total_munition=0
    #api response
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

    table_name = "GPS_data"
    #ScanIndexForward

    res=[]
    players=['Vitality_0','Vitality_1','Vitality_2','Vitality_3']
    table = dynamodb.Table(table_name)
    print("------------------------------------------------------------------------------------------------")

    for player in players:
        try:
            response = table.query(
                KeyConditionExpression=Key('player_id').eq(player),
                ScanIndexForward=False,
                Limit=1,

            )
        except ClientError as e:
            print(e.response['Error']['Message'])


        if(response["Count"]!=0):
            res.append(response['Items'][0])
            total_munition+=int(response['Items'][0]['munition'])





    return {'player': res,'total_munition':total_munition}





@app.get('/infoplayer/{g_id}')
#that will be the first thing do when user use api
async def root(g_id: int):
    #api response
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

    table_name = "info_data"
    #ScanIndexForward

    res=[]
    players=['Vitality_0','Vitality_1','Vitality_2','Vitality_3']
    table = dynamodb.Table(table_name)
    print("------------------------------------------------------------------------------------------------")

    for player in players:
        try:
            response = table.query(
                KeyConditionExpression=Key('player_id').eq(player),
                ScanIndexForward=False,
                FilterExpression=Attr('game_id').eq(str(g_id))



            )
        except ClientError as e:
            print(e.response['Error']['Message'])

        if(response["Count"]!=0):
            res.append(response['Items'][0])




    return {'player': res}




@app.get('/SOSevent/{g_id}')

async def root(g_id:int):
    #api response
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

    table_name = "SOS_data"
    #ScanIndexForward

    res=[]
    players=['Vitality_0','Vitality_1','Vitality_2','Vitality_3']
    table = dynamodb.Table(table_name)
    print("------------------------------------------------------------------------------------------------")

    for player in players:
        try:
            response = table.query(
                KeyConditionExpression=Key('player_id').eq(player),
                ScanIndexForward=False,
                Limit=1,
                FilterExpression=Attr('game_id').eq(str(g_id))


            )
        except ClientError as e:
            print(e.response['Error']['Message'])

        if(response["Count"]!=0):
            res.append(response['Items'][0])




    return {'player': res}




@app.get('/getkill/{g_id}')

async def root(g_id: int):
    #api response
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

    table_name = "info_data"
    #ScanIndexForward

    kill=0
    players=['PGNAT_0','PGNAT_1','PGNAT_2','PGNAT_3']
    table = dynamodb.Table(table_name)
    print("------------------------------------------------------------------------------------------------")

    for player in players:
        try:
            response = table.query(
                KeyConditionExpression=Key('player_id').eq(player),
                ScanIndexForward=False,
                FilterExpression=Attr('game_id').eq(str(g_id))



            )
        except ClientError as e:
            print(e.response['Error']['Message'])

        if(response["Count"]!=0):
            kill+=int(response['Count'])




    return {'kills': kill }





