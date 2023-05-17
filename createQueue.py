import os
##creating tEAMS queue
teams_name = ['Vitality', 'PGNAT', 'OutPlayed','Sosqueue']

for name in teams_name:
    os.system('aws sqs create-queue --queue-name '+ name +' --endpoint-url=http://localhost:4566')

os.system('aws sqs list-queues --endpoint-url=http://localhost:4566')
os.system('aws sqs get-queue-attributes --queue-url http://localhost:4566/000000000000/Vitality --attribute-name QueueArn --endpoint-url=http://localhost:4566')

#creating and attaching role
os.system(r'cd C:\Users\Daniele\IdeaProjects\SoftairAssistant')
os.system(r'aws iam create-role --role-name lambdarole --assume-role-policy-document file://role_policy.json --query '+"\'"+'Role.Arn'+"\'"+' --endpoint-url=http://localhost:4566')
os.system(r'aws iam put-role-policy --role-name lambdarole --policy-name lambdapolicy --policy-document file://policy.json --endpoint-url=http://localhost:4566')


#lambda function sendsosmessage
os.system('aws lambda create-function --function-name sendsosmessage --zip-file fileb://SOSmessage/sendsosfunc_pck.zip --handler SendSosMessage.lambda_handler --runtime python3.10 --role arn:aws:iam::000000000000:role/lambdarole --endpoint-url=http://localhost:4566')

os.system('aws lambda create-event-source-mapping --function-name sendsosmessage --batch-size 4 --maximum-batching-window-in-seconds 60 --event-source-arn arn:aws:sqs:us-east-2:000000000000:SOSqueue --endpoint-url=http://localhost:4566')
