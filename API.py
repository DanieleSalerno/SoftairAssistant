import time

import boto3
from fastapi import FastAPI
import random
from fastapi.middleware.cors import CORSMiddleware
from boto3.dynamodb.conditions import Key
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
@app.get('/')
#that will be the first thing do when user use api
async def root():
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
                KeyConditionExpression=Key('player_id').eq('Vitality_0'),
                ScanIndexForward=False,
                Limit=1
            )
        except ClientError as e:
            print(e.response['Error']['Message'])



        res.append(response['Items'][0])




    return {'player': res,'data':18}




