import time

import boto3
import datetime
import random
import numpy


last_lat_lon=[]
sqs = boto3.resource('sqs', endpoint_url='http://localhost:4566')

teams = [('Vitality', 4), ('PGNAT', 4)]
##in this cases to simulate the team we will just create 3 teams

start_lat=75.000
start_lon=75.000

for team,player_id in teams:

    arrayt=[]
    print("a")
    for j in range(player_id):
        print("B")
        arrayt.append([[start_lat,start_lon]])
    last_lat_lon.append(arrayt)

print(last_lat_lon)


duration_in_sec = 5;
for i in range(duration_in_sec):
    for team, player_id in teams:
        queue = sqs.get_queue_by_name(QueueName=team)
        measure_date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        team_num=1
        for i in range(player_id):

            latitudeplus = round(random.randrange(-1.0, 1))
            longitudeplus = round(random.randrange(-1.0, 1))

            newlat=last_lat_lon[team_num][i][0][0]+latitudeplus
            newlon=last_lat_lon[team_num][i][0][1]+longitudeplus

            last_lat_lon[team_num][i]=[[newlat,newlon]]

            print(last_lat_lon[team_num][i][0][0])
            msg_body = '{"player_id": "%s_%s","timestamp": "%s","latitude": "%s","longitude": "%s"}' \
                       % (team, str(i), measure_date, str(newlat), str(newlon))
            print(msg_body)
            queue.send_message(MessageBody=msg_body)
        team_num=team_num+1
    time.sleep(2)


print(last_lat_lon)
