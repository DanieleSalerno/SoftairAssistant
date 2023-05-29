import time

import boto3
import datetime
import random




sqs = boto3.resource('sqs', endpoint_url='http://localhost:4566')

teams = [('Vitality', 4), ('PGNAT', 4)]
##in this cases to simulate the team we will just create 2 teams
team_names=["Vitality","PGNAT"]
start_lat=41.01003
start_lon=15.09954

last_lat_lon=[]
last_ammo_number=[]
last_life_num=[]
#inizializing value
for team,player_id in teams:
    ammonumber=[]
    arrayt=[]
    lifenum=[]

    for j in range(player_id):

        arrayt.append([[start_lat,start_lon]])
        ammonumber.append(200)
        lifenum.append(3)
    last_lat_lon.append(arrayt)
    last_ammo_number.append(ammonumber)
    last_life_num.append(lifenum)

print(last_lat_lon)
print(last_ammo_number)
#GETTING QUEUES
queueinfo=sqs.get_queue_by_name(QueueName="Infoqueue")
queuesos=sqs.get_queue_by_name(QueueName="Sosqueue")

player_sos="aaaa"
sos=0
duration_in_sec = 100;
for i in range(duration_in_sec):
    team_num=0
    for team, player_id in teams:
        queue = sqs.get_queue_by_name(QueueName=team)
        measure_date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        for i in range(player_id):
            if(last_life_num[team_num][i]>0 and (team, str(i))!=player_sos):
                #simulating movement
                latitudeplus = 0.00002*round(random.randrange(-2.0, 4))
                longitudeplus = 0.00002*round(random.randrange(-2.0, 4))

                newlat=last_lat_lon[team_num][i][0][0]+latitudeplus
                newlon=last_lat_lon[team_num][i][0][1]+longitudeplus

                last_lat_lon[team_num][i]=[[newlat,newlon]]
            else:
                #print("player "+team+"_"+str(i)+"is DEAD")
                newlat=last_lat_lon[team_num][i][0][0]
                newlon=last_lat_lon[team_num][i][0][1]




            #simulating ammo
            #prob of 33# to shot
            if(random.randrange(0,100)>66):
                shotted=random.randrange(0,20)
                #print("shotted ammo for PLAYER_ID"+str(i)+"="+str(shotted))
                newammo=last_ammo_number[team_num][i] - shotted

                last_ammo_number[team_num][i]=newammo
                if(newammo<0):
                    last_ammo_number[team_num][i]=0
                    newammo=0


            #simulating hitted
            if team_num==0:
                hit_team=team_names[1]
            else:
                hit_team=team_names[0]
            #remember every player only know when he get hitted by someone
            if(last_ammo_number[team_num][i]>0 and last_life_num[team_num][i]>0):
                #prob of 10% of get hitted by someone
                prob_hit=random.randrange(0,100)
                print(prob_hit)
                if(prob_hit>90):
                    last_life_num[team_num][i]-=1

                    msg_info= '{"player_id": "%s_%s","timestamp": "%s","hittedby": "%s_%s","game_id": "%s","life":"%s"}' \
                       % (team, str(i), measure_date, hit_team, str(random.randrange(0,4)),str(1),str(last_life_num[team_num][i]))
                    #print(msg_info)

                    print("life of player:" +team+"_"+str(i)+"lifepoints: "+str(last_life_num[team_num][i]))
                    queueinfo.send_message(MessageBody=msg_info)



            #simulating SOS
            if(random.randrange(0,100)>95 and sos==0):
                player_sos=team, str(i)
                sos=1
                oxygen=90
                heartbeat=120
                sos_msg= '{"player_id": "%s_%s","timestamp": "%s","latitude": "%s","longitude": "%s","game_id":"%s","oxygen": "%s","heartbeat":"%s","status":"not_resolved"}' \
                                    % (team, str(i), measure_date, str(newlat), str(newlon),str(1),str(oxygen),str(heartbeat))
                print("SOS request player:"+team+str(i))
                queuesos.send_message(MessageBody=sos_msg)
                response=input("press a key to continue the game ")
                sos_msg= '{"player_id": "%s_%s","timestamp": "%s","latitude": "%s","longitude": "%s","game_id":"%s","oxygen": "%s","heartbeat":"%s","status":"resolved"}' \
                         % (team, str(i), measure_date, str(newlat), str(newlon),str(1),str(oxygen),str(heartbeat))
                queuesos.send_message(MessageBody=sos_msg)




            msg_body = '{"player_id": "%s_%s","timestamp": "%s","latitude": "%s","longitude": "%s","game_id":"%s","munition": "%s"}' \
                       % (team, str(i), measure_date, str(newlat), str(newlon),str(1),str(last_ammo_number[team_num][i]))
            #print(msg_body)
            queue.send_message(MessageBody=msg_body)



        team_num=team_num+1
    time.sleep(2)


print(last_lat_lon)




