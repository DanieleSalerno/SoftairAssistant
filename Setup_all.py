import os
import createDB
PATH="C:\\Users\\Daniele\\IdeaProjects\\SoftairAssistant"



##creating tEAMS queue
teams_name = ['Vitality', 'PGNAT', 'OutPlayed','Sosqueue','Infoqueue']

for name in teams_name:
    os.system('aws sqs create-queue --queue-name '+ name +' --endpoint-url=http://localhost:4566')

os.system('aws sqs list-queues --endpoint-url=http://localhost:4566')
#os.system('aws sqs get-queue-attributes --queue-url http://localhost:4566/000000000000/Vitality --attribute-name QueueArn --endpoint-url=http://localhost:4566')

#creating and attaching role
os.system(r'cd '+PATH)
os.system(r'aws iam create-role --role-name lambdarole --assume-role-policy-document file://role_policy.json --query '+"\'"+'Role.Arn'+"\'"+' --endpoint-url=http://localhost:4566')
os.system(r'aws iam put-role-policy --role-name lambdarole --policy-name lambdapolicy --policy-document file://policy.json --endpoint-url=http://localhost:4566')

os.system(r'aws iam put-role-policy --role-name lambdarole --policy-name dbpolicy --policy-document file://policyDB.json --endpoint-url=http://localhost:4566')

#Create Tables
createDB.create_table_gps()
createDB.create_table_info()
createDB.create_table_SOS()
#lambda function sendsosmessage
os.system('aws lambda create-function --function-name sendsosmessage --zip-file fileb://SOSmessage/sendsosfunc.zip --handler SendSosMessage.lambda_handler --runtime python3.9 --role arn:aws:iam::000000000000:role/lambdarole --endpoint-url=http://localhost:4566')
os.system('aws lambda create-event-source-mapping --function-name sendsosmessage --batch-size 5 --maximum-batching-window-in-seconds 60 --event-source-arn arn:aws:sqs:us-east-2:000000000000:Sosqueue --endpoint-url=http://localhost:4566')


#lambda function SaveGPS data
os.system('aws lambda create-function --function-name savegpsdata --zip-file fileb://SaveGpsData.zip --handler SaveGPSData.lambda_handler --runtime python3.9 --role arn:aws:iam::000000000000:role/lambdarole --endpoint-url=http://localhost:4566')
for name in teams_name:
    if name != 'Sosqueue' and name!='Infoqueue':

        os.system('aws lambda create-event-source-mapping --function-name savegpsdata --batch-size 5 --maximum-batching-window-in-seconds 60 --event-source-arn arn:aws:sqs:us-east-2:000000000000:'+name+' --endpoint-url=http://localhost:4566')

#lambda function sendinfofunc
os.system('aws lambda create-function --function-name sendinfofunc --zip-file fileb://sendinfofunc.zip --handler SendInfoFunc.lambda_handler --runtime python3.9 --role arn:aws:iam::000000000000:role/lambdarole --endpoint-url=http://localhost:4566')
os.system('aws lambda create-event-source-mapping --function-name sendinfofunc --batch-size 5 --maximum-batching-window-in-seconds 60 --event-source-arn arn:aws:sqs:us-east-2:000000000000:Infoqueue --endpoint-url=http://localhost:4566')
