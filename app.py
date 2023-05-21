import json
import sys
import logging
from flask import Flask, render_template
import time
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def getgpsdata():

    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

    table_name = "GPS_data"
    #ScanIndexForward


    players=['Vitality_0','Vitality_1','Vitality_2','Vitality_3']
    table = dynamodb.Table(table_name)
    print("------------------------------------------------------------------------------------------------")
    data=()
    for player in players:
        try:
            response = table.query(
                KeyConditionExpression=Key('player_id').eq(player),
                ScanIndexForward=False,
                Limit=1
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        item = response['Items'][0]
        player_id=item['player_id']
        latitude= item['latitude']
        longitude=item['longitude']
        data.__add__((player_id,latitude,longitude))
        app.logger.info(item)

    app.logger.info(data)
    return data




@app.route("/")
def index():
    gps_position=getgpsdata()
    app.logger.info(gps_position)

    return render_template('flasksite.html',gpsdata=gps_position)


if __name__=='__main__':
    app.run()


